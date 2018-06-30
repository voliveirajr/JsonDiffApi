from mongoengine import *
from datetime import datetime

class User(Document):
    created = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': 3600},
            {'fields': ['diff_id'], 'unique': True}
        ]
    }

    diff_id = StringField(required=True)
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class DiffReq(Document):
    created = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': 3600},
            {'fields': ['diff_id'], 'unique': True}
        ]
    }

    diff_id = StringField(required=True)
    created = DateTimeField(default=datetime.utcnow)
    left = StringField(required=False)
    right = StringField(required=False)
