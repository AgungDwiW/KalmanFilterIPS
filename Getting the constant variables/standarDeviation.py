# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 00:56:39 2020

@author: Project-C
"""


import math
import csv
import random
from os.path import join
import matplotlib.pyplot as plt
import statistics 

def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data


def getDistance(rssi, a, n):
    return pow(10, -1*((rssi-a)/(10*n)))


def getStatistic(acc):
    dictElement = {}
    for item in acc:
        if item not in dictElement:
            dictElement[item] = 1
        else:
            dictElement[item] += 1
    return dictElement

def trilateration(r1,r2,r3, x1,x2,x3, y1,y2,y3):
    A = 2*x2 - 2*x1;
    B = 2*y2 - 2*y1;
    C = r1*r1 - r2*r2 - x1*x1 + x2*x2 - y1*y1 + y2*y2;
    D = 2*x3 - 2*x2;
    E = 2*y3 - 2*y2;
    F = r2*r2 - r3*r3 - x2*x2 + x3*x3 - y2*y2 + y3*y3;
    x = (C*E - F*B) / (E*A - B*D);
    y = (C*D - A*F) / (B*D - A*E);
    return x,y

def trilat2 (d1,d2,d3, x1,x2,x3, y1,y2,y3):
    x = (d1 **2 - d2 **2 + x2 **2)/ 2 * x2
    y = d1**2 - d3 **2 + x3 **2 + y3 **2 
    y -= x3 * (d1 **2 - d2 **2 + x2 **2 ) / x2
    y /= 2 *y3
    return x,y

def createGraph(dataset, filename, label):
    x = [ round(i,2) for i in dataset.keys()]
    plt.bar(x, dataset.values())
    plt.xlabel("Coordinate")
    plt.ylabel("Estimation count")
    plt.title(label)
    plt.savefig(filename)
    plt.show()


def printCSV(filename, mylist):
    with open(filename, 'w', newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for item in mylist:
            wr.writerow(item)

if __name__ == "__main__":
    """
    ==================================
    loading constant variables
    ==================================
    """
    constant =loadDataset(join("output", "constant variables.csv"))
    a_tp = float(constant[1][2])
    n_tp = float(constant[1][3])
    x_tp = 600
    y_tp = 0
    bssid_tp = constant[1][1]
    
    
    a_hp = float(constant[2][2])
    n_hp = float(constant[2][3])
    x_hp = 300
    y_hp = 400
    bssid_hp = constant[2][1]
    
    a_dp = float(constant[3][2])
    n_dp = float(constant[3][3])
    x_dp = 0
    y_dp = 0
    bssid_dp = constant[3][1]
    
    """
    ==================================
    loading dataset
    ==================================
    """
    dataset = loadDataset(join("dataset15", "sd_at_18-06-20-1300(1).csv"))
    
    
    x = []
    y = []
    dist_tp=[]
    dist_hp=[]
    dist_dp=[]
    
    for item in dataset:
        rssi_tp = 0
        rssi_hp = 0
        rssi_dp = 0
        cur = 0
        for atom in item:
            if (atom == bssid_tp):
               rssi_tp = int(item[cur+1])
            elif (atom == bssid_hp):
               rssi_hp = int(item[cur+1] )
            elif (atom == bssid_dp):
               rssi_dp = int(item[cur+1] )
            cur+=1
            
        r_tp = getDistance(rssi_tp, a_tp, n_tp) *100
        r_hp = getDistance(rssi_hp, a_hp, n_hp) *100
        r_dp = getDistance(rssi_dp, a_dp, n_dp) *100
        
        dist_tp.append(r_tp)
        dist_hp.append(r_hp)
        dist_dp.append(r_dp)
        
        xN,yN = trilateration(r_tp, r_hp, r_dp, x_tp, x_hp, x_dp, y_tp, y_hp, y_dp)
        #xN,yN = trilat2 (r_dp, r_tp, r_hp, x_dp, x_tp, x_hp, y_dp, y_tp, y_hp)
        x.append(xN)
        y.append(yN)
        
    
    
    #removing noise
    
    
    stat_x = getStatistic(x)
    stat_y = getStatistic(y)
    createGraph(stat_x, join("output", "SD-x"), "Standard Deviation - x")
    createGraph(stat_y, join("output", "SD-y"), "Standard Deviation - y")
    y_std_meas = statistics.stdev(y)
    x_std_meas = statistics.stdev(x)
    
    output = [["axis", "standard deviation"],
              ["x", x_std_meas],
              ["y", y_std_meas]]
    
    printCSV(join("output", "std_meas.csv"), output)