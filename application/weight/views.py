"""Routes for weights data."""
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
from application.weight.forms import (AddWeightForm,
                                      DeleteWeightForm,
                                      EditWeightForm,
                                      DataValidation)

from application.general_forms import UploadFileForm
from werkzeug.utils import secure_filename

from application.weight.crudWeight import (read,
                                           insert,
                                           delete,
                                           edit,
                                           update)
from application.weight.formatWeight import formatW
from application.weight.graph_weight import graphWeights
from application.meta_tags_dict import metaTags

weight_bp = Blueprint('weight_bp', __name__,
                      template_folder='templates',
                      static_folder='static')

titleText = metaTags['weights']['pageTitleDict']
headerText = metaTags['weights']['headerDict']


@weight_bp.route("/main", methods=['GET', 'POST'])
def main():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))
    
    fAddWeight = AddWeightForm()
    fDeleteWeight = DeleteWeightForm()
    fEditWeight = EditWeightForm()
    weights = read(current_user)
    
    fUploadFile = None
    graph = ["","",""]
    graphFlag = 0

    redirectHoovering = 'main'
    default = {}

    # show weight graphic if requested by user
    if request.method == 'GET' and request.args.get('graph') == "true":
        graph = graphWeights()
        graphFlag = 1

    # show upload form if requested by user
    if request.method == 'GET' and request.args.get('uploadForm') == "show":
        fUploadFile = UploadFileForm()

    # edit a weight record if requested by user
    if request.method == 'GET' and request.args.get('id'):
        weightId = request.args.get('id')
        editThis = edit(weightId)
        default = {'id': weightId,
                   'weight': editThis.weight,
                   'date': datetime.date(editThis.weight_date)}

    # update or insert a record
    if fAddWeight.validate_on_submit() and request.method == 'POST':
        
        # if posted form contains a weightId, it is an update
        if fAddWeight.weightId.data:

            success = update(
                fAddWeight.weightId.data,
                fAddWeight.weight.data,
                fAddWeight.weightDate.data)

            if not success:
                flash('Couldn\'t update this weight, sorry', 'error')
                return redirect(url_for('weight_bp.main'))

            flash('Weight updated successfully!', 'message')
            return redirect(url_for('weight_bp.main'))

        # else insert a new record
        success = insert(current_user,
                         fAddWeight.weight.data,
                         fAddWeight.weightDate.data)

        if not success:
            flash('Couldn\'t save new weight, sorry', 'error')
            return redirect(url_for('weight_bp.main'))

        flash('Weight recorded successfully!', 'message')
        return redirect(url_for('weight_bp.main'))

    return render_template("weight/main.html",
                           titleText=titleText,
                           headerText=headerText,
                           fAddWeight=fAddWeight,
                           fDeleteWeight=fDeleteWeight,
                           fEditWeight=fEditWeight,
                           fUploadFile=fUploadFile,
                           weights=formatW(weights),
                           showGraph=graphFlag,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2],
                           redirectHoovering=redirectHoovering,
                           default=default)


@weight_bp.route("/edit", methods=['POST'])
def editWeight():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fEditWeight = EditWeightForm()

    if fEditWeight and request.method == 'POST':

        editThis = edit(fEditWeight.weightId.data)

        return redirect(url_for('weight_bp.main',
                                id=fEditWeight.weightId.data,))

    return redirect(url_for('weight_bp.main'))


@weight_bp.route("/delete", methods=['POST'])
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

    return redirect(url_for('weight_bp.main'))


@weight_bp.route("/upload", methods=['GET', 'POST'])
def upload():

    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))

    fUploadFile = UploadFileForm()

    redirectHoovering = 'upload'
    details = ""
    uploadForm = ''

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
            
            details = f"""Row number {rowNumber}. Reason:"""

            for row in reader:
                rowNumber = rowNumber + 1

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

            if errorRow != "":
                errorMsg = f"""File hasn't been proccessed!{nl}""" \
                            f"""Couldn't save new data.{nl}""" \
                            f"""{errorRow}"""

                flash(errorMsg, 'error')
                return redirect(url_for('weight_bp.upload'))

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
                        return redirect(url_for('weight_bp.upload'))

            flash('File uploaded successfully!', 'message')
            return redirect(url_for('weight_bp.upload'))

    return redirect(url_for('weight_bp.main', uploadForm='show'))
    # return render_template("weight/main.html",
    #                        titleText=titleText,
    #                        headerText=headerText,
    #                        fUploadFile=fUploadFile,
    #                        redirectHoovering=redirectHoovering)
