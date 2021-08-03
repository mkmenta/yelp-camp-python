from mongoengine import Document, fields, PULL

from models.review import Review
from models.user import User


class Campground(Document):
    title = fields.StringField(required=True)
    author = fields.ReferenceField(User)
    image = fields.StringField(required=True)
    price = fields.FloatField(required=True, min_value=0.)
    description = fields.StringField(required=True)
    location = fields.StringField(required=True)
    reviews = fields.ListField(fields.ReferenceField(Review, reverse_delete_rule=PULL))  # Auto-remove if Review removed