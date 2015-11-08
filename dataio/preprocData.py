import pickle
from datetime import datetime
import numpy as np
import pandas as pd

# def init(location):
location = 'data/trip_data_2.csv'
out_file = 'data/srtPkupClean.p'

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

srtPkupData = np.zeros((len(df),7))
srtPkupData[:, 0] = np.asarray(map(taxiIds.get, df.medallion.as_matrix()[df.pickup_datetime.order().index]))
srtPkupData[:, 1] = df.pickup_latitude.as_matrix()[df.pickup_datetime.order().index]
srtPkupData[:, 2] = df.pickup_longitude.as_matrix()[df.pickup_datetime.order().index]
srtPkupData[:,3] = (df.pickup_datetime.order().values - np.datetime64('1970-01-01'))/np.timedelta64(1,'s')
srtPkupData[:,4] =  df.dropoff_latitude.as_matrix()[ df.pickup_datetime.order().index] 
srtPkupData[:,5] =  df.dropoff_longitude.as_matrix()[ df.pickup_datetime.order().index] 
srtPkupData[:,6] = (df.pickup_datetime.order().values - np.datetime64('1970-01-01'))/np.timedelta64(1,'s')
srtPkupData = srtPkupData[(srtPkupData[:,6] - srtPkupData[:,3]) > 50,:]
vld_data = np.where((abs(srtPkupData[:,2]+73)<10) * (abs(srtPkupData[:,1]-40)<5) * (abs(srtPkupData[:,4]-40)<5) * (abs(srtPkupData[:,5]+73)<10))
srtPkupData = srtPkupData[vld_data,:]

pickle.dump(srtPkupData,open(out_file,'wb'))
#srtDrpData = np.zeros((len(df),5))
#srtDrpData[:,0] = np.asarray(map(taxiIds.get,df.medallion.as_matrix()[df.dropoff_datetime.order().index]))
#srtDrpData[:,1] = df.dropoff_latitude.as_matrix()[df.dropoff_datetime.order().index]
#srtDrpData[:,2] = df.dropoff_longitude.as_matrix()[df.dropoff_datetime.order().index]
#srtDrpData[:,3] = [(df.dropoff_datetime[i].to_datetime() - datetime(2013,02,1)).total_seconds() for i in df.dropoff_datetime.order().index]
#srtDrpData[:,4] = 0
#
