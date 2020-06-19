#!/usr/bin/env python3
import os

import connexion
from flask import send_from_directory

from swagger_server import encoder


def main():
    options = {'swagger_url': '/', "swagger_ui_config": {"defaultModelsExpandDepth": -1}}
    app = connexion.App(__name__, specification_dir='swagger/', options=options)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'API RDcode'}, pythonic_params=True)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # Force the direct encoding of accents in json
    # app.app.config['JSON_AS_ASCII'] = False
    # app.app.config['JSON_SORT_KEYS'] = False
    return app


if __name__ == '__main__':
    app = main()
    app.run(port=8080)
