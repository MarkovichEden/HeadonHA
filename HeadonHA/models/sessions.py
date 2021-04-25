from datetime import datetime, timedelta

import uuid

from api import db


THREE_WEEKS_IN_DAYS = 21


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    valid_time = db.Column(db.DateTime,
                           default=datetime.utcnow() + timedelta(days=THREE_WEEKS_IN_DAYS))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('models.user.User')
    token = db.Column(db.String, default=uuid.uuid4().hex)

    @classmethod
    def get_session_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def refresh_token(self):
        self.token = uuid.uuid4().hex
        self.valid_time = datetime.utcnow() + timedelta(days=THREE_WEEKS_IN_DAYS)

    def is_token_expired(self):
        return ((self.valid_time - datetime.utcnow()).days + THREE_WEEKS_IN_DAYS) <= 0

    def is_token_match(self, user_id: int, token: str) -> bool:
        return self.id == user_id and self.token == token

    def serialize(self):
        return {
            'id': self.id,
            'valid_time': self.valid_time,
            'token': self.token,
            'user_name': self.user.username
        }
