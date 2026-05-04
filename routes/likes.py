from flask import Blueprint, jsonify, request
from middleware.auth import require_auth
from models.like import toggle_like

likes_bp = Blueprint('likes', __name__)


@likes_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@require_auth
def like(post_id):
    """
    Toggle like on a post.
    Returns JSON so the browser can update the button without a page reload.

    Response: { "liked": true, "like_count": 5 }
    """
    result = toggle_like(user_id=request.user_id, post_id=post_id)
    return jsonify(result)