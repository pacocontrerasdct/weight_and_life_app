from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create an specific postgresql object to use on our app
# Globally accessible libraries/ plugins
db=SQLAlchemy()


def create_app():
  """Construct the core application"""
  app = Flask(__name__, instance_relative_config=False)

  # Configure Flask using config.py
  app.config.from_object('config.Config')

  # Initialise Plugins
  db.init_app(app)

  # Any part of our app which is not imported, or registered
  # within the 'with app.app_context()' block
  # effectively does not exist
  with app.app_context():
    # Include our Routes
    from . import routes
    
    # Register Blueprints
    # app.register_blueprint(auth.auth_bp)
    # app.register_blueprint(admin.admin_bp)

    db.create_all() # Create database tables for our data models
    return app



