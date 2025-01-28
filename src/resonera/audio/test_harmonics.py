"""
Unit tests for harmonic relationship calculations.
"""
import unittest
import numpy as np
import logging
from .harmonics import HarmonicCalculator

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestHarmonicCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = HarmonicCalculator()
        self.base_freq = 100.0  # 100 Hz base frequency
    
    def test_find_nearest_harmonic(self):
        """Test finding nearest harmonic frequency."""
        # Test exact harmonic match
        harmonic, ratio = self.calculator.find_nearest_harmonic(
            self.base_freq, self.base_freq * 2
        )
        self.assertEqual(harmonic, self.base_freq * 2)  # Octave
        self.assertEqual(ratio, 2.0)
        
        # Test approximate match
        harmonic, ratio = self.calculator.find_nearest_harmonic(
            self.base_freq, self.base_freq * 1.45
        )
        self.assertAlmostEqual(harmonic, self.base_freq * 1.5, places=1)  # Perfect fifth
        self.assertEqual(ratio, 1.5)
    
    def test_calculate_harmonic_series(self):
        """Test harmonic series calculation."""
        harmonics = self.calculator.calculate_harmonic_series(
            self.base_freq, num_harmonics=3
        )
        
        expected = [
            self.base_freq,      # Fundamental
            self.base_freq * 2,  # First harmonic
            self.base_freq * 3   # Second harmonic
        ]
        
        self.assertEqual(len(harmonics), 3)
        for actual, expected in zip(harmonics, expected):
            self.assertAlmostEqual(actual, expected)
    
    def test_find_common_harmonics(self):
        """Test finding common harmonics between frequencies."""
        # Test frequencies with common harmonics
        freq1 = 100.0  # 100 Hz
        freq2 = 150.0  # 150 Hz (3:2 ratio)
        
        common = self.calculator.find_common_harmonics(freq1, freq2)
        
        # Should find 300 Hz as common harmonic
        # (3rd harmonic of 100 Hz, 2nd harmonic of 150 Hz)
        self.assertTrue(any(abs(h - 300.0) < 0.1 for h in common))
    
    def test_optimize_carrier_frequency(self):
        """
        Test carrier frequency optimization.
        
        Core test cases represent scientifically validated carrier frequencies
        for key brainwave states:
        
        Alpha Wave (8-14 Hz):
        - Test frequency: 10 Hz
        - Carrier: 200 Hz (20:1 ratio = 2^4 * 1.25)
        - Primary use: Focus, relaxation, light meditation
        
        Theta Wave (4-8 Hz):
        - Test frequency: 6 Hz
        - Carrier: 288 Hz (48:1 ratio = 2^5 * 1.5)
        - Primary use: Deep meditation, REM sleep
        
        Delta Wave (0.5-4 Hz):
        - Test frequency: 2 Hz
        - Carrier: 256 Hz (128:1 ratio = 2^7)
        - Primary use: Deep sleep, healing
        
        Additional test cases verify proper harmonic relationships
        for frequencies outside these core brainwave states.
        """
        # Core test cases (must match exactly)
        core_test_cases = [
            # Alpha wave (10 Hz)
            (10.0, 200.0, 500.0, 200.0),  # 20x ratio (2^4 * 1.25)
            # Theta wave (6 Hz)
            (6.0, 200.0, 500.0, 288.0),   # 48x ratio (2^5 * 1.5)
            # Delta wave (2 Hz)
            (2.0, 200.0, 500.0, 256.0),   # 128x ratio (2^7)
        ]
        
        # Additional test cases (verify harmonic relationships)
        additional_test_cases = [
            # Test frequencies between core cases
            (8.0, 200.0, 500.0),   # Between 10 Hz and 6 Hz
            (4.0, 200.0, 500.0),   # Between 6 Hz and 2 Hz
            
            # Test edge cases
            (15.0, 200.0, 500.0),  # Just above range
            (1.0, 200.0, 500.0),   # Just below range
            
            # Test with different min/max carriers
            (10.0, 300.0, 600.0),  # Higher min carrier
            (10.0, 100.0, 400.0),  # Lower min carrier
        ]
        
        # Test core cases (exact matches required)
        for target_freq, min_carrier, max_carrier, expected in core_test_cases:
            logger.debug(f"\nTesting with target_freq={target_freq}Hz:")
            logger.debug(f"  min_carrier={min_carrier}Hz")
            logger.debug(f"  max_carrier={max_carrier}Hz")
            logger.debug(f"  expected={expected}Hz")
            
            carrier = self.calculator.optimize_carrier_frequency(
                target_freq,
                min_carrier=min_carrier,
                max_carrier=max_carrier
            )
            
            # Log the results
            ratio = carrier / target_freq
            logger.debug(f"  Found carrier={carrier}Hz (ratio={ratio})")
            
            # Calculate and log the decomposition
            power_of_2 = 2 ** int(np.log2(ratio))
            remaining_ratio = ratio / power_of_2
            logger.debug(f"  Ratio decomposition: {power_of_2} * {remaining_ratio}")
            
            # Log the deviation from expected
            deviation = abs(carrier - expected)
            logger.debug(f"  Deviation from expected: {deviation}Hz")
            
            # Carrier should be within range
            self.assertGreaterEqual(carrier, min_carrier)
            self.assertLessEqual(carrier, max_carrier)
            
            # Should match expected value exactly
            self.assertAlmostEqual(
                carrier,
                expected,
                delta=1.0,
                msg=f"Carrier frequency not optimal for {target_freq}Hz"
            )
        
        # Test additional cases (verify harmonic relationships)
        for target_freq, min_carrier, max_carrier in additional_test_cases:
            carrier = self.calculator.optimize_carrier_frequency(
                target_freq,
                min_carrier=min_carrier,
                max_carrier=max_carrier
            )
            
            # Carrier should be within range
            self.assertGreaterEqual(carrier, min_carrier)
            self.assertLessEqual(carrier, max_carrier)
            
            # Should form valid harmonic relationship
            ratio = carrier / target_freq
            remainder = self.calculator._decompose_ratio(ratio)
            self.assertLess(
                abs(remainder - 1.0),
                0.1,
                msg=f"Failed to find harmonic ratio for {target_freq}Hz"
            )
    
    def test_validate_frequency_combination(self):
        """Test frequency combination validation."""
        # Test harmonic relationship
        self.assertTrue(
            self.calculator.validate_frequency_combination(100.0, 200.0)
        )  # 2:1 ratio (octave)
        
        self.assertTrue(
            self.calculator.validate_frequency_combination(100.0, 150.0)
        )  # 3:2 ratio (perfect fifth)
        
        # Test non-harmonic relationship
        self.assertFalse(
            self.calculator.validate_frequency_combination(100.0, 237.0)
        )  # Non-harmonic ratio
        
        # Test with custom max ratio
        self.assertTrue(
            self.calculator.validate_frequency_combination(
                100.0, 180.0, max_ratio=1.8
            )
        )  # Within custom ratio limit

if __name__ == '__main__':
    unittest.main()
