from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from application.errors import ErrorsHandle

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
    errorHandler = ErrorsHandle(app)

    # Any part of our app which is not imported, or registered
    # within the 'with app.app_context()' block
    # effectively does not exist
    with app.app_context():

        # Register error handlers
        app.register_error_handler(404, errorHandler.page_not_found)
        app.register_error_handler(413, errorHandler.request_entity_too_large)

        # Register Blueprints
        from application.auth.views import auth_bp
        app.register_blueprint(auth_bp,
                               url_prefix='/auth')

        from application.dashboard.views import dashboard_bp
        app.register_blueprint(dashboard_bp,
                               url_prefix='/dashboard')

        from application.trip.views import trip_bp
        app.register_blueprint(trip_bp,
                               url_prefix='/trip')

        # Include our Routes
        from application import views, models
        from application.auth import views
        from application.dashboard import views
        from application.trip import views

        # Create database models
        db.create_all()

        return app
