"""Routes for user authentication."""
from flask import Blueprint, render_template, request

# Blueprint configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  return render_template("login.html", body="Hello login")



@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
  return render_template("signup.html", body="Hello signup")