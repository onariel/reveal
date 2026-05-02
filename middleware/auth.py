import jwt
import os
from functools import wraps
from flask import request, redirect, url_for


def generate_token(user_id, username):
    """Generate a JWT token for a user."""
    return jwt.encode(
        {'user_id': user_id, 'username': username},
        os.getenv('JWT_SECRET'),
        algorithm='HS256'
    )


def decode_token(token):
    """Decode a JWT token and return its payload, or None if invalid."""
    try:
        return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(f):
    """
    Decorator that protects a route behind JWT authentication.
    If the token is missing or invalid, redirects to login.
    If valid, injects request.user_id and request.username.

    Usage:
        @home_bp.route('/home')
        @require_auth
        def home():
            user_id = request.user_id
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return redirect(url_for('auth.login'))

        payload = decode_token(token)
        if payload is None:
            return redirect(url_for('auth.login'))

        # Inject user info directly into the request object
        request.user_id = payload['user_id']
        request.username = payload['username']

        return f(*args, **kwargs)

    return decorated