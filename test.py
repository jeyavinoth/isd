import isd.stations as stations
import numpy as np


stationList = stations.getStationList('isd-history.csv');
subList = stations.subsetStationList(stationList,['USAF','WBAN','CTRY','STATE']);
usData = stations.extractData(subList,'CTRY','US');
nyData = stations.extractData(usData,'STATE','NY');

print len(nyData['USAF'])

stations.downloadData('temp',nyData,2004,2004)


# for i, val in enumerate(stationList['USAF']):
  # print i
