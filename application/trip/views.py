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
                   url_for,
                   jsonify)

from flask_login import current_user
from application.meta_tags_dict import metaTags

from application.general_forms import UploadFileForm
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from application.trip.forms import (AddTripForm,
                                    EditTripForm,
                                    UpdateTripForm,
                                    DeleteTripForm,
                                    DataValidation)

from application.trip.crudTrip import (readOneTrip,
                                       readAllTrips,
                                       insertTrip,
                                       insertTrip2,
                                       updateTrip,
                                       deleteTrip)

from application.trip.crudAirport import readAirportList, readAirport
from application.trip.graph_trips import tripsPlot



titleText = metaTags['trips']['pageTitleDict']
headerText = metaTags['trips']['headerDict']

trip_bp = Blueprint('trip_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

from ast import literal_eval

tripsGraph = tripsPlot()
airportsList = readAirportList()


@trip_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    allTripsList = readAllTrips(current_user)

    fAddTrip = AddTripForm()

    fEditTrip = EditTripForm()
    fDeleteTrip = DeleteTripForm()
    graph = ["","",""]
    graphFlag = 0
    redirectHoovering = 'main'


    if request.method == 'GET' and request.args.get('messages') is not None :
        userForm = literal_eval(request.args.get('messages'))
        redirectHoovering = ''

        fAddTrip = AddTripForm(departure_origin=userForm.get('departure_origin'),
                           departure_destination=userForm.get('departure_destination'),
                           departure_date=datetime.strptime(userForm.get('departure_date'), '%Y-%m-%d') if userForm.get('departure_date') != 'None' else '',
                           return_origin=userForm.get('return_origin'),
                           return_destination=userForm.get('return_destination'),
                           return_date=datetime.strptime(userForm.get('return_date'), '%Y-%m-%d') if userForm.get('return_date') != 'None' else '',
                           passenger_companion=userForm.get('passenger_companion'))

    # show weight graphic if requested by user
    if request.method == 'GET' and request.args.get('graph') == "true":
        graph = tripsGraph
        graphFlag = 1

    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           trips=allTripsList,
                           airports=dict(airportsList),
                           fAddTrip=fAddTrip,
                           fEditTrip=fEditTrip,
                           fDeleteTrip=fDeleteTrip,
                           showGraph=graphFlag,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2],
                           redirectHoovering=redirectHoovering)


@trip_bp.route("/edit", methods=['GET', 'POST'])
def edit():
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fAddTrip = AddTripForm()

    fAddTrip.errors = set()

    # edit trip requested by user
    if request.method == 'GET' and len(request.args.get('tripId')) > 0:

        editThisTrip = readOneTrip(current_user, int(request.args.get('tripId')))

        fAddTrip = AddTripForm(tripId=editThisTrip.id,
                               departure_origin=editThisTrip.departure_origin,
                               departure_destination=editThisTrip.departure_destination,
                               departure_date=editThisTrip.departure_date,
                               return_origin=editThisTrip.return_origin,
                               return_destination=editThisTrip.return_destination,
                               return_date=editThisTrip.return_date,
                               passenger_companion=editThisTrip.passenger_companion,
                               errors = set()
                               )
        
        fUpdateTrip = UpdateTripForm(formName='updateIt')

        fDeleteTrip = DeleteTripForm(formName='deleteIt')

        redirectHoovering = ''

        return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           airports=dict(airportsList),
                           editThisTrip=editThisTrip,
                           fAddTrip=fAddTrip,
                           fUpdateTrip=fUpdateTrip,
                           fDeleteTrip=fDeleteTrip,
                           redirectHoovering=redirectHoovering)

    # update trip requested by user
    if fAddTrip.validate_on_submit() and request.method == 'POST':
        
        success = updateTrip(fAddTrip.tripId.data,
                        fAddTrip.departure_origin.data,
                        fAddTrip.departure_destination.data,
                        fAddTrip.departure_date.data,
                        fAddTrip.return_origin.data,
                        fAddTrip.return_destination.data,
                        fAddTrip.return_date.data,
                        fAddTrip.passenger_companion.data)        

        if not success:
            flash(f'''Couldn\'t add trip with id { fAddTrip.tripId.data }, sorry''',
                  'error')
            return redirect(url_for('trip_bp.edit'))

        else:
            flash('Trip added successfully!', 'message')

    else:

        count = 0
        for i in fAddTrip.errors:
            if count == 0:
                flash('Warning: ', 'error')
            if count > 0:
                i = f''', and {i.lower()}'''
            flash(i, 'error')
            count += 1
                

        return redirect(url_for('trip_bp.edit',
                                tripId=fAddTrip.tripId.data))


    return redirect(url_for('trip_bp.main'))


