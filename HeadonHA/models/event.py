from datetime import datetime

from api import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    resolve_time = db.Column(db.DateTime, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("models.user.User", backref='events')
    content = db.Column(db.String)
    free_html = db.Column(db.String)

    @classmethod
    def is_event_exists(cls, event_id: int) -> bool:
        return cls.query.filter_by(id=event_id).count() != 0

    @classmethod
    def get_event_by_id(cls, event_id: int) -> 'Event':
        return cls.query.filter_by(id=event_id).one()

    @classmethod
    def get_new_id(cls):
        return cls.query.order_by(cls.id.desc()).first().id + 1

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'create_time': str(self.create_time),
            'resolve_time': str(self.resolve_time),
            'user': {
                'user_id': self.user.id,
                'user_name': self.user.username,
                'user_role': self.user.role.role_name,
            }
        }