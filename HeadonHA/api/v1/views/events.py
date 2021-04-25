from flask import Response
from flask_restful import Resource, reqparse

from api import db
from api.v1.utils.response import create_response_json
from models import Event, authenticate
from api.v1.utils import HOST, FRONT_PORT


class EventById(Resource):
    def get(self, event_id):
        if not Event.is_event_exists(event_id):
            return Response(create_response_json(False, "event not found", event_id=event_id), status=404,
                            content_type='application/json')
        return Response(create_response_json(True, "event found", event=Event.get_event_by_id(event_id).serialize()),
                        status=200, content_type='application/json', headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })


class EventAll(Resource):
    def get(self):
        return Response(create_response_json(True, "all events",
                                             events=list([event.serialize() for event in Event.query.all()])),
                        status=200, content_type='application/json', headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })


class EventNewId(Resource):
    def get(self):
        return Response(create_response_json(True, "new event id", new_id=Event.get_new_id()), status=200,
                        content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })


class EventCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("subject", type=str, required=True)
    parser.add_argument("content", type=str, required=True)
    parser.add_argument("user_id", type=int, required=True)
    parser.add_argument("html", type=str, required=True)
    parser.add_argument("token", type=str, required=True, location='cookies')

    def post(self):
        args = self.parser.parse_args()
        subject = args['subject']
        user_id = args['user_id']
        content = args['content']
        html = args['html']
        auth = args['token']
        response = authenticate(user_id, auth)
        if response:
            return response
        new_event = Event(subject=subject, user_id=user_id, content=content, free_html=html)
        db.session.add(new_event)
        db.session.commit()
        return Response(create_response_json(True, "event created"), status=200,
                        content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })


class EventUpdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("event_id", type=int, required=True)
    parser.add_argument("user_id", type=int, required=True)
    parser.add_argument("token", type=str, location="cookies")
    parser.add_argument("event_data", type=dict, required=True, location='json')

    def post(self):
        args = self.parser.parse_args()
        event_id = args['event_id']
        user_id = args['user_id']
        data = args['event_data']
        auth = args['token']
        response = authenticate(user_id, auth)
        if response:
            return response

        event = Event.query.filter_by(id=event_id).first()
        if event:
            event.update(user_id=user_id, **data)
            return Response(create_response_json(True, "event updated", event=event.serialize()), status=200,
                            content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })
        return Response(create_response_json(False, "event not found", event_id=event_id), status=404,
                        content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })

class EventDelete(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("event_id", type=int, required=True)
    parser.add_argument("user_id", type=int, required=True)
    parser.add_argument("token", type=str, location="cookies")

    def post(self):
        args = self.parser.parse_args()
        event_id = args['event_id']
        user_id = args['user_id']
        auth = args['token']
        response = authenticate(user_id, auth)
        if response:
            return response

        event = Event.query.filter_by(id=event_id).first()
        if event:
            db.session.delete(event)
            db.session.commit()
            return Response(create_response_json(True, "event deleted", event_id=event_id), status=200,
                            content_type="application/json")
        return Response(create_response_json(False, "event id not found", event_id=event_id), status=404,
                        content_type="application/json")
