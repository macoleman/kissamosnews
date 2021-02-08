import requests, pandas as pd

resp = requests.get('https://covid-19-greece.herokuapp.com/confirmed')
txt = resp.json()
df = pd.DataFrame(txt['cases'])
#print(df)

df['daily'] = df['confirmed'].diff(1).convert_dtypes()#.astype(int, errors='ignore')
#df['daily'] = df['daily'].astype(int, errors='ignore')

#print(df['daily'])

population_greece = 10816286 # from Elstat 2011

df['Greece/100000']=df['daily']/population_greece*100000
df.index = df['date']
df.index = pd.to_datetime(df.index)
#print(df.index)
df = df.iloc[-40:, -2:]
print(df.index)

df.to_csv("InfectionsGreece.csv")
