from flask import Response

from api.v1.utils.response import create_response_json
from models.user import User
from models.event import Event
from models.sessions import Session
from models.role import Role


def authenticate(user_id, token):
    session = Session.get_session_by_user_id(user_id)
    if not User.is_user_exists(user_id):
        return Response(create_response_json(False, "user id not found", user_id=user_id), status=404,
                        content_type="application/json")
    if not session.is_token_match(user_id, token):
        return Response(create_response_json(False, "user token invalid"), status=401,
                        content_type="application/json")
