# Integrated Surface Database (ISD)

Code to download, search and read in information from the ISD.

Created by Jeyavinoth Jeyaratnam
@ The City College of New York 

## Information

Python module that downloads ISD data given a state and country.

Data can be downloaded from: ftp://ftp.ncdc.noaa.gov/pub/data/noaa/

This code can supports search criteria on ISD keywords. 

## Useful functions

### Reading in the station data

Read in the station data from isd-history.csv file. Manually donwload this file
from the ftp and call the python function. 
```
  stationList = stations.getStationList('isd-history.csv');
```
### Extracting subset's for different stations

You can get a sublist of information for all the stations listed in isd-history.csv
```
  subList = stations.subsetStationList(stationList,['USAF','WBAN','CTRY','STATE']);
```
The above extracts the columns of data for USAF, WBAN, CTRY & STATE

### Extracting the US station data

To extract only the US information from the above mentioned subset call the following 
```
  usData = stations.extractData(subList,'CTRY','US');
```
### Extracting station data by the state

To extract only the NY information from the above mentioned Country Subset call the following 
```
  nyData = stations.extractData(usData,'STATE','NY');
```
### General Searches

The above code can be run on any keyword from isd-history, thus creating a subset of a
list of data, that you can use to read in 

## Downloading data after getting the station information

After extracting the subset of data you want to read in, you can download the data for those stations
if available on ftp for the years requested.
```
  stations.downloadData('temp',nyData,2004,2004)
```
the data will be downloaded to the folder specified (in the example it will downloaded to './temp')

To read the data from a given file, you can use the readFile function, it returns
a list of dictionary for the available number of records
```
  stations.readFile('temp/2004/722098-99999-2004')
```

