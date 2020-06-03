from flask import Flask, render_template, redirect, url_for, request
from meta_tags_dict import *

from database.database import database_bp


app=Flask(__name__)

app.register_blueprint(database_bp)

# SQLALCHEMY_DATABASE_URI is global variable at the config file
# We need to set it with the path to our db
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("LOCAL_DATABASE_URL")




@app.route("/")
def index():
  return render_template("index.html",
                titleText=pageTitleDict["index"],
                headerText=headerDict["index"])

@app.route("/historical")
def historical():
  return render_template("historical.html",
                titleText=pageTitleDict["historical"],
                headerText=headerDict["historical"])

@app.route("/about")
def about():
  return render_template("about.html",
                titleText=pageTitleDict["about"],
                headerText=headerDict["about"])

@app.route("/login")
def login():
  return render_template("access-area.html",
                titleText=pageTitleDict["access"],
                headerText=headerDict["access"])

@app.route("/private")
def private():
  return render_template("private.html",
                titleText=pageTitleDict["private"],
                headerText=headerDict["private"])

if __name__ == '__main__':
  app.run(debug=True)

