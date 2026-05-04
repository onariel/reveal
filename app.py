from flask import Flask
from routes.auth import auth_bp
from routes.home import home_bp
from routes.posts import posts_bp
from routes.likes import likes_bp
from routes.comments import comments_bp

app = Flask(__name__)

# Max upload size: 100 MB
# Without this Flask would accept files of any size
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(comments_bp)

if __name__ == '__main__':
    app.run(debug=True)