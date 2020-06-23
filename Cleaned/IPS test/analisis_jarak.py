# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 17:52:46 2020

@author: Project-C
"""


from os.path import join
import csv
import math
import pandas as pd
from KalmanFilter import KalmanFilter
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


def getStatistic(acc):
    dictElement = {}
    for item in acc:
        if item not in dictElement:
            dictElement[item] = 1
        else:
            dictElement[item] += 1
    return dictElement

def avg(lists):
    return sum(lists) / len(lists)

def euclidDist(v1, v2):
    dist = 0
    for item in range(len(v1)):
        dist += (v1[item] - v2[item]) **2
    return math.sqrt(dist)

def drawRoomOnly():
    import matplotlib.pyplot as plt
    #drawing the room
    for item in range(len(x)): #drawing the AP
        plt.scatter(x[item], y[item], s = 20, color = "k",)
        plt.annotate("AP{}-({},{})".format(item, x[item], y[item]), (x[item] -10, y[item] + 10))
    
    lines = [[[  0,   0], [600,   0]], #room lines
             [[600,   0], [600, 400]],
             [[600, 400], [300, 400]],
             [[300, 400], [300, 300]],
             [[300, 300], [  0, 300]],
             [[  0, 300], [  0,   0]],
             ]
    
    trueLoc = [ [100, 100], [300,100],
                [500, 100], [500,300],
                [300, 300], [100,300],]
    label_point = ['a', 'b' , 'c', 'd','e', 'f']
    
    for item in lines: #drawing room lines
        plt.plot([item[0][0], item[1][0]], [item[0][1], item[1][1]], color = "k")
    
    color = ["gold", "navy", "slategrey", "springgreen", "orangered", "aqua"] 
    for item in range(len(trueLoc)):#Drawing the point
        plt.scatter(trueLoc[item][0],trueLoc[item][1], color = color[item])
        plt.annotate("{}-({},{})".format(label_point[item], 
                                         trueLoc[item][0],trueLoc[item][1]), 
                                         (trueLoc[item][0] - 50,trueLoc[item][1] + 10))
        
def drawRoom(scattered, title):
    import matplotlib.pyplot as plt
    drawRoomOnly()
    color = ["gold", "navy", "slategrey", "springgreen", "orangered", "aqua"] 
    est = scattered
    est =np.transpose(est).tolist()
    for item in est:#Drawing the estimated points

        plt.scatter(float(item[1]), float(item[2]), 
                    color = color[ord(item[0]) - ord('a')], 
                    alpha = "0.5",
                    s = 5) 
    plt.title(title)
    plt.savefig(join(join("output", "plot"), title + "-room accuracy"))
    plt.show()



def getDistance(rssi, a, n):
    return pow(10, -1*((rssi-a)/(10*n)))

if __name__ == "__main__":
    """
    ==================================
    loading constant variables
    ==================================
    """
    
    data = loadDataset(join("dataset", "ap2_1m_at_20-06-20-1934.csv"))
    constant =loadDataset(join(join(join("..","Getting constant variables"),"output"), "constant variables.csv"))
    
    KF = KalmanFilter(dt = 1, u_x = 1 ,u_y = 1, std_acc = 1 , x_std_meas = 1, y_std_meas = 1 )
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
    
    clean = []
    for item in data:
        temp = [[] for i in range(len(bssid) +1)]
        for atom in range(len(item)): 
            temp[0] = int(item[0])
            for itemB in range(len(bssid)):
                if item[atom] == bssid[itemB]:
                    temp[itemB+1] = int(item[atom+1])
        clean.append(temp)
    
    df = pd.DataFrame(columns = ['label', 'rssi1', 'rssi2', 'rssi3'], data = clean)
    
    dist = []
    for item in df.values:
        dist_cur = [[],[],[]]
        for atom in range(len(item)-1):
            dist_cur[atom] = getDistance(item[atom+1], a[atom], n[atom]) * 100
        dist.append(dist_cur)
    dist = np.transpose(dist).tolist()
    df['dist1'] = dist[0]
    df['dist2'] = dist[1]
    df['dist3'] = dist[2]
    df['n']= [0 for i in range(len(df["dist1"]))]
    
    
    
    df2 = pd.read_csv(join('dataset', 'ap2_5meter_at_20-06-20-1906.csv'))
    df = df[['label', 'n', 'rssi2', 'dist2']]
    df2 = df2[['label', 'n', 'rssi2', 'dist2']]
    
    df = df.append(df2)
    df['acc'] = abs(df['dist2'] - df['label'] *100)
    
    df.to_csv(join("output", "analisis_jarak.csv"))
        
    
    