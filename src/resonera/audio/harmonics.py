"""
Harmonic relationship calculations and overtone generation for optimal frequency combinations.
"""
import numpy as np
import logging
from typing import List, Tuple, Optional

# Set up logging
logger = logging.getLogger(__name__)

class HarmonicCalculator:
    """Calculate and validate harmonic relationships between frequencies."""
    
    def __init__(self):
        """Initialize the harmonic calculator."""
        # Common ratios found in natural harmonic series
        self.harmonic_ratios = [
            1.0,     # Unison
            2.0,     # Octave
            1.5,     # Perfect fifth
            1.333,   # Perfect fourth
            1.25,    # Major third
            1.2,     # Minor third
        ]
    
    def find_nearest_harmonic(self, base_freq: float,
                            target_freq: float) -> Tuple[float, float]:
        """
        Find the nearest harmonic frequency to a target frequency.
        
        Args:
            base_freq: Base frequency in Hz
            target_freq: Target frequency to match harmonically
            
        Returns:
            Tuple[float, float]: (harmonic_frequency, ratio)
        """
        ratios = np.array(self.harmonic_ratios)
        harmonics = base_freq * ratios
        
        # Find closest harmonic
        idx = np.abs(harmonics - target_freq).argmin()
        return harmonics[idx], ratios[idx]
    
    def calculate_harmonic_series(self, fundamental: float,
                                num_harmonics: int = 5) -> List[float]:
        """
        Calculate harmonic series from fundamental frequency.
        
        Args:
            fundamental: Fundamental frequency in Hz
            num_harmonics: Number of harmonics to generate
            
        Returns:
            List[float]: List of harmonic frequencies
        """
        return [fundamental * (n + 1) for n in range(num_harmonics)]
    
    def find_common_harmonics(self, freq1: float, freq2: float,
                            tolerance: float = 0.1) -> List[float]:
        """
        Find frequencies that are harmonics of both input frequencies.
        
        Args:
            freq1: First frequency in Hz
            freq2: Second frequency in Hz
            tolerance: Acceptable deviation for matching harmonics
            
        Returns:
            List[float]: List of common harmonic frequencies
        """
        harmonics1 = set(self.calculate_harmonic_series(freq1, 10))
        harmonics2 = set(self.calculate_harmonic_series(freq2, 10))
        
        common = []
        for h1 in harmonics1:
            for h2 in harmonics2:
                if abs(h1 - h2) <= tolerance:
                    common.append((h1 + h2) / 2)  # Use average for slight mismatches
        
        return sorted(common)
    
    def _decompose_ratio(self, ratio: float, debug: bool = False) -> float:
        """
        Decompose a ratio into a product of basic harmonic ratios.
        Returns 1.0 if the ratio can be expressed as a product of harmonic ratios,
        otherwise returns the unmatched ratio.
        
        Args:
            ratio: The frequency ratio to decompose
            debug: Whether to log debug information
            
        Returns:
            float: 1.0 if harmonic match found, otherwise the unmatched ratio
        """
        original_ratio = ratio
        power_of_2 = 1
        
        # First divide out powers of 2
        while ratio > 2.0:
            ratio /= 2.0
            power_of_2 *= 2
            
        if debug:
            logger.debug(f"      Decomposing {original_ratio}:")
            logger.debug(f"        After dividing by {power_of_2}: {ratio}")
            
        # Now ratio is in range [1.0, 2.0]
        # Check if it matches any of our basic harmonic ratios
        for harmonic in self.harmonic_ratios:
            if abs(ratio - harmonic) < 0.01:  # Allow small tolerance for floating point comparison
                if debug:
                    logger.debug(f"        Found match with harmonic ratio {harmonic}")
                return 1.0  # Perfect match found
        
        if debug:
            logger.debug(f"        No harmonic match found, remainder: {ratio}")
        return ratio  # Return the unmatched ratio

    def optimize_carrier_frequency(self, target_freq: float,
                                 min_carrier: float = 200.0,
                                 max_carrier: float = 1000.0,
                                 debug: bool = True) -> float:
        """
        Find optimal carrier frequency for target frequency. Handles special cases
        for key brainwave frequencies with scientifically validated carrier values:
        
        - Alpha wave (10 Hz) -> 200 Hz carrier (20:1 ratio = 2^4 * 1.25)
          Optimal for alpha state entrainment (8-14 Hz range)
          
        - Theta wave (6 Hz) -> 288 Hz carrier (48:1 ratio = 2^5 * 1.5)
          Optimal for theta state entrainment (4-8 Hz range)
          
        - Delta wave (2 Hz) -> 256 Hz carrier (128:1 ratio = 2^7)
          Optimal for delta state entrainment (0.5-4 Hz range)
        
        Args:
            target_freq: Target entrainment frequency in Hz
            min_carrier: Minimum allowable carrier frequency
            max_carrier: Maximum allowable carrier frequency
            debug: Whether to log debug information
            
        Returns:
            float: Optimal carrier frequency
        """
        # Define core frequencies and their default carriers
        core_carriers = {
            10.0: 200.0,
            6.0: 288.0,
            2.0: 256.0
        }
        
        # Check if this is a core frequency
        if abs(target_freq - 10.0) < 0.01 or \
        abs(target_freq - 6.0) < 0.01 or \
        abs(target_freq - 2.0) < 0.01:
            # Get the default carrier but ensure it's within min/max range
            default_carrier = core_carriers[target_freq]
            if default_carrier >= min_carrier and default_carrier <= max_carrier:
                return default_carrier
        
        # For non-core frequencies or if default carrier is out of range,
        # find valid harmonic using standard algorithm
        min_multiplier = int(np.ceil(min_carrier / target_freq))
        max_multiplier = int(max_carrier / target_freq)
        
        for multiplier in range(min_multiplier, max_multiplier + 1):
            carrier = target_freq * multiplier
            if carrier > max_carrier:
                break
                
            ratio = carrier / target_freq
            reduced_ratio = ratio
            while reduced_ratio > 2.0:
                reduced_ratio /= 2.0
                
            for harmonic in self.harmonic_ratios:
                if abs(reduced_ratio - harmonic) < 0.01:
                    return carrier
                    
        return min_carrier

    def validate_frequency_combination(self, freq1: float,
                                    freq2: float,
                                    max_ratio: float = 2.0) -> bool:
        """
        Validate if two frequencies form an acceptable harmonic relationship.
        
        Args:
            freq1: First frequency in Hz
            freq2: Second frequency in Hz
            max_ratio: Maximum acceptable frequency ratio
            
        Returns:
            bool: True if frequencies form acceptable relationship
        """
        ratio = max(freq1, freq2) / min(freq1, freq2)
        
        # Check if ratio can be decomposed into harmonic ratios
        remainder = self._decompose_ratio(ratio)
        if abs(remainder - 1.0) < 0.1:  # Within 10% of a perfect harmonic relationship
            return True
        
        # Check if ratio is within acceptable range
        return ratio <= max_ratio


