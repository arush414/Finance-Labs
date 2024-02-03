import numpy as np
import math,random
import matplotlib.pyplot as plt
from tabulate import tabulate as tab
from scipy.interpolate import CubicSpline


def funct(m,c,mu):
    cinv=np.linalg.inv(c)
    u=[1 for i in range(len(m))]
    num1 = [[1, u @ cinv @ np.transpose(m)], [mu, m @ cinv @ np.transpose(m)]]
    num2 = [[u @ cinv @ np.transpose(u), 1], [m @ cinv @ np.transpose(u), mu]]
    deno = [[u @ cinv @ np.transpose(u), u @ cinv @ np.transpose(m)], [m @ cinv @ np.transpose(u), m @ cinv @ np.transpose(m)]]
    det_1, det_2, det_d = np.linalg.det(num1), np.linalg.det(num2), np.linalg.det(deno)
    det_1 /= det_d
    det_2 /= det_d
    w = det_1 * (u @ cinv) + det_2 * (m @ cinv)
    return w

def mvp(M, C):
  u = [1 for i in range(len(M))]
  w = u @ np.linalg.inv(C) / (u @ np.linalg.inv(C) @ np.transpose(u))
  mu = w @ np.transpose(M)
  risk = math.sqrt(w @ C @ np.transpose(w))
  return risk, mu

M=[0.1,0.2,0.15]
C=[[0.005,-0.010,0.004],[-0.010,0.040,-0.002],[0.004,-0.002,0.023]]

ret=np.linspace(0,0.5,10000)
risk=[]

for mu in ret:
    w = funct(M, C, mu)
    sigma = math.sqrt(w @ C @ np.transpose(w))
    risk.append(sigma)

rmv, mumv = mvp(M, C)
ret1, risk1, ret2, risk2 = [], [], [], []

for i in range(len(ret)):
    if ret[i] >= mumv: 
        ret1.append(ret[i])
        risk1.append(risk[i])
    else:
        ret2.append(ret[i])
        risk2.append(risk[i])

plt.plot(risk1, ret1, color = 'yellow', label = 'Efficient frontier')
plt.plot(risk2, ret2, color = 'blue')
plt.xlabel("Risk (sigma)")
plt.ylabel("Returns") 
plt.title("Minimum variance line along with Markowitz Efficient Frontier")
plt.plot(rmv, mumv, color = 'green', marker = 'o')
plt.annotate('Minimum Variance Portfolio (' + str(round(rmv, 3)) + ', ' + str(round(mumv, 3)) + ')', 
            xy=(rmv, mumv), xytext=(rmv + 0.05, mumv))
plt.legend()
plt.grid(True)
plt.show()

print("\nFor Part B: \n")

rows=[]
mu10=[random.uniform(mumv,0.5) for i in range(10)]
mu10.sort()
w10=[]
for mu in mu10:
    w10.append(np.array(funct(M,C,mu)))
w10=np.array(w10)
s10=[]
for i in range(10):
    x=[]
    for j in range(3):
        x.append([w10[i][j]])
    x=np.array(x)
    s10.append(np.dot(x.T,np.dot(C,x)))
    rows.append([x.T,mu10[i],s10[i]])


table=tab(rows, ['Weights', 'Return', 'Risk'], tablefmt='grid')
print(table)

print("\nFor Part C: ")

spl=CubicSpline(risk1,ret1)
print("\nFor 15% Risk: ")
print("\nMaximum Return is : ",spl(0.15)*100," %")
print("And the corresponding weights are : ",funct(M,C,spl(0.15)))
risk2.sort()
ret2.sort(reverse=True)
spl=CubicSpline(risk2,ret2)
print("\nMinimum Return is : ",spl(0.15)*100," %")
print("And the corresponding weights are : ",funct(M,C,spl(0.15)))


print("\nFor Part D: ")

print("\nFor 18% return: ")
w18 = funct(M, C, 0.18)
sigma18 = math.sqrt(w18 @ C @ np.transpose(w18))
print("\nMinimum Risk is: ",sigma18)
print("And the corresponding weights are : ",w18)

print("\nFor Part E: ")

mu_rf = 0.1
u = np.array([1, 1, 1])

wmar = (M - mu_rf * u) @ np.linalg.inv(C) / ((M - mu_rf * u) @ np.linalg.inv(C) @ np.transpose(u) )
mumar = wmar @ np.transpose(M)
rmar = math.sqrt(wmar @ C @ np.transpose(wmar))

print("\nMarket Portfolio Weights = ", wmar)
print("Return = ", mumar)
print("Risk = ", rmar * 100 , " %")

retcml = []
rcml = np.linspace(0, 1, num = 10000)
for i in rcml:
    retcml.append(mu_rf + (mumar - mu_rf) * i / rmar)

slope, intercept = (mumar - mu_rf) / rmar, mu_rf

print("\nEquation of CML is:")
print("y = {:.3f} x + {:.3f}\n".format(slope, intercept))


plt.scatter(rmar, mumar, color = 'orange', linewidth = 3, label = 'Market portfolio')
plt.plot(risk, ret, color = 'blue', label = 'Minimum variance curve')
plt.plot(rcml, retcml, color = 'green', label = 'CML')
plt.xlabel("Risk (sigma)")
plt.ylabel("Returns") 
plt.title("Capital Market Line with Minimum variance curve")
plt.grid(True)
plt.legend()
plt.show()

print("\nFor Part F: ")

sigma = 0.1
muc = (mumar - mu_rf) * sigma / rmar + mu_rf
wrf = (muc - mumar) / (mu_rf - mumar)
wrisk = (1 - wrf) * wmar

print("\nRisk =", sigma * 100, " %")
print("Risk-free weights =", wrf)
print("Risky Weights =", wrisk)
print("Returns=", muc)

sigma = 0.25
muc = (mumar - mu_rf) * sigma / rmar + mu_rf
wrf = (muc - mumar) / (mu_rf - mumar)
wrisk = (1 - wrf) * wmar

print("\n\nRisk =", sigma * 100, " %")
print("Risk-free weights =", wrf)
print("Risky Weights =", wrisk)
print("Returns =", muc)