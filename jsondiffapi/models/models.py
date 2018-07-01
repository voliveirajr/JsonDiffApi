from mongoengine import *
from datetime import datetime

class DiffReq(Document):
    created = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            #Create a TTL of 1 hour and make diff_id unique
            {'fields': ['created'], 'expireAfterSeconds': 3600},
            {'fields': ['diff_id'], 'unique': True}
        ]
    }

    diff_id = StringField(required=True)
    created = DateTimeField(default=datetime.utcnow)
    left = StringField(required=False)
    right = StringField(required=False)
