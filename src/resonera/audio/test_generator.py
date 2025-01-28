"""
Unit tests for audio generation functionality.
"""
import unittest
import numpy as np
from unittest.mock import MagicMock, patch
from flask import Flask
from .generator import AudioGenerator

class TestAudioGenerator(unittest.TestCase):
    def setUp(self):
        # Create test Flask app
        self.app = Flask(__name__)
        self.app.config.update({
            'AUDIO_UPLOAD_FOLDER': '/tmp'
        })
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        self.generator = AudioGenerator()
        self.test_frequency = 10.0  # 10 Hz alpha wave
        self.test_duration = 1.0    # 1 second
        self.test_volume = 0.7      # 70% volume
    
    def tearDown(self):
        self.ctx.pop()
    
    def test_sine_wave_generation(self):
        """Test basic sine wave generation."""
        wave = self.generator.generate_sine_wave(
            self.test_frequency,
            self.test_duration,
            self.test_volume
        )
        
        # Check wave properties
        self.assertEqual(len(wave), int(self.generator.sample_rate * self.test_duration))
        self.assertLessEqual(np.max(wave), self.test_volume)
        self.assertGreaterEqual(np.min(wave), -self.test_volume)
    
    def test_binaural_beat_generation(self):
        """Test binaural beat generation."""
        left, right = self.generator.generate_binaural_beat(
            self.test_frequency,
            self.test_duration,
            self.test_volume
        )
        
        # Check both channels are generated
        self.assertEqual(len(left), len(right))
        self.assertEqual(len(left), int(self.generator.sample_rate * self.test_duration))
        
        # Check volume levels
        self.assertLessEqual(np.max(left), self.test_volume)
        self.assertLessEqual(np.max(right), self.test_volume)
    
    def test_isochronic_tone_generation(self):
        """Test isochronic tone generation."""
        tone = self.generator.generate_isochronic_tone(
            self.test_frequency,
            self.test_duration,
            self.test_volume
        )
        
        # Check tone properties
        self.assertEqual(len(tone), int(self.generator.sample_rate * self.test_duration))
        self.assertLessEqual(np.max(tone), self.test_volume)
    
    def test_frequency_transition(self):
        """Test frequency transition between states."""
        # Generate first audio
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.name = '/tmp/test1.wav'
            self.generator.generate(10.0, 1.0)  # Alpha
            
            # Generate second audio with transition
            mock_temp.return_value.name = '/tmp/test2.wav'
            audio_file = self.generator.generate(4.0, 2.0)  # Theta
            
            # Check that transition was used
            self.assertEqual(self.generator._last_frequency, 4.0)
    
    def test_optimal_carrier_frequency(self):
        """Test carrier frequency optimization for different ranges."""
        # Test each frequency range
        self.assertEqual(self.generator.get_optimal_carrier_frequency(2.0), 100.0)   # Delta
        self.assertEqual(self.generator.get_optimal_carrier_frequency(6.0), 200.0)   # Theta
        self.assertEqual(self.generator.get_optimal_carrier_frequency(10.0), 440.0)  # Alpha
        self.assertEqual(self.generator.get_optimal_carrier_frequency(40.0), 500.0)  # Gamma

if __name__ == '__main__':
    unittest.main()
