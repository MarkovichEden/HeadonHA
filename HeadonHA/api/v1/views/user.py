from flask import jsonify, Response
from flask_restful import Resource, reqparse

from api.v1.utils import HOST, FRONT_PORT
from api.v1.utils.response import create_response_json
from models import authenticate
from models.user import User as UserModel


class User(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('user_id', type=int, required=True)
    post_parser.add_argument('token', type=str, location='cookies')
    post_parser.add_argument('user_data', type=dict, required=True, location='json')

    def post(self):
        args = self.post_parser.parse_args()
        response = authenticate(args['user_id'], args['token'])
        if response:
            return response
        new_data = args['user_data']
        user = UserModel.get_user_by_id(args['user_id'])
        if user:
            user.update(**new_data)
            return Response(create_response_json(True, "user updated", user=user.serialize()), status=200,
                            content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true'
                    })
        return Response(create_response_json(False, "user with user id not found", user_id=args['user_id']), status=404,
                        content_type="application/json", headers={ 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                        'Access-Control-Allow-Origin': f"http://{HOST}:{FRONT_PORT}",
                        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,UPDATE,OPTIONS',
                        'Access-Control-Allow-Credentials': 'true'
                    })
