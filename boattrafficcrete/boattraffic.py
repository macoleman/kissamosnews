import pandas as pd

ports_crete = ['HER', 'CHQ', 'SUD', 'RET', 'KIS', 'JSH']

df_boat = pd.read_csv("BoatTrafficGovAPI.csv", usecols=['arrivalport', 'departureport', 'date', 'passengercount', 'vehiclecount'], index_col='date', parse_dates=True)

df_passengers = df_boat.groupby(["arrivalport", "date"])["passengercount"].sum()
df_vehicle = df_boat.groupby(["arrivalport", "date"])["vehiclecount"].sum()

dt = df_boat.groupby("date")['arrivalport'].count()
dt=dt.index

df_passengers_crete = pd.DataFrame(index=dt)
df_vehicle_crete = pd.DataFrame(index=dt)

for port in ports_crete:
    df_passengers_crete[port] = df_passengers[port]
    df_vehicle_crete[port] = df_vehicle[port]

df_passengers_crete = df_passengers_crete.fillna(value=0)
df_vehicle_crete = df_vehicle_crete.fillna(value=0)    

df_passengers_crete['Crete'] = df_passengers_crete.sum(1)
df_vehicle_crete['Crete'] = df_vehicle_crete.sum(1)

df_passengers_crete['Chania'] = df_passengers_crete['SUD']+df_passengers_crete['CHQ']
df_vehicle_crete['Chania'] = df_vehicle_crete['SUD']+df_vehicle_crete['CHQ']

df_passengers_crete.to_csv("BoatPassengers.csv")
df_vehicle_crete.to_csv("BoatVehicles.csv")