#
# Plot orbits , combined top and side view
# This script uses the information in the dynamic_input file to assign detector id's  and color them appropriately.
# It does not use oubit_output as information source
#
# Added the mid-plane intersections to get an estimate how the midplane probed. 

import numpy as np
import LT.box as B
from LT import parameterfile as PF
from LT import pdatafile as DF
import fileinput as FI
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
import argparse as AG
import glob as G

# import scritps from files
import get_flux as gf
import get_limiter as gl
import orbit_view_data as vd


dtr = np.pi/180.

#----------------------------------------------------------------------
# find the first mid-plane crossing of trajectory v
#----------------------------------------------------------------------  
def get_zero_crossing(v):
    is_z = np.where(v.zt<=0.)[0]
    if is_z.shape[0] == 0:
        # no crossing
        return np.nan
    i_n = is_z[0]
    i_p = i_n - 1
    
    if v.rt[i_p]>1.4:
        i_p= is_z[1]-1
    
    zp = v.zt[i_p]
    rp = v.rt[i_p]
    
    zn = v.zt[i_n]
    rn = v.rt[i_n]
    m = (zp -zn)/(rp - rn)
    r0 = rn - zn/m
    return r0

#----------------------------------------------------------------------
# find effective distance of trajectory from core
#----------------------------------------------------------------------  
def get_effective_dist(v):
    sigm=0.1
    rc=0.98 # core radial position, read from efit
    num=0
    den=0
    for i in range(1,len(v.zt)):
        rfc=np.sqrt(v.zt[i]**2+(v.rt[i]-rc)**2)
        dl=np.sqrt((v.zt[i]-v.zt[i-1])**2+(v.xt[i]-v.xt[i-1])**2+(v.yt[i]-v.yt[i-1])**2)
        #exponential weight factor of distance from core
        exp=np.exp(-rfc**2/(2*sigm**2))
        num=num+rfc*dl*exp
        den=den+dl*exp        
   
    rtc_eff=num/den
    return rtc_eff

#----------------------------------------------------------------------    
# get location of magnetic axis
# would be better to find it in corresponding efit file
#----------------------------------------------------------------------  
def get_magnetic_axis(of):
    z_ok = False
    r_ok = False
    for line in FI.input(of):
        if line.find('rmaxis')>=0:
            rmaxis = float(line.split('=')[1])
            r_ok = True
        if line.find('zmaxis')>=0:
            zmaxis = float(line.split('=')[1])
            z_ok = True
        if (r_ok & z_ok):
            FI.close()
            break
    return rmaxis, zmaxis 



#----------------------------------------------------------------------    
# draw orbit in side view
#----------------------------------------------------------------------  
def plot_view_top(PDv, color = 'b', **kwargs):
    first = True
    for v in PDv:
        if first:
            pl.plot(v.xt,v.yt,  color = color, **kwargs)
            first = False
        else:
            pl.plot(v.xt,v.yt,  color = color)

#----------------------------------------------------------------------  
# draw orbit in top view
#----------------------------------------------------------------------  
def plot_view_side(PDv, color = 'b', **kwargs):
    first = True
    for v in PDv:
        if first:
            pl.plot(v.rt,v.zt, color = color, **kwargs)
            first = False
        else:
            pl.plot(v.rt,v.zt,  color = color)


