from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
  """Set Flask configuration variables from .env file."""
  
  # General Flask config
  SECRET_KEY = environ.get('SECRET_KEY')
  FLASK_ENV = environ.get('FLASK_ENV')
  FLASK_APP = 'wsgi.py'
  FLASK_DEBUG = 1

  # Static Assets
  STATIC_FOLDER = 'static'
  TEMPLATES_FOLDER = 'templates'
  COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

  # Database
  SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False