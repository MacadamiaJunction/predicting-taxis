#import pandas as pd
#from pandas import DataFrame, read_csv
#import sys
import numpy as np
import cPickle as pickle

# columns in the data are  cabid, pickup_lat, pickup_long, pickup_time (epoch) , drp_lat, drp_long, drp_time
class DataProvider:
  def __init__(self,dataFile):
      self.data = pickle.load(open(dataFile,'r'))

  def getNextPickup(self,taxiId, ctime):
    ctx_dp = np.where(self.data[:,0] == taxiId)[0]
    ctxts_dp = np.where((self.data[:,0] == taxiId) * (self.data[:,3] == ctime))[0]
    assert(len(ctxts_dp) == 1)
    return self.data[ctx_dp[np.argmax(ctx_dp > ctxts_dp[0])],:]
