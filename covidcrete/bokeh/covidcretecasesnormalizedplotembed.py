import pandas as pd
from datetime import timedelta

df_infections = pd.read_csv("InfectionsAll.csv", index_col=0)
df_infections.index = pd.to_datetime(df_infections.index, format='%Y-%m-%d')

df_infections.index.name = 'dates'

df_infections_rolling_5 = df_infections.rolling(window=5).mean()

from bokeh.plotting import figure, output_file, show
output_file("bokeh/covidcasescretenormalized.html", title="Covid infections in Crete")

from bokeh.models import ColumnDataSource
source = ColumnDataSource(df_infections_rolling_5)

p = figure(x_axis_type="datetime", title="Covid-19 confirmed cases in Crete per 100,000 people - 5 day moving average", plot_width=640)#, plot_width=1200, plot_height=450)

locations = {'Crete': ['red', 8], 'Chania': ['orange', 6], 'Greece': ['purple', 4]}

for location in locations:
    p.line(x='dates', y=location+'/100000', source=source, muted_alpha=0.1, line_color=locations[location][0], line_dash="4 4", legend_label=location)
    p.circle(x='dates', y=location+'/100000', source=source, muted_alpha=0.1, fill_color=locations[location][0], size=locations[location][1], legend_label=location)

p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Normalized Confirmed Cases'
p.y_range.start = 0
p.x_range.start = df_infections.index[0]+timedelta(3)
p.xaxis.formatter.days = '%d/%m/%Y'
p.legend.click_policy='mute'
p.sizing_mode = "scale_width"
p.legend.location = "center_left"

from bokeh.models.tools import HoverTool
hover = HoverTool()
hover.tooltips=[
    ('Date', '@dates{%d %b %Y}'),
    ('Chania', '@{Chania/100000}{0.00}'),
    ('Crete', '@{Crete/100000}{0.00}'),
    ('Greece', '@{Greece/100000}{0.00}'),
]
hover.formatters = { "@dates": "datetime"}
p.add_tools(hover)


show(p)

from bokeh.embed import components

script, div = components(p)
with open('bokeh/scriptcases-'+str(df_infections.index[-1])+'.txt', 'w') as script_file:
    script_file.write(script)
with open('bokeh/divcases-'+str(df_infections.index[-1])+'.txt', 'w') as div_file:
    div_file.write(div)
