import pandas as pd
df_vaccinations = pd.read_csv("data/VaccinationsTotal.csv", index_col=0)
df_vaccinations.index = pd.to_datetime(df_vaccinations.index)

from bokeh.plotting import figure, output_file, show
output_file("bokeh/vaccinationscrete.html", title="Covid vaccinations in Crete")

from bokeh.models import ColumnDataSource
source = ColumnDataSource(df_vaccinations)

p = figure(x_axis_type="datetime", title="Percentage of population with Covid-19 vaccinations in Crete", plot_width=640)#, plot_width=1200, plot_height=450)

locations = {'Crete': 'red', 'Chania': 'orange', 'Greece': 'purple'}

for location in locations:
    p.line(x='referencedate', y=location+' %', source=source, muted_alpha=0.1, line_color=locations[location], legend_label=location, line_width=2)

p.legend.location = "top_left"
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Population percentage vaccinated'
p.y_range.start = 0
p.x_range.start = df_vaccinations.index[0]
p.xaxis.formatter.days = '%d/%m/%Y'
p.legend.click_policy='mute'
#p.sizing_mode = "scale_width"

from bokeh.models import NumeralTickFormatter
p.yaxis[0].formatter = NumeralTickFormatter(format="0.00%")

show(p)

from bokeh.embed import components

script, div = components(p)
with open('scriptvaccinationspercentage.txt', 'w') as script_file:
    script_file.write(script)
with open('divvaccinationspercentage.txt', 'w') as div_file:
    div_file.write(div)
