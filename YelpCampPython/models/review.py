from mongoengine import Document, fields

from models.user import User


class Review(Document):
    author = fields.ReferenceField(User)
    body = fields.StringField(required=True)
    rating = fields.FloatField(required=True, min_value=0.)

