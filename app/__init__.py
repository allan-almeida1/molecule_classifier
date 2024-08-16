from flask import Flask, render_template
from app.views import main, ketcher, api


def create_app():
    """Create the Flask app."""

    app = Flask(__name__)
    app.register_blueprint(main)
    app.register_blueprint(ketcher, url_prefix='/ketcher')
    app.register_blueprint(api, url_prefix='/api/v1')

    # Error handling
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
