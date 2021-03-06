import datetime

from datetime import date
from flask import current_app as app
from pandas import pandas as pd

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import (BoxSelectTool,
                          PanTool,
                          WheelZoomTool,
                          BoxZoomTool,
                          ResetTool,
                          HoverTool)


def graphWeights():

    df = pd.read_sql_query("SELECT * FROM weights ORDER BY weight_date",
                           app.config['SQLALCHEMY_DATABASE_URI'])
    _y = df["weight"]
    _x = df["weight_date"]

    box = BoxSelectTool()
    wheel = WheelZoomTool()
    panTool = PanTool()
    boxZoomTool = BoxZoomTool()
    resetTool = ResetTool()
    hover = HoverTool(show_arrow=True,
                      point_policy='follow_mouse',
                      tooltips=[
                      ("Date", " @x{%F}"),
                      ("Weight", " @y Kg")],
                      formatters={
                        # use 'datetime' formatter for '@x' field
                        '@x' : 'datetime'})

    TOOLS = [hover, box, wheel, panTool, boxZoomTool, resetTool]

    _plot = figure(title=("Historic data showing variations of my weight "
                          "since I moved to London"),
                    plot_width=650,
                    plot_height=450,
                    sizing_mode='scale_both',
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
