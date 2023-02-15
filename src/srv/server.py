import os
import socket
import webbrowser
import logging
from flask import Flask, request
from flask_compress import Compress 
from flask_socketio import SocketIO, emit

logger = logging.getLogger()

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000 

application = Flask(__name__)
socketio = SocketIO(manage_session=False, cors_allowed_origins="*")
# apply gzip compression 
Compress(application)


try:
    from security import SocketSecurityLayer, define_ssl_context
except ImportError:
    logger.error("Socket Layer Security is kinda optional and unavailable on environment.")

    # redefine method to imporve perf
    def define_ssl_context(private_key, certificate):
        return None

def run_server(
    *,
    host=DEFAULT_HOST,
    port=DEFAULT_PORT,
    private_key=None,
    certificate=None): 

    kwargs = {}

    ssl_context = define_ssl_context(private_key, certificate)

    if ssl_context:
        SocketSecurityLayer(application)
        kwargs["ssl_context"] = ssl_context

    url = "%s:%s" % (host, port)
    protocol = "http://"
    full_url = protocol + url

    if kwargs.get("ssl_context"):
        protocol = "https://"
        full_url = protocol + url

    socketio.server_options["allow_upgrades"] = False
    socketio.init_app(application)

    if host == DEFAULT_HOST:
        url = (DEFAULT_HOST, port)
    else:
        try:
            url = (socket.gethostbyname(socket.gethostname()), port)
        except Exception:
            url = (host, port)

    logger.info(f"Open dotgdb at {full_url}.")

    try:
        socketio.run(
            application,
            debug=False,
            port=int(port),
            host=host,
            **kwargs)
    except KeyboardInterrupt:
        pass

@socketio.on("content")
def content_handler(params):
    logger.debug("[socket/connect] Handler started.")
    path = params["path"]
    if path is None or os.path.isfile(path) is False:
        emit(
            "content_event",
            { "message": "Path does not exist.", "ok": False })
        return

    try:
        last_modified_datetime = os.path.getmtime(path)  
        with open(path, "r") as readable_file:
            source_code = readable_file.read()
            logger.debug("[socket/connect] Handler returns source code.") 
            emit(
                "content_event",
                { "content": source_code, "ok": True })

    except Exception as exc:
        emit(
            "content_event",
            { "message": f"Error message: {exc}", "ok": False })

@socketio.on("run_command")
def run_command_handler(params):
    logger.debug("[socket/run_command Handler started.")
    executable_path = params["path"]
    if executable_path is None or os.path.isfile(executable_path) is False:
        emit(
            "std_output",
            { "message": f"Provided executable path ({executable_path}) does not exist." })

    emit("std_output", { "message": "Stub message for running command" })


