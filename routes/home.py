from flask import Blueprint, render_template, request
from middleware.auth import require_auth
from models.post import get_feed_post_ids, get_posts_by_ids
from models.like import get_liked_post_ids

home_bp = Blueprint('home', __name__)


@home_bp.route('/home')
@require_auth
def home():
    # Step 1: get the ordered list of post IDs from the algorithm
    post_ids = get_feed_post_ids(request.user_id)

    # Step 2: fetch the full data for those posts
    posts = get_posts_by_ids(post_ids)

    # Step 3: find which of those posts the current user already liked
    # so the heart icon renders correctly on page load
    liked_ids = get_liked_post_ids(request.user_id, post_ids)

    return render_template('home/home.html',
        username=request.username,
        posts=posts,
        liked_ids=liked_ids       # a set like {4, 17}
    )