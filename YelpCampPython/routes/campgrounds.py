from bson import ObjectId
from flask import Blueprint, render_template, request, redirect

from models.campground import Campground
from routes.reviews import blueprint as reviews_blueprint

blueprint = Blueprint('campgrounds', __name__, template_folder='templates')
blueprint.register_blueprint(reviews_blueprint, url_prefix='/<campground_id>/reviews')


@blueprint.route('/', methods=['GET'])
def campgrounds():
    campgrounds = Campground.objects.all()
    return render_template('campgrounds/index.html', campgrounds=campgrounds)


@blueprint.route('/<campground_id>', methods=['GET'])
def show_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    return render_template('campgrounds/show.html', campground=campground)


@blueprint.route('/new', methods=['GET'])
def new_campground():
    return render_template('campgrounds/new.html')


@blueprint.route('/', methods=['POST'])
def post_campground():
    campground = Campground(**request.form)
    campground.save()
    return redirect(f'/campgrounds/{campground.id}')


@blueprint.route('/<campground_id>/edit', methods=['GET'])
def edit_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    return render_template('campgrounds/edit.html', campground=campground)


@blueprint.route('/<campground_id>', methods=['PUT'])
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


@blueprint.route('/<campground_id>', methods=['DELETE'])
def delete_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    # TODO: figure out how to do this automatically. Can't make it work with register_delete_rule...
    for review in campground.reviews:
        review.delete()
    campground.delete()
    return redirect(f'/campgrounds')
