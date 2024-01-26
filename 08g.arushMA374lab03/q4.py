import random
import math
from tabulate import tabulate
import time
S0=100
K=100
T=1
r= 0.08
sigma = 0.3
M_list= [1, 5, 10,20,25,30,50]
answer=[]



def binomial_model(M,fast):
    curr_time=time.time()
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
    
    if(fast==True):
        def prices(option,stepno,height):
            
            if(main_values[option][stepno][height]!=-1):
                return main_values[option][stepno][height]
            
            main_values[option][stepno][height]= (probab*(prices(option,stepno+1,height+1)) + (1-probab)*(prices(option,stepno+1,height)))/R
            return main_values[option][stepno][height]
        
        k=prices("call",0,0)
        final_time=time.time()
        return k,main_values,final_time-curr_time
    
    else:
        
        def prices(option,stepno,height):
            if(stepno==M):
                return main_values[option][stepno][height]
            main_values[option][stepno][height]= (probab*(prices(option,stepno+1,height+1)) + (1-probab)*(prices(option,stepno+1,height)))/R
            return main_values[option][stepno][height]
        
        k=prices("call",0,0)
        final_time=time.time()
        return k,main_values,final_time-curr_time

for M in M_list[:-1]:
    
    callprice1,main_values1,time_taken1= binomial_model(M,fast=False)
    
    callprice2,main_values2,time_taken2= binomial_model(M,fast=True)
    
    answer.append([M,callprice1,time_taken1,time_taken2])
    
callprice2,main_values2,time_taken2= binomial_model(50,fast=True)
answer.append([50,callprice2,"Not Feasible",time_taken2])

print(tabulate(answer, ['M', 'call option price ', 'Computational time without Markov','Computational time with Markov'], tablefmt='grid'), '\n')

        
        
        
        
        
        
        
       
    
    
    
    
    
    


    

