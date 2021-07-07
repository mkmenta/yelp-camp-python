import bcrypt
from flask_login import UserMixin
from mongoengine import Document, fields


class User(Document, UserMixin):
    username = fields.StringField(required=True, unique=True)
    email = fields.StringField(required=True, unique=True)
    hash = fields.StringField(required=True)

    @staticmethod
    def register(username: str, email: str, password: str):
        salt = bcrypt.gensalt()  # rounds=12 by default
        hashpw = bcrypt.hashpw(password.encode('utf-8'), salt)
        user = User(username=username, email=email, hash=hashpw)
        user.save()
        return user

    def authenticate(self, password: str):
        if bcrypt.checkpw(password.encode('utf-8'), self.hash.encode('utf-8')):
            return True
        else:
            return False
