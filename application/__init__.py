from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create an specific postgresql object to use on our app
db=SQLAlchemy()

def create_app():
  """Construct the core application"""
  app = Flask(__name__, instance_relative_config=False)

  # Configure Flask using config.py
  app.config.from_object(config.Config)




  db.init_app(app)

  with app.app_context():
    from . import routes
    db.create_all() # Create database tables for our data models
    return app



