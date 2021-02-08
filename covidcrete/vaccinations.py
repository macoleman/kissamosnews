import requests, pandas as pd

populations = {'Crete': 621340, 'Chania': 156585, 'Greece': 10816286}

resp = requests.get('https://covid-19-greece.herokuapp.com/vaccinations-per-region-history')
txt = resp.json()
df_vaccinations = pd.DataFrame(txt['vaccinations-history'])

df_vaccinations_total = df_vaccinations.groupby('area_en').get_group('Chania')

df_vaccinations_total.index = pd.to_datetime(df_vaccinations_total['referencedate'])
df_vaccinations_total = df_vaccinations_total['referencedate'].sort_index()

crete = ['Chania', 'Heraklion', 'Lasithi', 'Rethymno']

for region in crete:
    df_vaccinations_region = df_vaccinations.groupby('area_en').get_group(region)
    df_vaccinations_region.index = pd.to_datetime(df_vaccinations_region['referencedate'])
    df_vaccinations_region = df_vaccinations_region.sort_index()

    df_vaccinations_region_result = df_vaccinations_region.rename({'totaldistinctpersons': region}, axis=1)
    df_vaccinations_region_single = df_vaccinations_region_result[region]

    df_vaccinations_total = pd.concat([df_vaccinations_region_single, df_vaccinations_total], axis=1)

del df_vaccinations_total['referencedate']
df_vaccinations_total['Crete'] = df_vaccinations_total.sum(1)
df_vaccinations_total_greece = df_vaccinations.groupby('referencedate')['totaldistinctpersons'].sum(1)
df_vaccinations_total_greece.index = pd.to_datetime(df_vaccinations_total_greece.index)
df_vaccinations_total['Greece'] = df_vaccinations_total_greece

for pop in populations:
    df_vaccinations_total[pop+' %']=df_vaccinations_total[pop]/populations[pop]

df_vaccinations_total.to_csv("data/VaccinationsTotal.csv")
