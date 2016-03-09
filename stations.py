import numpy as np 
import csv
import os
from ftplib import FTP

def getStationList(filename):
  """Reading the inventory file to get the list of stations, for now only supports csv format
      Called in using getStationList("isd-history.csv")
      Returns a dicitionary of stations
  """

  #reading data into a dictionary

  f = open(filename,"r")
  dataIn = csv.DictReader(f,delimiter=",",quotechar='"')
  stationList = {}
  for row in dataIn:
    for iKey in row.keys():
      stationList.setdefault(iKey,[]).append(row[iKey]) 
  return stationList

  
def subsetStationList(stationList,requiredKeys):
  """subset the staionList, extract the necessary keys from the list
      Called using susbsetStationList(stationList, requiredKeys)
      Returns the dictionary of input with only the selected keys 
  """
  subsetDict = {iKey: stationList[iKey] for iKey in requiredKeys if iKey in stationList}
  return subsetDict 

def extractData(stationList,key,keyValue):
  """extracting a subset of station list for a requested value
      Called using extractData(stationList,key,keyvalue)
      Returns a new list with only the values that match te keyvalue entered for the specified key
  """

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
  """downloading the data into a given folder for a range of years
      Called using downloadData(out_folder,stationList,sYear,eYear)
      for now the downloaded data has to be manually gunzippped
      Returns nothing
  """

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

      # output file path
      outFile = yyFolder + '/' + filename

      # ftp download file
      ftpLink = "{0}{1}/{2}".format(ftpFolder,yy,filename)
  
      # opening the file to write the output to 
      f = open(outFile,'wb')
      try:
        # read from ftp and write to local file 
        ftp.retrbinary('RETR %s' % ftpLink,f.write)

        # closing the local file 
        f.close()
      except Exception as e: 
        print("Cannot find {0}".format(ftpLink))
        f.close()
        os.remove(outFile)
  
  # quitting ftp connnection
  ftp.quit()

def gunzipfile(filename):
  """have to write this funciton to unzip the downloaded files"""
  outfile = filename[:len(filename)-3]
  print outfile

def readDataByState(ctry,state,sYear,eYear,folder):
  """Reading in data given by state
      Called using readDataByState(country,state,starting_year,ending_year,data_folder)
  """
  # (Todo): Not completed the read in of all data by state
  # adjusting ending year to be able to be used in range 
  eYear = eYear + 1 

  # gettin the stationList from isd-hsitory.csv file 
  stationList=getStationList("isd-history.csv") 
  ctryList=extractData(stationList,'CTRY','US')
  stateList=extractData(ctryList,'STATE','NY')

  print("Number of stations from ISD list: {0}".format(len(stateList['USAF'])))

  # empty dictionary with data
  data = {}

  # loop through the years
  for yy in range(sYear,eYear):
    # for each file in the stateList 
    cnt = 0; 
    for ind, usaf_val in enumerate(stateList['USAF']):
      wban_val = stateList['WBAN'][ind]
      filename = "{0}/{1}/{2}-{3}-{1}".format(folder,yy,usaf_val,wban_val)
      if (os.path.exists(filename)):
        fileData = readFile(filename)
        cnt = cnt + 1 

  print("Read in {0} for year {1}".format(str(cnt).zfill(3),yy))
      
