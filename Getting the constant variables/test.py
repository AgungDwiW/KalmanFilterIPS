# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 16:31:02 2020

@author: Project-C
"""

from os.path import join
import csv
import math
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

def avg(lists):
    return sum(lists) / len(lists)

if __name__ == "__main__":
    data = loadDataset(join("dataset14", "f1000.csv"))
    constant =loadDataset(join("output", "constant variables.csv"))
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
    
    dataset = [[ "label", "rssi ap1", "rssi ap2", "rssi ap3", 
               "dist ap1", "dist ap2", "dist ap3",
               "true coordinate X", "true coordinate y",
               "estimated coordinate X", "estimated coordinate y",
               "acc coord X","acc coord Y",
               
               "true distance ap1","true distance ap2", "true distance ap3",
               "acc distance ap1","acc distance ap2", "acc distance ap3",]
               
               ]
    for item in data:
        temp = [item[0], 0,0,0, 0, 0, 0, trueLocX[item[0]], trueLocY[item[0]], 0, 0 , 0,0,
                math.sqrt((trueLocX[item[0]] - x[0]) **2  + (trueLocY[item[0]] - y[0]) **2),
                math.sqrt((trueLocX[item[0]] - x[1]) **2  + (trueLocY[item[0]] - y[1]) **2),
                math.sqrt((trueLocX[item[0]] - x[2]) **2  + (trueLocY[item[0]] - y[2]) **2),
                0,0,0]
        cur = 0
        for atom in item:
            if atom == bssid[0]:
                temp[1] = int(item[cur+1])
            elif atom == bssid[1]:
                temp[2] = int(item[cur+1])
            elif atom == bssid[2]:
                temp[3] = int(item[cur+1])
            cur+=1
        temp[4] = getDistance(temp[1], a[0], n[0]) * 100
        temp[5] = getDistance(temp[2], a[1], n[1]) * 100
        temp[6] = getDistance(temp[3], a[2], n[2]) * 100
        
        temp[9], temp[10] = trilateration(temp[4], temp[5], temp[6], 
                                         x[0],x[1],x[2],
                                         y[0],y[1],y[2])
        temp[11] = abs(temp[9] - temp[7])
        temp[12] = abs(temp[10] - temp[8])
        temp[16] = abs(temp [13] - temp[4])
        temp[17] = abs(temp [14] - temp[5])
        temp[18] = abs(temp [15] - temp[6])
        dataset.append(temp)
    
    dataframe = pd.DataFrame(data = dataset[1:], columns = dataset[0])
    
    acc_ap1 = avg(dataframe['acc distance ap1'])
    acc_ap2 = avg(dataframe['acc distance ap2'])
    acc_ap3 = avg(dataframe['acc distance ap3'])
    
    acc_x = avg(dataframe['acc coord X'])
    acc_y = avg(dataframe['acc coord Y'])