import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



def binomial_model(S0,T,K,r,sigma,M):
    
    delta= T/M
    R=math.exp(r*delta)
    
    up_factor = math.exp(sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
    down_factor = math.exp(-sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
    
        
    probab= (R-down_factor)/(up_factor-down_factor)
    
    if(R<=down_factor or R>=up_factor):
        print(f"Arbitrage oppurtunity exist for M={M}")
        return -1,-1,-1
    
    call = [[-1 for i in range(M + 1)] for j in range(M + 1)]
    put = [[-1 for i in range(M + 1)] for j in range(M + 1)]
    
    for i in range(M+1):
        call[M][i]= max(0,(up_factor**(i))*(down_factor**(M-i))*S0 - K )
        put[M][i]= max(0,K-(up_factor**(i))*(down_factor**(M-i))*S0)
        
    main_values = {"call":call,"put":put}
    
    def prices(option,stepno,height):
        
        if(main_values[option][stepno][height]!=-1):
            return main_values[option][stepno][height]
        if(option=="call"):
            main_values[option][stepno][height]= max((up_factor**(height))*(down_factor**(stepno-height))*S0 - K,(probab*(prices(option,stepno+1,height+1)) + (1-probab)*(prices(option,stepno+1,height)))/R)
        else:
            main_values[option][stepno][height]= max(K-(up_factor**(height))*(down_factor**(stepno-height))*S0,(probab*(prices(option,stepno+1,height+1)) + (1-probab)*(prices(option,stepno+1,height)))/R)
        return main_values[option][stepno][height]
    
    return prices("call",0,0),prices("put",0,0),main_values



call1,put1,main_values1= binomial_model(S0=100,T=1,K=100,r=0.08,sigma=0.3,M=100)


print("*****************************************")
print(f"Initial Call option price is {call1}")
print(f"Initial Put option price  is {put1}")
print("*****************************************")

def plot_graph_for2d(xlabel,x,ycall,yput):
    
    plt.xlabel(xlabel)
    plt.ylabel("Initial option prices")
    plt.title(f"Initial Option Prices vs {xlabel}")
    plt.plot(x,ycall,label="call option")
    plt.plot(x,yput,label="put option")
    plt.legend()
    plt.show()

def plot2d():
    
    S0_list = np.linspace(30,200,150)
    K_list= np.linspace(30,200,150)
    r_list=np.linspace(0,1,250)
    sigma_list=np.linspace(0.1,1,250)
    M_list=np.linspace(40,200,150)
    ycall=[]
    yput=[]
    for S0 in S0_list:
        call,put,main_values= binomial_model(S0=S0,T=1,K=100,r=0.08,sigma=0.3,M=100)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("S0",S0_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for K in K_list:
        call,put,main_values= binomial_model(S0=100,T=1,K=K,r=0.08,sigma=0.3,M=100)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("K",K_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for r in r_list:
        call,put,main_values= binomial_model(S0=100,T=1,K=100,r=r,sigma=0.3,M=100)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("r",r_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for sigma in sigma_list:
        call,put,main_values= binomial_model(S0=100,T=1,K=100,r=0.08,sigma=sigma,M=100)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("sigma",sigma_list,ycall,yput)
    
    for K in [95,100,105]:
        
        ycall=[]
        yput=[]
        for M in M_list:
            call,put,main_values= binomial_model(S0=100,T=1,K=K,r=0.08,sigma=0.3,M=int(M))
            ycall.append(call)
            yput.append(put)
        
        plt.plot(M_list,ycall)
        plt.xlabel("M")
        plt.ylabel("Initial Call Option Price")
        plt.title(f"Call Option Price vs M for K = {K}")
        plt.show()
        plt.plot(M_list,yput)
        plt.xlabel("M")
        plt.ylabel("Initial Put Option Price")
        plt.title(f"Put Option Price vs M for K = {K} ")
        plt.show()
        
    

    
# Plotting 2D graphs with varying S0,K,r and sigma
plot2d()


    
    
    