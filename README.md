
Created by Jeyavinoth Jeyaratnam
@ The City College of New York 

Python module that downloads ISD data given a state and country.

Data downloaded from: ftp://ftp.ncdc.noaa.gov/pub/data/noaa/

It can suppot other search criteria on ISD keywords, but has not been tested. 

To download the data, you have to  run the following 

Read in the station data from isd-history.csv file. Manually donwload this file
from the ftp and call the python function. 

  stationList = stations.getStationList('isd-history.csv');

You can get a sublist of information for all the stations listed in isd-history.csv

  subList = stations.subsetStationList(stationList,['USAF','WBAN','CTRY','STATE']);

The above extracts the columns of data for USAF, WBAN, CTRY & STATE

To extract only the US information from the above mentioned subset call the following 
  usData = stations.extractData(subList,'CTRY','US');

To extract only the NY information from the above mentioned Country Subset call the following 
  nyData = stations.extractData(usData,'STATE','NY');

The above code can be run on any keyword from isd-history, thus creating a subset of a
list of data, that you can use to read in 


After extracting the subset of data you want to read in, you can download the data for those stations
if available on ftp for the years requested.

  stations.downloadData('temp',nyData,2004,2004)

the data will be downloaded to the folder specified (in the example it will downloaded to './temp')

To read the data from a given file, you can use the readFile function, it returns
a list of dictionary for the available number of records

  stations.readFile('temp/2004/722098-99999-2004')


Currently working on: 

Still have to work on reading all the data for the years for a given state
  stations.readDataByState('US','NY',2004,2004,'temp')

Writing the data out to MAT file

