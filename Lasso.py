#! /usr/bin/env python3
from numpy import *
import numpy as np
import csv
import matplotlib.pyplot as plt
import time

d = 10
n = 15

x = np.random.random((d,n))
y = np.random.random((n,1))
w = np.zeros((d,1))

loss_history = []


# The lost function for lasso is 1 / 2 || X ^ T w - y ||^2_2 + \lambda ||w||_1, ( where ||w||_1 = \sum _j |w_j| )
def loss (x, y, w, lam):
    total_loss = 1 / 2 * np.linalg.norm(np.dot (x.T, w) - y)**2 + lam * np.linalg.norm(w, ord=1)
    # print("The total_loss is:")
    # print(total_loss)
    return total_loss


# the presodo code for lasso is :
# repeat
#   for j = 1, 2, ..., d do:
#       w_j = arg_min(z \in R) 1 / 2 || (X_j)^T z + \sum_{k \neq j} (X_k:)^T w_k - y||^2_2 + \lambda |z|
# until convergence

def Lasso (x, y, w, lam):
    d = x.shape[0]
    n = x.shape[1]
    round_cal = 0

    while(1):
        pre_w = w.copy()

        for i in range(0,d):
            a = 0
            b = 0
            M = np.zeros((n,1))
            
            # a = sum_{i = 1}^d X_ji ^ 2
            for j in range(0, d):
                a +=  x[j][i] * x[j][i]
                if (j != i):
                    s = x[j].reshape(n,1) * w[j]        
                    q = y - s
                    M += q

            # b = sum_{i = 1}^d M_i * X_ji
            for j in range(0,d):
                b += M[j] * x[j][i]
                

            if (b / a < 0):
                w[i] = -1 * max(0,(((-1) * b / a)  - lam / a))
            else:
                w[i] = max(0,(b / a) - lam / a)
        
        loss_this_round = loss (x, y, w, lam)

        loss_history.append(loss_this_round)
        round_cal += 1
        print (np.linalg.norm(w - pre_w))

        if (np.linalg.norm(w - pre_w) < 0.01):
            print ("The output w is:")
            print (w)
            return round_cal

round_cal = Lasso (x, y, w, 10)
loss_x = range (0,round_cal)
plt.plot(loss_x, loss_history,'o')
plt.show()        
   
