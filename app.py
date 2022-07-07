import connexion
from flask_cors import CORS

import sys

sys.path.append('openapi')
from openapi.openapi_server import encoder

def main():
    app = connexion.App(__name__, specification_dir='./resources/')
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('schema.yaml',
                arguments={'title': 'Gardnero'},
                pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
