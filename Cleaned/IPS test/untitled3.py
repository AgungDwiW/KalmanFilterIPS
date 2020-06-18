# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 23:22:01 2020

@author: Project-C
"""
import math
def  trilaterate2(L1,L2, L3, x1,x2,x3,y1,y2,y3,z1=0,z2=0,z3=0):
    LB1 = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1));
    LB2 = math.sqrt((x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2) + (z3 - z2) * (z3 - z2));
    LB3 = math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3) + (z1 - z3) * (z1 - z3));
    
    X = (L1*L1  - L2*L2  + LB1*LB1)/(2*LB1 );
    C1 = math.sqrt (L1*L1 - X*X);
       
    
    XB = (LB3*LB3 - LB2*LB2 + LB1*LB1 )/(2*LB1 );
    
    CB=  math.sqrt(LB3*LB3 - XB* XB );
    
    D1 = math.sqrt(C1*C1+(XB - X)*(XB - X));
    Y = (D1*D1 - L3*L3  + CB*CB  )/(2*CB );
    
    Z = math.sqrt(C1 * C1 - Y * Y);
    
    Xx = (x2-x1);
    Xy = (y2-y1);
    Xz = (z2-z1);
    Xl = math.sqrt(Xx*Xx+Xy*Xy+Xz*Xz);
    Xx = Xx / Xl;
    Xy = Xy / Xl;
    Xz = Xz / Xl;
    
    
    t =- ((x1-x3)*(x2-x1)+(y1-y3)*(y2-y1)+(z1-z3)*(z2-z1))/(LB1*LB1);
    Yx = (x1+(x2-x1)*t-x3);
    Yy = (y1+(y2-y1)*t-y3);
    Yz = (z1+(z2-z1)*t-z3);
    Yl = math.sqrt(Yx*Yx+Yy*Yy+Yz*Yz);
    Yx =- (Yx/Yl);
    Yy =- (Yy/Yl);
    Yz =- (Yz/Yl);
    
    Zx = (Xy * Yz - Xz * Yy);
    Zy = (Xz * Yx - Xx * Yz);
    Zz = (Xx * Yy - Xy * Yx);
    
    
    x = (x1 + X * Xx + Y * Yx + Z * Zx);
    y = (y1 + X * Xy + Y * Yy + Z * Zy);
    z = (z1 + X * Xz + Y * Yz + Z * Zz);
    
    x = (x1 + X * Xx + Y * Yx - Z * Zx);
    y = (y1 + X * Xy + Y * Yy - Z * Zy);
    z = (z1 + X * Xz + Y * Yz - Z * Zz);
     
    return x,y
    