"""Routes for trips data."""
from flask import (Blueprint,
                   render_template,
                   redirect,
                   request,
                   flash,
                   session,
                   url_for)

from flask_login import current_user, logout_user
from application import login_manager


trip_bp = Blueprint('trip_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@trip_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))
    
    return render_template("trip/main.html")
