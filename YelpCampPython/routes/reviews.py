import functools

from bson import ObjectId
from flask import Blueprint, redirect, request, flash
from flask_login import login_required, current_user

from models.campground import Campground
from models.review import Review

blueprint = Blueprint('reviews', __name__, template_folder='templates')


def author_required(func):
    @functools.wraps(func)
    def wrapper_author_required(campground_id, review_id):
        try:
            review = Review.objects.get(id=ObjectId(review_id))
        except:
            flash('Cannot find that review!', 'error')
            return redirect('/campgrounds')
        if current_user.is_anonymous or current_user.id != review.author.id:
            flash('You do not have permission to do that.', 'error')
            return redirect(f'/campgrounds/{campground_id}')
        return func(campground_id, review_id)
    return wrapper_author_required

@blueprint.route('/', methods=['POST'])
@login_required
def post_review(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    review = Review(**request.form)
    review.author = current_user
    review.save()
    campground.reviews.append(review)
    campground.save()
    flash('Created new review!', 'success')
    return redirect(f'/campgrounds/{campground.id}')


@blueprint.route('/<review_id>', methods=['DELETE'])
@author_required
@login_required
def delete_review(campground_id, review_id):
    review = Review.objects.get(id=ObjectId(review_id))
    review.delete()  # the reverse_delete_rule=PULL will automatically remove it from the campground
    flash('Review deleted successfully!', 'success')
    return redirect(f'/campgrounds/{campground_id}')
