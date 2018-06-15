from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.us_states import data as states
from bokeh.models import HoverTool, ColumnDataSource, Circle, TapTool
from bokeh.embed import components

import dill
del states["HI"]
del states["AK"]
lons, lats, citynames = dill.load(open('./localtype/latlontest.m','rb'))

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]
state_names = [states[code]["name"] for code in states]
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

def create_figure():
    p = figure(
        title='',
        toolbar_location="left",
        tools="",
        plot_width=800,
        plot_height=500)
    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.toolbar.logo = None
    p.toolbar_location = None
    state_source = ColumnDataSource(data=dict(
        x=state_xs,
        y=state_ys,
        name=state_names,
    ))
    p.patches(
        'x',
        'y',
        source=state_source,
        fill_alpha=0.0,
        line_color="#000000",
        line_width=1,
        line_alpha=1)

    # Plot towns as circles
    crx = lons
    cry = lats
    crnames = citynames
    crsource = ColumnDataSource(data=dict(x=crx,y=cry,name=crnames))
    cr = p.circle('x', 'y', size=10, source=crsource, fill_color="blue",line_color="black")
    p.add_tools(HoverTool(
        tooltips=[
            ("Name", "@name"),
        ],
        renderers=[cr],
    ))

    selected_circle = Circle(fill_alpha=1, fill_color="firebrick", line_color='firebrick')
    nonselected_circle = Circle(fill_alpha=0.5, fill_color="blue", line_color="black")
    cr.selection_glyph = selected_circle
    cr.nonselection_glyph = nonselected_circle
    script, div = components(p)
    return script, div

