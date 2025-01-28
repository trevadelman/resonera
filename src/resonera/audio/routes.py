"""
Routes for audio generation and session management.
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..database import db, Session, SafetyLog
from .generator import AudioGenerator
from ..safety.validator import SafetyValidator

bp = Blueprint('audio', __name__)
audio_generator = AudioGenerator()
safety_validator = SafetyValidator()

@bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_audio():
    """Generate neural entrainment audio."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required parameters
    required_params = ['target_frequency', 'duration']
    if not all(param in data for param in required_params):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Validate frequency range
    if not safety_validator.validate_frequency(data['target_frequency']):
        return jsonify({'error': 'Frequency out of safe range'}), 400
    
    try:
        # Create new session
        session = Session(
            user_id=user_id,
            target_frequency=data['target_frequency'],
            volume_level=data.get('volume', 0.7)
        )
        db.session.add(session)
        db.session.commit()
        
        # Generate audio
        audio_file = audio_generator.generate(
            frequency=data['target_frequency'],
            duration=data['duration'],
            volume=data.get('volume', 0.7)
        )
        
        # Log successful generation
        safety_log = SafetyLog(
            session_id=session.id,
            event_type='AUDIO_GENERATED',
            severity='INFO',
            description=f'Audio generated at {data["target_frequency"]}Hz'
        )
        db.session.add(safety_log)
        db.session.commit()
        
        return send_file(
            audio_file,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'entrainment_{session.id}.wav'
        )
        
    except Exception as e:
        # Log error
        if session:
            safety_log = SafetyLog(
                session_id=session.id,
                event_type='GENERATION_ERROR',
                severity='ERROR',
                description=str(e)
            )
            db.session.add(safety_log)
            db.session.commit()
        
        return jsonify({'error': 'Audio generation failed'}), 500

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    """Get user's entrainment sessions."""
    user_id = get_jwt_identity()
    
    sessions = Session.query.filter_by(user_id=user_id).order_by(Session.start_time.desc()).all()
    
    return jsonify([{
        'id': session.id,
        'start_time': session.start_time.isoformat(),
        'end_time': session.end_time.isoformat() if session.end_time else None,
        'target_frequency': session.target_frequency,
        'actual_frequency': session.actual_frequency,
        'volume_level': session.volume_level,
        'effectiveness_rating': session.effectiveness_rating,
        'notes': session.notes
    } for session in sessions]), 200

@bp.route('/sessions/<int:session_id>/rate', methods=['POST'])
@jwt_required()
def rate_session(session_id):
    """Rate the effectiveness of a session."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'rating' not in data:
        return jsonify({'error': 'Rating is required'}), 400
    
    session = Session.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    session.effectiveness_rating = data['rating']
    session.notes = data.get('notes')
    
    db.session.commit()
    
    return jsonify({'message': 'Session rated successfully'}), 200

@bp.route('/sessions/<int:session_id>/stop', methods=['POST'])
@jwt_required()
def stop_session(session_id):
    """Stop an active entrainment session."""
    user_id = get_jwt_identity()
    
    session = Session.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    if session.end_time:
        return jsonify({'error': 'Session already ended'}), 400
    
    from datetime import datetime
    session.end_time = datetime.utcnow()
    
    safety_log = SafetyLog(
        session_id=session.id,
        event_type='SESSION_STOPPED',
        severity='INFO',
        description='Session stopped by user'
    )
    
    db.session.add(safety_log)
    db.session.commit()
    
    return jsonify({'message': 'Session stopped successfully'}), 200
