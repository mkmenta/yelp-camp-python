from flask import Flask, render_template
from mongoengine import connect

from routes.campgrounds import blueprint as campgrounds_blueprint
from utils import HTTPMethodOverrideMiddleware

app = Flask(__name__)

connect("yelpCamp")

app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

app.register_blueprint(campgrounds_blueprint, url_prefix='/campgrounds')


@app.route('/', methods=['GET'])
def main():
    return render_template('home.html')


def error_page(e):
    return render_template('error.html', code=e.code, name=e.name, description=e.description), e.code


# TODO: can we do this for all codes?
for c in (404, 403, 410, 500):
    app.register_error_handler(c, error_page)
