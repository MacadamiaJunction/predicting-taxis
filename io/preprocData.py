import pandas as pd
from pandas import DataFrame, read_csv
import sys
import cPickle as pickle
from datetime import datetime
#def init(location):
location = 'data/trip_data_2.csv' 
df = pd.read_csv(location)
call_x = df.pickup_latitude
call_y = df.pickup_latitude
df['pickup_datetime'] = pd.to_datetime(df.pickup_datetime,'%Y-%m-%d %H:%M:%S')
df['dropoff_datetime'] = pd.to_datetime(df.dropoff_datetime,'%Y-%m-%d %H:%M:%S')

taxiIds = {}
i= 0
for tx in df.medallion.unique():
    taxiIds[tx] = i
    i = i+1
srtPkupData = np.zeros((len(df),5))
srtPkupData[:,0] = np.asarray(map(taxiIds.get,df.medallion.as_matrix()[df.pickup_datetime.order().index]))
srtPkupData[:,1] = df.pickup_latitude.as_matrix()[df.pickup_datetime.order().index]
srtPkupData[:,2] = df.pickup_longitude.as_matrix()[df.pickup_datetime.order().index]
srtPkupData[:,3] = [(df.pickup_datetime[i].to_datetime() - datetime(2013,02,1)).total_seconds() for i in df.pickup_datetime.order().index]
srtPkupData[:,4] = 1

srtDrpData = np.zeros((len(df),5))
srtDrpData[:,0] = np.asarray(map(taxiIds.get,df.medallion.as_matrix()[df.dropoff_datetime.order().index]))
srtDrpData[:,1] = df.dropoff_latitude.as_matrix()[df.dropoff_datetime.order().index]
srtDrpData[:,2] = df.dropoff_longitude.as_matrix()[df.dropoff_datetime.order().index]
srtDrpData[:,3] = [(df.dropoff_datetime[i].to_datetime() - datetime(2013,02,1)).total_seconds() for i in df.dropoff_datetime.order().index]
srtDrpData[:,4] = 0

