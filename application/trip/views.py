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

from application.trip.forms import (AddTripForm,
                                    DataValidation)

from application.trip.crudTrip import read, insert

from application.trip.graph_trips import graphTrips, twoPlotsSameFig


titleText = metaTags['trips']['pageTitleDict']
headerText = metaTags['trips']['headerDict']

trip_bp = Blueprint('trip_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

def makeMockData(current_user, number_):

    count = 0
    while count <= number_:
        count += 1
        insert(current_user,
               f"2019-0{count}-22",
               f"2019-0{count}-26",
               "London",
               "Murcia",
               1)


@trip_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fAddTrip = AddTripForm()

    # graph = graphTrips()

    graph = twoPlotsSameFig()

    default = {}

    # makeMockData(current_user, 1)


    # if fAddTrip.validate_on_submit() and request.method == 'POST':
    #     sucess = insert(
    #                     current_user,
    #                     fAddTrip.startingDate.data,
    #                     fAddTrip.endingDate.data,
    #                     fAddTrip.fromAirport.data,
    #                     fAddTrip.toAirport.data)
    #     if not sucess:
    #         flash('Error saving trip details!')
    #         return redirect(url_for('trip_bp.main'))

    
    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           fAddTrip=fAddTrip,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2],
                           default=default)
