#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import csv
import random
from os.path import join
import statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data

def getN(rssi, a,d):
    n =( -1 * (rssi -a)/ (10 * math.log10(d)))
    return   float("{:.4f}".format(n))

def averageDataset(filename, BSSID):
    #load dataset
    dataset = loadDataset(filename)
    #extract rssi
    rssi  = []
    for item in dataset:
        count = 0
        for atom in item:
            if atom == BSSID:
                rssi.append(int(item[count+1]))
            count+=1
    #get average rssi
    avg = sum(rssi) / len (rssi)
    #return average rssi
    return avg

def printCSV(filename, mylist):
    with open(filename, 'w', newline="") as myfile:
        wr = csv.writer(myfile)
        for item in mylist:
            wr.writerow(item)


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

def getAcc (filename, Tdist, a, n, bssid):
    dist = doDist(filename, a, n, bssid)
    acc = doAcc(dist, Tdist)
    stat, avg = getStatistic(acc)
    
    return float("{:.4f}".format(avg))
    

if __name__ == "__main__":
    
    bssid = ["c0:25:e9:7a:e6:2f", "14:4d:67:98:2b:64", "18:0f:76:91:f2:72"]
    ap = [1,2,3]
    ssid = ["TP-LINK_E630", "TOTOLINK_N210RE", "D-Link_DIR-612"]
    x_ap = [0, 300, 600 ]
    y_ap = [0, 400, 0]
    """
    name format: datasetxx/apy-z-w.csv
    """
    datasetSerial = ""
    z= [1,2,3,4]
    w_train = 1
    w_test = 2
    
    
    
    """
    ==============================
    Geting A
    ======================================
    """
    a = []
    count = 0
    for item in range(len(bssid)):
        filename = (join("dataset{}".format(datasetSerial),
                         "ap{}-{}-{}.csv".format(ap[count], 1, w_train)))
        a.append(averageDataset(filename, bssid[count]))
        count+=1
    
    """
    ==============================
    Geting n
    
    ....|dist
    ap   
    
    ======================================
    """ 
    
    avg2 = []
    n = []
    count = 0
    countZ = 1
    for count in range(len(ap)):
        n_now = []
        for countZ in range(1, len(z)):
            
            filename = (join("dataset{}".format(datasetSerial),
                             "ap{}-{}-{}.csv".format(ap[count], z[countZ], w_train)))
            avg = averageDataset(filename, bssid[count])
            avg2.append(avg)
            
            n_now.append(getN(avg, a[count], z[countZ]))
        n.append(n_now)

    
    
    """
    ==============================
    testing
    
    ....|dist
    ap   
    
    ======================================
    """
    #ap1
    stat = []
    stat_avg = []
    for ap_now in ap: #itterating each ap
        
        stat_now = []
        stat_now_avg= []
        for zCount in range (len(z)-1): #each n for current ap
            n_now = n[ap_now-1][zCount]
            avg= []
            
            for dCount in range(len(z)): #calculating the accuracy of a and n to data in various distance
                filename = (join("dataset{}".format(datasetSerial),
                             "ap{}-{}-{}.csv".format(ap_now, z[dCount], w_test)))
                avg.append(getAcc(filename, z[dCount], a[ap_now-1], n_now, bssid[ap_now-1]))
                
            avg_avg =float("{:.4f}".format(sum(avg)/len(avg)))
            avg.append(avg_avg)
            stat_now_avg.append(avg_avg)
            stat_now.append(avg)
        stat.append(stat_now)
        stat_avg.append(stat_now_avg)
               
    
    
    """
    ==============================
    Visualizing
    ======================================
    """
    #AP1 ----------------------------------------------------------
    frames = []
    for item in range(len(ap)):
        n_AP = ["%.4f"%i for i in n[item]]
        stat_AP = np.transpose(stat[item])
        dataAP = pd.DataFrame(columns = n_AP, data = stat_AP)
        dataAP['Distance'] = ['1 meter', '2 meter', '3 meter', '4 meter', 'avg']
        frames.append(dataAP)
    
    lines = ["b-", "y-", "r-", "g-"]
    titles = ["AP1", "AP2", "AP3"]
    xlabel = "Distance"
    ylabel = "Loss (m)"
    titleC = 0
    for ap_now in range(len(stat)): #each ap
        lineC = 0
        for n_now in range(len(stat[ap_now])): #each n
            x = list(range(len(stat[ap_now][n_now])))
            plt.plot(x, stat[ap_now][n_now], lines[lineC], label= "n = %.3f" % n[ap_now][n_now])
            plt.legend()
            lineC+=1
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(titles[titleC] + " ( A= {} )".format(a[ap_now]))
        plt.savefig(join( join( "output", "plot"), titles[titleC] + " - signal propagation"))
        plt.show()
        titleC+=1
            
    """
    ==============================
    Selecting best data
    ======================================
    """
    bestN = [0 for i in range(len(ap))]
    cur_ap = 0
    bestLoss = [0 for i in range(len(ap))]
    for each_ap in stat:
        min_loss = np.inf
        cur_n = 0
        for each_n in each_ap:
            if(each_n[-1] < min_loss):
                bestN[cur_ap] = n[cur_ap][cur_n]
                min_loss = each_n[-1]
                bestLoss[cur_ap] = each_n[-1]
            cur_n+=1
        cur_ap+=1
    """
    ==============================
    Printing
    ======================================
    """
    printed = [["SSID", "BSSID", "A", "n", "x", "y"]]
    
    for i in range(len(ap)):
        printed.append([ssid[i], bssid[i], a[i], bestN[i], x_ap[i], y_ap[i]])
        
    printCSV(join ("output", "constant variables.csv"),printed)
    
    count = 1
    for item in frames:
        item.to_csv(join(join("output", "acc AP"), "AP{}.csv".format(count)), 
                    index=False, header  = True)
        count+=1
    
    