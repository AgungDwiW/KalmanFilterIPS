# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:27:05 2020

@author: Project-C
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:28:20 2020

@author: temperantia
"""



import math
import csv
import random

def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data

def getN(rssi, a,d):
    return -1* ((rssi -a)/ (10 * math.log10(d)))


def testRSSI (rssi, n, a):
    return pow(10, -1*((rssi+a)/(10*n)))


def test2():
    return  pow(10,( 27.55 - (20 * math.log10(2412) + abs(-57000)) / 20.0))

def avg (nums):
    return sum(nums)/len(nums)

def getDist (dataset):
    datasetDist = [[]for i in range(5)]
    datasetDistAvg = []
    distDic = {"1" : 0, "1.5" :1, "2": 2, "2.5" : 3, "3": 4}
    for item in dataset:
        datasetDist[distDic[item[0]]].append(int(item[3]))
    for item in datasetDist:
        datasetDistAvg.append(avg(item))
    return datasetDistAvg, datasetDist

def getNDataset(dataset):
    #input avg dataset
    listDist = [1,1.5,2,2.5,3]
    n = []
    for i in range(1,len(dataset)):
        n.append(getN(dataset[i], dataset[0],  listDist[i]))
    return n


def printCSV(filename, lists):
    leng = len(lists)
    with open(filename, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        counter = 0
        for item in lists:
            print(str(counter) + " / " + str(leng))
            counter+=1
            spamwriter.writerow(item)
        
if __name__ == "__main__":
    
    """
    ==============================
    Geting A
    ======================================
    """
    #load dataset
    #dataset is 100 measurement of RSSI to AP at 1 metre distance
    datasetDP = loadDataset("dataset2/dp.csv")
    dpDistAvg, dpDist = getDist(datasetDP)
    nDP = getNDataset(dpDistAvg)
    nDPAvg = avg(nDP)
    
    datasetTP = loadDataset("dataset2/tp.csv")
    tpDistAvg, tpDist = getDist(datasetTP)
    nTP = getNDataset(tpDistAvg)
    nTPAvg = avg(nTP)
    
    datasetHP = loadDataset("dataset2/hp.csv")
    hpDistAvg, hpDist = getDist(datasetHP)
    nHP = getNDataset(hpDistAvg)
    nHPAvg = avg(nHP[1:])
    
    csvOutput = [["SSID", "BSSID", "A", "N"],
                 [datasetHP[0][1], datasetHP[0][2], hpDistAvg[0], nHPAvg],
                 [datasetDP[0][1], datasetDP[0][2], dpDistAvg[0], nDPAvg],
                 [datasetTP[0][1], datasetTP[0][2], tpDistAvg[0], nTPAvg]]
    
    printCSV("constant.csv", csvOutput)
    
    
    
    
    