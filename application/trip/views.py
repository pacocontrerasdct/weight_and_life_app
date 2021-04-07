"""Routes for trips data."""
import os
import re
from csv import DictReader
from ast import literal_eval
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
from application.models import db, Trip
from application.general_forms import UploadFileForm
from werkzeug.utils import secure_filename

from application.trip.forms import (AddTripForm,
                                    EditTripForm,
                                    DeleteTripForm)

from application.trip.crudTrip import (readOneTrip,
                                       readAllTrips,
                                       insertTrip,
                                       updateTrip,
                                       deleteTrip)

from application.trip.crudAirport import readAirportList, readAirport
from application.trip.graph_trips import tripsPlot

titleText = metaTags['trips']['pageTitleDict']
headerText = metaTags['trips']['headerDict']

trip_bp = Blueprint('trip_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

airportsList = readAirportList()


@trip_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    allTripsList = readAllTrips(current_user)

    fAddTrip = AddTripForm()
    fEditTrip = EditTripForm()
    fDeleteTrip = DeleteTripForm()
    tripsGraph = tripsPlot()

    showGraph = False
    redirectHoovering = 'main'

    # if user tried to add a new trip
    # but the validation failed
    # user's data will come on as part of the url
    if request.method == 'GET' and request.args.get('userForm') is not None :
        
        # use literal_eval to execute user's data string as dict
        # so I can read it easily
        userForm = literal_eval(request.args.get('userForm'))
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
        showGraph = True

    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           trips=allTripsList,
                           airports=dict(airportsList),
                           fAddTrip=fAddTrip,
                           fEditTrip=fEditTrip,
                           fDeleteTrip=fDeleteTrip,
                           showGraph=showGraph,
                           cdn_javascript=tripsGraph[0],
                           bokehScriptComponent=tripsGraph[1],
                           bokehDivComponent=tripsGraph[2],
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
                               errors = set())

        fDeleteTrip = DeleteTripForm(formName='deleteIt')

        redirectHoovering = ''

        return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           editThisTrip=editThisTrip,
                           fAddTrip=fAddTrip,
                           fDeleteTrip=fDeleteTrip,
                           redirectHoovering=redirectHoovering)

    # update trip requested by user
    if fAddTrip.validate_on_submit() and request.method == 'POST':
        
        success = updateTrip(fAddTrip)        

        if not success:
            flash(f'''Couldn\'t add trip with id { fAddTrip.tripId.data }, sorry''',
                  'error')
            return redirect(url_for('trip_bp.edit'))

    # if there are failures in the form validation
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

    flash('Trip added successfully!', 'message')
    
    return redirect(url_for('trip_bp.main'))


