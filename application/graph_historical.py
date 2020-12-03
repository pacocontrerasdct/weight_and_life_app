from flask import current_app as app
from pandas import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool

def graphHistorical():
    
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

    cdn_javascript = CDN.js_files[0]
    bokehScriptComponent, bokehDivComponent = components(_plot)

    graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]

    return graph
