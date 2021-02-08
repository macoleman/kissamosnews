import pandas as pd
df_dec = pd.read_csv("Dec2020InfectionsCrete.csv", index_col=0)
df_jan = pd.read_csv("Jan2021InfectionsCrete.csv", index_col=0)
#print(df_jan)

population_crete = 621340 # from Covid API
population_chania = 156585 # from Elstat 2011
population_greece = 10816286 # from Elstat 2011

df_infections = df_dec.append(df_jan)
#print(df_infections)
dt = pd.date_range(start='2020-12-18', periods=40, freq='D')
#print(dt)
df_infections.index = dt
#print(df_infections)
df_infections['Crete']=df_infections.sum(1)
df_infections.columns = ['Chania', 'Heraklion', 'Lasithi', 'Rethymno', 'Crete']
df_infections['Chania/100000']=df_infections['Chania']/population_chania*100000
df_infections['Crete/100000']=df_infections['Crete']/population_crete*100000

df_infections.index.name = 'dates'
df_infections.index = pd.to_datetime(df_infections.index)

print(df_infections)

df_infections.to_csv("InfectionsCrete.csv")

df_infections_4d = df_infections.resample(rule='4d').sum()
print(df_infections_4d)
df_infections_rolling_3 = df_infections_4d.rolling(window=3).mean()
print(df_infections_rolling_3)
