from flask import Flask,request
import argparse
app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_executable():
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return "Specified content type is not supported", 400 
    request_body = request.get_json()

    if request_body is None:
        return "Body is not specified", 400

    executable_path = request_body["path"]

    return executable_path

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        prog = "SDB Server",
        description = "Runner for Mono Soft Debugger client")

    argument_parser.add_argument("-p", "--port", help="server port accessible at", default=80)
    arguments = argument_parser.parse_args()

    app.run(host="0.0.0.0", port=arguments.port)
