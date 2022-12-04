from flask import Flask, request
from flask_cors import cross_origin
from flask_socketio import SocketIO
import argparse
import debug_agent
import debug_session

app = Flask(__name__)
# TODO: make cors allowed origins configurable
socketio = SocketIO(
    app,
    logger=True,
    cors_allowed_origins="http://localhost:3000")

session = debug_session.DbgSession()
agent = debug_agent.DbgAgent()


@socketio.on('connect')
def connected():
    print('on connect event')


@app.route("/run", methods=['POST'])
@cross_origin()
def run():
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Specified content type is not supported", 400
    request_body = request.get_json()

    if request_body is None:
        return "Body is not specified", 400

    executable_path = request_body["path"]

    #arguments = argparse.Namespace(executable=executable_path, port=None)
    # session.run(arguments)
    #agent.start(True, session.port, 10)
    # agent.vm.resume()
    # it means we are running and resuming
    return "Iam runni'"  # agent.vm.get_root_appdomain().__str__();


@app.route("/stop", methods=['POST'])
@cross_origin()
def stop():
    pass


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        prog="SDB Server",
        description="Runner for Mono Soft Debugger client")

    argument_parser.add_argument(
        "-p",
        "--port",
        help="server port accessible at",
        default=80)
    arguments = argument_parser.parse_args()

    socketio.run(app)
