import numpy as np
import datetime
import matplotlib.pyplot as plt

from datetime import date
from flask import current_app as app
from pandas import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import (BoxSelectTool,
                          PanTool,
                          WheelZoomTool,
                          BoxZoomTool,
                          ResetTool,
                          HoverTool,
                          Circle,
                          Line,
                          ColumnDataSource, Grid, LinearAxis, Plot)

def gTest():

    graph = []

    df_trips = pd.read_sql_table('trips',
                           app.config['SQLALCHEMY_DATABASE_URI'])

    df_trips['middle_date'] = df_trips['starting_date'] + ( ( df_trips['ending_date'] - df_trips['starting_date'] ) / 2 )
    df_trips['date_radius'] = ( df_trips['ending_date'] - df_trips['starting_date'] ) / 2
    df_trips['radius'] = df_trips['date_radius'] / pd.Timedelta(1, unit='d')

    print(df_trips['starting_date'])
    print(df_trips['middle_date'])
    print(df_trips['radius'])
    print(df_trips['date_radius'])

    N = 18
    y = np.linspace(2, 2, N)
    sizes = df_trips['radius']

    x = df_trips['middle_date'].to_numpy()
    xx = df_trips['starting_date'].apply(lambda x: x.year)

    source = ColumnDataSource(dict(x=x,
                                   y=y,
                                   sizes=df_trips['radius']))

    hover = HoverTool(tooltips=[(("Date"), "@xx")])
    box = BoxSelectTool()
    wheel = WheelZoomTool()
    panTool = PanTool()
    boxZoomTool = BoxZoomTool()
    resetTool = ResetTool()

    TOOLS = [hover, box, wheel, panTool, boxZoomTool, resetTool]

    plot_trip = Plot(title=None,
                       plot_width=650,
                       plot_height=450,
                       sizing_mode='scale_both',
                       tools=TOOLS)

    glyph = Circle(x="x",
                   y="y",
                   size="sizes",
                   line_color="#CCCCCC",
                   fill_color="red",
                   line_width=3)

    plot_trip.add_glyph(source, glyph)





    x = [1,2,3,4,5]
    y = [2,4,6,8,10]

    fig = figure(title = 'Line Plot example', x_axis_label = 'x', y_axis_label = 'y', plot_width = 400, plot_height = 400)
    fig.line(x,y)
    fig.hbar(y = [2,2,2,2], height = 1, left = 0, right = [1,.2,.3,.4], color = "Cyan")

    curdoc().add_root(fig)

    cdn_javascript = CDN.js_files[0]
    bokehScriptComponent, bokehDivComponent = components(fig)
    graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]

    return graph