@trip_bp.route("/add", methods=['GET', 'POST'])
def add():
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fAddTrip = AddTripForm()
    fEditTrip = EditTripForm()
    fDeleteTrip = DeleteTripForm()
    allTripsList = readAllTrips(current_user)
    airportsList = readAirportList()

    fAddTrip.errors = set()

    redirectHoovering = 'main'

    successflag = ""

    # Validate trip and save submitted form data
    if fAddTrip.validate_on_submit() and request.method == 'POST':

        print("TYPE TRIP: ", type(fAddTrip))

        success2 = insertTrip2(current_user, fAddTrip)
        
        success = insertTrip(current_user,
                        fAddTrip.departure_origin.data,
                        fAddTrip.departure_destination.data,
                        fAddTrip.departure_date.data,
                        fAddTrip.return_origin.data,
                        fAddTrip.return_destination.data,
                        fAddTrip.return_date.data,
                        fAddTrip.passenger_companion.data)

        if not success:
            flash('Error saving Trip details!', 'error')
        
        flash('Trip details saved!', 'message')
        return redirect(url_for('trip_bp.main'))

    else:
        # if validation has failed
        # use user data to rebuilt the form
        values = {}
        values['departure_origin'] = f'''{fAddTrip.departure_origin.data}''' # if fAddTrip.departure_origin.data is not None else "Empty"
        values['departure_destination'] = f'''{fAddTrip.departure_destination.data}''' # if fAddTrip.departure_destination.data is not None else "Empty"
        values['departure_date'] = f'''{fAddTrip.departure_date.data}''' # if fAddTrip.departure_date.data is not None else "Empty"
        values['return_origin'] = f'''{fAddTrip.return_origin.data}''' # if fAddTrip.return_origin.data is not None else "Empty"
        values['return_destination'] = f'''{fAddTrip.return_destination.data}''' # if fAddTrip.return_destination.data is not None else "Empty"
        values['return_date'] = f'''{fAddTrip.return_date.data}''' # if fAddTrip.return_date.data is not None else "Empty"
        values['passenger_companion'] = f'''{fAddTrip.passenger_companion.data}''' # if fAddTrip.passenger_companion.data is not None else "Empty"

        count = 0
        for i in fAddTrip.errors:
            if count == 0:
                flash('Warning: ', 'error')
            if count > 0:
                i = f''', and {i.lower()}'''
            flash(i, 'error')
            count += 1

        return redirect(url_for('trip_bp.main', messages=values))

    return render_template("trip/main.html",
                                   titleText=titleText,
                                   headerText=headerText,
                                   trips=allTripsList,
                                   airports=dict(airportsList),
                                   fAddTrip=fAddTrip,
                                   fEditTrip=fEditTrip,
                                   fDeleteTrip=fDeleteTrip,
                                   # showGraph=graphFlag,
                                   # cdn_javascript=graph[0],
                                   # bokehScriptComponent=graph[1],
                                   # bokehDivComponent=graph[2],
                                   redirectHoovering=redirectHoovering,
                                   success=successflag)



@trip_bp.route("/update", methods=['POST'])
def update():

    # if not current_user.is_authenticated:
    #     return redirect(url_for('auth_bp.login'))

    # fUpdateTrip = UpdateTripForm()
    # fAddTrip = AddTripForm()


    # # delete trip requested by user
    # if fUpdateTrip.validate_on_submit() and request.method == 'POST':
    #     here = fAddTrip.passenger_companion.data
    #     print(f'''yoyoyo yoyoyo yoyoyo yoyoyo yoyoyo yoyoyo yoyoyo yoyoyo yoyoyo yoyoyo  {here}''')
    #     print(fUpdateTrip.tripFormData.data)
    #     print(type(fUpdateTrip.tripFormData.data))

    #     print(fUpdateTrip.data)
    #     print(fUpdateTrip.data.get('tripFormData'))
    #     print(type(fUpdateTrip.data.get('tripFormData')))
    #     # return f"""Update Trip Data {here}"""
    #     # success = updateTrip(fUpdateTrip)


    #     # success = updateTrip(
    #     #                 fUpdateTrip.tripFormData.departure_origin.data,
    #     #                 fUpdateTrip.departure_destination.data,
    #     #                 fUpdateTrip.departure_date.data,
    #     #                 fUpdateTrip.return_origin.data,
    #     #                 fUpdateTrip.return_destination.data,
    #     #                 fUpdateTrip.return_date.data,
    #     #                 fUpdateTrip.tripFormData.passenger_companion.data)        

    #     # if success:
    #     #     return redirect(url_for('trip_bp.main'))

    # print(" PASO POR AQUI....")

    # return redirect(url_for('trip_bp.main'))
    return "coming from update route"


@trip_bp.route("/delete", methods=['POST'])
def delete():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fDeleteTrip = DeleteTripForm()

    # delete trip requested by user
    if request.method == 'POST' and fDeleteTrip.tripId.data is not None:
        
        success = deleteTrip(fDeleteTrip.tripId.data)

        if not success:
            flash('Couldn\'t delete trip with id {{ fDeleteTrip.tripId.data }}, sorry',
                  'error')
        else:
            flash('Trip deleted successfully!', 'message')

    return redirect(url_for('trip_bp.main'))








@trip_bp.route("/upload", methods=['GET','POST'])
def upload():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    dValidate = DataValidation()
    fUploadFile = UploadFileForm()
    redirectHoovering = 'upload'

    graph = tripsGraph

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
