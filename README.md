# OrbitGUI
Fusion products trajectories calculations GUI

The first step to run the Orbit simulation is to open the EFIT file which contains the mhd equilibrium magnetic field configuration.
Next is to select a dynamic input file to populate parameters controls which can be changed later befor running the simulation.
The short parameter descprition is available in drop down help which apperes when you leave the mouse pointer on the parameter.
To save the input parametes one can use the Save input button, it will prepare all the input files (dynamic file, static file, fixed
detectors file, control file, and orbit input nml file) based on the parameters entered and will save them in selected folder.
When Run Orbit button is pressed, the input files prepared again in case some parameters were changed, and placed in
MAST-U_input/temp folder and teh orbti code exectued with that input files. After the orbit code finishes executing, the ouput files
are placed in MAST-U_output/temp folder. If onewants to copy those files to some other directory to save them (they are being
overwriten every time the orbit runs) the Save output button is created.
