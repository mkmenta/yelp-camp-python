import os
from datetime import timedelta

import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask, render_template
from flask_session import Session
from mongoengine import connect

from routes.campgrounds import blueprint as campgrounds_blueprint
from routes.users import blueprint as users_blueprint, login_manager
from utils import HTTPMethodOverrideMiddleware

# Initialize app
app = Flask(__name__)

# Connect to MongoDB
connect("yelpCamp")

# Initialize sessions
app.secret_key = b'thisshouldbeabettersecret'
SESSION_USE_SIGNER = True  # Sign with secret key
SESSION_TYPE = 'filesystem'  # Save session data to file system
SESSION_FILE_DIR = '/tmp'  # Save session data into /tmp
SESSION_COOKIE_HTTPONLY = True  # Avoid XSS
PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # Lifetime of the session cookie
app.config.from_object(__name__)
Session(app)

# Add HTTP method override middleware (to allow PUT, DELETE etc.)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

# Initialize app with login manager
login_manager.init_app(app)

# Configure max file upload
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Configure cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_NAME'),
    api_key=os.environ.get('CLOUDINARY_KEY'),
    api_secret=os.environ.get('CLOUDINARY_SECRET'),
    secure=True
)

# Add extra routes from blueprints
app.register_blueprint(campgrounds_blueprint, url_prefix='/campgrounds')
app.register_blueprint(users_blueprint, url_prefix='/')


# Main routes
@app.route('/', methods=['GET'])
def main():
    return render_template('home.html')


def error_page(e):
    return render_template('error.html', code=e.code, name=e.name, description=e.description), e.code


# TODO: can we do this for all codes?
for c in (404, 403, 410, 500):
    app.register_error_handler(c, error_page)


# Jinja filters
@app.template_filter('env_override')
def env_override(value, key):
    return os.getenv(key, value)
