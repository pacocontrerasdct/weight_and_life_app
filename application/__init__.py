from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create an specific postgresql object to use on our app
# Globally accessible libraries/ plugins
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    """Construct the core application"""
    app = Flask(__name__, instance_relative_config=False)

    # Configure Flask using config.py
    app.config.from_object('config.Config')

    # Initialise Plugins
    db.init_app(app)
    login_manager.init_app(app)

    # Any part of our app which is not imported, or registered
    # within the 'with app.app_context()' block
    # effectively does not exist
    with app.app_context():

        # Register Blueprints
        from .auth import auth_bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from .dashboard import dashboard_bp as dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

        # Include our Routes
        from . import api, models
        from .auth import auth
        from .dashboard import dashboard

        # Create database models
        db.create_all()

        return app
