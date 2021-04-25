from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['APPLICATION_ROOT'] = "/api/v1"
api = Api(app, prefix=app.config['APPLICATION_ROOT'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


from api.v1.views.login import Login
from api.v1.views.user import User
from api.v1.views.events import EventById, EventAll, EventNewId, EventCreate, EventDelete, EventUpdate

api.add_resource(Login, "/login")
api.add_resource(User, "/user/update")
api.add_resource(EventById, "/event/<event_id>")
api.add_resource(EventAll, "/event/all")
api.add_resource(EventNewId, "/event/newid")
api.add_resource(EventCreate, "/event/create")
api.add_resource(EventDelete, "/event/delete")
api.add_resource(EventUpdate, "/event/update")
