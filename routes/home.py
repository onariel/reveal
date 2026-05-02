from flask import Blueprint, render_template, request
from middleware.auth import require_auth

home_bp = Blueprint('home', __name__)


@home_bp.route('/home')
@require_auth
def home():
    return render_template('home/home.html', username=request.username)