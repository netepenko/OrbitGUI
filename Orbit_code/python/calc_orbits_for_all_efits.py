# 
#


import os
import numpy
import sys

def calc_orb_efit(shot, RDist, RP_rotation):
    #shot=29975
    #t=0.5
    #RDist = 1.61
    #RP_rotation = 49 
    #------------------------------------------------------------

    allfiles = os.listdir('../MAST-U_efit/') 
    files = filter(lambda x: '_'+str(shot)+'_' in x, allfiles)
    #print files
    #print type(files)
    #sys.exit()
    times=map(lambda f: float(f.rsplit('_',1)[-1]), files)
    #nearest=min(enumerate(times), key=lambda x: abs(x[1]-t))
    #print nearest
    #efile = files[nearest[0]][1:]
    efiles = [file[1:] for file in files]
    

    #------------------------------------------------------------
    for efile in efiles:

        #open general control file and make new one in folder named by efit file
        controlf = open('../MAST-U_input/sample_control_files_set/control_file_by_efit.data').readlines()
        cfile = '../MAST-U_input/g'+efile+'/control_file.data'
        if not os.path.exists(os.path.dirname(cfile)):
            os.makedirs(os.path.dirname(cfile))
        else:
            continue
        ncontrol = open(cfile,'w+')
        ncontrol.writelines(controlf[:controlf.index('input_dir_ext = _input\n')])
        ncontrol.write('input_dir_ext = _input/g'+efile+'\n')
        ncontrol.writelines(controlf[controlf.index('input_dir_ext = _input\n')+1:controlf.index('input_file = orbit_input_file\n')])
        ncontrol.write('input_file = ' + efile + '\n')
        ncontrol.write('static_dir = ../MAST-U_input/g'+ efile +'\n')
        ncontrol.write('dynamic_dir = ../MAST-U_input/g'+ efile +'\n')
        ncontrol.writelines(controlf[controlf.index('input_file = orbit_input_file\n')+3:controlf.index('output_dir_ext = _output/\n')])
        ncontrol.write('output_dir_ext = _output/g' +'\n')
        ncontrol.writelines(controlf[controlf.index('output_dir_ext = _output/\n')+1:])
        ncontrol.close()

        #open dynamic file and save new one with changes to folder named by efit
        dynamicf = open('../MAST-U_input/sample_control_files_set/dynamic_file_by_efit.data').readlines()
        dfile = '../MAST-U_input/g'+efile+'/dynamic_file.data'
        ndfile = open(dfile, 'w+')
        ndfile.writelines(dynamicf[:dynamicf.index('#\RDist = 1.61\n')])
        ndfile.write('#\RDist = '+str(RDist)+'\n')
        ndfile.writelines(dynamicf[dynamicf.index('#\RDist = 1.61\n')+1:dynamicf.index('#\RP_rotation = 49.\n')])
        ndfile.write('#\RP_rotation = ' + str(RP_rotation)+'\n')
        ndfile.writelines(dynamicf[dynamicf.index('#\RP_rotation = 49.\n')+1:])
        ndfile.close()

        #open static file and save new one with changes to folder named by efit
        staticf = open('../MAST-U_input/sample_control_files_set/static_file_by_efit.nml').readlines()
        sfile = '../MAST-U_input/g'+efile+'/static_file.nml'
        nsfile = open(sfile, 'w+')
        nsfile.writelines(staticf[:staticf.index('    ifname =\n')])
        nsfile.write("    ifname = '"+ efile + "'\n")
        nsfile.writelines(staticf[staticf.index('    ifname =\n')+1:])
        nsfile.close()


        #run orbit code with new control file
        os.system('python run_all_par.py ' + cfile)
    return files
