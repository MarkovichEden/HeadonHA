from flask import request, jsonify, Response
from flask_restful import Resource

from api import db
from api.v1.utils.response import create_response_json
from models.sessions import Session
from models.user import User
from api.v1.utils import HOST, FRONT_PORT


class Login(Resource):
    def get(self):
        args = request.args
        username, password = args['username'], args['password']

        if User.validate_user(username, password):
            session = None
            user = User.get_user_by_name(username)
            if user:
                if Session.query.filter_by(user_id=user.id).count() == 0:
                    new_session = Session()
                    new_session.user_id = user.id
                    db.session.add(new_session)
                    db.session.commit()
                    session = new_session
                else:
                    session = Session.get_session_by_user_id(user.id)
                    if session:
                        if session.is_token_expired():
                            session.refresh_token()
                            db.session.commit()
                            session = Session.get_session_by_user_id(user.id)
                response = Response(create_response_json(True, "user logged in", username=username, password=password), status=200,
                                    content_type="application/json", headers={'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })
                response.set_cookie(key='token', value=session.token, expires=session.valid_time)
                return response
            return Response(create_response_json(False, "user with username not found", username=username), status=404,
                            content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })
        else:
            return Response(create_response_json(False, "log in invalid"), status=401,
                            content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true',

                    })
