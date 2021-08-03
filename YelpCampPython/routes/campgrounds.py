import functools

from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user

from models.campground import Campground
from routes.reviews import blueprint as reviews_blueprint

blueprint = Blueprint('campgrounds', __name__, template_folder='templates')
blueprint.register_blueprint(reviews_blueprint, url_prefix='/<campground_id>/reviews')


def author_required(func):
    @functools.wraps(func)
    def wrapper_author_required(campground_id):
        try:
            campground = Campground.objects.get(id=ObjectId(campground_id))
        except:
            flash('Cannot find that campground!', 'error')
            return redirect('/campgrounds')
        if current_user.is_anonymous or current_user.id != campground.author.id:
            flash('You do not have permission to do that.', 'error')
            return redirect(f'/campgrounds/{campground_id}')
        return func(campground_id)
    return wrapper_author_required


@blueprint.route('/', methods=['GET'])
def campgrounds():
    campgrounds = Campground.objects.all()
    return render_template('campgrounds/index.html', campgrounds=campgrounds)


@blueprint.route('/<campground_id>', methods=['GET'])
def show_campground(campground_id):
    try:
        campground = Campground.objects.get(id=ObjectId(campground_id))
    except:
        flash('Cannot find that campground!', 'error')
        return redirect('/campgrounds')
    return render_template('campgrounds/show.html', campground=campground)


@blueprint.route('/new', methods=['GET'])
@login_required
def new_campground():
    return render_template('campgrounds/new.html')


@blueprint.route('/', methods=['POST'])
@login_required
def post_campground():
    campground = Campground(**request.form)
    campground.author = current_user
    campground.save()
    flash('Successfully made a new campground!', 'success')
    return redirect(f'/campgrounds/{campground.id}')


@blueprint.route('/<campground_id>/edit', methods=['GET'])
@author_required
@login_required
def edit_campground(campground_id):
    try:
        campground = Campground.objects.get(id=ObjectId(campground_id))
    except:
        flash('Cannot find that campground!', 'error')
        return redirect('/campgrounds')
    return render_template('campgrounds/edit.html', campground=campground)


@blueprint.route('/<campground_id>', methods=['PUT'])
@author_required
@login_required
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
    flash('Successfully updated campground!', 'success')
    return redirect(f'/campgrounds/{campground.id}')


@blueprint.route('/<campground_id>', methods=['DELETE'])
@author_required
@login_required
def delete_campground(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    # TODO: figure out how to do this automatically. Can't make it work with register_delete_rule...
    for review in campground.reviews:
        review.delete()
    campground.delete()
    flash('Campground deleted successfully!', 'success')
    return redirect(f'/campgrounds')
