import os
import socket
import webbrowser
import logging
from flask import Flask
from flask_compress import Compress 
from flask_socketio import SocketIO

logger = logging.getLogger()

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000 

application = Flask(__name__)
socketio = SocketIO(manage_session=False)
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

