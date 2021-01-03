"""Routes for trips data."""
import os
import csv
from datetime import datetime
from flask import (Blueprint,
                   render_template,
                   redirect,
                   request,
                   flash,
                   session,
                   url_for)

from flask_login import current_user
from application.meta_tags_dict import metaTags

from application.general_forms import UploadFileForm
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from application.trip.forms import (AddTripForm,
                                    DataValidation)

from application.trip.crudTrip import readTrip, insertTrip
from application.trip.crudAirport import readAirportList, readAirport
from application.trip.graph_trips import tripsPlot


titleText = metaTags['trips']['pageTitleDict']
headerText = metaTags['trips']['headerDict']

trip_bp = Blueprint('trip_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

graph = tripsPlot()

@trip_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    airportsList = readAirportList()

    fAddTrip = AddTripForm()

    # Add airports list to dropdown selectors 
    fAddTrip.departure_origin.choices = airportsList
    fAddTrip.departure_destination.choices = airportsList
    fAddTrip.return_origin.choices = airportsList
    fAddTrip.return_destination.choices = airportsList

    redirectHoovering = 'main'
    default = {}

    # Validate and record submitted form
    if fAddTrip.validate_on_submit() and request.method == 'POST':

        success = insertTrip(current_user,
                        fAddTrip.departure_origin.data,
                        fAddTrip.departure_destination.data,
                        fAddTrip.departure_date.data,
                        fAddTrip.return_origin.data,
                        fAddTrip.return_destination.data,
                        fAddTrip.return_date.data,
                        fAddTrip.passenger_companion.data)

        if not success:
            flash('Error saving trip details!')
            return redirect(url_for('trip_bp.main'))
        else:
            flash('Trip details recorded!')

    if len(fAddTrip.errors) > 0:
        flash('Error saving trip details!', fAddTrip.errors)

    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           fAddTrip=fAddTrip,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2],
                           redirectHoovering=redirectHoovering,
                           default=default)


@trip_bp.route("/upload", methods=['GET','POST'])
def upload():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    dValidate = DataValidation()
    fUploadFile = UploadFileForm()
    redirectHoovering = 'upload'

    if request.method == 'POST' and fUploadFile.validate_on_submit():

        fileName = secure_filename(fUploadFile.file.data.filename)
        filePath = os.path.join('application/static/uploads', fileName)
        fUploadFile.file.data.save(filePath)

        with open(filePath, newline='') as csvfile:
            fNames = [
                'origin_departure',
                'destination_departure',
                'date_departure',
                'origin_return',
                'destination_return',
                'date_return',
                'passenger_companion']
            reader = csv.DictReader(csvfile, fieldnames=fNames, delimiter=';')
            rowNumber = 0
            errorRow = ""
            nl = '\n'

            for row in reader:

                originDepartureFromRow = readAirport(airport_iata_identifier=row['origin_departure'])
                destinationDepartureFromRow = readAirport(airport_iata_identifier=row['destination_departure'])
                dateDepartureFromRow = datetime.strptime((row['date_departure']), '%Y/%m/%d')
                originReturnFromRow = readAirport(airport_iata_identifier=row['origin_return'])
                destinationReturnFromRow = readAirport(airport_iata_identifier=row['destination_return'])
                dateReturnFromRow = datetime.strptime((row['date_return']), '%Y/%m/%d')
                passengerCompanionFromRow = str(row['passenger_companion'])

                success = insertTrip(current_user,
                                 originDepartureFromRow.id,
                                 destinationDepartureFromRow.id,
                                 dateDepartureFromRow,
                                 originReturnFromRow.id,
                                 destinationReturnFromRow.id,
                                 dateReturnFromRow,
                                 passengerCompanionFromRow)

                if not success:
                    flash('Something went wrong with the imported data.')
                    return redirect(url_for('trip_bp.upload'))
            
            flash('File uploaded successfully!', 'message')
            return redirect(url_for('trip_bp.upload'))

    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           fUploadFile=fUploadFile,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2],
                           redirectHoovering=redirectHoovering,)
