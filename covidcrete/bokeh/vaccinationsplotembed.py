import pandas as pd

df_vaccinations = pd.read_csv("VaccinationsTotal.csv", index_col=0)
df_vaccinations.index = pd.to_datetime(df_vaccinations.index)

from bokeh.plotting import figure, output_file, show
output_file("vaccinationscrete.html", title="Covid vaccinations in Crete")

from bokeh.models import ColumnDataSource
source = ColumnDataSource(df_vaccinations)

from bokeh.models.tools import HoverTool

p = figure(x_axis_type="datetime", title="People with Covid-19 vaccination in Crete and Chania province", plot_width=640)#, plot_width=1200, plot_height=450)

locations = {'Crete': 'red', 'Chania': 'orange'}#'Greece': 'purple', 

for location in locations:
    p.line(x='referencedate', y=location, source=source, muted_alpha=0.1, line_color=locations[location], legend_label=location, line_width=2)

p.legend.location = "top_left"
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'People with Covid-19 Vaccination'
p.y_range.start = 0
p.x_range.start = df_vaccinations.index[0]
p.xaxis.formatter.days = '%d/%m/%Y'
p.legend.click_policy='mute'
#p.yaxis[0].formatter.use_scientific = False
p.sizing_mode = "scale_width"

hover = HoverTool()
hover.tooltips=[
    ('Date', '@referencedate{%d %b}'),
    ('People vaccinated in Chania', '@Chania{0,0}'),
    ('People vaccinated in Crete', '@Crete{0,0}'),
]
hover.formatters = { "@referencedate": "datetime"}

p.add_tools(hover)

from bokeh.models import NumeralTickFormatter
p.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

show(p)

from bokeh.embed import components

script, div = components(p)
with open('scriptvaccinations.txt', 'w') as script_file:
    script_file.write(script)
with open('divvaccinations.txt', 'w') as div_file:
    div_file.write(div)
