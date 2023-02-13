import logging
from flask import Flask, abort, request, Blueprint, jsonify
from flask_compress import Compress
from flask_socketio import SocketIO, emit
from http_utils import csrf_protect, format_client_error

blueprint = Blueprint("http_routes", __name__)

logger = logging.getLogger()


@blueprint.route("/file_content", methods=["GET"])
@csrf_protect
def read_file_content():
    file_path = request.args.get("path")

    if file_path and os.path.isfile(file_path):
        try:
            last_modified_datetime = os.path.getmtime(file_path)
            with open(file_path, "r") as readable_file:
                source_code = readable_file.read()
                return jsonify({"source_code": source_code})
        except Exception as exc:
            return format_client_error({"error": "%s" % exc})
