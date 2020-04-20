# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 21:11:57 2020

@author: Project-C
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

data = loadDataset("a.csv")

dictBSSID = {"ce:73:14:c4:7a:28" : 0, "18:0f:76:91:f2:72" : 1, "c0:25:e9:7a:e6:30":2}
coordinate = [ [0,0] , [0,1], [0.5,1] ]
freq = [2472, 2452, 2412]
y = []
x = []
z = []

def getDistance(rssi, freq):
    #Distance (km) = 10(Free Space Path Loss – 32.44 – 20log10(f))/20
    rssi = abs(rssi)
    d = 10 * (rssi -32.44 -  20 * math.log10(freq))/20
    # (27.55 - (20 * Math.log10(freqInMHz)) + Math.abs(signalLevelInDb)) / 20.0;
    #d = 10 ^ ((Ptx - RSSI) / (10 * n))
    d = math.pow(10, ((18.5-rssi)/(16)))
    return d

def getCoordinate( temp,coordinate):
    x_c = [-1]
    y_c = [-1]
    for item in coordinate:
        x_c.append(item[0])
        y_c.append(item[1])
    r = [-1]
    for item in range(len(temp)):
        r.append(getDistance(temp[item], freq[item]))
    
    A = 2*x_c[2] - 2*x_c[1];
    B = 2*y_c[2] - 2*y_c[1];
    C = r[1]*r[1] - r[2]*r[2] - x_c[1]*x_c[1] + x_c[2]*x_c[2] - y_c[1]*y_c[1] + y_c[2]*y_c[2];
    D = 2*x_c[3] - 2*x_c[2];
    E = 2*y_c[3] - 2*y_c[2];
    F = r[2]*r[2] - r[3]*r[3] - x_c[2]*x_c[2] + x_c[3]*x_c[3] - y_c[2]*y_c[2] + y_c[3]*y_c[3];
    x = (C*E - F*B) / (E*A - B*D);
    y = (C*D - A*F) / (B*D - A*E);
    return round(x,2),round(y,2)


for item in data:
   
   temp = ['0' for a in range(3)]
   atomPrev= 0
   for atom in item[1:]:
       if atomPrev in dictBSSID.keys():
           temp[dictBSSID[atomPrev]] = int(atom)
       atomPrev = atom
   if '0' in temp:
       continue

   z.append(getCoordinate(temp, coordinate))
    
   x.append(temp)
   y.append(item[0])
   