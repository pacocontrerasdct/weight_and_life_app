from flask import current_app as app
from pandas import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool

def graphTrips():
    
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

    # _plot = figure(title="My weight",
    #                x_axis_label='Dates',
    #                x_range=_y,
    #                y_axis_label='Weight',
    #                plot_height=350,
    #                x_axis_type='datetime')
    # _plot.vbar(x=_y, top=_x, width=0.9)
    # _plot.y_range.start = 50

    cdn_javascript = CDN.js_files[0]
    bokehScriptComponent, bokehDivComponent = components(_plot)

    # print("cdb ", cdn_javascript)
    # print("data ", bokehScriptComponent)
    # print("bokehDivComponent", bokehDivComponent)

    graph = [cdn_javascript, bokehScriptComponent, bokehDivComponent]

    return graph
