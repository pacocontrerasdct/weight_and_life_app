"""Routes for dashboard private area."""
from flask import Blueprint, render_template, redirect, request, flash, session, url_for
from . import dashboard_bp

from application import login_manager
from application.meta_tags_dict import metaTags

from flask_login import current_user, logout_user
from .forms import AddWeightForm, UploadFileForm, DeleteWeightForm

from application.models import db, Admin, Weight, Trip
from datetime import datetime as dt

from .crudWeight import read, insert

titleText = metaTags['dashboard']['pageTitleDict']
headerText = metaTags['dashboard']['headerDict']

@dashboard_bp.route("/main", methods=['GET', 'POST'])
def dashboard():
  
  if not current_user.is_authenticated:
    return redirect(url_for('auth_bp.login'))

  fAddWeight = AddWeightForm()
  fDeleteWeight = DeleteWeightForm()
  weights = read(current_user)
  redirectHoovering='main'

  if fAddWeight.validate_on_submit() and request.method == 'POST':

    print ("enter add-weight form 1 is ", fAddWeight.weight.data)
    success = insert(current_user, fAddWeight.weight.data, fAddWeight.weightDate.data)

    if not success :
      flash('Couldn\'t save new weight, sorry', 'error')
      return redirect(url_for('.dashboard'))

    flash('Weight recorded successfully!', 'message')
    return redirect(url_for('.dashboard'))

  return render_template("dashboard.html",
                          titleText=titleText,
                          headerText=headerText,
                          fAddWeight=fAddWeight,
                          fDeleteWeight=fDeleteWeight,
                          weights=weights,
                          redirectHoovering=redirectHoovering)

@dashboard_bp.route("/upload", methods=['GET', 'POST'])
def upload():

  if not current_user.is_authenticated:
    return redirect(url_for('auth_bp.login'))

  fUploadFile = UploadFileForm()
  fDeleteWeight = DeleteWeightForm()
  weights = read(current_user)
  redirectHoovering='upload'

  if request.method == 'POST' and fUploadFile.validate_on_submit():

    print ("entering addFile ", fUploadFile.txtFile.data)
    
    flash('File uploaded successfully!', 'message')
    return redirect(url_for('.upload'))

  return render_template("dashboard.html",
                          titleText=titleText,
                          headerText=headerText,
                          fUploadFile=fUploadFile,
                          fDeleteWeight=fDeleteWeight,
                          weights=weights,
                          redirectHoovering=redirectHoovering,)

@dashboard_bp.route("/delete", methods=['POST'])
def deleteWeight():
  
  if not current_user.is_authenticated:
    return redirect(url_for('auth_bp.login'))

  fDeleteWeight = DeleteWeightForm()

  if fDeleteWeight and request.method == 'POST':
    print ("delete this id: ", fDeleteWeight.weightId.data)
    print ("delete this id: ", fDeleteWeight.submit.data)
    # return redirect(url_for('.dashboard'))

  return redirect(url_for('.dashboard'))


