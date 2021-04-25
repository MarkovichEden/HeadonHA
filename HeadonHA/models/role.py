from api import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String, unique=True)
    viewer = db.Column(db.Boolean)
    editor = db.Column(db.Boolean)

    def is_viewer(self):
        return self.viewer

    def is_editor(self):
        return self.editor

    def serialize(self):
        return {
            'id': self.id,
            'name': self.role_name,
            'viewer': self.viewer,
            'editor': self.editor,
        }
