from typing import Dict

from api import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship("models.role.Role")

    @classmethod
    def get_user_by_id(cls, user_id: int) -> 'User':
        return cls.query.filter_by(id=user_id).one()

    @classmethod
    def is_user_exists(cls, user_id: int) -> bool:
        return cls.query.filter_by(id=user_id).count() > 0

    @classmethod
    def validate_user(cls, username: str, password: str) -> bool:
        return cls.query.filter_by(username=username, password=password).count() == 1

    @classmethod
    def get_user_by_name(cls, username: str) -> 'User':
        return cls.query.filter_by(username=username).first()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role_id': self.role_id,
        }
