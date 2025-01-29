"""
Email functionality for the Resonera application.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import os
from .config import Config

class EmailSender:
    """Handles email sending functionality using MIME."""
    
    @staticmethod
    def send_email(
        to_addresses: List[str],
        subject: str,
        text_content: str,
        html_content: Optional[str] = None
    ) -> bool:
        """
        Send an email using MIME.
        
        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject line
            text_content: Plain text content of the email
            html_content: Optional HTML content of the email
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create message container
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = Config.EMAIL_FROM
            msg['To'] = ', '.join(to_addresses)
            
            # Add plain text part
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_content:
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
            
            print("Establishing SMTP connection...")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                print("✓ SMTP connection established")
                
                print("Starting TLS...")
                server.starttls()
                print("✓ TLS started")
                
                print("Attempting login...")
                server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
                print("✓ Login successful")
                
                print("Sending message...")
                server.send_message(msg)
                print("✓ Message sent")
                
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"Authentication failed: {str(e)}")
            print(f"Using email: {Config.EMAIL_USER}")
            print("Note: Password length:", len(Config.EMAIL_PASSWORD) if Config.EMAIL_PASSWORD else 0)
            return False
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return False

    @staticmethod
    def load_template(template_name: str) -> tuple[str, str]:
        """
        Load an email template from the templates directory.
        
        Args:
            template_name: Name of the template file (without extension)
            
        Returns:
            tuple: (text_content, html_content)
        """
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'email')
        
        # Load text version
        text_path = os.path.join(template_dir, f"{template_name}.txt")
        with open(text_path, 'r') as f:
            text_content = f.read()
            
        # Load HTML version if it exists
        html_content = None
        html_path = os.path.join(template_dir, f"{template_name}.html")
        if os.path.exists(html_path):
            with open(html_path, 'r') as f:
                html_content = f.read()
                
        return text_content, html_content
