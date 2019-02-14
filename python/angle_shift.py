# -*- coding: utf-8 -*-
"""
Script to check the angle advance if the trajectories calculation starts from detector 
compared to from outer collimator
Created on Thu Jan 11 11:40:38 2018

@author: Alex
"""


import LT.box as B
import numpy as np
import glob as G

dtr = np.pi/180.

pattern  = 'track_1????.data'

files_c = G.glob('C:/Users/Alex/Desktop/OrbitGUI/Orbit_code/MAST-U_output/start_at_collimator/' + pattern)
files_d = G.glob('C:/Users/Alex/Desktop/OrbitGUI/Orbit_code/MAST-U_output/start_at_detector/' + pattern)

nf = len(files_c) + len(files_d)
print 'found ', nf , ' files' 

angle = []

for i,f in enumerate(files_c):
#f = 'C:/Users/Alex/Desktop/Orbit_code/Trajectories_GUI/MAST-U_output/gFIESTA_A1_new2.dat/track_11111.data'

    t_c =  B.get_file(f)
    t_d = B.get_file(files_d[i])
    
    
    xt_c = np.array(t_c['x'])
    yt_c = np.array(t_c['y'])
    zt_c = np.array(t_c['z'])
    
    rt_c = np.array([xt_c,yt_c,zt_c]).T
    
    xt_d = np.array(t_d['x'])
    yt_d = np.array(t_d['y'])
    zt_d = np.array(t_d['z'])
    
    rt_d = np.array([xt_d,yt_d,zt_d]).T
    
    dr_c = rt_c[1] - rt_c[0]
    dr_d = rt_d[-1] - rt_d[-2]
    dr_cn = dr_c/np.sqrt(np.dot(dr_c,dr_c))
    dr_dn = dr_d/np.sqrt(np.dot(dr_d,dr_d))
    
    angle.append(np.arccos(np.dot(dr_cn,dr_dn))/dtr)
result=np.array(angle)
print result.max()
print result.mean()
#h = B.histo(result, bins=20)
#h.plot()