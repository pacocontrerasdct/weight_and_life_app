from flask import Blueprint
from flask import current_app as app

dashboard_bp = Blueprint('dashboard_bp', __name__,
                          template_folder='templates',
                          static_folder='static')

from . import dashboard