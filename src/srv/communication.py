import logging
import os
from flask_socketio import SocketIO, emit

logger = logging.getLogger()

# tbd: add csrf token validation


@socketio.on("content", namespace="dotgdb_listener")
def content_handler():
    desired_packetid = int(request.args.get("packetid", 0))
    path = request.args.get("path")
    if path is None or not os.path.isfile(path):
        emit(
            "content_event",
            { "message": "Path does not exist", "ok": False })
        return

    try:
        last_modified_datetime = os.path.getmtime(path)  
        with open(path, "r") as readeable_file:
            source_code = readable_file.read()
            emit(
                "content_event",
                { "content": source_code, "ok": True })

    except Exception as exc:
        emit(
            "content_event",
            { "message": f"Error message: {exc}", "ok": False })
