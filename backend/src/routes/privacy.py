# backend/src/routes/privacy.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, User

privacy_bp = Blueprint('privacy', __name__, url_prefix='/api/privacy')


@privacy_bp.route('', methods=['GET'])
@jwt_required()
def get_privacy_settings():
    """Get current user's privacy settings and profile info"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'displayName': user.display_name,
            'bio': user.bio,
            'privacyCollection': user.privacy_collection,
            'privacyRatings': user.privacy_ratings,
            'privacyStats': user.privacy_stats,
            'privacyProfileSearchable': user.privacy_profile_searchable,
        }), 200
        
    except Exception as e:
        print(f"Error getting privacy settings: {e}")
        return jsonify({'error': 'Failed to get privacy settings'}), 500


@privacy_bp.route('', methods=['PUT'])
@jwt_required()
def update_privacy_settings():
    """Update privacy settings and profile info"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update profile info
        if 'displayName' in data:
            user.display_name = data['displayName']
        
        if 'bio' in data:
            user.bio = data['bio']
        
        # Update privacy settings
        if 'privacyCollection' in data:
            if data['privacyCollection'] not in ['private', 'friends', 'public']:
                return jsonify({'error': 'Invalid privacy setting'}), 400
            user.privacy_collection = data['privacyCollection']
        
        if 'privacyRatings' in data:
            if data['privacyRatings'] not in ['private', 'friends', 'public']:
                return jsonify({'error': 'Invalid privacy setting'}), 400
            user.privacy_ratings = data['privacyRatings']
        
        if 'privacyStats' in data:
            if data['privacyStats'] not in ['private', 'friends', 'public']:
                return jsonify({'error': 'Invalid privacy setting'}), 400
            user.privacy_stats = data['privacyStats']
        
        if 'privacyProfileSearchable' in data:
            user.privacy_profile_searchable = bool(data['privacyProfileSearchable'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Settings updated successfully',
            'displayName': user.display_name,
            'bio': user.bio,
            'privacyCollection': user.privacy_collection,
            'privacyRatings': user.privacy_ratings,
            'privacyStats': user.privacy_stats,
            'privacyProfileSearchable': user.privacy_profile_searchable,
        }), 200
        
    except Exception as e:
        print(f"Error updating privacy settings: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update privacy settings'}), 500


@privacy_bp.route('/check/<int:target_user_id>', methods=['GET'])
@jwt_required()
def check_permissions(target_user_id):
    """
    Check what the current user can see about a target user.
    Used by friend system to determine visibility.
    """
    try:
        current_user_id = int(get_jwt_identity())
        target_user = User.query.get(target_user_id)
        
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        # If viewing own profile, can see everything
        if current_user_id == target_user_id:
            return jsonify({
                'canViewCollection': True,
                'canViewRatings': True,
                'canViewStats': True,
            }), 200
        
        # Check if they're friends
        from src.models import Friendship, FriendshipStatus
        from sqlalchemy import or_, and_
        
        friendship = Friendship.query.filter(
            and_(
                or_(
                    and_(Friendship.user_id_1 == current_user_id, Friendship.user_id_2 == target_user_id),
                    and_(Friendship.user_id_1 == target_user_id, Friendship.user_id_2 == current_user_id)
                ),
                Friendship.status == FriendshipStatus.ACCEPTED
            )
        ).first()
        
        are_friends = friendship is not None
        
        # Determine permissions based on privacy settings
        can_view_collection = (
            target_user.privacy_collection == 'public' or
            (target_user.privacy_collection == 'friends' and are_friends)
        )
        
        can_view_ratings = (
            target_user.privacy_ratings == 'public' or
            (target_user.privacy_ratings == 'friends' and are_friends)
        )
        
        can_view_stats = (
            target_user.privacy_stats == 'public' or
            (target_user.privacy_stats == 'friends' and are_friends)
        )
        
        return jsonify({
            'canViewCollection': can_view_collection,
            'canViewRatings': can_view_ratings,
            'canViewStats': can_view_stats,
        }), 200
        
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return jsonify({'error': 'Failed to check permissions'}), 500