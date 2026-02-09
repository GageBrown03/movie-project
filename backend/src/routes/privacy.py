# backend/src/routes/privacy.py
# Privacy settings API routes for Flask

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, User

privacy = Blueprint('privacy', __name__, url_prefix='/api/privacy')


# ==========================================
# GET /api/privacy - Get current user's privacy settings
# ==========================================

@privacy.route('/', methods=['GET'])
@jwt_required()
def get_privacy_settings():
    """Get current user's privacy settings"""
    current_user_id = get_jwt_identity()
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'privacyCollection': user.privacy_collection or 'private',
        'privacyRatings': user.privacy_ratings or 'private',
        'privacyStats': user.privacy_stats or 'private',
        'privacyProfileSearchable': user.privacy_profile_searchable or False,
        'emailNotificationsFriendRequests': user.email_notifications_friend_requests if user.email_notifications_friend_requests is not None else True,
    }), 200


# ==========================================
# PUT /api/privacy - Update privacy settings
# ==========================================

@privacy.route('/', methods=['PUT'])
@jwt_required()
def update_privacy_settings():
    """Update current user's privacy settings"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Validate privacy levels
    valid_levels = ['private', 'friends', 'public']
    
    # Update privacy settings
    if 'privacyCollection' in data:
        if data['privacyCollection'] not in valid_levels:
            return jsonify({'error': 'Invalid privacy level for collection'}), 400
        user.privacy_collection = data['privacyCollection']
    
    if 'privacyRatings' in data:
        if data['privacyRatings'] not in valid_levels:
            return jsonify({'error': 'Invalid privacy level for ratings'}), 400
        user.privacy_ratings = data['privacyRatings']
    
    if 'privacyStats' in data:
        if data['privacyStats'] not in valid_levels:
            return jsonify({'error': 'Invalid privacy level for stats'}), 400
        user.privacy_stats = data['privacyStats']
    
    if 'privacyProfileSearchable' in data:
        user.privacy_profile_searchable = bool(data['privacyProfileSearchable'])
    
    if 'emailNotificationsFriendRequests' in data:
        user.email_notifications_friend_requests = bool(data['emailNotificationsFriendRequests'])
    
    # Save changes
    db.session.commit()
    
    return jsonify({
        'message': 'Privacy settings updated',
        'privacyCollection': user.privacy_collection,
        'privacyRatings': user.privacy_ratings,
        'privacyStats': user.privacy_stats,
        'privacyProfileSearchable': user.privacy_profile_searchable,
        'emailNotificationsFriendRequests': user.email_notifications_friend_requests,
    }), 200


# ==========================================
# GET /api/privacy/check/:user_id - Check what you can see about another user
# ==========================================

@privacy.route('/check/<int:target_user_id>', methods=['GET'])
@jwt_required()
def check_privacy(target_user_id):
    """
    Check what the current user can see about target_user_id
    Returns permissions object
    """
    current_user_id = get_jwt_identity()
    
    # Can always see own data
    if current_user_id == target_user_id:
        return jsonify({
            'canSeeCollection': True,
            'canSeeRatings': True,
            'canSeeStats': True,
            'canSeeNotes': True,
        }), 200
    
    target_user = User.query.get(target_user_id)
    
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if they're friends
    from src.routes.friends import are_friends
    friends = are_friends(current_user_id, target_user_id)
    
    # Determine permissions based on privacy settings
    def check_permission(privacy_level):
        if privacy_level == 'public':
            return True
        elif privacy_level == 'friends':
            return friends
        else:  # private
            return False
    
    return jsonify({
        'canSeeCollection': check_permission(target_user.privacy_collection or 'private'),
        'canSeeRatings': check_permission(target_user.privacy_ratings or 'private'),
        'canSeeStats': check_permission(target_user.privacy_stats or 'private'),
        'canSeeNotes': False,  # Notes are always private
        'isFriend': friends,
    }), 200