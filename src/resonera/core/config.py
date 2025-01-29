"""
Configuration settings for the Resonera application.
"""
import os
from datetime import timedelta

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_ERROR_MESSAGE_KEY = 'msg'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///resonera.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Audio settings
    AUDIO_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio_files')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Safety settings
    MAX_FREQUENCY = 100  # Maximum frequency in Hz
    MIN_FREQUENCY = 0.5  # Minimum frequency in Hz
    MAX_VOLUME = 0.8    # Maximum volume (0-1)
    
    # Email settings
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL_FROM = os.environ.get('EMAIL_FROM', 'Resonera <noreply@resonera.com>')
    
    def init_app(self, app):
        """Initialize application configuration."""
        os.makedirs(self.AUDIO_UPLOAD_FOLDER, exist_ok=True)
