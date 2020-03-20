# make a csv file for the orbit trajectories
import LT.box as B
import glob as G
import os
import numpy as np
#destination folder
dest = 'C:/Users/Alex/Desktop/Tracks4Det/'
try:
    os.makedirs(dest)
except:
    print "Directory already exists, will overwrite the files in it"
#conv to inches
conv=1#39.37

def Bcheck(d):
    bphi = np.asarray(B.get_data(d, 'bphi'))
    
    return bphi.max()
    
input_dir = '../MAST-U_output/temp/'

pattern  = 'track_?????.data'

files = G.glob(input_dir + pattern)
nf = len(files)
print 'found ', nf , ' files' 
Bf=[]
for f in files:
    print 'working on : ', f
    d = B.get_file(f)
#    Bf.append(Bcheck(d))
    x = B.get_data(d, 'x')
    y = B.get_data(d, 'y')
    z = B.get_data(d, 'z')
    
    fo = dest + os.path.splitext(os.path.basename(f))[0]+ ".dat" 
#    os.path.splitext(f)[0]+'.dat'
    o = open(fo,'w+')
    for i, xx in enumerate(x):
        yy = y[i]
        zz = z[i]
        o.write('{}  {}  {}\n'.format(xx*conv,yy*conv,zz*conv))
    o.close()
# all done