@trip_bp.route("/add", methods=['GET', 'POST'])
def add():
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fAddTrip = AddTripForm()
    fEditTrip = EditTripForm()
    fDeleteTrip = DeleteTripForm()
    allTripsList = readAllTrips(current_user)

    fAddTrip.errors = set()

    redirectHoovering = 'main'

    successflag = ""

    # Validate trip and save submitted form data
    if fAddTrip.validate_on_submit() and request.method == 'POST':

        success = insertTrip(fAddTrip)

        if not success:
            flash('Error saving Trip details!', 'error')
        
        flash('Trip details saved!', 'message')
        return redirect(url_for('trip_bp.main'))

    else:
        # if validation has failed
        # use user data to rebuilt the form
        values = {}
        values['departure_origin'] = f'''{fAddTrip.departure_origin.data}'''
        values['departure_destination'] = f'''{fAddTrip.departure_destination.data}'''
        values['departure_date'] = f'''{fAddTrip.departure_date.data}'''
        values['return_origin'] = f'''{fAddTrip.return_origin.data}'''
        values['return_destination'] = f'''{fAddTrip.return_destination.data}'''
        values['return_date'] = f'''{fAddTrip.return_date.data}'''
        values['passenger_companion'] = f'''{fAddTrip.passenger_companion.data}'''

        count = 0
        for i in fAddTrip.errors:
            if count == 0:
                flash('Warning: ', 'error')
            if count > 0:
                i = f''', and {i.lower()}'''
            flash(i, 'error')
            count += 1

        return redirect(url_for('trip_bp.main', userForm=values))

    return render_template("trip/main.html",
                                   titleText=titleText,
                                   headerText=headerText,
                                   trips=allTripsList,
                                   airports=dict(airportsList),
                                   fAddTrip=fAddTrip,
                                   fEditTrip=fEditTrip,
                                   fDeleteTrip=fDeleteTrip,
                                   redirectHoovering=redirectHoovering,
                                   success=successflag)


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

    fUploadFile = UploadFileForm()
    fEditTrip = EditTripForm()
    redirectHoovering = 'upload'
    tripsGraph = tripsPlot()

    if request.method == 'POST' and fUploadFile.validate_on_submit():

        fileName = secure_filename(fUploadFile.file.data.filename)
        filePath = os.path.join('application/static/uploads', fileName)
        fUploadFile.file.data.save(filePath)

        fNames = [
            'origin_departure',
            'destination_departure',
            'date_departure',
            'origin_return',
            'destination_return',
            'date_return',
            'passenger_companion']

        with open(filePath, newline='') as csvfile:

            reader = DictReader(csvfile, fieldnames=fNames, delimiter=';')
            rowNum = 0
            errors = []
            _ = 'Error at row'

            datePattern = re.compile('([0-9]{4})[/.-]([0-9]{2})[/.-]([0-9]{2})$')
            companionPattern = re.compile("[\"\\*\\?\\!\'\\^\\+\\-\\%\\&\\/\\(\\)\\=\\}\\]\\|\\[\\{\\£\\$\\#\\]]")

            def isStr(val):
                return type(val) == str

            def isLen(val, num):
                return len(val) == num

            for row in reader:
                rowNum += 1
                od_, dd_, dap_, or_, dr_, dar_, pc_ = row.values()
                departure_origin = od_ if isStr(od_) and isLen(od_, 3) else errors.append(f'''{_} {rowNum}: origin_departure''')
                destination_departure = dd_ if isStr(dd_) and isLen(dd_, 3) else errors.append(f'''{_} {rowNum}: destination_departure''')
                date_departure = dap_ if isStr(dap_) and isLen(dap_, 10) and datePattern.match(dap_) else errors.append(f'''{_} {rowNum}: date_departure''')
                origin_return = or_ if isStr(or_) and isLen(or_, 3) else errors.append(f'''{_} {rowNum}: origin_return''')
                destination_return = dr_ if isStr(dr_) and isLen(dr_, 3) else errors.append(f'''{_} {rowNum}: destination_return''')
                date_return = dar_ if isStr(dar_) and isLen(dar_, 10) and datePattern.match(dar_) else errors.append(f'''{_} {rowNum}: date_return''')
                passenger_companion = pc_ if isStr(pc_) and companionPattern.search(pc_) == None else errors.append(f'''{_} {rowNum}: passenger_companion''')

            if errors:
                errorsData = "; ".join(errors)
                flash(f'''Something went wrong with the imported data.
                      There are some errors, please fix them
                      and try it again! {errorsData}''', 'error')
                return redirect(url_for('trip_bp.upload'))

        with open(filePath, newline='') as csvfile:

            reader_ = DictReader(csvfile, fieldnames=fNames, delimiter=';')
            tripList = []

            for row in reader_:
                departure_origin_ = readAirport(airport_iata_identifier=row['origin_departure'])
                departure_destination_ = readAirport(airport_iata_identifier=row['destination_departure'])
                return_origin_ = readAirport(airport_iata_identifier=row['origin_return'])
                return_destination_ = readAirport(airport_iata_identifier=row['destination_return'])

                tripList.append(
                                Trip(admin_id=current_user.id,
                                     departure_origin = departure_origin_.id,
                                     departure_destination = departure_destination_.id,
                                     departure_date = datetime.strptime((row['date_departure']), '%Y/%m/%d'),
                                     return_origin = return_origin_.id,
                                     return_destination = return_destination_.id,
                                     return_date = datetime.strptime((row['date_return']), '%Y/%m/%d'),
                                     passenger_companion = str(row['passenger_companion'])))

            if len(tripList) > 0:
                db.session.bulk_save_objects(tripList)
                db.session.commit()
                flash('File uploaded successfully!', 'message')

    return render_template("trip/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           fUploadFile=fUploadFile,
                           fEditTrip=fEditTrip,
                           cdn_javascript=tripsGraph[0],
                           bokehScriptComponent=tripsGraph[1],
                           bokehDivComponent=tripsGraph[2],
                           redirectHoovering=redirectHoovering)
