from bson import ObjectId
from flask import Blueprint, redirect, request

from models.campground import Campground
from models.review import Review

blueprint = Blueprint('reviews', __name__, template_folder='templates')


@blueprint.route('/', methods=['POST'])
def post_review(campground_id):
    campground = Campground.objects.get(id=ObjectId(campground_id))
    review = Review(**request.form)
    review.save()
    campground.reviews.append(review)
    campground.save()
    return redirect(f'/campgrounds/{campground.id}')


@blueprint.route('/<review_id>', methods=['DELETE'])
def delete_review(campground_id, review_id):
    review = Review.objects.get(id=ObjectId(review_id))
    review.delete()  # the reverse_delete_rule=PULL will automatically remove it from the campground
    return redirect(f'/campgrounds/{campground_id}')
