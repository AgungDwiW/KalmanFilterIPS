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

def loadDataset(name):
    data = []
    with open(name, newline='') as f:
        reader = csv.reader(f)
        reader = list(reader)
    data = reader.copy()
    return data

def getDistance(rssi, a, n):
    return pow(10, -1*((rssi-a)/(10*n)))

def doDist(filename ,a , n):
    data = loadDataset(filename)
    dataset = [int (i[3]) for i in data]
    dist = []
    for item in dataset:
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
    return dictElement

def createGraph(dataset, filename):
    x = [ round(i,2) for i in dataset.keys()]
    plt.bar(x, dataset.values())
    plt.xlabel("Error (m)")
    plt.ylabel("Error count")
    plt.savefig(filename)
    plt.show()

def printJSON(dataset, filename):
    with open(filename, 'w', newline="") as myfile:
        json.dump(dataset, myfile)

if __name__ == "__main__":
    
    """
    ==================================
    loading constant variables
    ==================================
    """
    constant =loadDataset(join("output", "constant variables"))
    a_tp = float(constant[1][2])
    n_tp = float(constant[1][3])
    
    a_hp = float(constant[2][2])
    n_hp = float(constant[2][3])
    
    a_dp = float(constant[3][2])
    n_dp = float(constant[3][3])
    
    
    """
    ==================================
    AP-1 TP-Link
    ==================================
    """
    
    #loading dataset and calculate distance and path loss
    tp_1_1 = doDist(join("dataset6", "tp-1-1.csv"), a_tp, n_tp)
    acc_tp_1_1 = doAcc(tp_1_1, 1)
    
    tp_1_2 = doDist(join("dataset6", "tp-1-2.csv"), a_tp, n_tp)
    acc_tp_1_2 = doAcc(tp_1_2, 1)
    
    tp_2_1 = doDist(join("dataset6", "tp-2-1.csv"), a_tp, n_tp)
    acc_tp_2_1 = doAcc(tp_2_1, 2)
    
    tp_2_2 = doDist(join("dataset6", "tp-2-2.csv"), a_tp, n_tp)
    acc_tp_2_2 = doAcc(tp_2_2, 2)
    
    tp_3_1 = doDist(join("dataset6", "tp-3-1.csv"), a_tp, n_tp)
    acc_tp_3_1 = doAcc(tp_3_1, 3)
    
    tp_3_2 = doDist(join("dataset6", "tp-3-2.csv"), a_tp, n_tp)
    acc_tp_3_2 = doAcc(tp_3_2, 3)
    
    acc_tp_1 = acc_tp_1_1 + acc_tp_1_2
    acc_tp_2 = acc_tp_2_1 + acc_tp_2_2
    acc_tp_3 = acc_tp_3_1 + acc_tp_3_2
    
    #get statistic of path loss
    stat_tp_1 = getStatistic(acc_tp_1)
    stat_tp_2 = getStatistic(acc_tp_2)
    stat_tp_3 = getStatistic(acc_tp_3)
    #create graph
    createGraph(stat_tp_1, join("output", "tp_1 "))
    createGraph(stat_tp_2, join("output", "tp_2 "))
    createGraph(stat_tp_3, join("output", "tp_3 "))
    
    """
    ==================================
    AP-2 HandPhone
    ==================================
    """
    
    #loading dataset and calculate distance and path loss
    hp_1_1 = doDist(join("dataset6", "hp-1-1.csv"), a_hp, n_hp)
    acc_hp_1_1 = doAcc(hp_1_1, 1)
    
    hp_1_2 = doDist(join("dataset6", "hp-1-2.csv"), a_hp, n_hp)
    acc_hp_1_2 = doAcc(hp_1_2, 1)
    
    hp_2_1 = doDist(join("dataset6", "hp-2-1.csv"), a_hp, n_hp)
    acc_hp_2_1 = doAcc(hp_2_1, 2)
    
    hp_2_2 = doDist(join("dataset6", "hp-2-2.csv"), a_hp, n_hp)
    acc_hp_2_2 = doAcc(hp_2_2, 2)
    
    hp_3_1 = doDist(join("dataset6", "hp-3-1.csv"), a_hp, n_hp)
    acc_hp_3_1 = doAcc(hp_3_1, 3)
    
    hp_3_2 = doDist(join("dataset6", "hp-3-2.csv"), a_hp, n_hp)
    acc_hp_3_2 = doAcc(hp_3_2, 3)
    
    acc_hp_1 = acc_hp_1_1 + acc_hp_1_2
    acc_hp_2 = acc_hp_2_1 + acc_hp_2_2
    acc_hp_3 = acc_hp_3_1 + acc_hp_3_2
    
    #get statistic of path loss
    stat_hp_1 = getStatistic(acc_hp_1)
    stat_hp_2 = getStatistic(acc_hp_2)
    stat_hp_3 = getStatistic(acc_hp_3)
    #create graph
    createGraph(stat_hp_1, join("output", "hp_1 "))
    createGraph(stat_hp_2, join("output", "hp_2 "))
    createGraph(stat_hp_3, join("output", "hp_3 "))
    
    """
    ==================================
    AP-3 DP-Link
    ==================================
    """
    #loading dataset and calculate distance and path loss
    dp_1_1 = doDist(join("dataset6", "dp-1-1.csv"), a_dp, n_dp)
    acc_dp_1_1 = doAcc(dp_1_1, 1)
    
    dp_1_2 = doDist(join("dataset6", "dp-1-2.csv"), a_dp, n_dp)
    acc_dp_1_2 = doAcc(dp_1_2, 1)
    
    dp_2_1 = doDist(join("dataset6", "dp-2-1.csv"), a_dp, n_dp)
    acc_dp_2_1 = doAcc(dp_2_1, 2)
    
    dp_2_2 = doDist(join("dataset6", "dp-2-2.csv"), a_dp, n_dp)
    acc_dp_2_2 = doAcc(dp_2_2, 2)
    
    dp_3_1 = doDist(join("dataset6", "dp-3-1.csv"), a_dp, n_dp)
    acc_dp_3_1 = doAcc(dp_3_1, 3)
    
    dp_3_2 = doDist(join("dataset6", "dp-3-2.csv"), a_dp, n_dp)
    acc_dp_3_2 = doAcc(dp_3_2, 3)
    
    acc_dp_1 = acc_dp_1_1 + acc_dp_1_2
    acc_dp_2 = acc_dp_2_1 + acc_dp_2_2
    acc_dp_3 = acc_dp_3_1 + acc_dp_3_2
    
    #get statistic of path loss
    stat_dp_1 = getStatistic(acc_dp_1)
    stat_dp_2 = getStatistic(acc_dp_2)
    stat_dp_3 = getStatistic(acc_dp_3)
    #create graph
    createGraph(stat_dp_1, join("output", "dp_1 "))
    createGraph(stat_dp_2, join("output", "dp_2 "))
    createGraph(stat_dp_3, join("output", "dp_3 "))
    
    """
    printing output
    """
    
    printJSON(stat_tp_1, join("output", "stat_tp_1"))
    printJSON(stat_tp_2, join("output", "stat_tp_2"))
    printJSON(stat_tp_3, join("output", "stat_tp_3"))
    
    printJSON(stat_hp_1, join("output", "stat_hp_1"))
    printJSON(stat_hp_2, join("output", "stat_hp_2"))
    printJSON(stat_hp_3, join("output", "stat_hp_3"))
    
    printJSON(stat_dp_1, join("output", "stat_dp_1"))
    printJSON(stat_dp_2, join("output", "stat_dp_2"))
    printJSON(stat_dp_3, join("output", "stat_dp_3"))