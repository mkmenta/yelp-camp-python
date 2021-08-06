from mongoengine import Document, fields, PULL, EmbeddedDocument

from models.review import Review
from models.user import User


class CampgroundImage(EmbeddedDocument):
    public_id = fields.StringField(required=True)
    url = fields.StringField(required=True)

    @property
    def thumbnail(self):
        return self.url.replace('upload', 'upload/w_200')


class Campground(Document):
    title = fields.StringField(required=True)
    author = fields.ReferenceField(User)
    images = fields.EmbeddedDocumentListField(CampgroundImage)
    price = fields.FloatField(required=True, min_value=0.)
    description = fields.StringField(required=True)
    location = fields.StringField(required=True)
    reviews = fields.ListField(fields.ReferenceField(Review, reverse_delete_rule=PULL))  # Auto-remove if Review removed
