import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def Lorenz63(t, y, sig, rho, beta):
# Lorenz '63 model
    out = np.zeros_like(y)
    out[0] = sig * ( y[1] - y[0] )
    out[1] = y[0] * ( rho - y[2] ) - y[1] 
    out[2] = y[0] * y[1] - beta * y[2] 
    return out 

def forwardModel_r( xt0, time, rayleigh, prandtl, b): 
#   perform integration of Lorentz63 model 
#   default integrator for solve_ivp is RK4 
    
    rho  = rayleigh
    beta = b
    sig  = prandtl 

    myParams = np.array( [sig, rho, beta], dtype=float )
    tstart = time[0]
    tend = time[-1]
    y0 = np.array( xt0, dtype=float )
    sol = solve_ivp( Lorenz63, [tstart,tend], y0, args=myParams, dense_output=True)
    xt = sol.sol(time)

    return xt
