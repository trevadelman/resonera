"""
Audio generation for neural entrainment.
"""
import numpy as np
from scipy.io import wavfile
import os
from flask import current_app
from tempfile import NamedTemporaryFile
from .transitions import FrequencyTransition
from .harmonics import HarmonicOvertoneGenerator

class AudioGenerator:
    """Generates neural entrainment audio using binaural beats and isochronic tones."""
    
    # Frequency ranges for different brainwave states
    FREQUENCY_RANGES = {
        'delta': (0.5, 4.0),    # Deep sleep
        'theta': (4.0, 8.0),    # Deep relaxation, meditation
        'alpha': (8.0, 14.0),   # Relaxed focus
        'gamma': (30.0, 100.0)  # High-level cognition
    }
    
    def __init__(self):
        """Initialize the audio generator with default parameters."""
        self.sample_rate = 44100  # Standard audio sample rate
        self.carrier_frequency = 440  # Base frequency for binaural beats (Hz)
        self.transition = FrequencyTransition(sample_rate=self.sample_rate)
        self.harmonic_generator = HarmonicOvertoneGenerator(sample_rate=self.sample_rate)
        
    def get_optimal_carrier_frequency(self, target_frequency: float) -> float:
        """
        Calculate optimal carrier frequency based on target frequency.
        Lower carrier frequencies for lower target frequencies to maintain clarity.
        
        Args:
            target_frequency: The desired entrainment frequency
            
        Returns:
            float: Optimal carrier frequency
        """
        if target_frequency <= 4.0:  # Delta
            return 100.0  # Lower carrier for better perception
        elif target_frequency <= 8.0:  # Theta
            return 200.0
        elif target_frequency <= 14.0:  # Alpha
            return 440.0
        else:  # Gamma
            return 500.0  # Higher carrier for gamma frequencies
    
    def generate_sine_wave(self, frequency: float, duration: float,
                          volume: float = 0.7) -> np.ndarray:
        """
        Generate a sine wave at the specified frequency.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            volume: Volume level (0-1)
            
        Returns:
            numpy.ndarray: Audio samples
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        sine_wave = np.sin(2 * np.pi * frequency * t)
        return sine_wave * volume
    
    def generate_binaural_beat(self, target_frequency: float, duration: float,
                              volume: float = 0.7) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate binaural beat using two slightly different frequencies with harmonic enhancement.
        
        Args:
            target_frequency: Desired beat frequency in Hz
            duration: Duration in seconds
            volume: Volume level (0-1)
            
        Returns:
            tuple: (left_channel, right_channel) audio samples
        """
        # Get optimal carrier frequency for the target frequency
        carrier = self.get_optimal_carrier_frequency(target_frequency)
        
        # Generate carrier frequencies for left and right channels
        left_freq = carrier
        right_freq = carrier + target_frequency
        
        # Generate enhanced carrier waves with harmonics
        left_channel = self.harmonic_generator.generate_enhanced_frequency(left_freq, duration, volume)
        right_channel = self.harmonic_generator.generate_enhanced_frequency(right_freq, duration, volume)
        
        return left_channel, right_channel
    
    def generate_isochronic_tone(self, frequency: float, duration: float,
                                volume: float = 0.7) -> np.ndarray:
        """
        Generate isochronic tone by modulating amplitude with harmonic enhancement.
        
        Args:
            frequency: Tone frequency in Hz
            duration: Duration in seconds
            volume: Volume level (0-1)
            
        Returns:
            numpy.ndarray: Audio samples
        """
        # Generate enhanced carrier wave with harmonics
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        carrier = self.harmonic_generator.generate_enhanced_frequency(self.carrier_frequency, duration, volume)
        
        # Generate modulation envelope
        modulation = 0.5 * (1 + np.sin(2 * np.pi * frequency * t))
        
        # Apply modulation
        return carrier * modulation
    
    def apply_fade(self, audio: np.ndarray, fade_duration: float = 0.1) -> np.ndarray:
        """
        Apply fade in/out to avoid clicks.
        
        Args:
            audio: Audio samples
            fade_duration: Fade duration in seconds
            
        Returns:
            numpy.ndarray: Audio with fades applied
        """
        fade_length = int(fade_duration * self.sample_rate)
        fade_in = np.linspace(0, 1, fade_length)
        fade_out = np.linspace(1, 0, fade_length)
        
        audio[:fade_length] *= fade_in
        audio[-fade_length:] *= fade_out
        
        return audio
    
    def generate(self, frequency: float, duration: float,
                volume: float = 0.7, transition_type: str = 'sigmoid') -> str:
        """
        Generate complete neural entrainment audio file.
        
        Args:
            frequency: Target frequency in Hz
            duration: Duration in seconds
            volume: Volume level (0-1)
            
        Returns:
            str: Path to generated audio file
        """
        # Generate frequency transition if needed
        if hasattr(self, '_last_frequency') and self._last_frequency != frequency:
            # Calculate optimal transition duration
            transition_duration = self.transition.calculate_optimal_duration(
                self._last_frequency, frequency
            )
            transition_duration = min(transition_duration, duration / 4)  # Max 25% of total duration
            
            # Generate transition frequencies
            if transition_type == 'linear':
                freq_curve = self.transition.linear_transition(
                    self._last_frequency, frequency, transition_duration
                )
            elif transition_type == 'exponential':
                freq_curve = self.transition.exponential_transition(
                    self._last_frequency, frequency, transition_duration
                )
            else:  # default to sigmoid
                freq_curve = self.transition.sigmoid_transition(
                    self._last_frequency, frequency, transition_duration
                )
            
            # Generate transition audio
            left_binaural = np.array([])
            right_binaural = np.array([])
            isochronic = np.array([])
            
            # Generate audio for each frequency step
            for freq in freq_curve:
                left_step, right_step = self.generate_binaural_beat(
                    freq, 1/self.sample_rate, volume * 0.5
                )
                iso_step = self.generate_isochronic_tone(
                    freq, 1/self.sample_rate, volume * 0.5
                )
                
                left_binaural = np.append(left_binaural, left_step)
                right_binaural = np.append(right_binaural, right_step)
                isochronic = np.append(isochronic, iso_step)
            
            # Generate remaining duration at target frequency
            remaining_duration = duration - transition_duration
            if remaining_duration > 0:
                left_main, right_main = self.generate_binaural_beat(
                    frequency, remaining_duration, volume * 0.5
                )
                iso_main = self.generate_isochronic_tone(
                    frequency, remaining_duration, volume * 0.5
                )
                
                left_binaural = np.append(left_binaural, left_main)
                right_binaural = np.append(right_binaural, right_main)
                isochronic = np.append(isochronic, iso_main)
        else:
            # No transition needed
            left_binaural, right_binaural = self.generate_binaural_beat(
                frequency, duration, volume * 0.5
            )
            isochronic = self.generate_isochronic_tone(
                frequency, duration, volume * 0.5
            )
        
        # Store current frequency for next transition
        self._last_frequency = frequency
        
        # Combine isochronic tones with binaural beats
        left_channel = left_binaural + isochronic
        right_channel = right_binaural + isochronic
        
        # Apply fades
        left_channel = self.apply_fade(left_channel)
        right_channel = self.apply_fade(right_channel)
        
        # Normalize to prevent clipping
        max_amplitude = max(np.max(np.abs(left_channel)),
                          np.max(np.abs(right_channel)))
        if max_amplitude > 1:
            left_channel /= max_amplitude
            right_channel /= max_amplitude
        
        # Combine channels
        stereo_audio = np.vstack((left_channel, right_channel)).T
        
        # Save to temporary file
        temp_file = NamedTemporaryFile(
            suffix='.wav',
            dir=current_app.config['AUDIO_UPLOAD_FOLDER'],
            delete=False
        )
        
        # Convert to 16-bit PCM
        audio_16bit = (stereo_audio * 32767).astype(np.int16)
        
        # Save WAV file
        wavfile.write(temp_file.name, self.sample_rate, audio_16bit)
        
        return temp_file.name
    
    def cleanup_old_files(self, max_age_hours: int = 1):
        """
        Clean up old generated audio files.
        
        Args:
            max_age_hours: Maximum age of files to keep in hours
        """
        audio_dir = current_app.config['AUDIO_UPLOAD_FOLDER']
        current_time = time.time()
        
        for filename in os.listdir(audio_dir):
            filepath = os.path.join(audio_dir, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getctime(filepath)
                if file_age > max_age_hours * 3600:
                    try:
                        os.remove(filepath)
                    except OSError:
                        pass  # Ignore errors in cleanup
