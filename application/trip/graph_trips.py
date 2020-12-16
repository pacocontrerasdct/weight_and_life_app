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
                 x_axis_label = 'x',
                 y_axis_label = 'y',
                 plot_width=650,
                 plot_height=450,
                 sizing_mode='scale_both')

    # WEIGHTS
    #################################
    
    # weight_dates
    line_x = [1,2,3,40,105]
    # weights
    line_y = [2,4,6,60,20]

    _line_color = "pink"
    _line_width = 8


    # TRIPS 
    #################################
    # _n = num of trips to show
    # _height = height of the vertical bar which depends on max height of line_y + 10%
    # _ye = distance from 'y' zero
    # _left = left start of the bar
    # _right = right end of the bar
    # _colors = global if one "color", individual if an array ["color_1", "color_2" [,...]]
   
    _n = 20
    _height = int(sorted(line_y)[-1]) + int(sorted(line_y)[-1] * 0.1)
    
    _ye = []
    for x in range(0,_n):
        _ye.append(_height/2)

    _left = [2,13,50,80]
    _right = [10,22,59,92]
    _colors = ["Cyan", "red", "orange", "Black"]







    # draw horizontal bars figure
    fig.hbar(y = _ye,
             height = _height,
             left = _left,
             right = _right,
             color = _colors)

    # draw line figure
    fig.line(line_x, line_y, color=_line_color, width=_line_width)









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

    # bar = []

    # for element in range(1,df.shape[0]):
    #     bar.append(5)

    # print(bar)

    # _y = 10
    # _x_start = df["starting_date"]
    # _x_end = df["ending_date"]

    # print(type(_x_start))
    # print(_x_start.size)
    # print(_x_start[0])
    # print(_x_end[0])

    # for i in range(1,_x_start.size):
    #     # diff = _x_end[x]  - _x_start[x]
    #     # print(diff/np.timedelta64(1,'D'))
    #     print(f"""start {_x_start[i]}""")
    #     print(f"""end {_x_end[i]}""")


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



    # y-coordinates is a series
    # from the very first ordered start_date minus a week
    # to the very last date plus a week
    # y = []
    # diff = []
    # right = myDates
    # height = []


      
    # x-coordinates of the right edges 
    # right = [5,5,5,5,5] 

    # height / thickness of the bars  
    # height = [0.5, 0.4, 0.3, 0.2, 0.1] 
      
    # color values of the bars 
    # fill_color = ["yellow", "pink", "blue", "green", "purple"]

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
