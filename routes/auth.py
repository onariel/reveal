import bcrypt
from flask import Blueprint, request, render_template, redirect, url_for, make_response
from models.user import get_user_by_email, create_user, email_exists, username_exists
from middleware.auth import generate_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Redirect root to login."""
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    # --- POST: process the login form ---
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    # Always use the same error message for wrong email or password
    # so attackers can't tell which one is wrong
    error = 'Invalid email or password.'

    user = get_user_by_email(email)
    if not user:
        return render_template('auth/login.html', error=error)

    password_matches = bcrypt.checkpw(password.encode(), user['password_hash'].encode())
    if not password_matches:
        return render_template('auth/login.html', error=error)

    # Generate JWT and store it in an HTTP-only cookie
    token = generate_token(str(user['id']), user['name'])
    response = make_response(redirect(url_for('home.home')))
    response.set_cookie(
        'token',
        token,
        httponly=True,   # JS cannot access this cookie (XSS protection)
        samesite='Lax'   # CSRF protection
    )
    return response


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    # --- POST: process the register form ---
    name     = request.form.get('name', '').strip()
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    confirm  = request.form.get('confirm_password', '').strip()

    # Validate inputs
    if not name or not email or not password:
        return render_template('auth/register.html', error='All fields are required.')

    if password != confirm:
        return render_template('auth/register.html', error='Passwords do not match.')

    #this should be put to 8 but for testing I am putting it to 1
    if len(password) < 1:
        return render_template('auth/register.html', error='Password must be at least 8 characters.')

    if email_exists(email):
        return render_template('auth/register.html', error='An account with this email already exists.')

    if username_exists(name):
        return render_template('auth/register.html', error='This username is already taken.')

    # Hash the password before storing it
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    create_user(name, email, password_hash)

    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    """Delete the JWT cookie to log the user out."""
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('token')
    return response