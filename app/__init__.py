from flask import Flask
from app.routes import app_routes  # Import the Blueprint

def create_app():
    app = Flask(__name__)

    # Register the blueprint
    app.register_blueprint(app_routes)

    return app
