from flask import Blueprint, jsonify, request
from middleware.auth import require_auth
from models.follow import toggle_follow

users_bp = Blueprint('users', __name__)


@users_bp.route('/users/<int:user_id>/follow', methods=['POST'])
@require_auth
def follow(user_id):
    """
    Toggle follow/unfollow for the given user.
    Returns JSON: { "following": true }
    """
    if user_id == request.user_id:
        return jsonify({'error': 'You cannot follow yourself.'}), 400

    result = toggle_follow(follower_id=request.user_id, following_id=user_id)
    return jsonify(result)