def main(c_file):
    control_file=c_file



    # contpour plotting controle
    cont_scale = 1.0
    ncont = 25
    
    #colormap = pl.get_cmap('CMRmap')
    #colormap = pl.get_cmap('gnuplot')
    #colormap = pl.get_cmap('gnuplot2')
    colormap = pl.get_cmap('gist_heat')
    #colormap = pl.get_cmap('jet')
    #colormap = pl.get_cmap('hot')
    
    
    # open control file
    p_file = control_file
    pf = PF.pfile(p_file)
    
    output_dir = pf.get_value('output_dir')
    # ???
    plot_em = pf.get_value('plot_em',var_type = pf.Bool)
    # ??
    em_filled = pf.get_value('em_filled',var_type = pf.Bool)
    # ??
    plot_psirel = pf.get_value('plot_psirel',var_type = pf.Bool)
    # ??
    psirel_filled = pf.get_value('psirel_filled',var_type = pf.Bool)
    ##
    all_yellow = pf.get_value('all_yellow',var_type = pf.Bool)

    # color array
    if all_yellow:
        colors = ['y','y','y','y','y','y','y', 'y', 'y', 'y'] # make everything yellow
    else:
        colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'orange',
          'lavenderblush', 'maroon', 'plum']
    
    
    # dynamic input file for detector/channels assignment
    di_dir = pf.get_value('dynamic_dir')
    di_file = pf.get_value('dynamic_file')
    
    
    dynamic_file = di_dir + di_file 
    df = B.get_file(dynamic_file)
    dfd = df.par
    
    # get channel/detector assignement
    try:
        dn = np.array(dfd.get_value('detector_to_use').split(','), dtype = int)
    except:
        dn = np.array([int(dfd.get_value('detector_to_use'))])
    
    channel_number = B.get_data(df, 'ch')
    detector_id = B.get_data(df, 'detector_id')
    ch_touse = channel_number[np.in1d(detector_id, dn)]

    # flux grid
    try:
        flux_data_file = pf.get_value('flux_data_file')
    except:
        flux_data_file = 'flux.data'
    print 'using : ', flux_data_file, ' for flux and Em data' 
    
    # flux limiter
    try:
        flux_limiter_file = pf.get_value('flux_limiter_file')
    except:
        flux_limiter_file = 'flux_limit.data'
    print 'using : ', flux_limiter_file, ' for flux limit data' 
    
    
    # plot n-flux at mid-plane
    try:
        flux_data_file_mp = pf.get_value('flux_data_file_mp')
    except:
        flux_data_file_mp = None
    
    
    orbit_output = open(output_dir + 'orbit_output').readlines()

    # find the EQ file used:
    eq_file = 'generic'
    for d in orbit_output:
        if (d.find('--> EQ File unit, name') >= 0.):
            eq_file = d.split()[-1:][0]
    
    # flux
    print 'reading flux data'
    fl = gf.flux(output_dir + flux_data_file)
    
    print 'reading flux limit data'
    fll_d = DF.dfile(output_dir + flux_limiter_file)
    r_fll = np.array(fll_d.get_data('xlim'))
    z_fll = np.array(fll_d.get_data('ylim'))
    
    # limiter
    print 'reading limiter data'
    li = gl.limiter(output_dir + 'limiter_drawing.data')
    #orbits
    
    print 'reading orbits data'
    
    
    
    # each view can now have several trajectories
    PD_views = []
    PD_views_f = []
    PD_accept = []
    PD_channel_number = []
    PD_step = []
    for i, i_d in enumerate(dn):
        cc = ch_touse[i]

        name_patt = output_dir + '/track_{}*.data'.format(i_d)
        
        PD_view_files = G.glob(name_patt)
        
        # use the first file in the list to get some parameters used for calculating rates
        PDd = DF.pdfile(PD_view_files[0])
        PD_accept.append(PDd.par.get_value('accept'))
        PD_channel_number.append( PDd.par.get_value('channel_number', var_type = int))
        PD_step.append(PDd.par.get_value('stepsize'))
        # load the trajectories for each view
        PD_v = [ vd.view(f) for f in PD_view_files]
        PD_views_f.append(PD_view_files)
        PD_views.append(PD_v)
        print 'channel : ', cc, ', detecor : ', i_d, ' loaded'
    PD_accept = np.array(PD_accept)


    #----------------------------------------------------------------------
    # start drawing
    #----------------------------------------------------------------------
    
    draw_top_view = pf.get_value('draw_top_view',var_type = pf.Bool)
    if draw_top_view:
        f1 = pl.figure(figsize= (11,6))
