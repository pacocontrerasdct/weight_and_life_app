from flask import Flask, render_template, redirect, url_for, request
from meta_tags_dict import *

app=Flask(__name__)

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

