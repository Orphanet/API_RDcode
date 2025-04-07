from swagger_server.API_main import main
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS, cross_origin
import os
import connexion
from swagger_server import encoder

application = connexion.App(__name__)
application.add_api('./swagger_server/swagger/swagger.yaml', arguments={'title': 'API RDcode'}, pythonic_params=True)

application.json_encoder = encoder.JSONEncoder

# Authorize cors from all sites
CORS(application.app, methods=["GET"])

@application.route("/", methods=["GET"])
@cross_origin(methods=["GET"])
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