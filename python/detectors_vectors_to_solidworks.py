# -*- coding: utf-8 -*-
"""
This segment writes detectors orientations vectors in tokamak coordinate system
which then can be imported in SolidWorks using Det_Directions macro.
It is useful for geometry test.  

Created on Wed Feb 06 14:39:28 2019

@author: Alex
"""

# #################Importing Modules##################
from LT import parameterfile as PF
import LT.box as B
import numpy as np
# parse arguments
import argparse as AG
###################Defining Constants################

# Convert mm to m
mm2m = 1.e-3
# Convert degrees to radians
dtr = np.pi/180


# ###################Defining Functions##############
# get a polar angle for a 2d vector
def pol_angle(rx, ry):
    phi = np.arccos(rx/np.sqrt(rx**2+ry**2))
    # set all values where ry  < 0 to 2pi - phi
    phic = np.where(ry > 0, phi, 2.*np.pi - phi)
    #returned angle in radians
    return phic


# return the angle corresponding to these
def rotate_det(phi, theta, alpha, dphd):
    #   import pdb
    eps = 1.e-7
    phi_r = np.zeros_like(phi)
    theta_r = np.zeros_like(theta)
    
    # unit vector of detector orientation
    nx = -np.cos(phi)*np.sin(theta)
    ny = -np.sin(phi)  # changed sign
    nz = np.cos(phi)*np.cos(theta)

    # rotate for alpha around X axis
    nxr1 = nx
    nyr1 = ny*np.cos(alpha) - nz*np.sin(alpha)
    nzr1 = ny*np.sin(alpha) + nz*np.cos(alpha)

    # rotate around z axis for dphd angle
    nxr = nxr1*np.cos(-dphd) - nyr1*np.sin(-dphd)
    nyr = nxr1*np.sin(-dphd) + nyr1*np.cos(-dphd)
    nzr = nzr1
    
    # now claculate new angles
    # handle limits
    case1 = (np.abs(nzr) <= eps) & (nyr > 0.)
    case2 = (np.abs(nzr) <= eps) & (nyr < 0.)
    case3 = (np.abs(nzr) <= eps) & (np.abs(nyr) <= eps) & (nx > 0.)
    case4 = (np.abs(nzr) <= eps) & (np.abs(nyr) <= eps) & (nx < 0.)
    case5 = np.logical_not(case1 | case2 | case3 | case4)
    
    theta_r[case1] = np.pi/2.
    phi_r[case1] = 3./2.*np.pi + theta[case1]
    
    theta_r[case2] = np.pi/2.
    phi_r[case2] = np.pi/2. - theta[case2]
    
    phi_r[case3] = 0.
    theta_r[case3] = 3.*np.pi/2.
    
    theta_r[case4] = np.pi/2.
    phi_r[case4] = 0.
    
    theta_r[case5] = -np.arctan(nxr[case5]/nzr[case5])
    sphi = nyr[case5]
    cphi = nzr[case5]/np.cos(theta_r[case5])
    phi_r[case5] = pol_angle(cphi, sphi)
    
    return np.array([phi_r, theta_r])

# ########################Proper Files###############
def main(control_file, output_folder, vlen):
    global plot_command

    # open control file and read parameters
    c_file = control_file 
    cd = PF.pfile(c_file)

    dynamic_dir = cd.get_value('dynamic_dir')
    dyn_file = cd.get_value('dynamic_file')
    
    plot_command = cd.get_value('plot_command') + ' ' + c_file

