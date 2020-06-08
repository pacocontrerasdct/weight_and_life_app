from flask import Blueprint
from flask import current_app as app
from flask_login import LoginManager

login_manager=LoginManager()
login_manager.init_app(app)

# Blueprint configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

from . import auth