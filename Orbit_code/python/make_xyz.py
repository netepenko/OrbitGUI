# make a csv file for the orbit trajectories
import LT.box as B
import glob as G
import os

input_dir = '../Trajectories_GUI/MAST-U_output/gFIESTA_A1_new2.dat/'

pattern  = 'track_?????.data'

files = G.glob(input_dir + pattern)
nf = len(files)
print 'found ', nf , ' files' 

for f in files:
    print 'working on : ', f
    d = B.get_file(f)
    x = B.get_data(d, 'x')
    y = B.get_data(d, 'y')
    z = B.get_data(d, 'z')
    fo ='D:/SolidWorksFiles/AnOrganized/Bundles/Input/' + os.path.splitext(os.path.basename(f))[0]+ ".dat" 
#    os.path.splitext(f)[0]+'.dat'
    o = open(fo,'w')
    for i, xx in enumerate(x):
        yy = y[i]
        zz = z[i]
        o.write('{}  {}  {}\n'.format(xx,yy,zz))
    o.close()
# all done
