import os
import uuid
from flask import Blueprint, request, render_template, redirect, url_for, current_app
from middleware.auth import require_auth
from models.post import create_post

posts_bp = Blueprint('posts', __name__)

# Allowed file extensions per media type
ALLOWED_IMAGES = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
ALLOWED_VIDEOS = {'mp4', 'mov', 'avi', 'webm'}


def get_extension(filename):
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


#This function checks if the file is of an allowed extension, and if also if is not of any
def get_media_type(extension):
    if extension in ALLOWED_IMAGES:
        return 'image'
    if extension in ALLOWED_VIDEOS:
        return 'video'
    return None


@posts_bp.route('/posts/create', methods=['GET', 'POST'])
@require_auth
def create():
    if request.method == 'GET':
        return render_template('posts/create.html')

    caption = request.form.get('caption', '').strip()
    file = request.files.get('media')

    if not file or file.filename == '':
        return render_template('posts/create.html', error='Please select an image or video.')

    extension = get_extension(file.filename)
    media_type = get_media_type(extension)

    if not media_type:
        return render_template('posts/create.html',
            error='Unsupported file type. Allowed: jpg, png, gif, webp, mp4, mov, avi, webm.')

    subfolder = 'images' if media_type == 'image' else 'videos'
    unique_name = f"{uuid.uuid4().hex}.{extension}"
    relative_path = f"uploads/{subfolder}/{unique_name}"
    absolute_path = os.path.join(current_app.static_folder, relative_path)

    file.save(absolute_path)

    create_post(
        user_id = request.user_id,
        caption = caption,
        media_path = relative_path,
        media_type = media_type
    )

    return redirect(url_for('home.home'))