#        f1=pickle.load(file('neutron.pickle_both_view'))
    else:
        f1 = pl.figure(figsize= (5,8))
    f1.text(0.1, 0.925, eq_file)
    
    # draw 3 regions
    if draw_top_view:
        li.draw_all()
    else:
        li.draw_side_all()
    
    # draw the rel. flux
    # get a nice set of contour lines
    # select the first plot
    Em_cont = None
    
    # axes = li.ax1.get_axes()
    # f1.sca( axes )
    axes = li.ax1
    f1.sca( axes )
    
    # draw the flux limit
    pl.plot(r_fll, z_fll, color = 'm', linewidth = 2.)
    
    
    if plot_em:
        Em_range = fl.Em.max() - fl.Em.min()
        Em_min = fl.Em.min() + Em_range/100.
        v = np.linspace(Em_min, fl.Em.max()*cont_scale, ncont)
        if em_filled :
            Em_cont = fl.draw_Em_filled(v, cmap = colormap)
        else:
            Em_cont = fl.draw_Em(v)
    
    if plot_psirel:
        v = np.linspace(-0.1, fl.Zrel.max(), 23)
        if psirel_filled:
            fl.draw_psirel_filled(v, cmap = colormap)
        else:
            fl.draw_psirel(v)
    
    # make a nice x-axis
    axes.xaxis.set_major_locator(MaxNLocator(4))
    
    #----------------------------------------------------------------------
    # draw orbits
    #----------------------------------------------------------------------
    # axes = li.ax1.get_axes()
    axes = li.ax1
    f1.sca( axes )
    for i, PDv in enumerate(PD_views):
        icol = dn[i]-1
        plot_view_side(PDv, color = colors[icol], label = 'Ch {0:d}'.format(dn[i]))
    
    #pl.legend(fontsize = 12,loc = 'upper left')  
    # draw  orbits into the top view
    draw_top_view=True
    if draw_top_view:
        # axes = li.ax2.get_axes()
        axes = li.ax2
        f1.sca( axes )
        # draw a few orbits
        for i, PDv in enumerate(PD_views):
            icol = dn[i]-1
            plot_view_top(PDv, color = colors[icol], label = 'Ch {0:d}'.format(dn[i]))
        # get the mid-plane emmissivity
        if plot_em:
            if (flux_data_file_mp != None):
                # load data file
                d = np.load(output_dir + '/'+flux_data_file_mp)
                X = d['X']
                Y = d['Y']
                Em_mid = d['EM_mp']
                Em_range = Em_mid.max() - Em_mid.min()
                Em_min = Em_mid.min() + Em_range/100.
                v = np.linspace(Em_min, Em_mid.max()*cont_scale, ncont)
                if em_filled :
                    Em_cont = pl.contourf(X,Y,Em_mid, v,cmap=colormap)
                else:
                    Em_cont = pl.contour(X,Y,Em_mid, v,cmap=colormap)
 
       
        pl.legend(fontsize = 12, loc = 'upper left')
# The following code plots histogram of orbits midplane intersection radii    
#    h_range =(0.0, 0.3)#(0.6, 1.6)
#    r0 = []
#    f2 = pl.figure()
#    for  i,PDv in enumerate( PD_views ):
#        icol = dn[i]-1
#        rr = []
#        for v in PDv:
#            rr.append(get_effective_dist(v))#get_zero_crossing(v))
#            
#        rr = np.array(rr)
#        r = rr.mean()
#        h = B.histo(rr, range =h_range, bins = 200)
#        h.plot(color = colors[icol])
#        print colors[icol]
#        sig_r = np.sqrt(rr.var())
#        r0.append([h, r, sig_r, rr])
#    # all done
#    pl.xlabel('R (m)')
#    pl.ylabel('counts')
#    pl.title('mid-plane Radius')
#    
#    #pl.savefig(orbit_dir+'image.png')
    pl.show()

def zoom_in(x_lim, y_lim):
    #axes = li.ax1
    pl.gcf().add_subplot(1,2,1)
    pl.xlim(x_lim)
    pl.ylim(y_lim)

def zoom_in2(x_lim, y_lim):
    #axes = li.ax2
    pl.gcf().add_subplot(1,2,2)
    pl.xlim(x_lim)
    pl.ylim(y_lim)

if __name__=='__main__':
    parser = AG.ArgumentParser()
    parser.add_argument("control_file", nargs = '?', help="Control file ", default = '../MAST-U_input/temp/control_file.data')
    args = parser.parse_args()
    p_file = args.control_file
    main(p_file)

#zoom_in((0.9,1.85),(-.6,.6));zoom_in2((.9,2.),(-.45,.65))

