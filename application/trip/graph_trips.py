import numpy as np
import datetime
from datetime import date
from flask import current_app as app
from pandas import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool

def graphTrips():
    
    graph = []
    
    df = pd.read_sql_table('trips',
                           app.config['SQLALCHEMY_DATABASE_URI'])

    oldestYear = df.sort_values(by='starting_date', ascending=True).iloc[0].starting_date.year

    print("min", oldestYear)

    newestYear = df.sort_values(by='ending_date', ascending=False).iloc[0].ending_date.year

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


    # # hover = HoverTool(tooltips=[(("Date, Weight"), "@x, @y Kg")])

    # # TOOLS = [hover]

    # # _plot = figure(title=(
    # #                       "Historic data showing variations of my weight "
    # #                       "since I moved to London"
    # #                       ),
    # #                         plot_width=650,
    # #                         plot_height=450,
    # #                         sizing_mode='scale_both',
    # #                         x_axis_label='Dates',
    # #                         y_axis_label='Kg',
    # #                         x_axis_type='datetime',
    # #                         tools=TOOLS)

    # # _plot.line(_x,
    # #            _y,
    # #            legend_label="My weight of life",
    # #            line_width=5)

    # _plot = figure(title="My dates",
    #                y_range='1,_x_start.size',
    #                y_axis_label='None',
    #                # x_range='_x_start,_x_end',
    #                x_axis_label='Dates',
    #                plot_height=350,
    #                x_axis_type='datetime')

    # # _plot.hbar(y="Year", left='_x_start', right='Time_max', height=0.4, source=source)
    # _plot.vbar(x=_y, top=_x_start, width=_x_end)
    # # _plot.y_range.start = 50

    # cdn_javascript = CDN.js_files[0]
    # bokehScriptComponent, bokehDivComponent = components(_plot)

    # # print("cdb ", cdn_javascript)
    # # print("data ", bokehScriptComponent)
    # # print("bokehDivComponent", bokehDivComponent)

    # graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]




    # instantiating the figure object 
    thisGraph = figure(title = "Bokeh Horizontal Bar Graph",
                       plot_width=650,
                       plot_height=450,
                       sizing_mode='scale_both') 
      
    # name of the x-axis 
    thisGraph.xaxis.axis_label = "x-axis"
          
    # name of the y-axis 
    thisGraph.yaxis.axis_label = "y-axis"
      
    # y-coordinates is a series
    # from the very first ordered start_date minus a week
    # to the very last date plus a week
    y = []
    right = []
    height = []

    for year in range(oldestYear,newestYear):
        y.append(year)        
        right.append(5)
        height.append(0.5)
      
    # x-coordinates of the right edges 
    # right = [5,5,5,5,5] 

    # height / thickness of the bars  
    # height = [0.5, 0.4, 0.3, 0.2, 0.1] 
      
    # color values of the bars 
    fill_color = ["yellow", "pink", "blue", "green", "purple"] 
      
    # plotting the thisGraph 
    thisGraph.vbar(y, 
               bottom = right, 
               width = height, 
               fill_color = fill_color) 

    cdn_javascript = CDN.js_files[0]
    bokehScriptComponent, bokehDivComponent = components(thisGraph)

    # print("cdb ", cdn_javascript)
    # print("data ", bokehScriptComponent)
    # print("bokehDivComponent", bokehDivComponent)

    graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]




















    return graph
