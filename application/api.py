"""Routes for core application."""
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user
# from datetime import datetime as dt
from flask import current_app as app
from .models import db, Admin, Subscriptor, Weight, Trip
from .meta_tags_dict import metaTags

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
  titleText=metaTags["index"]["pageTitleDict"]
  headerText=metaTags["index"]["headerDict"]

  return render_template("index.html", titleText=titleText, headerText=headerText)

@app.route("/thank-you", methods=['POST'])
def thank_you():

  if request.method=='POST':
    userName_=request.form["userName"]
    userEmail_=request.form["userEmail"]

    if userName_ and userEmail_:

      # Check if user is in the database
      isSubscriptor = Subscriptor.query.filter(Subscriptor.name == userName_ or Subscriptor.email == userEmail_).first()
      
      if isSubscriptor:
        flash('Subscriptor already in the list.', 'warning')
        return redirect(url_for('index'))

      newSubscriptor = Subscriptor(name=userName_,
                      email=userEmail_)
      db.session.add(newSubscriptor)
      db.session.commit()

      flash('Thanks for your interest! You will receive my newsletter next time I produce it!.', 'message')
      return redirect(url_for('index'))

  return redirect(url_for('index'))

@app.route("/historical")
def historical():
  titleText=metaTags["historical"]["pageTitleDict"]
  headerText=metaTags["historical"]["headerDict"]

  return render_template("historical.html", titleText=titleText, headerText=headerText)

@app.route("/about")
def about():
  titleText=metaTags["about"]["pageTitleDict"]
  headerText=metaTags["about"]["headerDict"]

  return render_template("about.html", titleText=titleText, headerText=headerText)


@app.route("/private", methods=['GET','POST'])
@login_required
def private():
  titleText=metaTags["private"]["pageTitleDict"]
  headerText=metaTags["private"]["headerDict"]

  return render_template("private.html", 
                          titleText=titleText,
                          headerText=headerText, 
                          current_user=current_user)






