# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 20:51:11 2020

@author: Project-C
"""

from os.path import join
import csv
import math
import pandas as pd
from KalmanFilter2 import KalmanFilter
import numpy as np
import statistics
import matplotlib.pyplot as plt

def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data

def euclidDist(v1, v2):
    dist = 0
    for item in range(len(v1)):
        dist += (v1[item] - v2[item]) **2
    return math.sqrt(dist)


if __name__ == "__main__":
    data = loadDataset(join("dataset", "all at 16-06-20-15 00.csv"))
    constant =loadDataset(join(join(join("..","Getting constant variables"),"output"), "constant variables.csv"))
    
    a = []
    n = []
    x = []
    y = []
    bssid = []
    for item in constant[1:]:
        bssid.append(item[1])
        a.append(float(item[2]))
        n.append(float(item[3]))
        x.append(float(item[4]))
        y.append(float(item[5]))
    
    trueLocX = {'a' : 100,
                'b' : 300,
                'c' : 500,
                'd' : 500,
                'e' : 300,
                'f' : 100}
    
    trueLocY = {'a' : 100,
                'b' : 100,
                'c' : 100,
                'd' : 300,
                'e' : 300,
                'f' : 300}
    
    trueLoc = [ [100, 100], [300,100],
                [500, 100], [500,300],
                [300, 300], [100,300],]
    
    trueDist = [[] for i in range(len(x))]
    for item in range(len(x)):
        d = []
        for atom in trueLoc:
            trueDist[item].append(euclidDist( [x[item], y[item]] , atom))
    
    label_point = list(trueLocX.keys())
    
    clean = []
    for item in data:
        temp = [[] for i in range(len(bssid) +1)]
        for atom in range(len(item)): 
            temp[0] = item[0]
            for itemB in range(len(bssid)):
                if item[atom] == bssid[itemB]:
                    temp[itemB+1] = int(item[atom+1])
        clean.append(temp)
    
    df = pd.DataFrame(columns = ['label', 'ap1', 'ap2', 'ap3'], data = clean)
    df = df[df['label' ]== 'a']
    sample = df['ap3'].values[:1000]
    KFed = []
    KF = KalmanFilter(R = 0.0001, Q = 10)
    
    for item in sample:
        KFed.append(KF.filter(item))
        
    x = list(range(len(sample)))
    plt.scatter(x, sample, s=5)
    
    plt.plot(x, KFed, color = "red", alpha = 0.4)
    plt.scatter(x, KFed, s=5, color = "red", alpha = 0.4)
    plt.title("Kalman filter RSSI")
    plt.xlabel = "RSSI"

        
    