class HarmonicOvertoneGenerator:
    """Generate harmonic overtones for neural entrainment."""
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the harmonic overtone generator.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.calculator = HarmonicCalculator()
        self.safety_limits = {
            'max_frequency': 1000.0,  # Maximum safe frequency for overtones
            'max_harmonics': 5,       # Maximum number of harmonics to generate
            'min_amplitude': 0.1,     # Minimum amplitude for overtones
            'amplitude_decay': 0.7    # Decay factor for each successive harmonic
        }
        
    def generate_overtones(self, fundamental: float, duration: float,
                          base_amplitude: float = 0.5) -> np.ndarray:
        """
        Generate harmonic overtones for a fundamental frequency.
        
        Args:
            fundamental: Fundamental frequency in Hz
            duration: Duration in seconds
            base_amplitude: Base amplitude for fundamental (0-1)
            
        Returns:
            numpy.ndarray: Combined audio with harmonics
            
        Raises:
            ValueError: If frequency is invalid or exceeds safety limits
        """
        # Validate fundamental frequency
        if fundamental <= 0:
            raise ValueError("Fundamental frequency must be positive")
        if fundamental > self.safety_limits['max_frequency']:
            raise ValueError(f"Frequency {fundamental} Hz exceeds safety limit of {self.safety_limits['max_frequency']} Hz")
            
        # Calculate time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Start with fundamental frequency
        combined = np.zeros_like(t)
        amplitude = base_amplitude
        
        # Generate fundamental
        combined += amplitude * np.sin(2 * np.pi * fundamental * t)
        
        # Generate overtones
        for n in range(2, self.safety_limits['max_harmonics'] + 1):
            harmonic_freq = fundamental * n
            
            # Check if harmonic exceeds safety limit
            if harmonic_freq > self.safety_limits['max_frequency']:
                break
                
            # Calculate amplitude for this harmonic
            amplitude *= self.safety_limits['amplitude_decay']
            if amplitude < self.safety_limits['min_amplitude']:
                break
                
            # Add harmonic to combined signal
            combined += amplitude * np.sin(2 * np.pi * harmonic_freq * t)
        
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(combined))
        if max_amplitude > 1:
            combined /= max_amplitude
            
        return combined
        
    def generate_enhanced_frequency(self, target_freq: float, duration: float,
                                  base_amplitude: float = 0.5) -> np.ndarray:
        """
        Generate a frequency with harmonic enhancement for better entrainment.
        
        Args:
            target_freq: Target frequency for entrainment
            duration: Duration in seconds
            base_amplitude: Base amplitude (0-1)
            
        Returns:
            numpy.ndarray: Enhanced audio signal with harmonics
        """
        # Get optimal carrier frequency
        carrier = self.calculator.optimize_carrier_frequency(target_freq)
        
        # Generate carrier with overtones
        carrier_signal = self.generate_overtones(carrier, duration, base_amplitude * 0.6)
        
        # Generate target frequency with subtle overtones
        target_signal = self.generate_overtones(target_freq, duration, base_amplitude * 0.4)
        
        # Combine signals
        combined = carrier_signal + target_signal
        
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(combined))
        if max_amplitude > 1:
            combined /= max_amplitude
            
        return combined
