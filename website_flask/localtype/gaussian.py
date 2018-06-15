import math
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Range1d
from bokeh.models.widgets import Slider
from bokeh.plotting import ColumnDataSource, Figure

# --------------------------------------------------------
#
# An interactive plot showing normally distributed points.
#
# --------------------------------------------------------

# number of points shown in the plot
NUM_POINTS = 100

standard_deviation_slider = Slider(title='standard deviation', value=2, start=0, end=4)
cutoff_slider = Slider(title='maximum radius', value=4, start=0, end=8)

source = ColumnDataSource()


def update_source_data(new_points):
    """Update the source data.

    If new_points is True, random points will be generated. A normal distribution is used, and its standard deviation
    is the value of the standard deviation slider.

    The opacity of the points is chosen according to whether their distance from the origin is greater than the value
    of the cutoff slider.

    Params:
    -------
    new_points: bool
        Whether to generate new points.
    """

    standard_deviation = standard_deviation_slider.value
    cutoff = cutoff_slider.value

    # generate new points if requested

    if new_points:
        if standard_deviation > 0:
            x = np.random.normal(0, standard_deviation, NUM_POINTS)
            y = np.random.normal(0, standard_deviation, NUM_POINTS)
        else:
            x = np.zeros(NUM_POINTS)
            y = np.zeros(NUM_POINTS)
        source.data['x'] = x
        source.data['y'] = y

    # update the opacity

    def radius(u, v):
        """The distance from the origin."""

        return math.sqrt(u ** 2 + v ** 2)

    x = source.data['x']
    y = source.data['y']
    alpha = [1 if radius(x[i], y[i]) <= cutoff else 0.1 for i in range(NUM_POINTS)]

    source.data['alpha'] = alpha


# initialize the plot data
update_source_data(True)

# make the plot responsive to slider changes
standard_deviation_slider.on_change('value', lambda attr, old_value, new_value: update_source_data(True))
cutoff_slider.on_change('value', lambda attr, old_value, new_value: update_source_data(False))

# create the figure

p = Figure(title='Normal Distribution')

p.scatter(source=source, x='x', y='y', color='green', alpha='alpha', radius=0.1)

p.x_range = Range1d(start=-8, end=8)
p.y_range = Range1d(start=-8, end=8)

content = column(standard_deviation_slider, cutoff_slider, p)

# register the figure

curdoc().add_root(content)
curdoc().title = 'Normal Distribution'