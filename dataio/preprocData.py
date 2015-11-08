from datetime import datetime

import numpy as np
import pandas as pd

# def init(location):
location = 'data/trip_data_2.csv'

dtypes = {'medallion': str,
          'pickup_datetime': str,
          'dropoff_datetime': str,
          'passenger_count': int,
          'trip_distance': np.float64,
          'pickup_longitude': np.float64,
          'pickup_latitude':np.float64,
          'dropoff_longitude':np.float64,
          'dropoff_latitude':np.float64}

df = pd.read_csv(location, dtype=dtypes,
                 usecols=dtypes.keys())

df['pickup_datetime'] = pd.to_datetime(df.pickup_datetime, format='%Y-%m-%d %H:%M:%S', errors='coerce')
df['dropoff_datetime'] = pd.to_datetime(df.dropoff_datetime, format='%Y-%m-%d %H:%M:%S', errors='coerce')

taxiIds = {}
i = 0
for tx in df.medallion.unique():
    taxiIds[tx] = i
    i = i + 1

srtPkupData = np.zeros((len(df), 5))
srtPkupData[:, 0] = np.asarray(map(taxiIds.get, df.medallion.as_matrix()[df.pickup_datetime.order().index]))
srtPkupData[:, 1] = df.pickup_latitude.as_matrix()[df.pickup_datetime.order().index]
srtPkupData[:, 2] = df.pickup_longitude.as_matrix()[df.pickup_datetime.order().index]
srtPkupData[:, 3] = [(df.pickup_datetime[i].to_datetime() - datetime(2013, 2, 1)).total_seconds() for i in
                     df.pickup_datetime.order().index]
srtPkupData[:, 4] = 1

srtDrpData = np.zeros((len(df), 5))
srtDrpData[:, 0] = np.asarray(map(taxiIds.get, df.medallion.as_matrix()[df.dropoff_datetime.order().index]))
srtDrpData[:, 1] = df.dropoff_latitude.as_matrix()[df.dropoff_datetime.order().index]
srtDrpData[:, 2] = df.dropoff_longitude.as_matrix()[df.dropoff_datetime.order().index]
srtDrpData[:, 3] = [(df.dropoff_datetime[i].to_datetime() - datetime(2013, 2, 1)).total_seconds() for i in
                    df.dropoff_datetime.order().index]
srtDrpData[:, 4] = 0
