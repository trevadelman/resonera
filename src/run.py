"""
Main entry point for the Resonera application.
"""
import os
from resonera import create_app
from resonera.core.config import Config

def main():
    """Run the Flask application."""
    # Create the audio upload directory if it doesn't exist
    os.makedirs(Config.AUDIO_UPLOAD_FOLDER, exist_ok=True)
    
    # Create and configure the app
    app = create_app()
    
    # Run the app in debug mode for development
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()
