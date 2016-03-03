import isd.stations as stations

stationList = stations.getStationList('isd-history.csv');
subList = stations.subsetStationList(stationList,("WBAN"))

print(stationList.keys())

for row in subList: 
    print(row)

