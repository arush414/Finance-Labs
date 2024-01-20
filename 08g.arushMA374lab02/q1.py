import random
import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



def binomial_model(S0,T,K,r,sigma,M,Set):
    

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
        
        main_values[option][stepno][height]= (probab*(prices(option,stepno+1,height+1)) + (1-probab)*(prices(option,stepno+1,height)))/R
        return main_values[option][stepno][height]
    
    return prices("call",0,0),prices("put",0,0),main_values



call1,put1,main_values1= binomial_model(S0=100,T=1,K=100,r=0.08,sigma=0.3,M=100,Set=1)
call2,put2,main_values2= binomial_model(S0=100,T=1,K=100,r=0.08,sigma=0.3,M=100,Set=2)

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
    
    S0_list = np.linspace(30,200,150)
    K_list= np.linspace(30,200,150)
    r_list=np.linspace(0,1,250)
    sigma_list=np.linspace(0.1,1,250)
    M_list=np.linspace(40,200,150)
    ycall=[]
    yput=[]
    for S0 in S0_list:
        call,put,main_values= binomial_model(S0=S0,T=1,K=100,r=0.08,sigma=0.3,M=100,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("S0",Set,S0_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for K in K_list:
        call,put,main_values= binomial_model(S0=100,T=1,K=K,r=0.08,sigma=0.3,M=100,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("K",Set,K_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for r in r_list:
        call,put,main_values= binomial_model(S0=100,T=1,K=100,r=r,sigma=0.3,M=100,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("r",Set,r_list,ycall,yput)
    
    ycall=[]
    yput=[]
    for sigma in sigma_list:
        call,put,main_values= binomial_model(S0=100,T=1,K=100,r=0.08,sigma=sigma,M=100,Set=Set)
        ycall.append(call)
        yput.append(put)
    
    plot_graph_for2d("sigma",Set,sigma_list,ycall,yput)
    
    for K in [95,100,105]:
        
        ycall=[]
        yput=[]
        for M in M_list:
            call,put,main_values= binomial_model(S0=100,T=1,K=K,r=0.08,sigma=0.3,M=int(M),Set=Set)
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
        
    

def plot_graph_for3d(x, y, ycall,yput, xlabel, ylabel,Set):
    
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, ycall, cmap='winter')
    
    plt.title(f"Initial Call Option Price vs {xlabel} vs {ylabel} for Set{Set}")
    ax.set_xlabel(xlabel) 
    ax.set_ylabel(ylabel) 
    ax.set_zlabel("Initial Call option price")
    plt.show()
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, yput, cmap='winter')
    plt.title(f"Initial Put Option Price vs {xlabel} vs {ylabel} for Set{Set}")
    ax.set_xlabel(xlabel) 
    ax.set_ylabel(ylabel) 
    ax.set_zlabel("Initial Put option price")
    plt.show()

def plot3d(Set):
    S0_list = np.linspace(30,200,100)
    K_list= np.linspace(30,200,100)
    r_list=np.linspace(0.1,0.8,150)
    sigma_list=np.linspace(0.1,1,150)
    M_list=np.linspace(40,200,100)
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for S0 in S0_list:
        for K in K_list:
            c, p,main_values = binomial_model(S0 = S0, K = K, T = 1, M = 100, r = 0.08, sigma = 0.30,Set=Set)
            x_axis.append(S0)
            y_axis.append(K)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"S0","K",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for S0 in S0_list:
        for r in r_list:
            c, p,main_values = binomial_model(S0 = S0, K = 100, T = 1, M = 100, r = r, sigma = 0.30,Set=Set)
            x_axis.append(S0)
            y_axis.append(r)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"S0","r",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for S0 in S0_list:
        for sigma in sigma_list:
            c, p,main_values = binomial_model(S0 = S0, K = 100, T = 1, M = 100, r = 0.08, sigma = sigma,Set=Set)
            x_axis.append(S0)
            y_axis.append(sigma)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"S0","sigma",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for S0 in S0_list:
        for M in M_list:
            c, p,main_values = binomial_model(S0 = S0, K = 100, T = 1, M = int(M), r = 0.08, sigma = 0.30,Set=Set)
            x_axis.append(S0)
            y_axis.append(M)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"S0","M",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for K in K_list:
        for r in r_list:
            c, p,main_values = binomial_model(S0 = 100, K = K, T = 1, M = 100, r = r, sigma = 0.30,Set=Set)
            x_axis.append(K)
            y_axis.append(r)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"K","r",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for K in K_list:
        for sigma in sigma_list:
            c, p,main_values = binomial_model(S0 = 100, K = K, T = 1, M = 100, r = 0.08, sigma = sigma,Set=Set)
            x_axis.append(K)
            y_axis.append(sigma)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"K","sigma",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for K in K_list:
        for M in M_list:
            c, p ,main_values= binomial_model(S0 = 100, K = K, T = 1, M =int(M), r = 0.08, sigma = 0.30,Set=Set)
            x_axis.append(K)
            y_axis.append(M)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"K","r",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for r in r_list:
        for sigma in sigma_list:
            c, p ,main_values= binomial_model(S0 = 100, K = 100, T = 1, M = 100, r = r, sigma = sigma,Set=Set)
            x_axis.append(r)
            y_axis.append(sigma)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"r","sigma",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for r in r_list:
        for M in M_list:
            c, p ,main_values= binomial_model(S0 = 100, K = 100, T = 1, M = int(M), r = r, sigma = 0.30,Set=Set)
            x_axis.append(r)
            y_axis.append(M)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"r","M",Set)
    
    ycall=[]
    yput=[]
    x_axis=[]
    y_axis=[]
    for sigma in sigma_list:
        for M in M_list:
            c, p,main_values = binomial_model(S0 = 100, K = 100, T = 1, M = int(M), r = 0.08, sigma = sigma,Set=Set)
            x_axis.append(sigma)
            y_axis.append(M)
            ycall.append(c)
            yput.append(p)
                
    plot_graph_for3d(x_axis,y_axis,ycall,yput,"sigma","M",Set)
    
# Plotting 2D and 3D graphs with varying S0,K,r,sigma and M
plot2d(Set=1)
plot2d(Set=2)
plot3d(Set=1)
plot3d(Set=2)


    
    
    