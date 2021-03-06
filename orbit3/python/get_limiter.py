# read limiter_drawing.data and setup for plot
import pdb
from LT.datafile import dfile 
import numpy as np
import matplotlib.pyplot as pl

dph = np.pi/180*0.1


def get_arc( r, phi1, phi2):
    n = int( (phi2 - phi1)/dph )
    phi = np.linspace(phi1, phi2, n)
    x = r*np.cos(phi)
    y = r*np.sin(phi)
    return (x, y)

def draw_pos(rad, phi, *args, **kwargs):
    # draw arcs 
    # pdb.set_trace()
    for i, r in enumerate(rad[:-1]):
        if r == rad[i+1] :
            # draw an arc
            x, y = get_arc(r, phi[i], phi[i+1])
        else:
            # draw a straight line
            x1 = r*np.cos(phi[i])
            y1 = r*np.sin(phi[i])
            x2 = rad[i+1]*np.cos(phi[i+1])
            y2 = rad[i+1]*np.sin(phi[i+1])
            x = np.array([x1,x2])
            y = np.array([y1,y2])
        pl.plot(x,y,*args, **kwargs)
    # all done

class limiter:
    def __init__(self,file):
        # all data have been read w/o cr and remove leading 
        # and trailing blanks
        self.data = [ l[:-1].strip() for l in open(file).readlines() ]
        nreg = 0
        counter = 0
        p_counter = 0
        polygons  = []
        l_regions = []
        r_regions = []
        midplanes = []
        add_region = False
        do_left_rz = False
        do_right_rz = False
        do_midplane = False
        do_inner = False
        do_outer = False
        do_polygon = False
#        pdb.set_trace()
        for l in self.data:
            if l.find('-region') >=0 :
                # found new region
                add_region = True
            if l.find('--polygon') >= 0:
                do_polygon = True
                p_counter += 1
                ndat = int (l.split(',')[-1].strip() )
                counter = 0
                xpos = []
                ypos = []
                continue
           
            if l.find('--midplane') >= 0:
                do_midplane = True
                ndat_mid = int (l.split(',')[-1].strip() )
                counter = 0
                xpos = []
                ypos = []
                continue
            if l.find('---inner') >= 0:
                do_inner = True
#                pdb.set_trace()
                counter = 0
                xpos = []
                ypos = []
                continue
            if l.find('---outer') >= 0:
                do_outer = True
#                pdb.set_trace()
                counter = 0
                xpos = []
                ypos = []
                continue
            # do the various things
            if add_region:
                nreg += 1
                add_region = False
                continue
            if do_polygon:
                counter += 1
                f = l.split()
                xpos.append( float(f[0]) )
                ypos.append( float(f[1]) )
                if counter >= ndat:
                    ndat = 0
                    polygons.append( [xpos, ypos] )
                    do_polygon = False
                continue
            if do_inner:
                counter += 1
                f = l.split()
                xpos.append( float(f[0]) )
                ypos.append( float(f[1]) )
                if counter >= ndat_mid:
                    midplanes.append( [xpos, ypos] )
                    do_inner = False
                continue
            if do_outer:
                counter += 1
                f = l.split()
                xpos.append( float(f[0]) )
                ypos.append( float(f[1]) )
                if counter >= ndat_mid:
                    midplanes.append( [xpos, ypos] )
                    do_outer = False
                continue
        self.midplanes = midplanes
        self.nregs = nreg
        
        self.polygons=np.array(polygons)
#        self.l_regions = np.array(l_regions)
#        self.r_regions = np.array(r_regions)
                      
    
    def draw_side(self, ireg = 0, adjust_aspect = True, *args, **kwargs):
        # draw limiter in r-z plane 
        for i in range(self.polygons.shape[0]):
            pl.plot(self.polygons[i][0], self.polygons[i][1], *args, **kwargs)
        if adjust_aspect:
            pl.axes().set_aspect('equal')
        pl.xlabel('R (m)')
        pl.ylabel('Z (m)')

    def draw_top(self, adjust_aspect = True, *args, **kwargs):
        # draw the limiter in mid-plane
        # inner
        draw_pos( self.midplanes[0][0], self.midplanes[0][1])
        # draw_outer
        draw_pos( self.midplanes[1][0], self.midplanes[1][1])
        if adjust_aspect:
            pl.axes().set_aspect('equal')
        pl.xlabel('X (m)')
        pl.ylabel('Y (m)')

    def draw_all(self):
        # draw both views
        self.ax1 = pl.subplot(1,2,1)
        for i in range(self.nregs):
            self.draw_side(ireg = i, adjust_aspect = False)
        #self.draw_side(ireg = 3, adjust_aspect = False, ls = '--')
        pl.xlabel('R (m)')
        pl.ylabel('Z (m)')
        self.ax1.set_aspect('equal')
        self.ax2 = pl.subplot(1,2,2)
        self.draw_top( adjust_aspect = False)
        pl.xlabel('X (m)')
        pl.ylabel('Y (m)')
        self.ax2.set_aspect('equal')

    def draw_side_all(self):
        # draw both views
        self.ax1 = pl.subplot(1,1,1)
        for i in range(self.nregs):
            self.draw_side(ireg = i, adjust_aspect = False)
        #self.draw_side(ireg = 3, adjust_aspect = False, ls = '--')
        pl.xlabel('R (m)')
        pl.ylabel('Z (m)')
        self.ax1.set_aspect('equal')

    def draw_top_all(self):
        # draw both views
        self.ax2 = pl.subplot(1,1,1)
        self.draw_top( adjust_aspect = False)
        pl.xlabel('X (m)')
        pl.ylabel('Y (m)')
        self.ax2.set_aspect('equal')
