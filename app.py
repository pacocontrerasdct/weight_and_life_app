from flask import Flask, render_template, redirect, url_for, request
from meta_tags_dict import pageTitleDict

app=Flask(__name__)


@app.route("/layout")
def layout():
  return render_template("layout.html")

@app.route("/")
def index():
  return render_template("layout.html",
                header='header.html',
                menu='menu.html',
                footer='footer.html',
                page="index.html",
                titleText=pageTitleDict["index"])

@app.route("/historical")
def historical():
  return render_template("layout.html",
                header='header.html',
                menu='menu.html',
                footer='footer.html',
                page="historical.html",
                titleText=pageTitleDict["historical"])


@app.route("/about")
def about():
  return render_template("layout.html",
                header='header.html',
                menu='menu.html',
                footer='footer.html',
                page="about.html",
                titleText=pageTitleDict["about"])

if __name__ == '__main__':
  app.run(debug=True)