def twoPlotsSameFig():

    # designing the plot style and information
    fig = figure(title = 'Line Plot example',
                 x_axis_label='Dates',
                 y_axis_label='Kg',
                 x_axis_type="datetime",
                 plot_width=650,
                 plot_height=450,
                 sizing_mode='scale_both')

    weights_y = None


    # WEIGHTS
    #################################
    df_weights = pd.read_sql_table('weights',
                                   app.config['SQLALCHEMY_DATABASE_URI'])

    weightDates_x = [1,2,3,40,105]
    weights_y = [2,4,6,60,20]

    weightDates_x = df_weights['weight_date']
    weights_y = df_weights['weight']
    
    line_color = "pink"
    line_width = 8


    # SOLO TRIPS 
    #################################

    df_trips = pd.read_sql_query('select * from trips where solo_flight = true',
                                 app.config['SQLALCHEMY_DATABASE_URI'])

    df_trips['middle_date'] = df_trips['starting_date'] + ( ( df_trips['ending_date'] - df_trips['starting_date'] ) / 2 )
    df_trips['date_radius'] = ( df_trips['ending_date'] - df_trips['starting_date'] ) / 2
    df_trips['radius'] = df_trips['date_radius'] / pd.Timedelta(1, unit='d')

    print(df_trips['starting_date'])
    print(df_trips['middle_date'])
    print(df_trips['radius'])
    print(df_trips['date_radius'])


    # tripsBarHeight = height of the vertical bar which depends on max height of weights_y + 10%
    # tripsBarStart = left start of the bar
    # tripsBarEnd = right end of the bar
    # tripsBarColors = global if one "color", individual if an array ["color_1", "color_2" [,...]]

    # Make sure we have a default bar height
    # in case there is no Weight data to show
    weights_y = weights_y if not weights_y.empty else [9]

    highestWeight_y = int(sorted(weights_y)[-1])

    tripsBarHeight = highestWeight_y + (highestWeight_y * 0.1)

    tripsBarStart = [2,13,50,80,100]
    tripsBarEnd = [10,22,59,92,105]

    tripsBarStart = df_trips['starting_date']
    tripsBarEnd = df_trips['ending_date']

    tripsBarColors = "red" # Or individual colors for each value ["Cyan", "red",...]


    # draw horizontal bars figure
    fig.hbar(name = "red",
             y = (tripsBarHeight/2),
             height = tripsBarHeight,
             left = tripsBarStart,
             right = tripsBarEnd,
             color = tripsBarColors)


   # DUO TRIPS 
    #################################

    df_trips = pd.read_sql_query('select * from trips where solo_flight = false',
                                 app.config['SQLALCHEMY_DATABASE_URI'])

    df_trips['middle_date'] = df_trips['starting_date'] + ( ( df_trips['ending_date'] - df_trips['starting_date'] ) / 2 )
    df_trips['date_radius'] = ( df_trips['ending_date'] - df_trips['starting_date'] ) / 2
    df_trips['radius'] = df_trips['date_radius'] / pd.Timedelta(1, unit='d')

    # Make sure we have a default bar height
    # in case there is no Weight data to show
    weights_y = weights_y if not weights_y.empty else [9]

    highestWeight_y = int(sorted(weights_y)[-1])

    tripsBarHeight = highestWeight_y + (highestWeight_y * 0.1)
    tripsBarStart = df_trips['starting_date']
    tripsBarEnd = df_trips['ending_date']
    tripsBarColors = "blue" # Or individual colors for each value ["Cyan", "red",...]

    # draw horizontal bars figure
    fig.hbar(name = "blue",
             y = (tripsBarHeight/2),
             height = tripsBarHeight,
             left = tripsBarStart,
             right = tripsBarEnd,
             color = tripsBarColors)


    # draw line figure
    fig.line(weightDates_x, weights_y, color=line_color, width=line_width)

    # Technicalities to show the graph
    curdoc().add_root(fig)

    cdn_javascript = CDN.js_files[0]
    bokehScriptComponent, bokehDivComponent = components(fig)
    graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]

    return graph


def graphTrips():
    
    graph = []
    
    df = pd.read_sql_table('trips',
                           app.config['SQLALCHEMY_DATABASE_URI'])

    myDates = df.sort_values(by='starting_date', ascending=True)

    daysBetweenDates = myDates.ending_date - myDates.starting_date

    print("my dates ", myDates)
    print("dates BETWEEN ", daysBetweenDates)

    oldestYear = myDates.iloc[0].starting_date.year
    newestYear = myDates.iloc[-1].ending_date.year

    print("min", oldestYear)
    print("max", newestYear)
    
    print("diff", newestYear - oldestYear)
    # print(df.shape[0])

    hover = HoverTool(tooltips=[(("Date"), "@x")])

    TOOLS = hover, "pan,wheel_zoom,box_zoom,reset"

    yearsRange = []
    top = []


    for year in range(myDates.shape[0]):
        yearsRange.append(year)
        # diff.append(myDates.ending_date - myDates.starting_date)        
        # right.append(5)
        # height.append(0.5)
        top.append(1)

    print(top)
    yearsRange = myDates.loc[:, 'starting_date']
    print("daterange ", yearsRange)

    # instantiating the figure object 
    thisGraph = figure(title = "Bokeh Horizontal Bar Graph",
                       x_axis_type="datetime",
                       plot_width=650,
                       plot_height=450,
                       sizing_mode='scale_both',
                       tools=TOOLS)
      
    # name of the x-axis 
    thisGraph.xaxis.axis_label = "Dates"          
    # name of the y-axis 
    # thisGraph.yaxis.axis_label = "none"

    thisGraph.x_range.start = myDates.starting_date.min()

    # plotting the thisGraph
    thisGraph.vbar(x = myDates.starting_date,
                   width = (myDates.ending_date - myDates.starting_date),
                   bottom=0,
                   top=top,
                   fill_color = "blue") 

    cdn_javascript = CDN.js_files[0]
    bokehScriptComponent, bokehDivComponent = components(thisGraph)

    # print("cdb ", cdn_javascript)
    # print("data ", bokehScriptComponent)
    # print("bokehDivComponent", bokehDivComponent)

    graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]

    return graph
