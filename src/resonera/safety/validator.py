"""
Safety validation for audio generation and playback.
"""
from flask import current_app

class SafetyValidator:
    """Validates safety parameters for audio generation."""
    
    def validate_frequency(self, frequency: float) -> bool:
        """
        Validate if the requested frequency is within safe range.
        
        Args:
            frequency: The target frequency in Hz
            
        Returns:
            bool: True if frequency is safe, False otherwise
        """
        return (current_app.config['MIN_FREQUENCY'] <= frequency <= 
                current_app.config['MAX_FREQUENCY'])
    
    def validate_volume(self, volume: float) -> bool:
        """
        Validate if the requested volume is within safe range.
        
        Args:
            volume: The target volume level (0-1)
            
        Returns:
            bool: True if volume is safe, False otherwise
        """
        return 0 <= volume <= current_app.config['MAX_VOLUME']
    
    def validate_session_parameters(self, frequency: float, volume: float,
                                  duration: int) -> tuple[bool, str]:
        """
        Validate all session parameters for safety.
        
        Args:
            frequency: The target frequency in Hz
            volume: The target volume level (0-1)
            duration: Session duration in seconds
            
        Returns:
            tuple: (is_safe, message) where is_safe is a boolean and message
                  provides details if validation fails
        """
        if not self.validate_frequency(frequency):
            return False, f"Frequency {frequency}Hz is outside safe range"
        
        if not self.validate_volume(volume):
            return False, f"Volume level {volume} is outside safe range"
        
        if duration <= 0 or duration > 3600:  # Max 1 hour
            return False, f"Duration {duration}s is invalid"
        
        return True, "Parameters validated successfully"
    
    def validate_user_safety(self, user) -> tuple[bool, str]:
        """
        Validate user-specific safety considerations.
        
        Args:
            user: User model instance
            
        Returns:
            tuple: (is_safe, message) indicating if it's safe for user
        """
        if user.has_medical_condition and not user.emergency_contact:
            return False, "Emergency contact required for users with medical conditions"
        
        if user.max_frequency < current_app.config['MAX_FREQUENCY']:
            current_app.config['MAX_FREQUENCY'] = user.max_frequency
            
        return True, "User safety validated"
