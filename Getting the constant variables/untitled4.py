# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:25:39 2020

@author: Project-C
"""

from scipy.optimize import minimize, rosen, rosen_der

def loss (x, r):
    
    x_ap = [0, 300, 600]
    y_ap = [0, 400, 0]
    err= 0
    for item in range(len(r)):
        err += (r[item] ** 2 - (x[0] - x_ap[item]) **2 + (x[1] - y_ap[item]) **2) **2
    return err



data_a = route_frame[route_frame["label" ] == "a"]
data_a = data_a[["dist1","dist2", "dist3"]]

est = []
for item in data_a.values:
    init_guess = [0,0]
    
    est.append(minimize(loss, init_guess, args = (item), method='least_squares'))

est_accu = []

for item in est:
    accu=[]
    for i in item:
        accu.append(abs(i - 100))
    est_accu.append(accu)
    


data_a_acc =  route_acc_frame[route_frame["label" ] == "a"]
data_a_acc = data_a_acc[["acc estimated x", "acc estimated y"]]
est_accu = list(np.transpose(est_accu))

avgs = [avg(i) for i in est_accu]


data_a_acc = data_a_acc.values

data_a_acc  = list(np.transpose(data_a_acc ))
avg_tril = [avg(i) for i in data_a_acc  ]