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
from application.meta_tags_dict import metaTags
from application.models import db, Admin, Trip

from application.general_forms import UploadFileForm
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from application.trip.forms import (AddTripForm,
                                    DataValidation)

from application.trip.crudTrip import read, insert

from application.trip.graph_trips import graphTrips, twoPlotsSameFig


titleText = metaTags['trips']['pageTitleDict']
headerText = metaTags['trips']['headerDict']

trip_bp = Blueprint('trip_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@trip_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fAddTrip = AddTripForm()

    # graph = graphTrips()

    graph = twoPlotsSameFig()

    default = {}


    if fAddTrip.validate_on_submit() and request.method == 'POST':
        sucess = insert(current_user,
                        fAddTrip.departure_origin.data,
                        fAddTrip.departure_destination.data,
                        fAddTrip.departure_date.data,
                        fAddTrip.return_origin.data,
                        fAddTrip.return_destination.data,
                        fAddTrip.return_date.data,
                        fAddTrip.passenger_companion.data)


        if not sucess:
            flash('Error saving trip details!')
            return redirect(url_for('trip_bp.main'))
        else:
            flash('Trip details recorded!')

    
    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           fAddTrip=fAddTrip,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2],
                           default=default)


@trip_bp.route("/upload", methods=['GET','POST'])
def upload():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))
    
    graph = twoPlotsSameFig()

    dValidate = DataValidation()
    fUploadFile = UploadFileForm()
    redirectHoovering = 'upload'
    details = ""

    if request.method == 'POST' and fUploadFile.validate_on_submit():

        print("Uploading trips file................")
    else:
        print("Wrong file................")

    # return redirect(url_for('trip_bp.main'))
    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           fUploadFile=fUploadFile,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2],
                           redirectHoovering=redirectHoovering,)

