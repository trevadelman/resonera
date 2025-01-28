"""
Resonera - Neural Entrainment Platform
Core initialization module
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from .database import init_db
from .core.config import Config

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure logging
    import logging
    logging.basicConfig(level=logging.INFO)
    
    app.logger.info("Creating Flask application")
    app.logger.info(f"SQLAlchemy Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Initialize extensions
    jwt = JWTManager(app)
    app.logger.info("JWT Manager initialized")
    
    # Initialize database
    init_db(app)
    app.logger.info("Database initialized")
    
    # Register blueprints
    from .core.routes import bp as core_bp
    from .audio.routes import bp as audio_bp
    app.register_blueprint(core_bp)
    app.register_blueprint(audio_bp, url_prefix='/audio')
    app.logger.info("Blueprints registered")
    
    return app
