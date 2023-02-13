from functools import wraps
from flask import jsonify

HTTP_CSRF_TOKEN = "HTTP_X_CSRFTOKEN"
FORBIDDEN_HTTP_CODE = 403

def csrf_protect(wrapped):

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        csrf_token = session.get("csrf_token", None)
        if csrf_token is None or csrf_token != request.environ.get(HTTP_CSRF_TOKEN):
            logger.warning("Received invalid CSRF token. Aborting...")
            abort(FORBIDDEN_HTTP_CODE)

        return wrapped(*args, **kwargs)

    return wrapper


def format_client_error(resp):
    return jsonify(resp), 400
