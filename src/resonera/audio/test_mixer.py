"""
Unit tests for background sound mixing and equalization.
"""
import unittest
import numpy as np
from .mixer import Equalizer, BackgroundSoundMixer

class TestEqualizer(unittest.TestCase):
    def setUp(self):
        """Initialize equalizer for testing."""
        self.sample_rate = 44100
        self.equalizer = Equalizer(sample_rate=self.sample_rate)
        self.test_duration = 1.0  # 1 second
        
    def generate_test_signal(self, frequency: float) -> np.ndarray:
        """Generate a test sine wave."""
        t = np.linspace(0, self.test_duration,
                       int(self.sample_rate * self.test_duration), False)
        return np.sin(2 * np.pi * frequency * t)
        
    def test_band_filter(self):
        """Test frequency band filtering."""
        # Generate test signals in different bands
        low_freq = 100    # Hz (in low band)
        mid_freq = 1000   # Hz (in mid band)
        high_freq = 8000  # Hz (in high band)
        
        signals = {
            'low': self.generate_test_signal(low_freq),
            'mid': self.generate_test_signal(mid_freq),
            'high': self.generate_test_signal(high_freq)
        }
        
        # Test boosting each band
        for band in ['low', 'mid', 'high']:
            # Apply +6dB boost to band
            filtered = self.equalizer.apply_band_filter(
                signals[band], band, 6.0
            )
            
            # Check that output is not all zeros
            self.assertTrue(np.any(filtered != 0))
            
            # Check that amplitude is approximately doubled (+6dB)
            original_peak = np.max(np.abs(signals[band]))
            filtered_peak = np.max(np.abs(filtered))
            self.assertAlmostEqual(
                filtered_peak / original_peak,
                2.0,  # +6dB should double amplitude
                places=1
            )
            
    def test_invalid_band(self):
        """Test handling of invalid frequency band."""
        signal = self.generate_test_signal(1000)
        with self.assertRaises(ValueError):
            self.equalizer.apply_band_filter(signal, 'invalid_band', 0)
            
    def test_full_eq_chain(self):
        """Test processing through complete EQ chain."""
        # Generate complex test signal
        signal = (self.generate_test_signal(100) +   # Low
                 self.generate_test_signal(1000) +   # Mid
                 self.generate_test_signal(8000))    # High
                 
        # Apply EQ settings
        gains = {
            'low': -6,    # Cut lows
            'mid': 0,     # Leave mids
            'high': +6    # Boost highs
        }
        
        processed = self.equalizer.process(signal, gains)
        
        # Check that output is not all zeros
        self.assertTrue(np.any(processed != 0))
        
        # Check that output is properly normalized
        self.assertLessEqual(np.max(np.abs(processed)), 1.0)


class TestBackgroundSoundMixer(unittest.TestCase):
    def setUp(self):
        """Initialize mixer for testing."""
        self.sample_rate = 44100
        self.mixer = BackgroundSoundMixer(sample_rate=self.sample_rate)
        self.test_duration = 1.0  # 1 second
        
    def test_white_noise_generation(self):
        """Test white noise background generation."""
        volume = 0.1
        noise = self.mixer.generate_white_noise(
            self.test_duration,
            volume=volume
        )
        
        # Check basic properties
        self.assertEqual(
            len(noise),
            int(self.sample_rate * self.test_duration)
        )
        self.assertLessEqual(np.max(np.abs(noise)), volume)
        
        # Check that it's not silent
        self.assertTrue(np.any(noise != 0))
        
        # Check that it's roughly centered around zero
        self.assertAlmostEqual(np.mean(noise), 0, places=2)
        
    def test_ambient_drone_generation(self):
        """Test ambient drone background generation."""
        volume = 0.1
        base_freq = 100.0
        
        drone = self.mixer.generate_ambient_drone(
            self.test_duration,
            base_freq=base_freq,
            volume=volume
        )
        
        # Check basic properties
        self.assertEqual(
            len(drone),
            int(self.sample_rate * self.test_duration)
        )
        self.assertLessEqual(np.max(np.abs(drone)), volume)
        
        # Check that it's not silent
        self.assertTrue(np.any(drone != 0))
        
        # Verify presence of base frequency using FFT
        fft = np.fft.rfft(drone)
        freqs = np.fft.rfftfreq(len(drone), 1/self.sample_rate)
        base_idx = np.argmin(np.abs(freqs - base_freq))
        self.assertTrue(np.abs(fft[base_idx]) > 0)
        
    def test_background_mixing_mono(self):
        """Test mixing background with mono audio."""
        # Generate simple test signal
        t = np.linspace(0, self.test_duration,
                       int(self.sample_rate * self.test_duration), False)
        main_audio = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        
        # Test mixing with white noise
        mixed = self.mixer.mix_background(
            main_audio,
            background_type='white_noise',
            volume=0.1
        )
        
        # Check that output matches input length
        self.assertEqual(len(mixed), len(main_audio))
        
        # Check that output is normalized
        self.assertLessEqual(np.max(np.abs(mixed)), 1.0)
        
        # Check that output is different from input
        self.assertTrue(np.any(mixed != main_audio))
        
    def test_background_mixing_stereo(self):
        """Test mixing background with stereo audio."""
        # Generate simple stereo test signal
        t = np.linspace(0, self.test_duration,
                       int(self.sample_rate * self.test_duration), False)
        left = np.sin(2 * np.pi * 440 * t)
        right = np.sin(2 * np.pi * 444 * t)
        stereo = (left, right)
        
        # Test mixing with ambient drone
        mixed = self.mixer.mix_background(
            stereo,
            background_type='ambient',
            volume=0.1,
            eq_gains={'low': -3, 'mid': 0, 'high': 3}
        )
        
        # Check that output is stereo
        self.assertTrue(isinstance(mixed, tuple))
        self.assertEqual(len(mixed), 2)
        
        # Check that each channel is properly normalized
        self.assertLessEqual(np.max(np.abs(mixed[0])), 1.0)
        self.assertLessEqual(np.max(np.abs(mixed[1])), 1.0)
        
        # Check that output channels are different from input
        self.assertTrue(np.any(mixed[0] != stereo[0]))
        self.assertTrue(np.any(mixed[1] != stereo[1]))


if __name__ == '__main__':
    unittest.main()
