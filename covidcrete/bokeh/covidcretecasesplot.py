import pandas as pd
from datetime import timedelta
df_infections = pd.read_csv("data/InfectionsAll.csv", index_col=0)
df_infections.index = pd.to_datetime(df_infections.index)
df_infections.index.name = 'dates'

from bokeh.plotting import figure, output_file, show
output_file("bokeh/covidcasescrete.html", title="Covid-19 confirmed cases in Crete")

from bokeh.models import ColumnDataSource
source = ColumnDataSource(df_infections)

p = figure(x_axis_type="datetime", title="Covid-19 confirmed cases in Crete and Chania Province", plot_width=640, plot_height=360)

p.line(x='dates', y='Crete', source=source, line_color="red", muted_alpha=0.2, line_dash="1 8", legend_label="Crete")
p.circle(x='dates', y='Crete', source=source, fill_color="red", muted_alpha=0.2, size=8, legend_label="Crete")
p.line(x='dates', y='Chania', source=source, line_color="orange", muted_alpha=0.2, line_dash="1 8", legend_label="Chania Province")
p.circle(x='dates', y='Chania', source=source, fill_color="orange", muted_alpha=0.2, size=4, legend_label="Chania Province")

p.legend.location = "top_left"
p.y_range.start = 0
p.x_range.start = df_infections.index[0]-timedelta(1)
p.xaxis.formatter.days = '%d/%m/%Y'
p.legend.click_policy='mute'

from bokeh.models.tools import HoverTool
hover = HoverTool()
hover.tooltips=[
    ('Date', '@dates{%d %b %Y}'),
    ('Chania', '@Chania{0,0}'),
    ('Crete', '@Crete{0,0}'),
]
hover.formatters = { "@dates": "datetime"}
p.add_tools(hover)

show(p)