def readFile(filename):
  """Reading in data for a single file 
      Called using readFile('<file-name>')
      returns an array of dictionary for the read records
  """
  maxRecordSize = 2844;
  maxBlockLength = 8192;


  fid = open(filename,"r")
  lines = fid.read().splitlines()
  
  recordCnt = 0
  records = [] 

  # for every line in the file
  for line in lines: 

    #empty dictionary
    temp = {}

    # reading in the control data section
    controlData = line[:60]

    # extracting control data
    numVarChar = int(line[:4])
    temp['usaf'] = int(line[4:10]) #5-10
    temp['wban'] = int(line[10:15]) #11-15
    temp['date'] = int(line[15:23]) #16-23
    temp['time'] = int(line[23:27]) #24-27
    temp['source_flag'] = line[27:28] #24-27
    temp['lat'] = float(line[28:34])/1000
    temp['lon'] = float(line[34:41])/1000 
    temp['type_code'] = line[41:46] 
    temp['elev'] = int(line[46:51]) 
    temp['call_letter'] = line[51:56] 
    temp['qc_process'] = int(line[57:60]) 

    # reading in the mandatory data section
    mandotaryData = line[60:105] 
    temp['wo_angel'] = int(line[60:63])
    temp['wo_direction_qc'] = int(line[63:64])
    temp['wo_type_code'] = line[64:65]
    temp['wo_speed_rate'] = int(line[65:69])
    temp['wo_speed_qc'] = int(line[69:70])

    temp['so_ceiling_height_dim'] = int(line[70:75])
    temp['so_ceiling_qc'] = int(line[75:76])
    temp['so_ceiling_determination_code'] = line[76:77]
    temp['so_cavok_code'] = line[77:78]

    temp['vo_distance_dim'] = int(line[78:84])
    temp['vo_distance_qc'] = int(line[84:85])
    temp['vo_variability_code'] = line[85:86]
    temp['vo_quality_variability_code'] = int(line[86:87])
    
    temp['ato_air_temp'] = float(line[87:92])/10
    temp['ato_temp_qc'] = line[92:93]
    temp['ato_dew_temp'] = float(line[93:98])/10
    temp['ato_dew_qc'] = line[98:99]

    temp['apo_sealevel_pres'] = float(line[99:104])/10
    temp['ato_sealevel_pres_qc'] = int(line[104:105])

    # additional data section
    if (numVarChar != 0):
      sectionDef = line[105:108]
      variableData = line[108:105+numVarChar]

      print ("<-->Start: {0}".format(variableData))
      # looping through variableData to read in all sections
      sectionCharCnt = -1
      tempCnt = numVarChar 
      while (sectionCharCnt != 0):
        # reading in section by section
        sectionCharCnt, sectionData  = extractVariableData(variableData)

        # updating the temp dictionary to include the section data
        temp.update(sectionData)
       
        # removing the read section from variableData
        variableData = variableData[sectionCharCnt:]

    records.append(temp)
    # print line
    # print temp
    # break;
    recordCnt = recordCnt + 1

  print ("Number of records read: {0}".format(len(records)))

  fid.close()
  return records

def extractVariableData(vData):
  """extract the variable data depending on the identifier"""
  # LIQUID-PRECIPITATION occurrence identifier : AA1-AA4
  # LIQUID-PRECIPITATION MONTHLY TOTAL identifier : AB1
  # PRECIPITATION-OBSERVATION-HISTORY identifier : AC1
  
  sectionID = vData[:3]

  sDict = {}
  cnt = 0
  
  # precipitation
  if (sectionID[:2] == 'AA'):
    sDict[sectionID] = vData[:15] 
    cnt = 15
  elif (sectionID[:2] == 'GD'):
    sectionSize = 15
    # sDict[sectionID] = vData[:15] 
    while sectionID[:2] == 'GD':
      sDict.setdefault(sectionID[:2],[]).append(vData[:sectionSize])
      vData = vData[sectionSize:]
      sectionID = vData[:3]
      cnt = cnt + sectionSize
    print(sDict)
  elif (sectionID[:2] == 'GF'):
    sectionSize = 26
    while sectionID[:2] == 'GF':
      sDict.setdefault(sectionID[:2],[]).append(vData[:sectionSize])
      vData = vData[sectionSize:]
      sectionID = vData[:3]
      cnt = cnt + sectionSize
    print(sDict)
  elif (sectionID[:2] == 'MA'):
    sectionSize = 15 
    while sectionID[:2] == 'MA':
      sDict.setdefault(sectionID[:2],[]).append(vData[:sectionSize])
      vData = vData[sectionSize:]
      sectionID = vData[:3]
      cnt = cnt + sectionSize
    print(sDict)
  elif (sectionID[:2] == 'MW'):
    sectionSize = 6 
    while sectionID[:2] == 'MW':
      sDict.setdefault(sectionID[:2],[]).append(vData[:sectionSize])
      vData = vData[sectionSize:]
      sectionID = vData[:3]
      cnt = cnt + sectionSize
    print(sDict)
  # remarks section
  elif (sectionID == 'REM'):
    sectionSize = 9 + int(vData[6:9])
    sDict.setdefault(sectionID[:2],[]).append(vData[:sectionSize])
    vData = vData[sectionSize:]
    sectionID = vData[:3]
    cnt = cnt + sectionSize
    print(sDict)
  # element quality data section
  elif (sectionID == 'EQD'):
    sectionSize = 16
    vData = vData[3:]
    print(vData)
    sectionID = vData[0] 
    while (sectionID in ['Q', 'P', 'R', 'C', 'D']):
      sDict.setdefault('EQD',[]).append("EQD{0}".format(vData[:sectionSize]))
      vData = vData[sectionSize:]
      if (len(vData) == 0): 
          break; 
      sectionID = vData[0]
      cnt = cnt + sectionSize
    print(sDict)
  else:
    print (sectionID)
    cnt = 0
    tempOut = {}
  
  # print(sDict)

  return (cnt , sDict)


def convertToMat(records):
  """convert input records to matlab files"""

  arr = np.zeros((len(records),), dtype=np.object)
  cnt = 0 
  for record in records:
    arr[cnt] = record
    cnt = cnt + 1
  
  return arr
    
