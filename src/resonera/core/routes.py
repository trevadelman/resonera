"""
Core routes for authentication and user management.
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db, User

bp = Blueprint('core', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        has_medical_condition=data.get('has_medical_condition', False),
        emergency_contact=data.get('emergency_contact')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    # Find and validate user
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create access token with string ID
    access_token = create_access_token(identity=str(user.id))
    current_app.logger.info(f'User {user.username} logged in successfully')
    return jsonify({
        'access_token': access_token,
        'token_type': 'Bearer',
        'user_id': user.id
    }), 200

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile."""
    try:
        user_id = int(get_jwt_identity())
        current_app.logger.info(f'Fetching profile for user ID: {user_id}')
        
        user = User.query.get(user_id)
        if not user:
            current_app.logger.error(f'User ID {user_id} not found in database')
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'username': user.username,
            'email': user.email,
            'max_frequency': user.max_frequency,
            'volume_preference': user.volume_preference,
            'has_medical_condition': user.has_medical_condition,
            'emergency_contact': user.emergency_contact
        }), 200
    except Exception as e:
        current_app.logger.error(f'Error fetching profile: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    allowed_fields = [
        'max_frequency', 'volume_preference',
        'has_medical_condition', 'emergency_contact'
    ]
    
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    db.session.commit()
    
    return jsonify({'message': 'Profile updated successfully'}), 200
