import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import time

def compute_option_price(i, S0, u, d, M):
    
    path = format(i, 'b').zfill(M)
    curr_max = S0

    for idx in path:
        if idx == '1':
            
            S0 *= d
        else:
            S0 *= u

        curr_max = max(curr_max, S0)
    
    return curr_max - S0


def lookback_model(S0,T,r,sigma,M,tabulate=False):
    
    curr_time = time.time()
    delta= T/M
    R=math.exp(r*delta)
    
    up_factor = math.exp(sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
    down_factor = math.exp(-sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
   
    probab= (R-down_factor)/(up_factor-down_factor)
    
    if(R<=down_factor or R>=up_factor):
        print(f"Arbitrage oppurtunity exist for M={M}")
        return -1,-1
    if(tabulate):
        tabulate_values =[]
        for i in range(0, M + 1):
            D = []
            for j in range(int(pow(2, i))):
                D.append(0)
            tabulate_values.append(D)
        
        
        for i in range(int(pow(2, M))):
            req_price = compute_option_price(i, S0, up_factor, down_factor, M)
            tabulate_values[M][i] = max(req_price, 0)
        
        for j in range(M - 1, -1, -1):
            for i in range(0, int(pow(2, j))):
                tabulate_values[j][i] = (probab*tabulate_values[j + 1][2*i+1] + (1 - probab)*tabulate_values[j + 1][2*i]) / R;
                
        return tabulate_values
        
        
    else:
        def call_price(stepno,current,maxima,height):    
            if(stepno==M):
                return max(0,maxima-(S0*(up_factor**height)*(down_factor**(M-height))))
            
            return (probab*(call_price(stepno+1,current*up_factor,max(maxima,current*up_factor),height+1)) + (1-probab)*(call_price(stepno+1,current*down_factor,maxima,height)))/R
            
    
        Call=call_price(0,S0,S0,0)
        final_time=time.time()
        if(tabulate==False):
            return Call,final_time-curr_time
        else:
            return Call,final_time-curr_time,tabulate_values
  

print("***************************** Part A *******************************")
answers=[]
for M in [5,10,25]:
    
    callprice,time_taken= lookback_model(S0=100,T=1,r=0.08,sigma=0.3,M=M)
    answers.append([M,callprice,time_taken])

print("For M=50 it is taking too much time so Putting Not Feasible\n")
answers.append([50,"Not Feasible","Not Feasible"])
print(tabulate(answers, ['M', 'Initial Option Price','Time Taken'], tablefmt='grid'), '\n')

print("\n ***************************** Part B *******************************")

M_list = [i for i in range(1, 21)]
prices=[]
for M in M_list:
    callprice,time_taken=lookback_model(S0=100,T=1,r=0.08,sigma=0.3,M=M)
    prices.append(callprice)

plt.plot(M_list,prices)
plt.title("Initial Option Prices vs M")
plt.xlabel("M")
plt.ylabel("Initial Option Prices")
plt.show()
 
    
print("\n ***************************** Part C *******************************")

tabulate_values=lookback_model(S0=100,T=1,r=0.08,sigma=0.3,M=5,tabulate=True)


answers=[]
for i in range(6):
    answers.append([f"t = {i}",tabulate_values[i][:2**i]])

print(tabulate(answers,["Time step","Values"],tablefmt="fancy_grid", numalign="center", stralign="center"))
