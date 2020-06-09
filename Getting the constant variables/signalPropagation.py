#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import csv
import random
from os.path import join

def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data

def getN(rssi, a,d):
    return  ( -1 * (rssi -a)/ (10 * math.log10(d)))

def averageDataset(filename):
    #load dataset
    dataset = loadDataset(filename)
    #extract rssi
    rssi = [int(i[3]) for i in dataset]
    #get average rssi
    avg = sum(rssi) / len (rssi)
    #return average rssi
    return avg

def printCSV(filename, mylist):
    with open(filename, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for item in mylist:
            wr.writerow(item)
            
if __name__ == "__main__":
    
    """
    ==============================
    Geting A
    ======================================
    """
    #load dataset
    #dataset is 1000 measurement of each RSSI of AP at 1 metre distance to android device
    #A is RSSI recorded at 1 meter distance
    a_TP = averageDataset(join("dataset6", "tp-1-1.csv"))
    a_HP = averageDataset(join("dataset6", "hp-1-1.csv"))
    a_DP = averageDataset(join("dataset6", "dp-1-1.csv"))
    
    
    
    """
    ==============================
    Geting n
    ======================================
    """
    #load dataset
    #dataset is 1000 measurement of each RSSI of AP at 2 metre distance to android device
    #n taken by giving RSSI value at 2 meter distance   
    #average the data
    avgTP2 = averageDataset(join("dataset6", "tp-2-2.csv"))
    avgHP2= averageDataset(join("dataset6", "hp-2-1.csv"))
    avgDP2 = averageDataset(join("dataset6", "dp-2-1.csv"))
    
    n_TP = getN(avgTP2, a_TP, 2)
    n_HP = getN(avgHP2, a_HP, 2)
    n_DP = getN(avgDP2, a_DP, 2)
    
    """
    ==============================
    Printing output
    ======================================
    """
    #getting attribut of each dataset
    tp = loadDataset(join("dataset3", "tp-1.csv"))[0]
    hp = loadDataset(join("dataset3", "hp-1.csv"))[0]
    dp = loadDataset(join("dataset3", "dp-1.csv"))[0]
    output = [["SSID", "BSSID", "A", "n"],
              [tp[1], tp[2], a_TP, n_TP],
              [hp[1], hp[2], a_HP, n_HP],
              [dp[1], dp[2], a_DP, n_DP]]
    
    printCSV(join("output", "constant variables"),output)
    
    