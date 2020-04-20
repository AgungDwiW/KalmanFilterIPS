#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:28:20 2020

@author: temperantia
"""



import math
import csv
import random

def dataPick(data):
    dic = {}
    for item in data:
        if item not in dic.keys():
            dic[item]=0
        else:
            dic[item]+=1
    maxim = 0
    max_key = 0
    for i in dic:
        if dic[i]>maxim:
            max_key = i
    return max_key

def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data

def getN(rssi, a,d):
    return -1* ((rssi +a)/ (10 * math.log10(d)))


def cleanDistanceData(dataset, distanceDict):
    datasetClean = [[] for i in range(len(distanceDict))] 
    datasetAverage = []
    for item in dataset:
        datasetClean[distanceDict[float(item[0])]].append(int(item[3]))
    for item in datasetClean:
        datasetAverage.append(dataPick(item))
    return datasetAverage, datasetClean

def testRSSI (rssi, n, a):
    return pow(10, -1*((rssi+a)/(10*n)))

def test():
    print(round(testRSSI(-58.98, -4.82136367559017, avgRSSI[1]),2))


def test2():
    return  pow(10,( 27.55 - (20 * math.log10(2412) + abs(-57000)) / 20.0))

if __name__ == "__main__":
    
    """
    ==============================
    Geting A
    ======================================
    """
    #load dataset
    #dataset is 100 measurement of RSSI to AP at 1 metre distance
    datasetA = loadDataset("getA.csv")
    
    
    #separate dataset according to its prespective AP
    AP = {"Elfais":0, "Ephemeral blessing" : 1, "TP-LINK_E630" : 2}
    RSSI = [[] for a in range(len(AP))]
    avgRSSI = []
    for item in datasetA:
        RSSI[AP[item[1]]].append(int(item[3]))
        
        
    #get the value of A by averaging the dataset
    for item in RSSI:
        avgRSSI.append(dataPick(item))
    
    """
    ==============================
    Geting n
    ======================================
    """
    #load dataset
    #dataset is 100 measurement of RSSI to AP at 1,1.5,2,2.5 metre distance
    datasetAP1 = loadDataset("dp.csv")
    datasetAP2 = loadDataset("hp.csv")
    datasetAP3 = loadDataset("tp.csv")
    
    #clean dataset 
    distanceDict = {1.5 : 0 ,2 : 1, 2.5 : 2, 3:3}
    distanceList = [1.5, 2, 2.5, 3]
    datasetCAP1, dataAP1 = cleanDistanceData(datasetAP1, distanceDict)
    datasetCAP2, dataAP2 = cleanDistanceData(datasetAP2, distanceDict)
    datasetCAP3, dataAP3 = cleanDistanceData(datasetAP3, distanceDict)
 
    n = []
    count = -1
    for i in range(len(AP.keys())):
        n.append([])
        count+=1
        count_y = 0
        for item in datasetCAP1:
            n[count].append(getN(avgRSSI[count], item, distanceList[count_y]))
            count_y+=1
    n_avg = []
    for item in n:
        n_avg.append(sum(item)/len(item))
  