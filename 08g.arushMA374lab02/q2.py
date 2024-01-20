import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def lookback_model(S0,T,K,r,sigma,M,Set):
      
    delta= T/M
    R=math.exp(r*delta)
    if(Set==2):
        up_factor = math.exp(sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
        down_factor = math.exp(-sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
    else:
        up_factor = math.exp(sigma*math.sqrt(delta) )
        down_factor = math.exp(-sigma*math.sqrt(delta))
        
    probab= (R-down_factor)/(up_factor-down_factor)
    
    if(R<=down_factor or R>=up_factor):
        print(f"Arbitrage oppurtunity exist for M={M}")
        return -1,-1
    
   
    
    def call_price(stepno,current,maxima):
        
        if(stepno==M):
            
            return max(0,maxima-K)
        
        return (probab*(call_price(stepno+1,current*up_factor,max(maxima,current*up_factor))) + (1-probab)*(call_price(stepno+1,current*down_factor,maxima)))/R
    
    def put_price(stepno,current,minima):
        if(stepno==M):
            
            return max(0,K-minima)
        
        return (probab*(put_price(stepno+1,current*up_factor,minima)) + (1-probab)*(put_price(stepno+1,current*down_factor,min(minima,current*down_factor))))/R
    
    return call_price(0,S0,S0),put_price(0,S0,S0)
  
call1,put1= lookback_model(S0=100,T=1,K=100,r=0.08,sigma=0.3,M=10,Set=1)
call2,put2= lookback_model(S0=100,T=1,K=100,r=0.08,sigma=0.3,M=10,Set=2)


print("*****************************************")
print(f"Initial Call option price for SET1 is {call1}")
print(f"Initial Put option price for SET1 is {put1}")
print("*****************************************")
print(f"Initial Call option price for SET2 is {call2}")
print(f"Initial Put option price for SET2 is {put2}")


def plot_graph_for2d(xlabel,Set,x,ycall,yput):
    
    plt.xlabel(xlabel)
    plt.ylabel("Initial option prices")
    plt.title(f"Initial Option Prices vs {xlabel} for Set{Set}")
    plt.plot(x,ycall,label="call option")
    plt.plot(x,yput,label="put option")
    plt.legend()
    plt.show()

def plot2d(Set):
    
    S0_list = np.linspace(50,150,100)
    K_list= np.linspace(50,150,100)
    r_list=np.linspace(0,0.8,250)
    sigma_list=np.linspace(0.1,1,250)
    M_list =  [i for i in range(5, 20)]
    ycall=[]
    yput=[]
    for S0 in S0_list:
        call,put=lookback_model(S0=S0,T=1,K=100,r=0.08,sigma=0.3,M=10,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("S0",Set,S0_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for K in K_list:
        call,put= lookback_model(S0=100,T=1,K=K,r=0.08,sigma=0.3,M=10,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("K",Set,K_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for r in r_list:
        call,put= lookback_model(S0=100,T=1,K=100,r=r,sigma=0.3,M=10,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("r",Set,r_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for sigma in sigma_list:
        call,put= lookback_model(S0=100,T=1,K=100,r=0.08,sigma=sigma,M=10,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("sigma",Set,sigma_list,ycall,yput)
    
    for K in [95,100,105]:
        
        ycall=[]
        yput=[]
        for M in M_list:
            call,put= lookback_model(S0=100,T=1,K=K,r=0.08,sigma=0.3,M=int(M),Set=Set)
            ycall.append(call)
            yput.append(put)
        
        plt.plot(M_list,ycall)
        plt.xlabel("M")
        plt.ylabel("Initial Call Option Price")
        plt.title(f"Call Option Price vs M for Set{Set} and K = {K}")
        plt.show()
        plt.plot(M_list,yput)
        plt.xlabel("M")
        plt.ylabel("Initial Put Option Price")
        plt.title(f"Put Option Price vs M for Set{Set} and K = {K} ")
        plt.show()
        
    

      
    
# Plotting 2D graphs with varying S0,K,r and sigma
plot2d(Set=1)
plot2d(Set=2)

