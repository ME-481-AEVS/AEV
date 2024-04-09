import os

from dotenv import load_dotenv
from flask import Flask


def create_app():
    load_dotenv()
    app = Flask(__name__)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    from .ws import sock
    sock.init_app(app)

    # app.run(host='0.0.0.0', debug=True)

    return app

