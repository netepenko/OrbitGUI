#
# run the orbit code using the namelist version
#
# essential parameters are controlled using a parameter file
#
import shutil as SU
import os
import sys
import argparse as AG
from LT import parameterfile as PF

#handling symbolic links on Windows
__CSL = None
def symlink(source, link_name):
    '''symlink(source, link_name)
       Creates a symbolic link pointing to source named link_name'''
    if '\\' not in source:
        source=source.replace('/',"\\")
    if '\\' not in link_name:
        link_name=link_name.replace('/',"\\")
    global __CSL
    if __CSL is None:
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        __CSL = csl
    flags = 0
    if source is not None and os.path.isdir(source):
        flags = 1
    if __CSL(link_name, source, flags) == 0:
        raise ctypes.WinError()



# run the command written in string 'cmd' and put the output into a file name
# stored in 'out_file' and the error output into a file stored in 'err_file'
# if the program run reads from stdin (e.g. an interactive program)
# put the answers into a argument_file, open it and pass the file like 
# my_file = open('argument_file') with the stdin=my_file keyword argument to run_command


import subprocess as su
import platform

def run_command(cmd, out_file, err_file, **kwargs):
    """Runs Oribt 3 code"""
    #print '\n', cmd, '\n', out_file, '\n', err_file
    output_f = open(out_file, "w")
    error_f = open(err_file, "w")
    #print '\n'+ str(kwargs) +'\n'
    #raw_input('in run command')
    if platform.system()=='Windows':
        cmd = cmd.replace('/', "\\")	
        subp = su.Popen(cmd, \
                        shell=True, \
                        stdout=output_f, \
                        stderr=error_f, \
                        #close_fds=True, \
                        **kwargs)
    else:
    	subp = su.Popen(cmd, \
                        shell=True, \
                        stdout=output_f, \
                        stderr=error_f, \
                        close_fds=True, \
                        **kwargs)
    subp.communicate(None)
    #raw_input('end of popen')
    error_f.close()
    output_f.close()
    return subp.returncode
#------------------------------------------------------------



# Finding and deleting orb symbolic directory. This step is necessary to avoid an error which will occur
# if run_orbit_nml.py is not fully executed. Ohterwise it gets deleted at the end of execution.
#
if os.path.exists('orb') == True:
	try:
		os.rmdir('orb')
	except:
		os.remove('orb')
	print "./orb directory has been removed."


# parsing arguments
parser = AG.ArgumentParser()
parser.add_argument("control_file", nargs = '?', help = "Control file ", default = '../MAST-U_input/temp/control_file.data')
args = parser.parse_args()


# open control file
p_file = args.control_file
pf = PF.pfile(p_file)

# read control parameters
input_dir = pf.get_value('input_dir')
input_file = pf.get_value('input_file')

output_dir = pf.get_value('output_dir')


# create output directory (if necessary)
try:
    os.mkdir(output_dir)
except:
    SU.rmtree(output_dir)
    os.mkdir(output_dir)

print '--------------------------------------------------------------'
print 'Calculation using : ', input_dir + input_file
print 'ALL output in : ', output_dir
print '--------------------------------------------------------------'


# create a symbolic link called ./orb where the default track output of orbit goes
try:
    os.symlink(output_dir, './orb')
except:
    os.symlink = symlink
    try:
        os.symlink(output_dir, '.\\orb')
    except:
        msg = sys.exc_info()[1]
        print "problem with link : ", msg
        sys.exit()

#write the command file to run orb3
o = open('orbit_input','w')
o.write( input_dir + input_file + '\n')
o.write( 'y\n')
o.close()

# run the code
command = pf.get_value('orbit_exec')
input_f = open('orbit_input')

ret = run_command(command, 'orbit_output', 'orbit_error', stdin = input_f)
errors = open('orbit_error').readlines()
input_f.close()

for l in errors:
    if l.find('Fortran runtime error:') >=0:
        print l
        sys.exit(-1)
    if l.find('No such file or directory') >0:
        print l
        sys.exit(-1)

try:
    # copy the important data file ro the standard  output directory    
    SU.copy('orbits.data', output_dir + 'orbits.data')
    SU.copy('orbit_output', output_dir + 'orbit_output')
    SU.copy('orbit_input', output_dir + 'orbit_input')
    SU.copy('orbit_error', output_dir + 'orbit_error')
    #SU.copy('collimator.data',output_dir + '/collimator.data')
except:
    print '--------------------------------------------------------------'
    print 'problem running orbit'
    print '--------------------------------------------------------------'
    sys.exit(-1)

try:
    SU.copy(input_dir + input_file, output_dir)
    SU.copy('flux.data', output_dir + 'flux.data')
    SU.copy('flux_limit.data', output_dir + 'flux_limit.data')
    SU.copy('limiter_drawing.data', output_dir + 'limiter_drawing.data')
    SU.copy('fort.8', output_dir + 'fort.8')
except:
    print '--------------------------------------------------------------'
    print 'problem with flux data (orbit)'
    print '--------------------------------------------------------------'
    sys.exit(-1)

#remove temp. files
os.remove('./orbits.data')	
os.remove('./orbit_output')
os.remove('./orbit_input')
os.remove('./orbit_error')
os.remove('./collimator.data')

#for windows backslashes used
try:
    os.rmdir('.\\orb') 
except:
    os.remove('./orb')

os.remove('./flux.data')
os.remove('./flux_limit.data')
os.remove('./limiter_drawing.data')
os.remove('./fort.8')

