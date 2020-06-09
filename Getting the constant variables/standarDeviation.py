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


if __name__ == "__main__":
    """
    ==================================
    loading constant variables
    ==================================
    """
    constant =loadDataset(join("output", "constant variables"))
    a_tp = float(constant[1][2])
    n_tp = float(constant[1][3])
    x_tp = 475
    y_tp = 460
    bssid_tp = constant[1][1]
    
    
    a_hp = float(constant[2][2])
    n_hp = float(constant[2][3])
    x_hp = 320
    y_hp = 0
    bssid_hp = constant[2][1]
    
    a_dp = float(constant[3][2])
    n_dp = float(constant[3][3])
    x_dp = 0
    y_dp = 460
    bssid_dp = constant[3][1]
    
    """
    ==================================
    loading dataset
    ==================================
    """
    dataset = loadDataset(join("dataset6", "sd.csv"))
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
        x.append(xN)
        y.append(yN)
        
    
    
    #removing noise
    y = y[6:]
    
    y_std_meas = statistics.stdev(y)
    x_std_meas = statistics.stdev(x)