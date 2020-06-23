from os.path import join
import csv
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    for item in est:#Drawing the estimated points

        plt.scatter(float(item[1]), float(item[2]), 
                    color = color[ord(item[0]) - ord('a')], 
                    alpha = "0.2",
                    s = 8) 
    plt.title(title)
    plt.xlim([-200, 800])
    plt.ylim([-200, 600])
    plt.savefig(join(join("output", "plot"), title + "-room accuracy"))
    plt.show()


def trilateration(r,x,y):
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    r1 = r[0]
    r2 = r[1]
    r3 = r[2]
    y1 = y[0]
    y2 = y[1]
    y3 = y[1]
    A = 2*x2 - 2*x1;
    B = 2*y2 - 2*y1;
    C = r1*r1 - r2*r2 - x1*x1 + x2*x2 - y1*y1 + y2*y2;
    D = 2*x3 - 2*x2;
    E = 2*y3 - 2*y2;
    F = r2*r2 - r3*r3 - x2*x2 + x3*x3 - y2*y2 + y3*y3;
    x = (C*E - F*B) / (E*A - B*D);
    y = (C*D - A*F) / (B*D - A*E);
    return x,y

def getDistance(rssi, a, n):
    return pow(10, -1*((rssi-a)/(10*n)))

if __name__ == "__main__":
    """
    ==================================
    loading constant variables
    ==================================
    """
    
    df = pd.read_csv(join('dataset', 'dataset.csv'))
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
    
    """
    ==================================
    Calculating accuracy
    ==================================
    """
    acc = [[],[],[],[],[],[]]
    for item in df.values:
        acc[0].append(abs(item[5] - euclidDist([trueLocX[item[0]], trueLocY[item[0]]], [x[0],y[0]]) ))
        acc[1].append(abs(item[6] - euclidDist([trueLocX[item[0]], trueLocY[item[0]]], [x[1],y[1]]) ))
        acc[2].append(abs(item[7] - euclidDist([trueLocX[item[0]], trueLocY[item[0]]], [x[2],y[2]]) ))
        acc[3].append(abs(item[8] - trueLocX[item[0]]))
        acc[4].append(abs(item[9] - trueLocX[item[0]]))
        acc[5].append(euclidDist([item[8], item[9]], [trueLocX[item[0]], trueLocY[item[0]]]))
        
    df['acc dist 1'] = acc[0]
    df['acc dist 2'] = acc[1]
    df['acc dist 3'] = acc[2]
    
    df['acc x'] = acc[3]
    df['acc y'] = acc[4]
    df['acc coord'] = acc[5]
    
    for i in range(0,11,5):
        cur = df[df["n"] == i]
        est = cur[['label','x', 'y']].values
        drawRoom(est, " n = {}".format(i ))
    
    df.to_csv(join('output', 'analisis ips.csv'))
    
    acc_point= []
    for item in range(0,11,5):
        cur = df[df['n'] == item].sort_values(by=['label'])
        
        for i in  ['a', 'b' , 'c', 'd','e', 'f']:
            means_n = [i, item]
            cur_label = cur[cur['label'] == i]
            means_n.append(sum(cur_label['acc dist 1']) / len(cur_label['acc dist 1']))
            means_n.append(sum(cur_label['acc dist 2']) / len(cur_label['acc dist 2']))
            means_n.append(sum(cur_label['acc dist 3']) / len(cur_label['acc dist 3']))
            means_n.append(sum(cur_label['acc x']) / len(cur_label['acc x']))
            means_n.append(sum(cur_label['acc y']) / len(cur_label['acc y']))
            means_n.append(sum(cur_label['acc coord']) / len(cur_label['acc coord']))    
            acc_point.append(means_n)
    
    
    acc_point = pd.DataFrame(columns = ['label', 'n',
                                        'acc dist 1' , 'acc dist 2', 'acc dist 3',
                                        'acc x', 'acc y',
                                        'acc coord'],
                             data = acc_point)
    acc_point.to_csv(join('output', 'analisis ips per point.csv'))
    
    
    """
    ==================================
    Visualizing
    ==================================
    """
    
    color = ["red", "blue", "black"]
    for item in range(0,11,5):
        cur = df[df['n'] == item].sort_values(by=['label'])
        plt.plot(list(range(599)), cur['acc coord'].values[:599], 
                 color = color[int(item/5)], alpha =0.8, label = "n = {}".format(item))
    plt.ylabel("kesalahan estimasi (cm)")
    plt.legend()
    
    plt.title("Kesalahan estimasi posisi")
    plt.savefig(join(join('output','plot'), 'kesalahan estimasi posisi'))
    plt.show()
    
    #kesalahan per poin
    
    labels = ['a', 'b' , 'c', 'd','e', 'f']    
    
    x = np.array(list(range(0,11,2)))
    width = 0.5  # the width of the bars
        
    fig, ax = plt.subplots()
    rects1 = ax.bar(x  - width , acc_point[acc_point['n'] ==0]['acc coord'], width, label='n = 0', color = "cornflowerblue")
    rects2 = ax.bar(x , acc_point[acc_point['n'] ==5]['acc coord'], width, label='n = 5', color = "lightskyblue")
    rects3 = ax.bar(x  + width, acc_point[acc_point['n'] ==10]['acc coord'], width, label='n = 10',  color = "paleturquoise")
    
    ax.set_ylabel('Error (cm)')
    ax.set_title('Kesalahan estimasi posisi')
    ax.set_xlabel('Titik pengambilan data')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
      
    fig.tight_layout()
    plt.savefig(join(join('output','plot'), 'kesalahan estimasi posisi bar'))
    plt.show()
       
            
