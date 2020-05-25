#!/usr/bin/env python
# coding: utf-8

# In[45]:


# SIR model showing progression of disease through a population 
# to be modeled on an annealing quantum computer

#
#    @2020 Alex Khan. All rights reserved
#    
#    This model is not indented to accurately predict or simulate real results
#    the goal is to create a simplifed version that can then be modeled on
#    an annealing quantum computer through a QUBO

#    This code simulates the movement of the disease over a distance x[0] to x[end]

#    Acknowledgements:
#    The original formula and code was taken from 
#    https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
#    The SIR model differential equations:
#    def deriv(y, t, N, beta, gamma):
#    S, I, R = y
#    dSdt = -beta * S * I / N
#    dIdt = beta * S * I / N - gamma * I
#    dRdt = gamma * I
#    return dSdt, dIdt, dRdt
#    equations describing this model were first derived by Kermack and McKendrick [Proc. R. Soc. A, 115, 772 (1927)

#    More information on the formula and code is described 
#    by David Smith and Lang Moore
#    and can be found at:
#    https://www.maa.org/book/export/html/115606

#    An interesting simulation and models can be found at:    
#    https://gabgoh.github.io/COVID/index.html
#    https://python.quantecon.org/sir_model.html


import numpy as np
import matplotlib.pyplot as plt
import random
end=100
x = [0] * (end)

#x[0]=1.0
c=.7
dt=.001

#### Change the time scale
tend=50
nPlots=10

printwhen=tend/dt/nPlots
printnow=0
t=0.0



Nper0 = 100
Ninf0 = 1


# Total population, N.
# If not using random population
# Initialize Population per x
N = [Nper0] * (end)

# If using random population
#N = [random.randint(50, Nper0) for x in range(0,end)]

# If using pattern population
for kk in range (0,40):
    N[kk]=100
for kk in range (41,60):
    N[kk]=100
for kk in range (61, 100):
    N[kk]=100

S=N


# Initial number of infected and recovered individuals, I0 and R0.
R = [0] * (end)
I = [0] * (end)
D = [0] * (end)
T = [0] * (end)

Rt=[]
St=[]
Dt=[]
It=[]
Tt=[]
# Everyone else, S0, is susceptible to infection initially.
#S0 = N - I0 - R0

# Where does the infection start
## comment if using random population
#S = [Nper0-Ninf0] * (end)

I[0]=Ninf0
S[0]=N[0]-Ninf0

# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 0.005, 0.06
delta=0.01
transfer_rate=0.0005


def fdSdt(S,I,N):
    if N==0:
        return(0)
    return(-beta * S * I)
    #return(-beta * S * I/N)
    

def fdSdt_tr(S,I,N):
    if N==0:
        return(0)
    return(-transfer_rate * S * I)
    #return(-transfer_rate * S * I/N)

def fdIdt(S,I,N):
    if N==0:
        return(0)
    return(beta * S * I  - gamma * I- delta * I)
    #return(beta * S * I/N  - gamma * I- delta * I)

def fdIdt_tr(S,I,N):
    if N==0:
        return(0)
    return(transfer_rate * S * I )
    #return(transfer_rate * S * I/N )
    

def fdRdt(I):
    return(gamma * I)
    

def fS(I,R,N, D):
    Sus=N-I-R-D
    if Sus<0:
        return(0)
    else:
        return(Sus)

def fDdt(I):
    return(delta*I)
    

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(R, label='Recovered')
ax.plot(S, label='Susceptible')
ax.plot(D, label='Dead')
ax.plot(I, label='Infected')
legend=ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()

