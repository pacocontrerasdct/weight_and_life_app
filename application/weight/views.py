"""Routes for trips data."""
from flask import (Blueprint,
                   render_template,
                   redirect,
                   request,
                   flash,
                   session,
                   url_for)

from flask_login import current_user
from application.meta_tags_dict import metaTags


titleText = metaTags['weights']['pageTitleDict']
headerText = metaTags['weights']['headerDict']

weight_bp = Blueprint('weight_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@weight_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    redirectHoovering = 'main'
    default = {}

    return render_template("weight/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           redirectHoovering=redirectHoovering,
                           default=default)
