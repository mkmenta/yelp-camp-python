from mongoengine import Document, fields


class Review(Document):
    body = fields.StringField(required=True)
    rating = fields.FloatField(required=True, min_value=0.)

