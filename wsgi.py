from swagger_server.API_main import main
from flask import Flask, send_from_directory, send_file
import os

application = Flask(__name__, root_path="./")

@application.route("/")
def API():
    return send_from_directory(os.path.join(application.root_path), "static/index.html")

@application.route("/media/<path:path>")
def media(path):
    return send_file(os.path.join(application.root_path, "static/media") + "/" + path)

@application.route("/swagger.yaml")
def swagger():
    return send_file(os.path.join(application.root_path, "swagger_server/swagger/swagger.yaml"))

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8080)
