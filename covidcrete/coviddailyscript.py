import tabula
import pandas as pd
from datetime import date, timedelta
import requests

### Open local data and extract last date
df_all = pd.read_csv("data/InfectionsAll.csv", index_col=0)
last_date_old_data = pd.to_datetime(df_all.index[-1])

### Download latest data and extract most recent date
resp = requests.get('https://covid-19-greece.herokuapp.com/confirmed')
txt = resp.json()
df_greece_today = pd.DataFrame(txt['cases'])
df_greece_today.index = pd.to_datetime(df_greece_today['date'])
last_date_api_data = df_greece_today.at[df_greece_today.index[-1], 'date']

#date_today = date.today().strftime('%Y%m%d')

### Set date ranges and region data
missing_dates_range = pd.date_range(last_date_old_data+timedelta(1), last_date_api_data)
crete = {'Chania': 'ΧΑΝΙΩΝ', 'Heraklion': 'ΗΡΑΚΛΕΙΟΥ', 'Lasithi': 'ΛΑΣΙΘΙΟΥ', 'Rethymno': 'ΡΕΘΥΜΝΟΥ'}
populations = {'Chania': 156585, 'Crete': 621340, 'Greece': 10816286} # from Elstat 2011
dict_infections = {}

### Loop over dates missing from local data
for d in missing_dates_range:
    
    ### Open and read the pdf for each date
    report_date = d.strftime('%Y%m%d')
    urllocal = "DailyReports/covid-gr-daily-report-"+report_date+".pdf"
    table = tabula.read_pdf(urllocal,pages=3)
    df = table[0]
    
    ### Clean header rows in dataframe extracted from pdf
    if len(df) >= 29:
        new_header = df.iloc[-29] #grab the correct row for the header
        df = df[-28:] #take the dataframe less the header rows
    else:
        new_header = df.iloc[0] #grab the first row for the header
        df = df[1:] #take the dataframe less the header row
    df.columns = new_header #set the appropriate row as the df header
    
    ### Clean and join the split in the table resulting from reading the pdf
    df1 = df.iloc[:, :4]
    df2 = df.iloc[:, 4:]
    df3 = df1.append(df2)
    
    ### Give index to dataframe
    new_row_labels = df3.iloc[:, 0] #grab the first col for the index
    df3 = df3.iloc[:, 1:] #take the dataframe less the index column
    df3.index = new_row_labels #set the first col as the df index
    
    ### Loop over regions of Crete
    dict_regions = {}
    for region in crete:
        dict_regions[region] = 0
        ### Assign a number of cases when the number exists in the dataframe
        if crete[region] in df3.index:
            dict_regions[region] = int(df3.at[crete[region], df3.columns[0]])
    
    ### Insert the cases from the regions to the day's values and calculate totals for Crete and Greece
    dict_infections[d] = dict_regions
    dict_infections[d]['Crete'] = sum(dict_infections[d].values())
    dict_infections[d]['Greece'] = df_greece_today.at[d, 'confirmed'] - df_greece_today.at[d+timedelta(-1), 'confirmed']
    
    ### Calculate percentages for the day and insert them
    for pop in populations:
        dict_infections[d][pop+'/100000']=dict_infections[d][pop]/populations[pop]*100000

### Transform final dictionary to dataframe and add it to local csv file
df_all_recent = pd.DataFrame(dict_infections).transpose()
df_all = pd.read_csv("data/InfectionsAll.csv", index_col=0)
df_all = df_all.append(df_all_recent)

df_all.to_csv("data/InfectionsAll.csv")
