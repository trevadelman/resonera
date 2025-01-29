"""
Test script for email functionality.
"""
from .email import EmailSender
from .config import Config
import os
import sys

def test_welcome_email():
    """Send a test welcome email."""
    print("Starting email test...")
    
    # Verify environment variables are loaded
    print(f"Email configuration loaded: {bool(Config.EMAIL_USER)}")
    print(f"Using email address: {Config.EMAIL_USER[:3]}...{Config.EMAIL_USER[-10:]}")
    
    # Test recipient email
    recipient = Config.EMAIL_USER  # Send to self for testing
    
    try:
        print("\nLoading email templates...")
        # Load welcome email templates
        text_content, html_content = EmailSender.load_template('welcome')
        print("✓ Templates loaded successfully")
        
        print("\nAttempting to send email...")
        # Send email
        success = EmailSender.send_email(
            to_addresses=[recipient],
            subject="Welcome to Resonera - Test Email",
            text_content=text_content,
            html_content=html_content
        )
        
        if success:
            print("✓ Test email sent successfully!")
        else:
            print("✗ Failed to send test email")
            
    except FileNotFoundError as e:
        print(f"✗ Template file not found: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error during test: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        sys.exit(1)

if __name__ == '__main__':
    test_welcome_email()
