from flask import Flask
from app.views import main, ketcher


def create_app():
    """Create the Flask app."""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(main)
    app.register_blueprint(ketcher, url_prefix='/ketcher')

    return app