#print('total:',int(N[0]),'susceptible:',int(S[0]),'infected:',int(I[0]),'recovered:',int(R[0]), 'dead:',int(D[0]))
Tstart=np.sum(S)+np.sum(I)+np.sum(R)+np.sum(D)
print('xxxxxx t, Total=',t,Tstart)
while t<tend:
    #print('======= At time=',t)
    # Run forward through the population
    for x in range (0,end):   
        #print('--- new x',x, S[x],I[x],R[x],dt)
        if N[x]>0:
            if x==0:
                
                S[x]=(S[x]+fdSdt(S[x],I[x],N[x])*dt
                          +fdSdt_tr(S[x+1],I[x+1],N[x+1])*dt)
                #print(' S',S[x])
                I[x]=(I[x]+fdIdt(S[x],I[x],N[x])*dt
                          +fdIdt_tr(S[x+1],I[x+1],N[x+1])*dt)
                #print(' x',x,'trans',trans_rate*fdIdt(S[x+1],I[x+1],N[x+1])*dt)
                #print(' I',I[x])
                R[x]=R[x]+fdRdt(I[x])*dt
                #print(' R',R[x])
                D[x]=D[x]+fDdt(I[x])*dt
                #print(' D',D[x])
                #N[x]=N[x]-fDdt(I[x])*dt
                #print(' N',N[x])
                #if N[x]<0:
                #    N[x]=0
                I[x]=I[x]-fDdt(I[x])*dt
                #print(' I',I[x])
            elif x==end-1:
                
                S[x]=(S[x]+fdSdt(S[x],I[x],N[x])*dt
                          +fdSdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                #print(S[n])
                I[x]=(I[x]+fdIdt(S[x],I[x],N[x])*dt
                          +fdIdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                #print(' x',x,'trans', trans_rate*fdIdt(S[x-1],I[x-1],N[x-1])*dt)
                #print(' I',I[x])
                R[x]=R[x]+fdRdt(I[x])*dt
                #print(' R',R[x])
                D[x]=D[x]+fDdt(I[x])*dt
                #print(' D',D[x])
                #N[x]=N[x]-fDdt(I[x])*dt
                #print(' N',N[x])
                #if N[x]<0:
                #    N[x]=0
                I[x]=I[x]-fDdt(I[x])*dt
                #print(' I',I[x])
            else:
                
                S[x]=(S[x]+fdSdt(S[x],I[x],N[x])*dt
                          +fdSdt_tr(S[x+1],I[x+1],N[x+1])*dt
                          +fdSdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                #print('x=',x,I[x])
                I[x]=(I[x]+fdIdt(S[x],I[x],N[x])*dt
                          +fdIdt_tr(S[x+1],I[x+1],N[x+1])*dt
                          +fdIdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                #print(' x',x,'trans', trans_rate*fdIdt(S[x+1],I[x+1],N[x+1])*dt
                #          +trans_rate*fdIdt(S[x-1],I[x-1],N[x-1])*dt)
                #print(' I',I[x])
                R[x]=R[x]+fdRdt(I[x])*dt
                #print(' R',R[x])
                D[x]=D[x]+fDdt(I[x])*dt
                #print(' D',D[x])
                #N[x]=N[x]-fDdt(I[x])*dt
                #print(' N',N[x])
                #if N[x]<0:
                #    N[x]=0
                I[x]=I[x]-fDdt(I[x])*dt 
                #print(' I',I[x])
                #if I[x]>100:
                #if x==50:
                #    print(I[50])
                #    print(' x=',x, 'total N:',int(N[x]), 'Total SIRD', np.sum(S)+sum(I)+sum(R)+sum(D),'susceptible:',S[x],'infected:',I[x],'diff', S[x]-I[x],'recovered:',R[x], 'dead:',D[x])
                #print(' x=',x, 'total N:',int(N[x]), 'Total', np.sum(S)+sum(I)+sum(R)+sum(D),'susceptible:',int(S[x]),'infected:',int(I[x]),'recovered:',int(R[x]), 'dead:',int(D[x]))
    #print('total:',int(N[1]),'susceptible:',int(S[1]),'infected:',int(I[1]),'recovered:',int(R[1]), 'dead:',int(D[1]))        
    # Run backwards through the population
    for x in range (end-1,-1,-1):   
        #print(n, S[n],I[n],R[n],dt)
        if N[x]>0:
            if x==0:
                
                S[x]=(S[x]+fdSdt(S[x],I[x],N[x])*dt
                          +fdSdt_tr(S[x+1],I[x+1],N[x+1])*dt)
                #print(S[n])
                I[x]=(I[x]+fdIdt(S[x],I[x],N[x])*dt
                          +fdIdt_tr(S[x+1],I[x+1],N[x+1])*dt)
                R[x]=R[x]+fdRdt(I[x])*dt
                D[x]=D[x]+fDdt(I[x])*dt
                #N[x]=N[x]-fDdt(I[x])*dt
                #if N[x]<0:
                #    N[x]=0
                I[x]=I[x]-fDdt(I[x])*dt
            elif x==end-1:
                
                S[x]=(S[x]+fdSdt(S[x],I[x],N[x])*dt
                          +fdSdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                #print(S[n])
                I[x]=(I[x]+fdIdt(S[x],I[x],N[x])*dt
                          +fdIdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                R[x]=R[x]+fdRdt(I[x])*dt
                D[x]=D[x]+fDdt(I[x])*dt
                #N[x]=N[x]-fDdt(I[x])*dt
                #if N[x]<0:
                #    N[x]=0
                I[x]=I[x]-fDdt(I[x])*dt
            else:
                
                S[x]=(S[x]+fdSdt(S[x],I[x],N[x])*dt
                          +fdSdt_tr(S[x+1],I[x+1],N[x+1])*dt
                          +fdSdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                #print('x=',x,I[x])
                I[x]=(I[x]+fdIdt(S[x],I[x],N[x])*dt
                          +fdIdt_tr(S[x+1],I[x+1],N[x+1])*dt
                          +fdIdt_tr(S[x-1],I[x-1],N[x-1])*dt)
                R[x]=R[x]+fdRdt(I[x])*dt
                D[x]=D[x]+fDdt(I[x])*dt
                #N[x]=N[x]-fDdt(I[x])*dt
                #if N[x]<0:
                #    N[x]=0
                I[x]=I[x]-fDdt(I[x])*dt 
        T[x]=S[x]+I[x]+R[x]+D[x]
        #S[x]=fS(I[x],R[x],N[x])
    Tt.append(np.sum(S)+np.sum(I)+np.sum(R)+np.sum(D))
    St.append(np.sum(S))
    It.append(np.sum(I))
    Rt.append(np.sum(R))
    Dt.append(np.sum(D))
    
    #print('xxxxxx t, Total=',t,Tend, 'Difference=',Tmid-Tstart, 'Deaths', np.sum(D))
    #print('total:',int(N[1]),'susceptible:',int(S[1]),'infected:',int(I[1]),'recovered:',int(R[1]), 'dead:',int(D[1]))            
    #print(printnow)
    if (printnow==printwhen):
        
        plt.plot(I)
        
        printnow=0
    printnow+=1
    t+=dt
Tend=np.sum(S)+np.sum(I)+np.sum(R)+np.sum(D)
#print('xxxxxx t, Total=',t,Tend, 'Difference=',Tend-Tstart, 'Deaths', np.sum(D))
    #print('xxxxxx t, Total=',t,np.sum(S)+sum(I)+sum(R)+sum(D))
plt.show()   
# Plot    
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(R, label='Recovered')
ax.plot(S, label='Susceptible')
ax.plot(D, label='Dead')
ax.plot(I, label='Infected')
ax.plot(T, label='Total')
legend=ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
print('This plot has distance on the horizontal axis')
print('Time:', t)
print('Total Population: ', Tend)
print('Total Deaths:     ', np.sum(D))
print('Total Infected:   ', np.sum(I))
print('Total Recovered:  ', np.sum(R))


fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(Rt, label='Recovered')
ax.plot(St, label='Susceptible')
ax.plot(Dt, label='Dead')
ax.plot(It, label='Infected')
ax.plot(Tt, label='Total')
legend=ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
print('This plot has time on the horizontal axis')

# A grid of time points (in days)
#t = np.linspace(0, 160, 160)
# Plot the data on three separate curves for S(t), I(t) and R(t)
#fig = plt.figure(facecolor='w')
#ax = fig.add_subplot(111, axis_bgcolor='#dddddd', axisbelow=True)
#ax = fig.add_subplot(111, axisbelow=True)
#ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
#ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
#ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
#ax.set_xlabel('Time /days')
#ax.set_ylabel('Number (1000s)')
#ax.set_ylim(0,1.2)
#ax.yaxis.set_tick_params(length=0)
#ax.xaxis.set_tick_params(length=0)
#ax.grid(b=True, which='major', c='w', lw=2, ls='-')
#legend = ax.legend()
#legend.get_frame().set_alpha(0.5)
#for spine in ('top', 'right', 'bottom', 'left'):
#    ax.spines[spine].set_visible(False)
#plt.show()


# In[ ]:





# In[ ]:




