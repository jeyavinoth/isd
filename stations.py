import numpy as np 
import csv
import os
from ftplib import FTP

def getStationList(filename):
  """Reading the inventory file to get the list of stations, for now only supports csv format"""

  #reading data into a dictionary

  f = open(filename,"r")
  dataIn = csv.DictReader(f,delimiter=",",quotechar='"')
  stationList = {}
  for row in dataIn:
    for iKey in row.keys():
      stationList.setdefault(iKey,[]).append(row[iKey])

  return stationList

  
def subsetStationList(stationList,requiredKeys):
  """subset the staionList, extract the necessary keys from the list"""
  subsetDict = {iKey: stationList[iKey] for iKey in requiredKeys if iKey in stationList}
  return subsetDict 

def extractData(stationList,key,keyValue):
  """extracting a subset of station list for a requested value"""

  # enumerating the list for the key and selecitng the values that match the requested value
  ind = [i for i, val in enumerate(stationList[key]) if val==keyValue]

  # crate empty output dict
  outData = {}

  # loop through the indexes 
  for i in ind:
    # loop through the key values 
    for iKey in stationList.keys():
      # appending to output dict
      outData.setdefault(iKey,[]).append(stationList[iKey][i])

  return outData

def downloadData(outFolder,stationList,sYear,eYear):
  """downloading the data into a given folder for a range of years"""

  # ftp folder
  ftpSite = 'ftp.ncdc.noaa.gov'; 
  ftpFolder = 'pub/data/noaa/'; 
 
  # opening up connection
  ftp = FTP(ftpSite)
  ftp.login()

  # creating out folder if it doesnt exist
  eYear = eYear + 1
  if (not os.path.exists(outFolder)):
      os.makedirs(outFolder)

  # error checking syear vs eyear
  if (eYear < sYear):
    raise Exception('downloadData: Start year is less than end year')

  

  # looping through all the years
  for yy in range(sYear,eYear):

    # creatin year folder
    yyFolder = outFolder + '/' + str(yy).zfill(4);
    if (not os.path.exists(yyFolder)):
      os.makedirs(yyFolder)

    # enumerating the given list
    for i, val in enumerate(stationList['USAF']):
      # temp value extracted from list
      wban_val = stationList['WBAN'][i]
      usaf_val = stationList['USAF'][i]
      filename = "{0}-{1}-{2}.gz".format(usaf_val,wban_val,yy)

      outFile = yyFolder + '/' + filename
      ftpLink = "{0}{1}/{2}".format(ftpFolder,yy,filename)

      f = open(outFile,'wb')
      try:
        ftp.retrbinary('RETR %s' % ftpLink,f.write)
        f.close()
      except Exception as e: 
        print("Cannot find {0}".format(ftpLink))
        f.close()
        os.remove(outFile)
 
  ftp.quit()
