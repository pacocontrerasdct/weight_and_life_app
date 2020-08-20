"""Routes for dashboard private area."""
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
from . import dashboard_bp

from application import login_manager
from ..meta_tags_dict import metaTags

from flask_login import current_user, logout_user
from .forms import (AddWeightForm,
                    UploadFileForm,
                    DeleteWeightForm,
                    EditWeightForm,
                    DataValidation)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from ..models import db, Admin, Weight, Trip
# from datetime import datetime as dt

from .crudWeight import read, insert, delete, edit, update
from .formatWeight import formatW

titleText = metaTags['dashboard']['pageTitleDict']
headerText = metaTags['dashboard']['headerDict']


@dashboard_bp.route("/main", methods=['GET', 'POST'])
def dashboard():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fAddWeight = AddWeightForm()
    fDeleteWeight = DeleteWeightForm()
    fEditWeight = EditWeightForm()
    weights = read(current_user)

    redirectHoovering = 'main'

    if request.method == 'GET' and request.args.get('id'):
        weightId = request.args.get('id')
        editThis = edit(weightId)
        default = {'id': weightId,
                   'weight': editThis.weight,
                   'date': datetime.date(editThis.weight_date)}
    else:
        default = {}

    if fAddWeight.validate_on_submit() and request.method == 'POST':

        # if form contains and weightId, update that record
        if fAddWeight.weightId.data:

            success = update(
                fAddWeight.weightId.data,
                fAddWeight.weight.data,
                fAddWeight.weightDate.data)

            if not success:
                flash('Couldn\'t update this weight, sorry', 'error')
                return redirect(url_for('.dashboard'))

            flash('Weight updated successfully!', 'message')
            return redirect(url_for('.dashboard'))

        # else insert a new record
        success = insert(
            current_user,
            fAddWeight.weight.data,
            fAddWeight.weightDate.data)

        if not success:
            flash('Couldn\'t save new weight, sorry', 'error')
            return redirect(url_for('.dashboard'))

        flash('Weight recorded successfully!', 'message')
        return redirect(url_for('.dashboard'))

    return render_template("dashboard.html",
                           titleText=titleText,
                           headerText=headerText,
                           fAddWeight=fAddWeight,
                           fDeleteWeight=fDeleteWeight,
                           fEditWeight=fEditWeight,
                           weights=formatW(weights),
                           redirectHoovering=redirectHoovering,
                           default=default,)


@dashboard_bp.route("/upload", methods=['GET', 'POST'])
def upload():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))
    dValidate = DataValidation()
    fUploadFile = UploadFileForm()
    fDeleteWeight = DeleteWeightForm()
    fEditWeight = EditWeightForm()
    weights = read(current_user)
    redirectHoovering = 'upload'
    details = ""

    if request.method == 'POST' and fUploadFile.validate_on_submit():

        fileName = secure_filename(fUploadFile.file.data.filename)
        filePath = os.path.join('application/static/uploads', fileName)
        fUploadFile.file.data.save(filePath)

        with open(filePath, newline='') as csvfile:
            fNames = ['weight', 'date']
            reader = csv.DictReader(csvfile, fieldnames=fNames, delimiter=';')
            rowNumber = 0
            errorRow = ""
            nl = '\n'

            for row in reader:
                rowNumber = rowNumber + 1
                details = f"""Row number {rowNumber}. Reason:"""

                print(row['weight'], row['date'])

                try:
                    weight = float(row['weight'])
                    dateFromRow = datetime.strptime((row['date']), '%Y/%m/%d')
                    today = datetime.now()

                    if float(row['weight']) < 20 or float(row['weight']) > 200:
                        e = "Weight out of range from 20 to 200 Kg."
                        errorRow += f"""{details} {e}{nl}"""

                    if today < dateFromRow:
                        e = "Date can't be in the future."
                        errorRow += f"""{details} {e}{nl}"""

                except Exception as e:
                    errorRow += f"""{details} {e}{nl}"""

                # try:
                #     dateFromRow = datetime.strptime((row['date']), '%Y/%m/%d')
                #     today = datetime.now()
                #     if today < dateFromRow:
                #         e = "Date can't be in the future."
                #         errorRow += f"{details}- 3Found exception: {e}{nl}"

                # except Exception as e:
                #     errorRow = f"{details}- 4Found exception: {e}.\n"

            if errorRow != "":
                errorMsg = f"""File hasn't been proccessed!{nl}""" \
                            f"""Couldn't save new data.{nl}""" \
                            f"""{errorRow}"""

                flash(errorMsg, 'error')
                return redirect(url_for('.upload'))

            # if all imported data is correct, save it to the db
            with open(filePath, newline='') as csvfile:
                fNames = ['weight', 'date']
                reader = csv.DictReader(
                    csvfile, fieldnames=fNames, delimiter=';')

                for row in reader:
                    weightFromRow = float(row['weight'])
                    dateFromRow = datetime.strptime((row['date']), '%Y/%m/%d')
                    success = insert(current_user, weightFromRow, dateFromRow)

                    if not success:
                        details = "{{ weightFromRow }} ; {{ dateFromRow }}"
                        flash('Something went wrong with data {{ details }}',
                              'error')
                        return redirect(url_for('.upload'))

            flash('File uploaded successfully!', 'message')
            return redirect(url_for('.upload'))

    return render_template("dashboard.html",
                           titleText=titleText,
                           headerText=headerText,
                           fUploadFile=fUploadFile,
                           fDeleteWeight=fDeleteWeight,
                           fEditWeight=fEditWeight,
                           weights=formatW(weights),
                           redirectHoovering=redirectHoovering,)


@dashboard_bp.route("/delete", methods=['POST'])
def deleteWeight():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fDeleteWeight = DeleteWeightForm()

    if fDeleteWeight and request.method == 'POST':
        success = delete(fDeleteWeight.weightId.data)

        if not success:
            details = "{{ fDeleteWeight.weightId.data }}"
            flash('Couldn\'t delete weight with id {{ details }}, sorry',
                  'error')
        else:
            flash('Weight deleted successfully!', 'message')

    return redirect(url_for('.dashboard'))


@dashboard_bp.route("/edit", methods=['POST'])
def editWeight():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fEditWeight = EditWeightForm()

    if fEditWeight and request.method == 'POST':

        editThis = edit(fEditWeight.weightId.data)

        return redirect(url_for('.dashboard',
                                id=fEditWeight.weightId.data,))

    return redirect(url_for('.dashboard'))


@dashboard_bp.errorhandler(413)
@dashboard_bp.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    flash('File too large, maximum size admitted is 1MB.', 'error')
    return redirect(url_for('.upload'))
    # return 'Este File Too Large', 413
