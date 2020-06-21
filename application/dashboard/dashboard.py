"""Routes for dashboard private area."""
from flask import Blueprint, render_template, redirect, request, flash, session, url_for
from . import dashboard_bp

from application import login_manager
from application.meta_tags_dict import metaTags
from application.models import db, Admin, Weight, Trip

from flask_login import current_user, logout_user

from .forms import AddWeightForm, UploadFileForm
from datetime import datetime as dt


titleText = metaTags['dashboard']['pageTitleDict']
headerText = metaTags['dashboard']['headerDict']

@dashboard_bp.route("/main", methods=['GET', 'POST'])
def dashboard():
  
  if not current_user.is_authenticated:
    return redirect(url_for('auth_bp.login'))

  fAddWeight = AddWeightForm()

  if fAddWeight.validate_on_submit() and request.method == 'POST':

    print ("enter add-weight form 1 is ", fAddWeight.weight.data)

    flash('Here add-weight fAddWeight validated', 'message')
    return redirect(url_for('.dashboard'))

  return render_template("dashboard.html",
                          titleText=titleText,
                          headerText=headerText,
                          fAddWeight=fAddWeight,)

@dashboard_bp.route("/upload", methods=['GET', 'POST'])
def upload():

  if not current_user.is_authenticated:
    return redirect(url_for('auth_bp.login'))

  fUploadFile = UploadFileForm()

  if request.method == 'POST' and fUploadFile.validate_on_submit():

    print ("entering addFile ", fUploadFile.txtFile.data)
    
    flash('fUploadFile validated', 'message')
    return redirect(url_for('.upload'))

  return render_template("dashboard.html",
                          titleText=titleText,
                          headerText=headerText,
                          fUploadFile=fUploadFile)

@login_manager.user_loader
def load_user(user_id):
  """Check if admin is logged on every page load."""
  if user_id is not None:
    return Admin.query.get(user_id)
  return None

@login_manager.unauthorized_handler
def unauthorized():
  """Redirect unauthorized admins to login page"""
  flash('You must be logged to view that page.')
  return redirect(url_for('auth_bp.login'))
