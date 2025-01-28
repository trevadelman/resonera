"""
Unit tests for audio generation functionality.
"""
import unittest
import numpy as np
from .generator import AudioGenerator

class TestAudioGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = AudioGenerator()
        self.test_duration = 1.0    # 1 second
        self.test_volume = 0.7      # 70% volume
        
        # Test frequencies for each brainwave state
        self.test_frequencies = {
            'delta': 2.0,    # Deep sleep
            'theta': 6.0,    # Meditation
            'alpha': 10.0,   # Relaxed focus
            'gamma': 40.0    # High cognition
        }
    
    def test_optimal_carrier_frequency(self):
        """Test carrier frequency optimization for different ranges."""
        # Test each frequency range
        self.assertEqual(self.generator.get_optimal_carrier_frequency(2.0), 100.0)   # Delta
        self.assertEqual(self.generator.get_optimal_carrier_frequency(6.0), 200.0)   # Theta
        self.assertEqual(self.generator.get_optimal_carrier_frequency(10.0), 440.0)  # Alpha
        self.assertEqual(self.generator.get_optimal_carrier_frequency(40.0), 500.0)  # Gamma
    
    def test_sine_wave_generation(self):
        """Test basic sine wave generation for all frequency ranges."""
        for wave_type, freq in self.test_frequencies.items():
            wave = self.generator.generate_sine_wave(
                freq,
                self.test_duration,
                self.test_volume
            )
        
        # Check wave properties
        self.assertEqual(len(wave), int(self.generator.sample_rate * self.test_duration))
        self.assertLessEqual(np.max(wave), self.test_volume)
        self.assertGreaterEqual(np.min(wave), -self.test_volume)
    
    def test_binaural_beat_generation(self):
        """Test binaural beat generation for all frequency ranges."""
        for wave_type, freq in self.test_frequencies.items():
            left, right = self.generator.generate_binaural_beat(
                freq,
                self.test_duration,
                self.test_volume
            )
            
            # Check both channels are generated
            self.assertEqual(len(left), len(right))
            self.assertEqual(len(left), int(self.generator.sample_rate * self.test_duration))
            
            # Check volume levels
            self.assertLessEqual(np.max(left), self.test_volume)
            self.assertLessEqual(np.max(right), self.test_volume)
            
            # Verify carrier frequency is appropriate for the range
            carrier = self.generator.get_optimal_carrier_frequency(freq)
            self.assertGreater(carrier, freq)  # Carrier should be higher than target
        
        # Check both channels are generated
        self.assertEqual(len(left), len(right))
        self.assertEqual(len(left), int(self.generator.sample_rate * self.test_duration))
        
        # Check volume levels
        self.assertLessEqual(np.max(left), self.test_volume)
        self.assertLessEqual(np.max(right), self.test_volume)
    
    def test_isochronic_tone_generation(self):
        """Test isochronic tone generation for all frequency ranges."""
        for wave_type, freq in self.test_frequencies.items():
            tone = self.generator.generate_isochronic_tone(
                freq,
                self.test_duration,
                self.test_volume
            )
        
        # Check tone properties
        self.assertEqual(len(tone), int(self.generator.sample_rate * self.test_duration))
        self.assertLessEqual(np.max(tone), self.test_volume)
        
        # Check for amplitude modulation
        peaks = np.where(tone == np.max(tone))[0]
        if len(peaks) > 1:
            # Calculate average time between peaks
            avg_peak_distance = np.mean(np.diff(peaks))
            expected_distance = self.generator.sample_rate / self.test_frequency
            # Allow 5% tolerance
            self.assertAlmostEqual(
                avg_peak_distance,
                expected_distance,
                delta=expected_distance * 0.05
            )

if __name__ == '__main__':
    unittest.main()