##########################Obtaining Parameters and Data########################

    # Grabbing dynamic data file
    dd = B.get_file(dynamic_dir + dyn_file)
    dpar = dd.par



    
    # get the assigned detectors ids
    detector_id = B.get_data(dd, 'detector_id')
    
    # total number of detectors in dynamic file
    N_det = len(detector_id)

    # Port angle of each detector when the Reciprocating probe arm is at a rotation angle of 0, convert to rads
    ppb = B.get_data(dd, 'phi_port_base')*dtr
    
    # Theta angle of each detector when the Reciprocating
    # probe arm is at a rotation angle of 0
    # Port angle was input in degrees
    tpb = B.get_data(dd, 'theta_port_base')*dtr

    # Horizontal offset, from the center of the diagnostic, of each detector
    # Horizontal offset was input in mm
    dyo = B.get_data(dd, 'detector_horizontal_offset')*mm2m

    # Radial offset of each detector (measured from the base)
    # Radial offset was input in mm
    dro = B.get_data(dd, 'detector_radial_axis_offset')*mm2m

    # Height offset of each detector (measured from the center)
    # Height offset was input in mm
    dzo = B.get_data(dd, 'detector_height_offest')*mm2m

    # detector type (Probe or Fixed)
    det_type = B.get_data(dd, 'det_type')
    
    # Alpha is the rotational angle of the RP arm
    # converted to radians
    alpha = dpar.get_value('RP_rotation')*dtr

    
    
    ##############################Making Calculations##########################
    # indexes of fixed detectors
    fixed_dets = np.where(det_type == 'Fixed')
    
    # calculation of positions change for each Probe detector due to rotation
    dyor = np.sqrt(dyo**2 + dzo**2)*np.cos(alpha + pol_angle(dyo, dzo))
    dzor = np.sqrt(dyo**2 + dzo**2)*np.sin(alpha + pol_angle(dyo, dzo))
    
    # RDist is the distance from the center of the tokamak to each detector (m)
    RDist = np.sqrt((dpar.get_value('RDist') + dro + dpar.get_value('RDist_offset'))**2 + dyor**2)
    RDist[fixed_dets] = dro[fixed_dets]
    
    # ZDist here is the height of each detector relative to the centr of the
    # tokamak, in dynamic file ZDist is RP position hight
    ZDist = dpar.get_value('ZDist') + dzor
    ZDist[fixed_dets] = dzor[fixed_dets]
    
    #RP phd angle
    RP_phd = dpar.get_value('PHDangle')
    
    # PHD angle shift for each detector relative to RP_phd
    dphd= np.arcsin(dyor/RDist)/dtr
    
    # phdangle is the toroidal angle of each detector in radians
    phdangle = RP_phd + dphd
    phdangle[fixed_dets] = dyo[fixed_dets]

    # The following are the calculations for the change in phi and theta angles
    phi_port, theta_port = rotate_det(ppb, tpb, alpha, dphd*dtr)
    phi_port /= dtr
    theta_port /= dtr
    
    phi_port[fixed_dets] = ppb[fixed_dets]/dtr
    theta_port[fixed_dets] = tpb[fixed_dets]/dtr
    
    
    for k in range(N_det):
        geom = open(output_folder + 'track' + str(k)+ '.dat', 'w')
        xx=RDist[k]*np.cos(phdangle[k])
        yy=RDist[k]*np.sin(phdangle[k])
        zz=ZDist[k]
        
        geom.write('{}  {}  {}\n'.format(xx,yy,zz))

        print(xx, yy, zz)
        
        vx =  -vlen*np.cos(phi_port[k]*dtr)*np.sin(theta_port[k]*dtr)
        vy =  -vlen*np.sin(phi_port[k]*dtr)
        vz =   vlen*np.cos(phi_port[k]*dtr)*np.cos(theta_port[k]*dtr)

        print("V", vx, vy, vz)
        
        v1 = vx*np.cos(phdangle[k]*dtr) - vy*np.sin(phdangle[k]*dtr)
        v2 = vx*np.sin(phdangle[k]*dtr) + vy*np.cos(phdangle[k]*dtr)
        v3 = vz
        
        print("Vr", v1,v2,v3)
        xx = xx + v1
        yy = yy + v2
        zz = zz + v3
        
        print(xx, yy, zz)
        geom.write('{}  {}  {}\n'.format(xx,yy,zz))
        geom.close()

if __name__ == '__main__':
    parser = AG.ArgumentParser(description='Prepares the input and runs Orbit code',
                               formatter_class=AG.ArgumentDefaultsHelpFormatter)
    parser.add_argument("control_file", nargs = '?', help="Input control file with its location",
                        default = '../MAST-U_input/sample_input_files/control_file.data')
    args = parser.parse_args()
    c_file = args.control_file
    
    output_folder = 'D:/SolidWorksFiles/AnOrganized/Bundles/Detectors_vectors/'
    vlen = 0.1 # vector length in (m)
    main(c_file, output_folder, vlen)