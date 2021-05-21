import re

from bson import ObjectId
from flask import Flask, render_template, request, redirect
from mongoengine import connect

from models.campground import Campground
from models.review import Review

app = Flask(__name__)

connect("yelpCamp")


class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app, field='_method'):
        self.app = app
        self._regex = re.compile('.*' + field + '=([a-zA-Z]+)(&.*|$)')

    def __call__(self, environ, start_response):
        method = self._regex.match(environ.get('QUERY_STRING', ''))
        if method is not None:
            method = method.group(1).upper()
            if method in self.allowed_methods:
                environ['REQUEST_METHOD'] = method
            if method in self.bodyless_methods:
                environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)


app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)


@app.route('/', methods=['GET'])
def main():
    return render_template('home.html')


@app.route('/campgrounds', methods=['GET'])
def campgrounds():
    campgrounds = Campground.objects.all()
    return render_template('campgrounds/index.html', campgrounds=campgrounds)


@app.route('/campgrounds/<campground_id>', methods=['GET'])
def show_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    return render_template('campgrounds/show.html', campground=campground)


@app.route('/campgrounds/new', methods=['GET'])
def new_campground():
    return render_template('campgrounds/new.html')


@app.route('/campgrounds', methods=['POST'])
def post_campground():
    campground = Campground(**request.form)
    campground.save()
    return redirect(f'/campgrounds/{campground.id}')


@app.route('/campgrounds/<campground_id>/edit', methods=['GET'])
def edit_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    return render_template('campgrounds/edit.html', campground=campground)


@app.route('/campgrounds/<campground_id>', methods=['PUT'])
def put_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    for k, v in request.form.items():
        if isinstance(getattr(campground, k), str):
            setattr(campground, k, v)
        elif isinstance(getattr(campground, k), float):
            setattr(campground, k, float(v))
        else:
            raise NotImplementedError
    campground.save()
    return redirect(f'/campgrounds/{campground.id}')


@app.route('/campgrounds/<campground_id>', methods=['DELETE'])
def delete_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    # TODO: figure out how to do this automatically. Can't make it work with register_delete_rule...
    for review in campground.reviews:
        review.delete()
    campground.delete()
    return redirect(f'/campgrounds')


@app.route('/campgrounds/<campground_id>/reviews', methods=['POST'])
def post_review(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    review = Review(**request.form)
    review.save()
    campground.reviews.append(review)
    campground.save()
    return redirect(f'/campgrounds/{campground.id}')


@app.route('/campgrounds/<campground_id>/reviews/<review_id>', methods=['DELETE'])
def delete_review(campground_id, review_id):
    review = Review.objects.get(id=ObjectId(review_id))
    review.delete()  # the reverse_delete_rule=PULL will automatically remove it from the campground
    return redirect(f'/campgrounds/{campground_id}')


def error_page(e):
    return render_template('error.html', code=e.code, name=e.name, description=e.description), e.code


# TODO: can we do this for all codes?
for c in (404, 403, 410, 500):
    app.register_error_handler(c, error_page)
