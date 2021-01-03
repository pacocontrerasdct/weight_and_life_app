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


def plotWeightsAndTrips():

    weights_y = None

    # Weights and dates
    df_weights = pd.read_sql_query("SELECT * FROM weights ORDER BY weight_date",
                                   app.config['SQLALCHEMY_DATABASE_URI'])
    weightDates_x = df_weights['weight_date']
    weights_y = df_weights['weight']
    line_color = "black"
    line_width = 4

    df_solo_trips = pd.read_sql_query("select * from trips where passenger_companion = '' ",
                                 app.config['SQLALCHEMY_DATABASE_URI'])

    df_companion_trips = pd.read_sql_query("select * from trips where passenger_companion != '' ",
                                 app.config['SQLALCHEMY_DATABASE_URI'])
    
    if (df_solo_trips.empty == True 
        and df_companion_trips.empty == True
        and df_weights.empty == True):
            return ["","",""]

    # Make sure we have a default bar height
    # in case there is no Weight data to show
    weights_y = weights_y if weights_y is not None else [0,9]
    highestWeight_y = int(sorted(weights_y)[-1])
    lowestWeight_y = int(sorted(weights_y)[0])

    # tripsBarHeight = height of the vertical bar 
    #                   which depends on max height of weights_y
    #                   + 10%
    # tripsBarStart = left start of the bar
    # tripsBarEnd = right end of the bar
    # tripsBarColors = global if one "color",
    #                   individual if an array
    #                   ["color_1", "color_2" [,...]]

    # Solo trips horizontal bars data
    tripsBarHeight = (highestWeight_y - lowestWeight_y) + (highestWeight_y - lowestWeight_y)*0.1
    tripsBarStart = df_solo_trips['departure_date']
    tripsBarEnd = df_solo_trips['return_date']
    tripsBarColors = "red" # Or individual colors for each value ["Cyan", "red",...]

    # Group trips horizontal bars data
    tripsBarGroupStart = df_companion_trips['departure_date']
    tripsBarGroupEnd = df_companion_trips['return_date']
    tripsBarGroupColors = "blue"

    # designing the plot style and information
    hover = HoverTool(show_arrow=True,
                      point_policy='follow_mouse',
                      tooltips=[
                      ("Trip from", " @left{%F}"),
                      ("to", " @right{%F}"),
                      ("Date", " @x{%F}"),
                      ("Weight", " @y Kg")],
                      formatters={
                        # use 'datetime' formatter for 'date' fields
                        # default 'numeral' formatter for other fields            
                        '@x' : 'datetime',
                        '@left' : 'datetime',
                        '@right' : 'datetime'})
    box = BoxSelectTool()
    wheel = WheelZoomTool()
    panTool = PanTool()
    boxZoomTool = BoxZoomTool()
    resetTool = ResetTool()

    TOOLS = [hover, box, wheel, panTool, boxZoomTool, resetTool]

    _plot = figure(title="Personal data registered since June 2014.",
                   x_axis_label='Dates',
                   x_axis_type='datetime',
                   y_axis_label='Kilograms',
                   y_axis_type='auto',
                   plot_width=650,
                   plot_height=450,
                   sizing_mode='scale_both',
                   tools=TOOLS)

    _plot.hbar(name = "red",
               y = highestWeight_y*0.96,
               height = tripsBarHeight,
               left = tripsBarStart,
               right = tripsBarEnd,
               color = tripsBarColors,
               legend_label="Solo trips")

    _plot.hbar(name = "blue",
               y = highestWeight_y*0.96,
               height = tripsBarHeight,
               left = tripsBarGroupStart,
               right = tripsBarGroupEnd,
               color = tripsBarGroupColors,
               legend_label="Group trips")
 
    # add weights' line to the figure
    _plot.line(weightDates_x,
               weights_y,
               color=line_color,
               width=line_width,
               legend_label="Weights",
               line_width=5)

    # Technicalities to show the graph
    curdoc().add_root(_plot)

    cdn_javascript = CDN.js_files[0]
    bokehScriptComponent, bokehDivComponent = components(_plot)
    graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]

    return graph
