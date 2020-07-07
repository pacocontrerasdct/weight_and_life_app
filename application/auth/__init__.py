from flask import Blueprint
from flask import current_app as app

# Blueprint configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

from . import auth