import os
import logging
import exceptions
from commands.selector import select_command 
from refreshers.selector import select_refresher 
from state_store_service import StateStoreService
from interop.constants import *
from flask import Flask
from flask_compress import Compress 
from flask_socketio import SocketIO, emit

logger = logging.getLogger()

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000 

state_store_service = StateStoreService()

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

agnet = None

def process_server(
    *,
    agent,
    session,
    arguments,
    host=DEFAULT_HOST,
    port=DEFAULT_PORT,
    private_key=None,
    certificate=None): 

    application.config["application"] = agent
    kwargs = {}

    ssl_context = define_ssl_context(private_key, certificate)

    if ssl_context:
        SocketSecurityLayer(application)
        kwargs["ssl_context"] = ssl_context

    socketio.server_options["allow_upgrades"] = False
    socketio.init_app(application)

    try:
        session.run(
            arguments.executable, arguments.port), agent.start(
            True, session.port, 10)

        agent.vm.resume(), agent.vm.suspend()
        state_store_service.state.executable_path = arguments.executable
    except exceptions.ExecutableNotFound:
        logger.error(
            f"Couldn't find an executable to run. Ensure it exists in {arguments.executable}.")
        return

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
                { 
                    "last_modified_datetime": last_modified_datetime,
                    "content": source_code,
                    "ok": True
                })

    except Exception as exc:
        emit(
            "content_event",
            { "message": f"Error message: {exc}", "ok": False })

@socketio.on("command")
def run_command_handler(params):
    logger.debug("[socket/command] Handler started.")
    input_command = params["command"]
    input_command_arguments = params["arguments"]
    if input_command is None or len(input_command) == 0 or input_command is not str: 
        emit(
            "std_output",
            { "message": "Provided invalid command." })

    command = select_command(input_command)

    if command is None:
        emit(
            "std_output",
            { "message": "Unknown command. Try 'help' or 'supportedcommands' to see all supported commands." })
        return

    agent = application.config["application"]; 
    command.execute(agent, [input_command_arguments])
    refreshers = select_refresher(command.scopes) 

    for refresher in refreshers:
        refresher.execute(agent=agent, socket=socketio)