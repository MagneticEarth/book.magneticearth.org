import numpy as np
from forwardModel import *

def myEnKF( n_steps, dt, nobs, time_obs, gap, Ne, H, R, y, x0, P0, rayleigh, prandtl, b): 
# Implementation of the ensemble Kalman filter 
# 
# See e.g. Evensen, Ocean Dynamics (2003), Eqs. 44--54
# 

    x     = np.zeros( (3,   nobs+1), dtype=float ) 
    x_ave  = np.zeros( (3,n_steps+1), dtype=float )
    x_ens  = np.zeros( (3,n_steps+1,Ne), dtype=float )
    D     = np.zeros( (np.shape(H)[0], Ne), dtype=float )
    Xe    = np.zeros( (3, Ne), dtype=float )
    Xp    = np.zeros_like( Xe )
    sR    = np.sqrt(R)
    sP    = np.sqrt(P0)

    # construct initial ensemble 
    Xe =    np.transpose([x0,] * Ne)  + np.dot(sP,  np.random.normal( loc=0., scale=1.0, size=(3,Ne) ))
    x[:,0] = np.mean( Xe, axis=1 )
    one_over_Ne_minus_one = 1./ (Ne -1.) 
    one_over_Ne = 1. / Ne 
#
    current_time = 0
    for iobs in range(nobs+1):
        istart = iobs*gap
        istop  = istart + gap+1
        running_mean = np.zeros( (3, gap+1), dtype=float)
        time_fw = np.linspace(current_time, time_obs[iobs], gap+1, endpoint=True)
        for e in range(Ne):
#           prediction phase for each ensemble member
            xf = forwardModel_r( Xe[:,e], time_fw, rayleigh, prandtl, b) 
            x_ens[:, istart:istop, e] = xf
            Xp[:,e] = xf[:,-1]
            running_mean = running_mean + xf
            #Noise the obs (Burgers et al, 1998)
            D[:, e] = y[:,iobs] + np.dot( sR, np.random.normal( loc=0., scale=1.0, size=(np.shape(H)[0]) )) 
        E = np.mean( Xp, axis=1) 
        A = Xp - np.transpose( [E,] * Ne ) 
        Pe = one_over_Ne_minus_one * np.dot( A, A.T) 
#       Assembly of the Kalman gain matrix 
        K = np.dot( H, np.dot(Pe,H.T) ) + R
#       Solve
        w = np.linalg.solve(K , D - np.dot(H, Xp)  )
#       Update
        Xe = Xp + np.dot( Pe, np.dot(H.T, w ) )
        running_mean = one_over_Ne * running_mean 
        x_ave[:, istart:istop] = running_mean
        current_time = time_obs[iobs]
        
    return x_ave, x_ens
    
