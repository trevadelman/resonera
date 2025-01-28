"""
Database initialization and models for Resonera.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Log initialization
        app.logger.info("Database initialized successfully")
        app.logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

class User(db.Model):
    """User model for authentication and profile management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # User preferences
    max_frequency = db.Column(db.Float, default=40.0)  # Maximum safe frequency for user
    volume_preference = db.Column(db.Float, default=0.7)  # Preferred volume level
    
    # Safety settings
    has_medical_condition = db.Column(db.Boolean, default=False)
    emergency_contact = db.Column(db.String(120))
    
    def __repr__(self):
        return f'<User {self.username}>'

class Session(db.Model):
    """Session model for tracking user entrainment sessions."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    end_time = db.Column(db.DateTime(timezone=True))
    target_frequency = db.Column(db.Float, nullable=False)
    actual_frequency = db.Column(db.Float)
    volume_level = db.Column(db.Float, nullable=False)
    effectiveness_rating = db.Column(db.Integer)  # User-provided rating
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Session {self.id} for User {self.user_id}>'

class SafetyLog(db.Model):
    """Safety monitoring log for tracking potential issues."""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    event_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # INFO, WARNING, ERROR
    action_taken = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SafetyLog {self.id} for Session {self.session_id}>'
