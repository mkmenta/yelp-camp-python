import functools

import cloudinary
import cloudinary.uploader
import cloudinary.api
from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user

from models.campground import Campground, CampgroundImage
from routes.reviews import blueprint as reviews_blueprint
from utils import allowed_file

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
    images = request.files.getlist('image')
    for image in images:
        if not allowed_file(image.filename):
            flash('Invalid file.', 'error')
            return redirect('/campgrounds/new')
    upload_images = []
    for image in images:
        res = cloudinary.uploader.upload(image,
                                         folder="yelpCamp",
                                         allowed_formats=['jpeg', 'jpg', 'png'])
        upload_images.append(CampgroundImage(url=res['url'], public_id=res['public_id']))
    campground = Campground(**request.form)
    campground.images.extend(upload_images)
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
    # Get campground
    campground = Campground.objects.get(id=ObjectId(campground_id))

    # Check image filenames
    images = request.files.getlist('image')
    images = [image for image in images if image.filename != '']
    for image in images:
        if not allowed_file(image.filename):
            flash('Invalid file.', 'error')
            return redirect(f'/campgrounds/{campground.id}/edit')

    # Update fields
    for k, v in request.form.items():
        if not hasattr(campground, k):
            continue
        if isinstance(getattr(campground, k), str):
            setattr(campground, k, v)
        elif isinstance(getattr(campground, k), float):
            setattr(campground, k, float(v))
        else:
            raise NotImplementedError

    # Delete images
    delete_images = [dim for dim in request.form.getlist('deleteImages') if dim != '']
    campground.images = [image for image in campground.images if image.public_id not in delete_images]
    for dimage in delete_images:
        cloudinary.uploader.destroy(dimage)

    # Add images
    for image in images:
        res = cloudinary.uploader.upload(image,
                                         folder="yelpCamp",
                                         allowed_formats=['jpeg', 'jpg', 'png'])
        campground.images.append(CampgroundImage(url=res['url'], public_id=res['public_id']))
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
