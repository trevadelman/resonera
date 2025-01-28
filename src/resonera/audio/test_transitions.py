"""
Unit tests for frequency transition functionality.
"""
import unittest
import numpy as np
from .transitions import FrequencyTransition

class TestFrequencyTransition(unittest.TestCase):
    def setUp(self):
        self.transition = FrequencyTransition()
        self.start_freq = 8.0   # Alpha
        self.end_freq = 4.0     # Theta
        self.duration = 5.0     # 5 seconds
        self.expected_samples = int(self.transition.sample_rate * self.duration)
    
    def test_linear_transition(self):
        """Test linear frequency transition."""
        frequencies = self.transition.linear_transition(
            self.start_freq,
            self.end_freq,
            self.duration
        )
        
        # Check array properties
        self.assertEqual(len(frequencies), self.expected_samples)
        self.assertAlmostEqual(frequencies[0], self.start_freq)
        self.assertAlmostEqual(frequencies[-1], self.end_freq)
        
        # Check linearity
        mid_point = len(frequencies) // 2
        expected_mid_freq = (self.start_freq + self.end_freq) / 2
        self.assertAlmostEqual(frequencies[mid_point], expected_mid_freq, places=1)
    
    def test_exponential_transition(self):
        """Test exponential frequency transition."""
        frequencies = self.transition.exponential_transition(
            self.start_freq,
            self.end_freq,
            self.duration
        )
        
        # Check array properties
        self.assertEqual(len(frequencies), self.expected_samples)
        self.assertAlmostEqual(frequencies[0], self.start_freq)
        self.assertAlmostEqual(frequencies[-1], self.end_freq)
        
        # Check exponential nature
        mid_point = len(frequencies) // 2
        mid_freq = frequencies[mid_point]
        # In exponential curve, midpoint should be closer to start than linear
        self.assertGreater(mid_freq, (self.start_freq + self.end_freq) / 2)
    
    def test_sigmoid_transition(self):
        """Test sigmoid frequency transition."""
        frequencies = self.transition.sigmoid_transition(
            self.start_freq,
            self.end_freq,
            self.duration
        )
        
        # Check array properties
        self.assertEqual(len(frequencies), self.expected_samples)
        self.assertAlmostEqual(frequencies[0], self.start_freq, places=1)
        self.assertAlmostEqual(frequencies[-1], self.end_freq, places=1)
        
        # Check sigmoid nature (symmetric around midpoint)
        quarter_point = len(frequencies) // 4
        three_quarter_point = 3 * len(frequencies) // 4
        mid_point = len(frequencies) // 2
        
        first_quarter_change = frequencies[quarter_point] - frequencies[0]
        last_quarter_change = frequencies[-1] - frequencies[three_quarter_point]
        
        # Changes should be similar due to sigmoid symmetry
        self.assertAlmostEqual(
            first_quarter_change,
            last_quarter_change,
            places=1
        )
    
    def test_optimal_duration(self):
        """Test optimal duration calculation."""
        # Small frequency change
        duration = self.transition.calculate_optimal_duration(10.0, 11.5)
        self.assertEqual(duration, 5.0)
        
        # Medium frequency change
        duration = self.transition.calculate_optimal_duration(10.0, 14.0)
        self.assertEqual(duration, 10.0)
        
        # Large frequency change
        duration = self.transition.calculate_optimal_duration(10.0, 40.0)
        self.assertEqual(duration, 20.0)
    
    def test_transition_points(self):
        """Test transition points calculation."""
        frequencies = [10.0, 8.0, 6.0, 4.0]  # Alpha to Theta progression
        timestamps = [0.0, 10.0, 20.0, 30.0]  # 10-second intervals
        
        transitions = self.transition.get_transition_points(frequencies, timestamps)
        
        # Check number of transitions
        self.assertEqual(len(transitions), len(frequencies) - 1)
        
        # Check transition properties
        for i, (start_time, end_time, duration) in enumerate(transitions):
            self.assertEqual(start_time, timestamps[i])
            self.assertEqual(end_time, timestamps[i + 1])
            self.assertEqual(duration, 10.0)  # Each transition is 10 seconds
    
    def test_invalid_transition_points(self):
        """Test error handling for invalid transition points."""
        frequencies = [10.0, 8.0, 6.0]
        timestamps = [0.0, 10.0]  # Mismatched lengths
        
        with self.assertRaises(ValueError):
            self.transition.get_transition_points(frequencies, timestamps)

if __name__ == '__main__':
    unittest.main()
