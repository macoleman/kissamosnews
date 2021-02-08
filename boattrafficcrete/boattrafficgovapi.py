import requests
import pandas as pd
url = 'https://data.gov.gr/api/v1/query/sailing_traffic?date_from=2019-01-01&date_to=2021-02-01'
headers = {'Authorization':'Token 6887b45be3a89930b7bd277edc5cd1bec97a42ef '}
response = requests.get(url, headers=headers)
df = pd.DataFrame(response.json())
df.to_csv("BoatTrafficGovAPI.csv")

print(df.tail())