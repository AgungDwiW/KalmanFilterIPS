# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:13:52 2020

@author: Project-C
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 02:58:06 2020

@author: Project-C
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 15:52:12 2020

@author: Project-C
"""


from os.path import join
import csv
import math
import pandas as pd
from KalmanFilter1D import KalmanFilter as KF1D
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

def avgCol(lists):
    cols = np.transpose(lists)
    cols = cols[1:].astype(np.float32).tolist()
           
    avgs = []
    for item in range(len(cols)):
        i = cols[item]
        avgs.append(avg(cols[item]))
    return avgs        

def cleanNfold (bssid, data, fold, classes):
    clean = []
    for item in data:
        temp = [[] for i in range(len(bssid) +1)]
        for atom in range(len(item)): 
            temp[0] = item[0]
            for itemB in range(len(bssid)):
                if item[atom] == bssid[itemB]:
                    temp[itemB+1] = int(item[atom+1])
        clean.append(temp)
    
    separated = [[] for i in range(len(classes))]
    for item in clean:
        for itemB in range(len(classes)):
            if (item[0] == classes[itemB]):
                separated[itemB].append(item)
    
    folded = [[]for i in range(len(classes))]
    sep_c = 0
    for item in separated:
        for i in range (int(len(item) / fold)):
            avg_c = avgCol(item[i * fold: (i+1) * fold])
            avg_c.insert(0, item[0][0])
            folded[sep_c].append(avg_c)
        sep_c+=1
        
    return folded


def cleanNfoldKF (bssid, data, fold, classes):
    
    
    clean = []
    for item in data:
        temp = [[] for i in range(len(bssid) +1)]
        for atom in range(len(item)): 
            temp[0] = item[0]
            for itemB in range(len(bssid)):
                if item[atom] == bssid[itemB]:
                    temp[itemB+1] = int(item[atom+1])
        clean.append(temp)
    
    separated = [[] for i in range(len(classes))]
    
    for item in clean:
        for itemB in range(len(classes)):
            if (item[0] == classes[itemB]):              
                separated[itemB].append( item)
    
    folded = [[]for i in range(len(classes))]
    KFed = []
    sep_c = 0
    for item in separated:
        for i in range (int(len(item) / fold)):
            KF = [KF1D(1,1,1,1) for i in range(len(item[0])-1)]
            fold_item = item[i * fold: (i+1) * fold]
            fold_KF = []
            for i_fold in fold_item:
                i2 = [i_fold[0]]
                for atom in range(1,len(i_fold)):
                    KF[atom-1].predict()
                    i2.append(float(KF[atom-1].update([[i_fold[atom],0]]).tolist()[0][0]))
                    
                fold_KF.append(i2)
            
            avg_c = avgCol(fold_KF)
            avg_c.insert(0, item[0][0])
            KFed.append(fold_KF)   
            folded[sep_c].append(avg_c)
        sep_c+=1
        
    return folded,KFed



def euclidDist(v1, v2):
    dist = 0
    for item in range(len(v1)):
        dist += (v1[item] - v2[item]) **2
    return math.sqrt(dist)

def drawRoom(scattered, title):
    
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
    for item in lines: #drawing room lines
        plt.plot([item[0][0], item[1][0]], [item[0][1], item[1][1]], color = "k")
    
    color = ["gold", "navy", "slategrey", "springgreen", "orangered", "aqua"] 
    for item in range(len(trueLoc)):#Drawing the point
        plt.scatter(trueLoc[item][0],trueLoc[item][1], color = color[item])
        plt.annotate("{}-({},{})".format(label_point[item], 
                                         trueLoc[item][0],trueLoc[item][1]), 
                                         (trueLoc[item][0] - 50,trueLoc[item][1] + 10))
    est = scattered
    est =np.transpose(est).tolist()
    for item in est:#Drawing the estimated points

        plt.scatter(float(item[1]), float(item[2]), 
                    color = color[ord(item[0]) - ord('a')], 
                    alpha = "0.5",
                    s = 2) 
    plt.title(title)
    plt.savefig(join(join("output", "plot"), title + "-room accuracy"))
    plt.show()
    

def stdev_ap(filename, BSSID,a ,n):
    #load dataset
    dataset = loadDataset(filename)
    #extract rssi
    fold = 100
    rssi  = []
    for item in dataset:
        count = 0
        for atom in item:
            if atom == BSSID:
                rssi.append(int(item[count+1]))
            count+=1
    #get average rssi
    
    folded = []
    
    for i in range(int(len(rssi)/fold)):
        avg_c = avg(rssi[i * fold: (i+1) * fold])
        folded.append(avg_c)
    
    dists =  []
    
    for item in folded:
        i = 0
        dists.append(getDistance(item, a, n))
        i+=1
    
    #return average rssi
    return statistics.stdev(dists)

if __name__ == "__main__":
    """
    ==================================
    loading constant variables
    ==================================
    """
    
    data = loadDataset(join("dataset15", "all at 16-06-20-15 00.csv"))
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
    
    trueLoc = [ [100, 100], [300,100],
                [500, 100], [500,300],
                [300, 300], [100,300],]
    
    trueDist = [[] for i in range(len(x))]
    for item in range(len(x)):
        d = []
        for atom in trueLoc:
            trueDist[item].append(euclidDist( [x[item], y[item]] , atom))
    
    label_point = list(trueLocX.keys())
    std_measses = []
    KFs = []
    for item in range(len(bssid)):
        KFs.append( KF1D(dt = 1, u = 1, std_acc = 1, std_meas = 1))
        std_measses.append(stdev_ap(join("dataset13", "ap{}-1-2.csv".format(item+1)), 
                                                                           bssid[item], a[item], n[item] ))
    
    """
    ==================================
    Measuring distance and position
    ==================================
    """
    #average 100 data to one data
    data = cleanNfoldKF(bssid, data, 100, ['a', 'b', 'c', 'd', 'e', 'f'])
    
    column = ["label", "rssi1", "rssi2", "rssi3", 
              "KF rssi1", "KF rssi2", "KF rssi3", 
              "dist1", "dist2", "dist3",
              "measured dist1", "measured dist2", "measured dist3",
              "estimated x", "estimated y", #13
              "estimated x (KF)", "estimated y (KF)", #15
              #"predicted x", "predicted y",
              #"measured x", "measured y"
              ]
    column_acc = ["label", 
              "acc dist1", "acc dist2", "acc dist3",
              "acc measured dist1", "acc measured dist2", "acc measured dist3",
              "acc estimated x", "acc estimated y", "acc estimated", #7
              #"acc predicted x", "acc predicted y", "acc predicted",
              "acc measured x", "acc measured y", "acc measured", #10
              ]
    
    routes = []
    routes_acc = []
    point_dict = {}
    point_acc_dict = {}
    for item in label_point:
        point_dict[item] = []
        point_acc_dict[item] = []
        
    for item in range(len(data[0])):
        for itemB in range(len(data)):
            
            true_x = trueLocX[data[itemB][item][0]]
            true_y = trueLocY[data[itemB][item][0]]
            point = [[] for i in range(len(column))]
            point_acc= [[] for i in range(len(column_acc))]    
            
            point[0] = data[itemB][item][0] #label
            point_acc[0] = data[itemB][item][0] #label
            
            for i in range (1, len(data[itemB][item])):
                point[i] = data[itemB][item][i] #rssi
            
            """
            ------------
            Estimating distance
            ---------------------------
            """
            d_kfs = []
            for i in range (1, len(data[itemB][item])):
                
                d = getDistance(data[itemB][item][i], a[i-1], n[i-1]) * 100
                point[7+i-1] = d
                point_acc[i] = abs(d - trueDist[i-1][ itemB]) #distance
            
            c = 0
            for i in range (1, len(data[itemB][item])):
                
                KFs[i-1].predict()
                
                rsKF = KFs[i-1].update(data[itemB][item][i])
                rsKF = rsKF.tolist()[0][0]
                point[i + 3] = rsKF
                
                d_kf = getDistance(rsKF, a[i-1], n[i-1]) * 100
                point[9+i] = d_kf
                point_acc[i+3] = abs(d_kf - trueDist[c][ itemB]) #distance
                c+=1
                
            """
            ------------
            filtering distance
            ---------------------------
            """
            
            
            """
            ------------
            Estimating Location
            ---------------------------
            """
            #trilateration
            est_x, est_y = trilateration(point[7], point[8], point[9], x[0],x[1],x[2], y[0],y[1],y[2])
            est_x2, est_y2 = trilateration(point[10], point[11], point[12], x[0],x[1],x[2], y[0],y[1],y[2])
            
            acc_x = abs(est_x - true_x)
            acc_y = abs(est_y - true_y)
            
            acc_x2 = abs(est_x2 - true_x)
            acc_y2 = abs(est_y2 - true_y)
            
            #kalman filtering
            #pred = KF.predict().tolist()
            #upd = KF.update([[est_x], [est_y]]).tolist()
            
            #pred_x = pred[0][0]
            #pred_y = pred[1][0]
            #upd_x = upd[0][0]
            #upd_y = upd[1][0]
            
            #calculating accuracy
            #acc_pred_x = abs(pred_x -true_x)
            #acc_pred_y = abs(pred_y -true_y)
            #acc_upd_x = abs(upd_x -true_x)
            #acc_upd_y = abs(upd_y -true_y)
            
            """
            ----------
            Updating the frame
            --------------------------
            """
            
            point[13] = est_x #estimation x coordinate by trilateration
            point[14] = (est_y) #estimation y coordinate by trilateration
            point[15] = (est_x2) #estimation x coordinate by trilateration
            point[16] = (est_y2) #estimation y coordinate by trilateration
            
            #point.append(pred_x) #prediction x coordinate by kalman filter
            #point.append(pred_y) #prediction y coordinate by kalman filter
            #point.append(upd_x) #measured x coordinate by kalman filter
            #point.append(upd_y) #measured x coordinate by kalman filter
            
            point_acc[7] = acc_x #accuracy x coordinate by trilateration
            point_acc[8] = acc_y #accuracy x coordinate by trilateration
            point_acc[9] = euclidDist([est_x,est_y], [true_x,true_y]) #accuracy overall coordinate by trilateration
            point_acc[10] = acc_x2 #accuracy x coordinate by trilateration
            point_acc[11] = acc_y2 #accuracy x coordinate by trilateration
            point_acc[12] = euclidDist([est_x2,est_y2], [true_x,true_y]) #accuracy overall coordinate by trilateration
            
            
            #point_acc.append(acc_pred_x) #accuracy x coordinate by kalman filter predicted coordinate
            #point_acc.append(acc_pred_y) #accuracy y coordinate by kalman filter predicted coordinate
            #point_acc.append(euclidDist([pred_x,pred_y], [true_x,true_y])) #accuracy coordinate by kalman filter predicted coordinate
            
            #point_acc.append(acc_upd_x) #accuracy x coordinate by kalman filter measured coordinate
            #point_acc.append(acc_upd_y) #accuracy x coordinate by kalman filter measured coordinate
            #point_acc.append(euclidDist([upd_x,upd_y], [true_x,true_y])) #accuracy coordinate by kalman filter measured coordinate
            
            routes.append(point)
            routes_acc.append(point_acc)
            point_dict[point[0]].append(point)
            point_acc_dict[point[0]].append(point_acc)
    route_frame = pd.DataFrame(columns = column, data = routes)
    route_acc_frame = pd.DataFrame(columns = column_acc, data = routes_acc)
    
    for item in label_point:
        point_dict[item] = pd.DataFrame(columns = column, data = point_dict[item])
        point_acc_dict[item] = pd.DataFrame(columns = column_acc, data = point_acc_dict[item])
    
    """
    ==================================
    Creating summary
    ==================================
    """
    column_summary= ["label", "acc x", "acc y", "acc"]
    data = [["acc_estimated" , avg(route_acc_frame['acc estimated x']),
             avg(route_acc_frame['acc estimated y']) , avg(route_acc_frame['acc estimated'])],
            
            #["acc_predicted", avg(route_acc_frame['acc predicted x']),
            # avg(route_acc_frame['acc predicted y']) , avg(route_acc_frame['acc predicted'])],
            
            ["acc_measured",avg(route_acc_frame['acc measured x']),
             avg(route_acc_frame['acc measured y']) , avg(route_acc_frame['acc measured'])],
        ]
    
    summary_frame = pd.DataFrame(columns = column_summary, data = data)
    
    data_per_point = []
    for item in label_point:
        data_now = [item, 
                    avg(point_acc_dict[item]["acc dist1"]),
                    avg(point_acc_dict[item]["acc dist2"]),
                    avg(point_acc_dict[item]["acc dist3"]),
                    
                    avg(point_acc_dict[item]["acc measured dist1"]),
                    avg(point_acc_dict[item]["acc measured dist2"]),
                    avg(point_acc_dict[item]["acc measured dist3"]),
                    
                    avg(point_acc_dict[item]["acc estimated x"]),
                    avg(point_acc_dict[item]["acc estimated y"]),
                    avg(point_acc_dict[item]["acc estimated"]),
                    
                    #avg(point_acc_dict[item]["acc predicted x"]),
                    #avg(point_acc_dict[item]["acc predicted y"]),
                    #avg(point_acc_dict[item]["acc predicted"]),
                    
                    avg(point_acc_dict[item]["acc measured x"]),
                    avg(point_acc_dict[item]["acc measured y"]),
                    avg(point_acc_dict[item]["acc measured"]),
                    ]
        data_per_point.append(data_now)
    
    summary_per_point_frame = pd.DataFrame(columns = column_acc, data = data_per_point)
    
        
    """
    ==================================
    Visualizing
    ==================================
    """
    
    """
    ------------
    visualizing room
    ---------------------------
    """  
   
    est = [route_frame["label"].values.tolist(), 
           route_frame["estimated x"].values.tolist(), 
           route_frame["estimated y"].values.tolist()]
    drawRoom(est, "Estimated")
    
    #est = [route_frame["label"].values.tolist(), 
    #       route_frame["predicted x"].values.tolist(), 
    #       route_frame["predicted y"].values.tolist()]
    #drawRoom(est, "Predicted")
    
    est = [route_frame["label"].values.tolist(), 
           route_frame["estimated x (KF)"].values.tolist(), 
           route_frame["estimated y (KF)"].values.tolist()]
    drawRoom(est, "Measured")
    
    x_frame = list(range(len(route_frame['rssi1'])))
    plt.plot(x_frame, route_frame['rssi1'], color = "blue")
    plt.plot(x_frame, route_frame['KF rssi1'], color = "red")
    
    avg(route_frame['rssi1'])
    avg(route_frame['KF rssi1'])