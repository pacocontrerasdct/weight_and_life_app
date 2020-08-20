"""Routes for core application."""
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user
# from datetime import datetime as dt
from flask import current_app as app
from .models import db, Admin, Subscriptor, Weight, Trip
from .meta_tags_dict import metaTags

from pandas import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool


@app.route("/home")
@app.route("/index")
@app.route("/")
def index():
    titleText = metaTags["index"]["pageTitleDict"]
    headerText = metaTags["index"]["headerDict"]

    return render_template("index.html",
                           titleText=titleText,
                           headerText=headerText,
                           redirectHoovering='/')


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

    return redirect(url_for('index'))


@app.route("/historical")
def historical():
    titleText = metaTags["historical"]["pageTitleDict"]
    headerText = metaTags["historical"]["headerDict"]

    df = pd.read_sql_table('weights',
                           app.config['SQLALCHEMY_DATABASE_URI'])
    _y = df["weight"]
    _x = df["weight_date"]

    print(type(_x))
    print(_x[0])

    hover = HoverTool(tooltips=[(("Date, Weight"), "@x, @y Kg")])

    TOOLS = [hover]

    _plot = figure(title=(
        "Historic data showing variations of my weight "
        "since I moved to London"
    ),
        x_axis_label='Dates',
        y_axis_label='Kg',
        x_axis_type='datetime',
        tools=TOOLS)

    _plot.line(_x,
               _y,
               legend_label="My weight of life",
               line_width=5)

    # _plot = figure(title="My weight",
    #                x_axis_label='Dates',
    #                x_range=_y,
    #                y_axis_label='Weight',
    #                plot_height=350,
    #                x_axis_type='datetime')
    # _plot.vbar(x=_y, top=_x, width=0.9)
    # _plot.y_range.start = 50

    cdn_javascript = CDN.js_files[0]
    myData, myDiv = components(_plot)

    print("cdb ", cdn_javascript)
    # print("data ", myData)
    # print("myDiv", myDiv)

    return render_template("historical.html",
                           titleText=titleText,
                           headerText=headerText,
                           cdn_javascript=cdn_javascript,
                           myData=myData,
                           myDiv=myDiv)


@app.route("/about")
def about():
    titleText = metaTags["about"]["pageTitleDict"]
    headerText = metaTags["about"]["headerDict"]

    return render_template("about.html",
                           titleText=titleText,
                           headerText=headerText,)
