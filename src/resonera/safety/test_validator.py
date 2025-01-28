"""
Unit tests for safety validation functionality.
"""
import unittest
from flask import Flask
from .validator import SafetyValidator

class TestSafetyValidator(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = Flask(__name__)
        self.app.config.update({
            'MIN_FREQUENCY': 0.5,
            'MAX_FREQUENCY': 100.0,
            'MAX_VOLUME': 0.8
        })
        
        # Create validator within app context
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.validator = SafetyValidator()
    
    def tearDown(self):
        self.ctx.pop()
    
    def test_frequency_validation(self):
        """Test frequency range validation."""
        # Test valid frequencies
        self.assertTrue(self.validator.validate_frequency(10.0))  # Alpha wave
        self.assertTrue(self.validator.validate_frequency(0.5))   # Min boundary
        self.assertTrue(self.validator.validate_frequency(100.0)) # Max boundary
        
        # Test invalid frequencies
        self.assertFalse(self.validator.validate_frequency(0.1))   # Too low
        self.assertFalse(self.validator.validate_frequency(150.0)) # Too high
    
    def test_volume_validation(self):
        """Test volume level validation."""
        # Test valid volumes
        self.assertTrue(self.validator.validate_volume(0.5))
        self.assertTrue(self.validator.validate_volume(0.0))
        self.assertTrue(self.validator.validate_volume(0.8))
        
        # Test invalid volumes
        self.assertFalse(self.validator.validate_volume(-0.1))
        self.assertFalse(self.validator.validate_volume(1.1))
    
    def test_session_parameters(self):
        """Test complete session parameter validation."""
        # Test valid parameters
        is_safe, message = self.validator.validate_session_parameters(
            frequency=10.0,
            volume=0.7,
            duration=300  # 5 minutes
        )
        self.assertTrue(is_safe)
        self.assertEqual(message, "Parameters validated successfully")
        
        # Test invalid duration
        is_safe, message = self.validator.validate_session_parameters(
            frequency=10.0,
            volume=0.7,
            duration=4000  # Over 1 hour
        )
        self.assertFalse(is_safe)
        self.assertTrue("Duration" in message)
        
        # Test invalid frequency
        is_safe, message = self.validator.validate_session_parameters(
            frequency=150.0,
            volume=0.7,
            duration=300
        )
        self.assertFalse(is_safe)
        self.assertTrue("Frequency" in message)
    
    def test_user_safety(self):
        """Test user-specific safety validation."""
        class MockUser:
            def __init__(self, has_medical_condition, emergency_contact, max_frequency):
                self.has_medical_condition = has_medical_condition
                self.emergency_contact = emergency_contact
                self.max_frequency = max_frequency
        
        # Test user with medical condition but no emergency contact
        unsafe_user = MockUser(True, None, 40.0)
        is_safe, message = self.validator.validate_user_safety(unsafe_user)
        self.assertFalse(is_safe)
        self.assertTrue("Emergency contact required" in message)
        
        # Test user with medical condition and emergency contact
        safe_user = MockUser(True, "123-456-7890", 40.0)
        is_safe, message = self.validator.validate_user_safety(safe_user)
        self.assertTrue(is_safe)

if __name__ == '__main__':
    unittest.main()
