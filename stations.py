import numpy as np 
import csv


def getStationList(filename):
    """Reading the inventory file to get the list of stations, for now only supports csv format"""

    #error exception for reading in file 
    try:
        f = open(filename,'r')
    except Exception as e: 
        print(e)
    
    #reading data into a dictionary
    dataIn = csv.DictReader(f,delimiter=",")

    stationList = {}
    cnt = 1
    for row in dataIn:
        for key, value in row: 
            stationList[key][cnt] = value 
            cnt = cnt + 1
    
    return stationList

    
def subsetStationList(stationList,requiredKeys):
    """subset the staionList, extract the necessary keys from the list"""
    subsetDict = {iKey: stationList[iKey] for iKey in requiredKeys if iKey in stationList}
    return subsetDict 
