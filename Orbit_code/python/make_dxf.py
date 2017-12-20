# make a dxf file for the orbit trajectories
import LT.box as B
import glob as G
import os

# import sdxf
import ezdxf

inch = 2.54

# input_dir = './NSTX_output/nml_orb3_NSTX-Case_3/'
input_dir = '../Trajectories_GUI/MAST-U_output/gFIESTA_A1_new2.dat/'

pattern  = 'track_?????.data'

files = G.glob(input_dir + pattern)
nf = len(files)
print 'found ', nf , ' files' 

idet_open = -1
drawing = None
fo = None
first = True
groups = []
names = []
# group files by detector numbers
for f in files:
    #extract detector number
    idet = int(f.split('/')[-1].split('_')[-1].split('.')[0])/10000
    new_detector = (idet != idet_open)    
    if new_detector:
        print 'new detector : ', idet
        idet_open = idet
        if not first:
            groups.append(names)
        else:
            first = False
        names = []
    names.append(f)
groups.append(names)

# create a dxf file for each detector
for i,g in enumerate(groups):
    idet = i
    drawing = ezdxf.new(dxfversion='AC1024')
    modelspace = drawing.modelspace()
    fo = 'detector_{}'.format(idet)+'.dxf'
    for f in g:
        d = B.get_file(f)
        x = B.get_data(d, 'x')*100./inch
        y = B.get_data(d, 'y')*100./inch
        z = B.get_data(d, 'z')*100./inch
        
        r = B.np.array([x,y,z]).T
        modelspace.add_polyline3d(r, dxfattribs={'color': 7})
    # save file
    drawing.saveas(fo)
# all done
