import json


def create_response_json(success: bool, message:str, **data):
    return json.dumps({
        "success": success,
        "message": message,
        "data": {**data}
    })