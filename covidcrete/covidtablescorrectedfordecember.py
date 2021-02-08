import tabula
import pandas as pd

crete = ['ΧΑΝΙΩΝ', 'ΗΡΑΚΛΕΙΟΥ', 'ΛΑΣΙΘΙΟΥ', 'ΡΕΘΥΜΝΟΥ']
dict_infections = {}
df_index = []
daystart = 18
dayend = 32
for i in range(daystart,dayend):
    df_index.append('202012'+str(i).zfill(2))
df_infections = pd.DataFrame(0, index=df_index, columns=crete)

### Days that didn't work:
### 20210107 - throwing error
### 20210113 - throwing error

for i in range(daystart,dayend):
    urlday = str(i).zfill(2)
    urllocal = "covid-gr-daily-report-202012"+urlday+".pdf"
    table = tabula.read_pdf(urllocal,pages=3)

    df = table[0]
    if len(df) >= 29:
        new_header = df.iloc[-29] #grab the first row for the header
        df = df[-28:] #take the data less the header row
    else:
        new_header = df.iloc[0] #grab the first row for the header
        df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    
    df1 = df.iloc[:, :4]
    df2 = df.iloc[:, 4:]
    df3 = df1.append(df2)
    
    new_row_labels = df3.iloc[:, 0] #grab the first col for the row labels
    df3 = df3.iloc[:, 1:] #take the data less the header column
    df3.index = new_row_labels #set the header column as the df row labels

    for region in crete:
        if region in df3.index:
            df_infections.at['202012'+str(i).zfill(2), region] = df3.at[region, df3.columns[0]]

#df_infections.loc['20210107', :] = [3,2,8,1]
df_infections.to_csv("Dec2020InfectionsCrete.csv")
