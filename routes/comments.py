from flask import Blueprint, jsonify, request
from middleware.auth import require_auth
from models.comment import add_comment, get_comments_by_post

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@require_auth
def get_comments(post_id):
    comments = get_comments_by_post(post_id)
    return jsonify(comments)


@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@require_auth
def post_comment(post_id):
    data = request.get_json()
    text = data.get('text', '').strip() if data else ''

    if not text:
        return jsonify({'error': 'Comment cannot be empty.'}), 400

    if len(text) > 1000:
        return jsonify({'error': 'Comment is too long.'}), 400

    comment = add_comment(
        user_id=request.user_id,
        post_id=post_id,
        text=text
    )
    return jsonify(comment), 201