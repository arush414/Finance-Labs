import random
import math
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt

S0=100
K=105
T=5
r= 0.05
sigma = 0.3
M_list= [1, 5, 10, 20, 50, 100, 200, 400]
answer=[]

def binomial_model(M):
    
    delta= T/M
    R=math.exp(r*delta)
    up_factor = math.exp(sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
    down_factor = math.exp(-sigma*math.sqrt(delta) + (r - 0.5*sigma*sigma)*delta)
    probab= (R-down_factor)/(up_factor-down_factor)
    
    if(R<=down_factor or R>=up_factor):
        print(f"Arbitrage oppurtunity exist for M={M}")
        exit()
    
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

    

def plot_graph(option,step):
    
    plt.title(f"{option} option for step value = {step}")
    plt.xlabel("Number of subintervals (M)")
    plt.ylabel(f"{option} option price for initial time step")
    X=np.arange(1,401,step)
    Y=[]
    if(option=="call"):
        for i in X:
            callprice,putprice,main_values= binomial_model(i)
            Y.append(callprice)
    else:
        for i in X:
            callprice,putprice,main_values= binomial_model(i)
            Y.append(putprice)
        
    plt.plot(X,Y)
    plt.show()
    
    

plot_graph("call",1)
plot_graph("call",5)
plot_graph("put",1)
plot_graph("put",5)
        
        
        
        
        
        
        
       
    
    
    
    
    
    


    

