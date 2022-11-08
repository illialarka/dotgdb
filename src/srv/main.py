from flask import Flask
import argparse
app = Flask(__name__)

@app.route("/")
def index():
    return "Index!"

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/members")
def members():
    return "Members"

@app.route("/members/<string:name>/")
def getMember(name):
  return "somename"

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        prog = "SDB Server",
        description = "Runner for Mono Soft Debugger client")

    argument_parser.add_argument("-p", "--port", help="server port accessible at", default=80)
    arguments = argument_parser.parse_args()

    app.run(host="0.0.0.0", port=arguments.port)
