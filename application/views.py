"""Routes for core application."""
import operator
import os
import csv
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user

from flask import current_app as app
from application.models import db, Subscriptor
from application.meta_tags_dict import metaTags
from application.graph_historical import graphHistorical
from application.trip.crudAirport import readAirportList

from application.general_forms import UploadFileForm
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge


@app.route("/home")
@app.route("/index")
@app.route("/")
def index():
    titleText = metaTags["index"]["pageTitleDict"]
    headerText = metaTags["index"]["headerDict"]

    hasAirportListBeenLoaded = loadAirportsList()

    return render_template("index.html",
                           titleText=titleText,
                           headerText=headerText,
                           redirectHoovering='/')

def loadAirportsList():
    airportsList = readAirportList()

    if len(airportsList) == 0:

        fileName = 'airport_list_dataset.csv'
        filePath = os.path.join('application/static/uploads/', fileName)

        with open(filePath, newline='') as csvfile:
            fNames = ['airport_country', 'airport_city', 'airport_name', 'iata_identifier']
            reader = csv.DictReader(csvfile, fieldnames=fNames, delimiter=';')

            for row in reader:
                countryFromRow = row['airport_country']
                cityFromRow = row['airport_city']
                airportFromRow = row['airport_name']
                identifierFromRow = row['iata_identifier']

                success = insertAirport(countryFromRow, cityFromRow, airportFromRow, identifierFromRow)

                if not success:
                    flash('Something went wrong loading the airports list.',
                          'error')


@app.route("/thank-you", methods=['POST'])
def thank_you():

    if request.method == 'POST':
        userName_ = request.form["userName"]
        userEmail_ = request.form["userEmail"]

        if userName_ and userEmail_:

            # Check if user is in the database
            isSubscriptor = Subscriptor.query.filter(
                Subscriptor.name == userName_
                or Subscriptor.email == userEmail_).first()

            if isSubscriptor:
                flash('Subscriptor already in the list.', 'warning')
                return redirect(url_for('index'))

            newSubscriptor = Subscriptor(name=userName_,
                                         email=userEmail_)
            db.session.add(newSubscriptor)
            db.session.commit()

            flash(f"""Thanks for your interest!
                  You will receive my newsletter
                  next time I produce it!.""",
                  'message')

    return redirect(url_for('index'))


@app.route("/historical")
def historical():
    
    titleText = metaTags["historical"]["pageTitleDict"]
    headerText = metaTags["historical"]["headerDict"]

    graph = graphHistorical()

    return render_template("historical.html",
                           titleText=titleText,
                           headerText=headerText,
                           cdn_javascript=graph[0],
                           bokehScriptComponent=graph[1],
                           bokehDivComponent=graph[2])


@app.route("/about")
def about():
    titleText = metaTags["about"]["pageTitleDict"]
    headerText = metaTags["about"]["headerDict"]

    return render_template("about.html",
                           titleText=titleText,
                           headerText=headerText)


@app.route("/all-routes")
def all_routes():
    rules = []
    routes = []

    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))

    for endpoint, methods, rule in sorted(rules, key=operator.itemgetter(2)):
        routes.append((endpoint, methods, rule))

    return render_template("all_links.html", routes=routes)

