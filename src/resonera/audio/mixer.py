"""
Background sound mixing and equalization for neural entrainment audio.
"""
import numpy as np
from typing import Literal, Union, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

class Equalizer:
    """Simple parametric equalizer for audio processing."""
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the equalizer.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.bands = {
            'low': (20, 250),     # Low frequencies
            'mid': (250, 4000),   # Mid frequencies
            'high': (4000, 20000) # High frequencies
        }
        
    def apply_band_filter(self, audio: np.ndarray, band: str,
                         gain_db: float) -> np.ndarray:
        """
        Apply gain to a specific frequency band.
        
        Args:
            audio: Input audio array
            band: Frequency band ('low', 'mid', 'high')
            gain_db: Gain in decibels (-12 to +12 dB)
            
        Returns:
            numpy.ndarray: Filtered audio
        """
        if band not in self.bands:
            raise ValueError(f"Invalid band: {band}")
            
        # Convert gain from dB to linear scale
        gain = 10 ** (gain_db / 20)
        
        # Get frequency range for band
        low_freq, high_freq = self.bands[band]
        
        # Perform FFT
        fft = np.fft.rfft(audio)
        freqs = np.fft.rfftfreq(len(audio), 1/self.sample_rate)
        
        # Create band mask
        mask = (freqs >= low_freq) & (freqs <= high_freq)
        
        # Apply gain to band
        fft[mask] *= gain
        
        # Inverse FFT
        return np.fft.irfft(fft, len(audio))
        
    def process(self, audio: np.ndarray, gains: dict) -> np.ndarray:
        """
        Process audio through all equalizer bands.
        
        Args:
            audio: Input audio array
            gains: Dictionary of band gains in dB (e.g., {'low': -3, 'mid': 0, 'high': 2})
            
        Returns:
            numpy.ndarray: Equalized audio
        """
        result = np.copy(audio)
        for band, gain in gains.items():
            result = self.apply_band_filter(result, band, gain)
            
        # Normalize after applying all filters
        max_amplitude = np.max(np.abs(result))
        if max_amplitude > 1:
            result /= max_amplitude
            
        return result


class BackgroundSoundMixer:
    """Mix background sounds with neural entrainment audio."""
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the background sound mixer.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.equalizer = Equalizer(sample_rate=sample_rate)
        
    def generate_white_noise(self, duration: float,
                           volume: float = 0.1) -> np.ndarray:
        """
        Generate white noise background.
        
        Args:
            duration: Duration in seconds
            volume: Volume level (0-1)
            
        Returns:
            numpy.ndarray: White noise audio
        """
        samples = int(self.sample_rate * duration)
        noise = np.random.normal(0, 1, samples)
        
        # Shape noise with pink filter (more natural sounding)
        fft = np.fft.rfft(noise)
        freqs = np.fft.rfftfreq(len(noise))
        pink_filter = 1 / np.sqrt(freqs[1:])  # 1/f filter
        fft[1:] *= pink_filter
        noise = np.fft.irfft(fft)
        
        # Normalize and apply volume
        noise = noise / np.max(np.abs(noise)) * volume
        return noise
        
    def generate_ambient_drone(self, duration: float, base_freq: float = 100.0,
                             volume: float = 0.1) -> np.ndarray:
        """
        Generate ambient drone background.
        
        Args:
            duration: Duration in seconds
            base_freq: Base frequency for drone
            volume: Volume level (0-1)
            
        Returns:
            numpy.ndarray: Ambient drone audio
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Generate multiple harmonics for rich drone sound
        harmonics = [1.0, 1.5, 2.0, 2.5, 3.0]  # Harmonic series
        amplitudes = [1.0, 0.5, 0.3, 0.2, 0.1]  # Decreasing amplitudes
        
        drone = np.zeros_like(t)
        for harmonic, amplitude in zip(harmonics, amplitudes):
            freq = base_freq * harmonic
            drone += amplitude * np.sin(2 * np.pi * freq * t)
        
        # Add subtle modulation
        mod_freq = 0.1  # 0.1 Hz modulation
        modulation = 1 + 0.1 * np.sin(2 * np.pi * mod_freq * t)
        drone *= modulation
        
        # Normalize and apply volume
        drone = drone / np.max(np.abs(drone)) * volume
        return drone
        
    def mix_background(self, main_audio: Union[np.ndarray, tuple[np.ndarray, np.ndarray]],
                      background_type: Literal['white_noise', 'ambient'] = 'white_noise',
                      volume: float = 0.1,
                      eq_gains: Optional[dict] = None) -> Union[np.ndarray, tuple[np.ndarray, np.ndarray]]:
        """
        Mix background sounds with main entrainment audio.
        
        Args:
            main_audio: Primary audio (mono array or stereo tuple)
            background_type: Type of background sound
            volume: Background volume level (0-1)
            eq_gains: Optional EQ gains for background (e.g., {'low': -3, 'mid': 0, 'high': 2})
            
        Returns:
            Mixed audio (same format as input)
        """
        # Handle stereo input
        is_stereo = isinstance(main_audio, tuple)
        if is_stereo:
            duration = len(main_audio[0]) / self.sample_rate
            channels = [np.array(ch) for ch in main_audio]
        else:
            duration = len(main_audio) / self.sample_rate
            channels = [np.array(main_audio)]
            
        # Generate background
        if background_type == 'white_noise':
            background = self.generate_white_noise(duration, volume)
        else:  # ambient
            background = self.generate_ambient_drone(duration, volume=volume)
            
        # Apply EQ if specified
        if eq_gains:
            background = self.equalizer.process(background, eq_gains)
            
        # Mix with each channel
        mixed_channels = [ch + background for ch in channels]
        
        # Normalize to prevent clipping
        for i, channel in enumerate(mixed_channels):
            max_amplitude = np.max(np.abs(channel))
            if max_amplitude > 1:
                mixed_channels[i] = channel / max_amplitude
                
        return tuple(mixed_channels) if is_stereo else mixed_channels[0]
