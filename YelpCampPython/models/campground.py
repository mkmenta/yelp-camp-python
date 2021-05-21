from mongoengine import Document, fields, CASCADE, PULL

from models.review import Review


class Campground(Document):
    title = fields.StringField(required=True)
    image = fields.StringField(required=True)
    price = fields.FloatField(required=True, min_value=0.)
    description = fields.StringField(required=True)
    location = fields.StringField(required=True)
    reviews = fields.ListField(fields.ReferenceField(Review, reverse_delete_rule=PULL))  # Auto-remove if Review removed