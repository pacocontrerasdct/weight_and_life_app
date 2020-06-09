"""Routes for dashboard private area."""
from flask import Blueprint, render_template, redirect, request, flash, session, url_for
from . import dashboard_bp

from application import login_manager
from application.meta_tags_dict import metaTags
from application.models import db, Admin, Weight, Trip

from flask_login import current_user, logout_user

from .forms import AddWeightForm, UploadFileForm
from datetime import datetime as dt




@dashboard_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():

  form1 = AddWeightForm()
  form2 = UploadFileForm()

  if not current_user.is_authenticated:
    return redirect(url_for('auth_bp.login'))

  if form2.validate_on_submit() and request.method == 'POST':

    print (form2.txtFile.data)
    
    flash('form2 validated', 'message')
    return render_template("dashboard.html",
                          form1=form1,
                          form2=form2)


  flash('form2 not validated', 'error')

  return render_template("dashboard.html",
                          titleText=metaTags['dashboard']['pageTitleDict'],
                          headerText=metaTags['dashboard']['headerDict'],
                          form1=form1,
                          form2=form2)


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