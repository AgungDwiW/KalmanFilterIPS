# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:51:14 2020

@author: Project-C
"""

import math
import csv
import random
from os.path import join
import matplotlib.pyplot as plt
import json
import pandas as pd


def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data

def getDistance(rssi, a, n):
    return pow(10, -1*((rssi-a)/(10*n)))

def doDist(filename ,a , n, BSSID):
    data = loadDataset(filename)
    
    #extract rssi
    rssi  = []
    for item in data:
        count = 0
        for atom in item:
            if atom == BSSID:
                rssi.append(int(item[count+1]))
            count+=1
        
    dist = []
    for item in rssi:
        dist.append(getDistance(item,a,n))
    return dist

def doAcc(dataset, trueDist):
    acc = []
    for item in dataset:
        acc.append(abs(item - trueDist))
    return acc

def getStatistic(acc):
    dictElement = {}
    for item in acc:
        if item not in dictElement:
            dictElement[item] = 1
        else:
            dictElement[item] += 1
    avg = sum(acc) / len(acc)
    return dictElement, avg

def createGraph(dataset, filename, label):
    x = [ round(i,2) for i in dataset.keys()]
    plt.bar(x, dataset.values())
    plt.xlabel("Error (m)")
    plt.ylabel("Error count")
    plt.title(label)
    plt.savefig(filename)
    plt.show()

def printToCSV(dataset, filename):
    out = [["measurement", "measurement count"]]
    for item in dataset.keys():
        out.append([item, dataset[item]])
    mylist = out
    filename+=".csv"
    
    with open(filename, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for item in mylist:
            wr.writerow(item)

if __name__ == "__main__":
    dataset = "dataset13"
    
    """
    ==================================
    loading constant variables
    ==================================
    """
    constant =loadDataset(join("output", "constant variables.csv"))
    bssid_ap1 = constant[1][1]
    a_ap1 = float(constant[1][2])
    n_ap1 = float(constant[1][3])
    
    bssid_ap2 = constant[2][1]
    a_ap2 = float(constant[2][2])
    n_ap2 = float(constant[2][3])
    
    bssid_ap3 = constant[3][1]
    a_ap3 = float(constant[3][2])
    n_ap3 = float(constant[3][3])
    
    
    """
    ==================================
    AP-1 TP-Link
    ==================================
    """
    
    #loading dataset and calculate distance and path loss
    ap1_1_2 = doDist(join(dataset, "ap1-1-2.csv"), a_ap1, n_ap1, bssid_ap1)
    acc_ap1_1_2 = doAcc(ap1_1_2, 1)
    
    ap1_2_2 = doDist(join(dataset, "ap1-2-2.csv"), a_ap1, n_ap1, bssid_ap1)
    acc_ap1_2_2 = doAcc(ap1_2_2, 2)
    
    ap1_3_2 = doDist(join(dataset, "ap1-3-2.csv"), a_ap1, n_ap1, bssid_ap1)
    acc_ap1_3_2 = doAcc(ap1_3_2, 3)
    
    ap1_4_2 = doDist(join(dataset, "ap1-4-2.csv"), a_ap1, n_ap1, bssid_ap1)
    acc_ap1_4_2 = doAcc(ap1_3_2, 4)
    
    #get statistic of path loss
    stat_ap1_1, avg_ap1_1 = getStatistic(acc_ap1_1_2)
    stat_ap1_2, avg_ap1_2 = getStatistic(acc_ap1_2_2)
    stat_ap1_3, avg_ap1_3 = getStatistic(acc_ap1_3_2)
    stat_ap1_4, avg_ap1_4 = getStatistic(acc_ap1_4_2)
    #create graph
    createGraph(stat_ap1_1, join("output", "ap1_1 "), "AP 1, distance 1 meter")
    createGraph(stat_ap1_2, join("output", "ap1_2 "), "AP 1, distance 2 meter")
    createGraph(stat_ap1_3, join("output", "ap1_3 "), "AP 1, distance 3 meter")
    createGraph(stat_ap1_4, join("output", "ap1_4 "), "AP 1, distance 4 meter")
    
    """
    ==================================
    AP-2 HandPhone
    ================================== 
    """
    
    #loading dataset and calculate distance and path loss
    ap2_1_2 = doDist(join(dataset, "tt-1-2.csv"), a_ap2, n_ap2, bssid_ap2)
    acc_ap2_1_2 = doAcc(ap2_1_2, 1)
    
    ap2_2_2 = doDist(join(dataset, "tt-2-2.csv"), a_ap2, n_ap2, bssid_ap2)
    acc_ap2_2_2 = doAcc(ap2_2_2, 2)
    
    ap2_3_2 = doDist(join(dataset, "tt-3-2.csv"), a_ap2, n_ap2, bssid_ap2)
    acc_ap2_3_2 = doAcc(ap2_3_2, 3)
    
    ap2_4_2 = doDist(join(dataset, "tt-4-2.csv"), a_ap2, n_ap2, bssid_ap2)
    acc_ap2_4_2 = doAcc(ap2_4_2, 4)
    
    #get statistic of path loss
    stat_ap2_1, avg_ap2_1 = getStatistic(acc_ap2_1_2)
    stat_ap2_2, avg_ap2_2 = getStatistic(acc_ap2_2_2)
    stat_ap2_3, avg_ap2_3 = getStatistic(acc_ap2_3_2)
    stat_ap2_4, avg_ap2_4 = getStatistic(acc_ap2_4_2)
    
    #create graph
    createGraph(stat_ap2_1, join("output", "tt_1 "), "AP 2, distance 1 meter")
    createGraph(stat_ap2_2, join("output", "tt_2 "), "AP 2, distance 2 meter")
    createGraph(stat_ap2_3, join("output", "tt_3 "), "AP 2, distance 3 meter")
    createGraph(stat_ap2_4, join("output", "tt_3 "), "AP 2, distance 4 meter")
    
    """
    ==================================
    AP-3 DP-Link
    ==================================
    """
    #loading dataset and calculate distance and path loss
    ap3_1_2 = doDist(join(dataset, "dp-1-2.csv"), a_ap3, n_ap3, bssid_ap3)
    acc_ap3_1_2 = doAcc(ap3_1_2, 1)
    
    ap3_2_2 = doDist(join(dataset, "dp-2-2.csv"), a_ap3, n_ap3, bssid_ap3)
    acc_ap3_2_2 = doAcc(ap3_2_2, 2)
    
    
    ap3_3_2 = doDist(join(dataset, "dp-3-2.csv"), a_ap3, n_ap3, bssid_ap3)
    acc_ap3_3_2 = doAcc(ap3_3_2, 3)
    
    ap3_4_2 = doDist(join(dataset, "dp-4-2.csv"), a_ap3, n_ap3, bssid_ap3)
    acc_ap3_4_2 = doAcc(ap3_4_2, 3)
    
    #get statistic of path loss
    stat_ap3_1, avg_ap3_1 = getStatistic(acc_ap3_1_2)
    stat_ap3_2, avg_ap3_2 = getStatistic(acc_ap3_2_2)
    stat_ap3_3, avg_ap3_3 = getStatistic(acc_ap3_3_2)
    stat_ap3_4, avg_ap3_4 = getStatistic(acc_ap3_4_2)
    
    #create graph
    createGraph(stat_ap3_1, join("output", "ap3_1 "), "AP 3, distance 1 meter")
    createGraph(stat_ap3_2, join("output", "ap3_2 "), "AP 3, distance 2 meter")
    createGraph(stat_ap3_3, join("output", "ap3_3 "), "AP 3, distance 3 meter")
    createGraph(stat_ap3_4, join("output", "ap3_3 "), "AP 3, distance 4 meter")
    
    """
    Analysing
    """
    
    stat_ap1_1["avg"] = avg_ap1_1
    stat_ap1_2["avg"] = avg_ap1_2
    stat_ap1_3["avg"] = avg_ap1_3
    stat_ap1_4["avg"] = avg_ap1_4
    
    stat_ap2_1["avg"] = avg_ap2_1
    stat_ap2_2["avg"] = avg_ap2_2
    stat_ap2_3["avg"] = avg_ap2_3
    stat_ap2_4["avg"] = avg_ap2_4
    
    stat_ap3_1["avg"] = avg_ap3_1
    stat_ap3_2["avg"] = avg_ap3_2
    stat_ap3_3["avg"] = avg_ap3_3
    stat_ap3_4["avg"] = avg_ap3_4
    
    col = ["ap1", "ap2", "ap3"]
    
    data = [[ stat_ap1_1['avg'],  stat_ap2_1['avg'], stat_ap3_1['avg'],],
            [ stat_ap1_2['avg'],  stat_ap2_2['avg'], stat_ap3_2['avg'],],
            [ stat_ap1_3['avg'],  stat_ap2_3['avg'], stat_ap3_3['avg'],],
            [ stat_ap1_4['avg'],  stat_ap2_4['avg'], stat_ap3_4['avg'],],
        ]
    
    dataf = pd.DataFrame(columns = col, data = data)

    
    """
    printing output
    """
    
   
    
    printToCSV(stat_ap1_1, join("output", "stat_ap1_1"))
    printToCSV(stat_ap1_2, join("output", "stat_ap1_2"))
    printToCSV(stat_ap1_3, join("output", "stat_ap1_3"))
    printToCSV(stat_ap1_4, join("output", "stat_ap1_4"))
    
    printToCSV(stat_ap2_1, join("output", "stat_ap2_1"))
    printToCSV(stat_ap2_2, join("output", "stat_ap2_2"))
    printToCSV(stat_ap2_3, join("output", "stat_ap2_3"))
    printToCSV(stat_ap2_3, join("output", "stat_ap2_3"))
    
    printToCSV(stat_ap3_1, join("output", "stat_ap3_1"))
    printToCSV(stat_ap3_2, join("output", "stat_ap3_2"))
    printToCSV(stat_ap3_3, join("output", "stat_ap3_3"))