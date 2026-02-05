from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models import User, db

auth_router = Blueprint('auth', __name__, url_prefix='/auth')


@auth_router.post('/register')
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if not email or '@' not in email:
            return jsonify({'error': 'Valid email is required'}), 400
        
        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already taken'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user (password is hashed in __init__)
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Create access token / revised for cloud prod
        access_token = create_access_token(identity=str(new_user.user_id))
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_router.post('/login')
def login():
    """Login existing user"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Create access token / revised for cloud prod
        access_token = create_access_token(identity=str(user.user_id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_router.get('/me')
@jwt_required()
def get_current_user():
    """Get current logged-in user's info"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500