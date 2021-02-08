import pandas as pd
from datetime import timedelta
df_boat_passengers = pd.read_csv("BoatPassengers.csv", index_col=0)
df_boat_vehicle = pd.read_csv("BoatVehicles.csv", index_col=0)
df_boat_passengers.index = pd.to_datetime(df_boat_passengers.index)
df_boat_vehicle.index = pd.to_datetime(df_boat_vehicle.index)
#df_boat_passengers_bymonth = df_boat_passengers.resample(rule='1M').sum()/30
df_boat_passengers = df_boat_passengers.resample(rule='1w').sum()
df_boat_vehicle = df_boat_vehicle.resample(rule='1w').sum()

from bokeh.plotting import figure, output_file, show
output_file("boatpassengerscrete.html", title="Passengers arriving in Crete by boat")

from bokeh.models import ColumnDataSource, Range1d
source = ColumnDataSource(df_boat_passengers)

p = figure(x_axis_type="datetime", title="Passengers entering Crete and Chania by boat per week", plot_height=800, plot_width=1900)

locations = {'Crete': 'red', 'Chania': 'orange'}#, 'KIS': 'purple'}
for location in locations:
    p.vbar(x='date', top=location, source=source, alpha=0.7, muted_alpha=0.2, width=0.9*timedelta(days=7), color=locations[location], legend_label=location)
#    p.line(x='date', y=location, source=source_bymonth, muted_alpha=0.2, line_color=locations[location], legend_label=location, line_width=2)
p.legend.location = "top_left"
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Passenger Arrivals per week'
p.y_range.start = 0
p.x_range = Range1d(df_boat_passengers.index[0]-timedelta(5), df_boat_passengers.index[-1]+timedelta(5))
p.xaxis.formatter.days = '%d/%m/%Y'
p.legend.click_policy='mute'
p.sizing_mode = "scale_width"

from bokeh.models.tools import HoverTool
hover = HoverTool()
hover.tooltips=[
    ('Date', '@date{%d %b %Y}'),
    ('Chania', '@Chania{0,0}'),
    ('Crete', '@Crete{0,0}'),
]
hover.formatters = { "@date": "datetime"}

p.add_tools(hover)

from bokeh.models import NumeralTickFormatter
p.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

show(p)

from bokeh.embed import components

script, div = components(p)
with open('scriptboatpassengers.txt', 'w') as script_file:
    script_file.write(script)
with open('divboatpassengers.txt', 'w') as div_file:
    div_file.write(div)

output_file("boatvehiclescrete.html", title="Vehicles arriving in Crete by boat")

#from bokeh.models import ColumnDataSource
source = ColumnDataSource(df_boat_vehicle)

p = figure(x_axis_type="datetime", title="Vehicles entering Crete and Chania by boat per week", plot_height=800, plot_width=1900)

locations = {'Crete': 'red', 'Chania': 'orange'}#, 'KIS': 'purple'}
for location in locations:
    p.vbar(x='date', top=location, source=source, alpha=0.7, muted_alpha=0.2, width=0.9*timedelta(days=7), color=locations[location], legend_label=location)#, line_width=2)
#    p.line(x='date', y=location, source=source_bymonth, muted_alpha=0.2, line_color=locations[location], legend_label=location, line_width=2)
p.legend.location = "top_left"
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Vehicle Arrivals per week'
p.y_range.start = 0
p.x_range = Range1d(df_boat_passengers.index[0]-timedelta(5), df_boat_passengers.index[-1]+timedelta(5))
p.xaxis.formatter.days = '%d/%m/%Y'
p.legend.click_policy='mute'
p.sizing_mode = "scale_width"

#from bokeh.models.tools import HoverTool
hover = HoverTool()
hover.tooltips=[
    ('Date', '@date{%d %b %Y}'),
    ('Chania', '@Chania{0,0}'),
    ('Crete', '@Crete{0,0}'),
]
hover.formatters = { "@date": "datetime"}

p.add_tools(hover)

#from bokeh.models import NumeralTickFormatter
p.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

show(p)

#from bokeh.embed import components

script, div = components(p)
with open('scriptboatvehicles.txt', 'w') as script_file:
    script_file.write(script)
with open('divboatvehicles.txt', 'w') as div_file:
    div_file.write(div)
