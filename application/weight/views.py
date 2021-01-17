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
    
    graph = ["","",""]
    graphFlag = 0

    redirectHoovering = 'main'
    default = {}

    # show weight graphic if requested by user
    if request.method == 'GET' and request.args.get('graph') == "true":
        graph = graphWeights()
        graphFlag = 1

    # edit a weight record
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

