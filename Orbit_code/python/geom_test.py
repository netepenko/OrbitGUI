# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:12:16 2017

@author: Alex
"""

import LT.box as B
import numpy as np
import glob as G

dtr = np.pi/180.

pattern  = 'track_1????.data'

files = G.glob('C:/Users/Alex/Desktop/Orbit_code/Trajectories_GUI/MAST-U_output/gFIESTA_A1_new2.dat/' + pattern)

nf = len(files)
print 'found ', nf , ' files' 

plane = []
norm = []

for f in files:
#f = 'C:/Users/Alex/Desktop/Orbit_code/Trajectories_GUI/MAST-U_output/gFIESTA_A1_new2.dat/track_11111.data'

    t =  B.get_file(f)
    
    # detector position
    phi_d = 333.053784737*dtr
    theta_d = 28.3000524327*dtr
    
    # det unit vector
    #!!! this unit vector is in detector coord system,
    # need to brin it to NSTX system
    u_d = np.array([-np.cos(phi_d) * np.sin(theta_d), \
                    np.sin(phi_d),\
                    np.cos(phi_d)*np.cos(theta_d)])
    
    
    # det position vector
    zdist = 0.135165698604
    rdist = 1.61952
    phd = 1.36630675088
    #=
    
    u_d = np.array([u_d[0]*np.cos(phd)-u_d[1]*np.sin(phd), \
                    u_d[0]*np.sin(phd)+u_d[1]*np.cos(phd), \
                    u_d[2]])
    
    r_det = np.array([rdist * np.cos(phd), \
                      rdist * np.sin(phd), \
                      zdist])
    
    r_det_s=r_det + 0.1*u_d
    xt = np.array(t['x'])
    yt = np.array(t['y'])
    zt = np.array(t['z'])
    
    rt = np.array([xt,yt,zt]).T
    
    dr = rt[0]-r_det
    dr1 = rt[1] - rt[0]
    dr1_n = dr1/np.sqrt(np.dot(dr1,dr1))
    norm.append(np.dot(dr1_n, u_d))
    plane.append( np.dot(dr, u_d))
result = np.array(plane)
para = np.array(norm)




