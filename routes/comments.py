from flask import Blueprint, jsonify, request
from middleware.auth import require_auth
from models.comment import add_comment, get_comments_by_post, comment_belongs_to_post
from services.notification_service import notify_post_commented

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@require_auth
def get_comments(post_id):
    comments = get_comments_by_post(post_id)
    tree = build_comment_tree(comments)   # ← organise into nested structure
    return jsonify(tree)    


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

    notify_post_commented(
    actor_user_id=request.user_id,
    post_id=post_id,
    comment_id=comment['id']
    )
    return jsonify(comment), 201


@comments_bp.route('/posts/<int:post_id>/comments/<int:comment_id>/reply', methods=['POST'])
@require_auth
def reply_comment(post_id, comment_id):
    data = request.get_json()
    text = data.get('text', '').strip() if data else ''

    if not text:
        return jsonify({'error': 'Reply cannot be empty.'}), 400

    if len(text) > 1000:
        return jsonify({'error': 'Reply is too long.'}), 400
    
    if not comment_belongs_to_post(comment_id, post_id):
        return jsonify({'error': 'Parent comment not found for this post.'}), 404

    reply = add_comment(
        user_id=request.user_id,
        post_id=post_id,
        text=text,
        parent_id=comment_id
    )

    notify_post_commented(
    actor_user_id=request.user_id,
    post_id=post_id,
    comment_id=reply['id']
    )

    return jsonify(reply), 201