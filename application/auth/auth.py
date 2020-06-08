"""Routes for user authentication."""
from . import auth_bp
from flask import Blueprint, render_template, redirect, request, flash, session, url_for
from . import login_manager
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from .forms import LoginForm, SignupForm
from application.models import db, Admin
from datetime import datetime as dt
from application.meta_tags_dict import metaTags


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
  """
  Administrators sign-up page

  GET: Serve sign-up page.
  POST: Validate form, create account, redirect admin to private area.
  """
  titleText=metaTags['signup']['pageTitleDict']
  headerText=metaTags['signup']['headerDict']
  access=False
  form = SignupForm()

  if form.validate_on_submit() and request.method == 'POST':
    # Check if admin is already registered
    existing_admin = Admin.query.filter_by(email=form.email.data).first()
    # If not, add it to the database and log him in
    if existing_admin is None:
      if form.email.data == "pacocontrerasdct@gmail.com":
        access=True
      admin = Admin(name=form.name.data,
                    email=form.email.data,
                    full_access=access,
                    created=dt.now(),
                    last_login=dt.now())
      admin.set_password(form.password.data)
      db.session.add(admin)
      db.session.commit()
      login_user(admin)

      return redirect(url_for('private'))

    # If admin exists show error message
    flash('A admin user already exists with that email address.', 'error')

  return render_template("signup.html", form=form, titleText=titleText, headerText=headerText)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  """
  Log-in page for registered administrators

  GET: Serve log-in page
  POST: Validate form and redirect admin to private area
  """
  titleText=metaTags['login']['pageTitleDict']
  headerText=metaTags['login']['headerDict']

  if current_user.is_authenticated:
    # return render_template("private.html", titleText=titleText, headerText=headerText)
    return redirect(url_for('private'))

  form = LoginForm()

  if form.validate_on_submit() and request.method == 'POST':
    admin = Admin.query.filter_by(email=form.email.data).first()
    if admin and admin.check_password(password=form.password.data):
      
      admin.last_login=dt.now()
      db.session.commit()

      login_user(admin)
      next_page = request.args.get('next')
      return redirect(next_page or url_for('private'))

    flash ('Invalid user name or password', 'error')
    return redirect(url_for('auth_bp.login'))

  return render_template("login.html", form=form, titleText=titleText, headerText=headerText)


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
  """Logout user deleting session"""
  current_user.last_logout=dt.now()
  db.session.commit()

  logout_user()

  if session.get('was_once_logged_in'):
    del session['was_once_logged_in']
  
  flash('You have logged out successfully', 'message')
  return redirect(url_for('index'))


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

