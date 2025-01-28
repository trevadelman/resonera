"""
Frequency transition algorithms for smooth brainwave state changes.
"""
import numpy as np
from typing import List, Tuple

class FrequencyTransition:
    """Handles smooth transitions between different brainwave frequencies."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def linear_transition(self, start_freq: float, end_freq: float,
                         duration: float) -> List[float]:
        """
        Create a linear frequency transition.
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Target frequency in Hz
            duration: Transition duration in seconds
            
        Returns:
            List[float]: Array of frequencies for each time step
        """
        num_steps = int(self.sample_rate * duration)
        return np.linspace(start_freq, end_freq, num_steps)
    
    def exponential_transition(self, start_freq: float, end_freq: float,
                             duration: float, curve: float = 2.0) -> List[float]:
        """
        Create an exponential frequency transition for more natural changes.
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Target frequency in Hz
            duration: Transition duration in seconds
            curve: Exponential curve factor (higher = steeper curve)
            
        Returns:
            List[float]: Array of frequencies for each time step
        """
        num_steps = int(self.sample_rate * duration)
        t = np.linspace(0, 1, num_steps)
        
        # Create exponential curve
        curve_factor = np.power(t, curve)
        
        # Map to frequency range
        return start_freq + (end_freq - start_freq) * curve_factor
    
    def sigmoid_transition(self, start_freq: float, end_freq: float,
                         duration: float, smoothness: float = 6.0) -> List[float]:
        """
        Create a sigmoid frequency transition for smooth acceleration/deceleration.
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Target frequency in Hz
            duration: Transition duration in seconds
            smoothness: Controls the steepness of the sigmoid curve
            
        Returns:
            List[float]: Array of frequencies for each time step
        """
        num_steps = int(self.sample_rate * duration)
        t = np.linspace(-smoothness/2, smoothness/2, num_steps)
        
        # Create sigmoid curve normalized to [0,1]
        sigmoid = 1 / (1 + np.exp(-t))
        sigmoid = (sigmoid - sigmoid[0]) / (sigmoid[-1] - sigmoid[0])
        
        # Map sigmoid [0,1] to frequency range
        return start_freq + (end_freq - start_freq) * sigmoid
    
    def calculate_optimal_duration(self, start_freq: float,
                                 end_freq: float) -> float:
        """
        Calculate optimal transition duration based on frequency difference.
        Larger frequency changes need more time for comfort.
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Target frequency in Hz
            
        Returns:
            float: Recommended transition duration in seconds
        """
        freq_diff = abs(end_freq - start_freq)
        
        if freq_diff < 2.0:
            return 5.0  # Small changes: 5 seconds
        elif freq_diff < 5.0:
            return 10.0  # Medium changes: 10 seconds
        else:
            return 20.0  # Large changes: 20 seconds
    
    def get_transition_points(self, frequencies: List[float],
                            timestamps: List[float]) -> List[Tuple[float, float, float]]:
        """
        Calculate transition points between a sequence of frequencies.
        
        Args:
            frequencies: List of target frequencies in Hz
            timestamps: List of times when each frequency should be reached
            
        Returns:
            List[Tuple[float, float, float]]: List of (start_time, end_time, duration)
        """
        if len(frequencies) != len(timestamps):
            raise ValueError("frequencies and timestamps must have same length")
        
        transitions = []
        for i in range(len(frequencies) - 1):
            start_time = timestamps[i]
            end_time = timestamps[i + 1]
            duration = end_time - start_time
            transitions.append((start_time, end_time, duration))
        
        return transitions
