from flask import render_template, redirect, url_for, request, flash
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Admin, Subscriptor, Weight, Trip
from . import meta_tags_dict as meta


@app.route("/")
def index():
  titleText=meta.pageTitleDict["index"]
  headerText=meta.headerDict["index"]

  return render_template("index.html", titleText=titleText, headerText=headerText)

@app.route("/thank-you", methods=['POST'])
def thank_you():

  if request.method=='POST':
    userName_=request.form["userName"]
    userEmail_=request.form["userEmail"]
    print(userName_, userEmail_)

    if userName_ and userEmail_:

      # Check if user is in the database
      isSubscriptor = Subscriptor.query.filter(Subscriptor.name == userName_ or Subscriptor.email == userEmail_).first()
      
      if isSubscriptor:
        flash('Subscriptor already in the list.', 'warning')
        return render_template("index.html")

      newSubscriptor = Subscriptor(name=userName_,
                      email=userEmail_,
                      created=dt.now())
      db.session.add(newSubscriptor)
      db.session.commit()

      flash('Thanks for your interest! You will receive my newsletter next time I produce it!.', 'message')
      return render_template("index.html")

      # Render Subscriptor List
      # messageText="Thanks for your interest! You will receive my newsletter next time I produce it!."
      # return render_template("users-list.html", users=Subscriptor.query.all(), titleText=titleText, headerText="List of Users in newsletter", messageText=messageText)

  return render_template("index.html")

@app.route("/historical")
def historical():
  titleText=meta.pageTitleDict["historical"]
  headerText=meta.headerDict["historical"]

  return render_template("historical.html", titleText=titleText, headerText=headerText)

@app.route("/about")
def about():
  titleText=meta.pageTitleDict["about"]
  headerText=meta.headerDict["about"]

  return render_template("about.html", titleText=titleText, headerText=headerText)



@app.route("/login")
def login():
  titleText=meta.pageTitleDict["access"]
  headerText=meta.headerDict["access"]

  return render_template("access-area.html", titleText=titleText, headerText=headerText)


@app.route("/private", methods=['POST'])
def private():
  titleText=meta.pageTitleDict["private"]
  headerText=meta.headerDict["private"]


  if request.method == 'POST':

    loginEmail_=request.form["loginEmail"]
    loginPassword_=request.form["loginPassword"]

    if loginEmail_ and loginPassword_:

      # Check if user is in the database and has admin rights
      isAdminUser = Admin.query.filter(Admin.email == loginEmail_ and Admin.password == loginPassword_ and Admin.full_access == "true" ).first()
      
      if isAdminUser:

        messageText="Welcome {}".format(isAdminUser.name)

        # Update login 
        isAdminUser.last_login = dt.now()
        db.session.commit()

        return render_template("private.html", titleText=titleText, headerText=headerText, messageText=messageText)
      else:

        flash('User name or password incorrect. Try it again!', 'error')
        return redirect(url_for('login'))

  return redirect(url_for('login'))
