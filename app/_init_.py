from flask import Flask
from .config import configure_app

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app)

    with app.app_context():
        from . import routes
        return app

