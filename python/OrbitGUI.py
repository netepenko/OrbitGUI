# Graphical User Interface for running Orbit calculations
# with variable input parameters and graphical output
# athor: Aleander Netepenko


from PyQt5 import QtCore, QtWidgets, QtGui  # Python GUI module
import run_all_par as rap
import plot_orbits_combined_par as pocp
import os
import LT.box as B
import numpy as np
import shutil

n_prob = 10  # table size for detectors orientations
colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'orange',
          'lavenderblush', 'maroon', 'plum']


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Orbits calculation")
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 780, 580))
        self.tabWidget.setAutoFillBackground(True)

        self.tab = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  "Dynamic Input")

        self.efitLabel = QtWidgets.QLabel(self.tab)
        self.efitLabel.setGeometry(QtCore.QRect(40, 10, 50, 23))
        self.efitLabel.setText('EFIT File:')

        self.efitDisp = QtWidgets.QTextEdit(self.tab)
        self.efitDisp.setGeometry(QtCore.QRect(90, 10, 140, 23))
        self.efitDisp.setReadOnly(True)

        self.efitButton = QtWidgets.QPushButton(self.tab)
        self.efitButton.setGeometry(QtCore.QRect(260, 10, 120, 23))
        self.efitButton.clicked.connect(self.selecteFile)
        self.efitButton.setText('Select EFIT file')
        self.efitButton.setToolTip('Select geqdsk file (MHD equilibrium '
                                   ' magnetic field configuration)\nFile must'
                                   ' be located in MAST-U/efit folder')

        self.dynamicfButton = QtWidgets.QPushButton(self.tab)
        self.dynamicfButton.setGeometry(QtCore.QRect(450, 10, 120, 23))
        self.dynamicfButton.clicked.connect(self.selectdFile)
        self.dynamicfButton.setText('Select Dynamic file')
        self.dynamicfButton.setToolTip('Select saved file to load'
                                       ' parametes or enter them manually')

        self.saveInpBut = QtWidgets.QPushButton(self.tab)
        self.saveInpBut.setGeometry(QtCore.QRect(640, 10, 120, 23))
        self.saveInpBut.clicked.connect(self.saveInput)
        self.saveInpBut.setText('Save input')
        self.saveInpBut.setToolTip('Saves control, dynamic, static,'
                                   ' orbit3_input files into selected folder')

        self.Rdist = QtWidgets.QDoubleSpinBox(self.tab)
        self.Rdist.setGeometry(QtCore.QRect(40, 50, 150, 22))
        self.Rdist.setMinimum(0.0)
        self.Rdist.setMaximum(2.0)
        self.Rdist.setDecimals(3)
        self.Rdist.setSingleStep(0.001)
        self.Rdist.setPrefix("Rdist = ")
        self.Rdist.setSuffix(" m")
        self.Rdist.setToolTip('Radial position of reciprocating probe')

        self.Zdist = QtWidgets.QDoubleSpinBox(self.tab)
        self.Zdist.setGeometry(QtCore.QRect(40, 80, 150, 22))
        self.Zdist.setMinimum(-2.0)
        self.Zdist.setMaximum(2.0)
        self.Zdist.setSingleStep(0.1)
        self.Zdist.setPrefix("Zdist = ")
        self.Zdist.setSuffix(" m")
        self.Zdist.setToolTip('Vertical position of reciprocating probe')

        self.RProt = QtWidgets.QDoubleSpinBox(self.tab)
        self.RProt.setGeometry(QtCore.QRect(230, 50, 150, 22))
        self.RProt.setMinimum(-180)
        self.RProt.setMaximum(180)
        self.RProt.setSingleStep(1)
        self.RProt.setPrefix("RP_rotation = ")
        self.RProt.setSuffix(" deg")
        self.RProt.setToolTip('Reciprocating probe rotation angle')

        self.PHD = QtWidgets.QDoubleSpinBox(self.tab)
        self.PHD.setGeometry(QtCore.QRect(230, 80, 150, 22))
        self.PHD.setMinimum(-180)
        self.PHD.setMaximum(180)
        self.PHD.setSingleStep(1)
        self.PHD.setPrefix("PHDangle = ")
        self.PHD.setSuffix(" deg")
        self.PHD.setToolTip('Toroidal angle of the port')

        self.bfs = QtWidgets.QDoubleSpinBox(self.tab)
        self.bfs.setGeometry(QtCore.QRect(420, 50, 150, 22))
        self.bfs.setMinimum(-100)
        self.bfs.setMaximum(100)
        self.bfs.setSingleStep(1)
        self.bfs.setPrefix("bfield_scale = ")
        self.bfs.setToolTip('Scaling coefficient applied to magnetic field')

        self.trajl = QtWidgets.QDoubleSpinBox(self.tab)
        self.trajl.setGeometry(QtCore.QRect(610, 50, 150, 22))
        self.trajl.setMinimum(0.01)
        self.trajl.setMaximum(10.0)
        self.trajl.setSingleStep(0.1)
        self.trajl.setPrefix("SSTP = ")
        self.trajl.setSuffix(" m")
        self.trajl.setToolTip('Maximum orbit length in meters')
        
        self.trajs = QtWidgets.QDoubleSpinBox(self.tab)
        self.trajs.setGeometry(QtCore.QRect(610, 80, 150, 22))
        self.trajs.setMinimum(0.0001)
        self.trajs.setMaximum(0.1)
        self.trajs.setSingleStep(0.001)
        self.trajs.setDecimals(4)
        self.trajs.setPrefix("S = ")
        self.trajs.setSuffix(" m")
        self.trajs.setToolTip('Integration step size')

        self.poldir = QtWidgets.QCheckBox(self.tab)
        self.poldir.setGeometry(QtCore.QRect(420, 84, 15, 15))

        self.poldirLabel = QtWidgets.QLabel(self.tab)
        self.poldirLabel.setGeometry(QtCore.QRect(435, 80, 150, 23))
        self.poldirLabel.setText('Invert B poloidal componet')
        self.poldirLabel.setToolTip('Inverse poloidal componet of magnetic '
                                    'field\nNecessary due to some '
                                    'inconsistencies in efit files formats')

        self.rpLabel = QtWidgets.QLabel(self.tab)
        self.rpLabel.setGeometry(QtCore.QRect(40, 110, 180, 23))
        self.rpLabel.setText('Detectors positions and orientations:')

        self.runOrbitButton = QtWidgets.QPushButton(self.tab)
        self.runOrbitButton.setGeometry(QtCore.QRect(530, 500, 100, 23))
        self.runOrbitButton.clicked.connect(self.Execute)
        self.runOrbitButton.setText('Run Orbit')

        self.saveOutBut = QtWidgets.QPushButton(self.tab)
        self.saveOutBut.setGeometry(QtCore.QRect(640, 500, 120, 23))
        self.saveOutBut.clicked.connect(self.saveOutput)
        self.saveOutBut.setText('Save output')
        self.saveOutBut.setToolTip('Saves orbit output into selected folder')

#        self.drawTop = QtWidgets.QCheckBox(self.tab)
#        self.drawTop.setGeometry(QtCore.QRect(150, 500, 15, 15))
#
#        self.drawTopLable = QtWidgets.QLabel(self.tab)
#        self.drawTopLable.setGeometry(QtCore.QRect(170, 495, 150, 23))
#        self.drawTopLable.setText('Draw top view')
        

#        self.plotTrajButton = QtWidgets.QPushButton(self.tab)
#        self.plotTrajButton.setGeometry(QtCore.QRect(360, 500, 100, 23))
#        self.plotTrajButton.clicked.connect(self.plotTraj)
#        self.plotTrajButton.setText('Plot Trajectories')

        MainWindow.setCentralWidget(self.centralwidget)

        # table of detector positions
        self.posTable = QtWidgets.QTableWidget(self.tab)
        self.posTable.setRowCount(n_prob)
        self.posTable.setColumnCount(9)
        self.posTable.setGeometry(QtCore.QRect(40, 130, 720, 325))
        TableHeader = ['Color','Det_id','Ch','Phi Port Base','Theta Port','Hor. offset', 'Radial offset',
                       'Hight Offset','Type']
        self.posTable.setHorizontalHeaderLabels(TableHeader)
        self.posTable.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)
        self.posTable.verticalHeader().setVisible(False)


        # checkboxes
        self.chb = []
        for i in range(n_prob):
            self.chb.append(QtWidgets.QCheckBox(self.tab))
            self.chb[i].setGeometry(QtCore.QRect(20, 162 + int(29.7*i), 15, 15))
        # declare some attributes
        self.efitFile = ''  # name of efit file without folder and 'g' first letter
        self.dFile = ''  # dynamic file name with full path
        self.ifdir = '' # efit file directory

    def populate(self):
        # clear the tables and unselect checkboxes
        self.posTable.clearContents()
        for i in self.chb:
            i.setChecked(False)
        
        # open dynamic file and load parameters to fill in tables and controls
        dfile = self.dFile
        try:
            dd = B.get_file(dfile)
        except:
            print "Couldn't open dynamic file to load parameters inputs"
            return
        dpar = dd.par

        # Which detectors are used in the calculations
        try:
            det_use = np.array(dpar.get_value('detector_to_use').split(','),
                          dtype=int)
        except:
            det_use = np.array(int(dpar.get_value('detector_to_use')))

        # get the assigned channel numbers
        detector_id = B.get_data(dd, 'detector_id')
        
        # total number of detectors in dynamic file
        N_det = len(detector_id)
        
        # get the assigned channel numbers
        channel_number = B.get_data(dd, 'ch')
        
        # Port angle of each detector in RP ref. frame
        ppb = B.get_data(dd, 'phi_port_base')

        # Theta angle of each detector in RP ref. frame
        tpb = B.get_data(dd, 'theta_port_base')

        # Horizontal offset of each detector (in mm)
        dyo = B.get_data(dd, 'detector_horizontal_offset')

        # Radial offset of each detector (measured from the base in mm)
        dro = B.get_data(dd, 'detector_radial_axis_offset')

        # Height offset of each detector (measured from the center in mm)
        dzo = B.get_data(dd, 'detector_height_offest')
        
        # detector type (Probe or Fixed)
        det_type = B.get_data(dd, 'det_type')

        # Alpha is the rotational angle of the RP arm (in degrees)
        alpha = dpar.get_value('RP_rotation')

        # Radial position of the probe (in m)
        Rdist = dpar.get_value('RDist')

        # Radial position of the probe (in m)
        Zdist = dpar.get_value('ZDist')

        # Toroidal angle of the port
        PHDangle = dpar.get_value('PHDangle')

        

        # open static file to read some data (below is a list of possible static file locations)
        sfile=['../MAST-U_input/g' + self.efitFile.rsplit('.')[0] + '/static_file.nml', '../MAST-U_input/temp/static_file.nml',
               os.path.dirname(dfile) + '/static_file.nml', '../MAST-U_input/sample_input_files/static_file.nml']
        for sfile in sfile:
            try:
                staticf = open(sfile).readlines()
                self.static_file = sfile
                print 'Using %s for new input files preparation' %sfile
                break
            except:
                print "No static file in %s" %os.path.dirname(sfile)
        
        for line in staticf:
            if 'bfield_scale' in line:
                bfield_scale = float(line[line.find('=') + 1: line.find('!')])
            if 'IPOLDIR' in line:
                ipoldir = int(line[line.find('=') + 1: line.find('!')])
                self.poldir.setChecked(bool(ipoldir))
            if 'SSTP' in line:
                sstp = float(line[line.find('=') + 1: line.find('!')])
            if ' S =' in line:
                s = float(line[line.find('=') + 1: line.find('!')])



        # push values to their indicators on GUI
        self.Rdist.setValue(Rdist)
        self.Zdist.setValue(Zdist)
        self.RProt.setValue(alpha)
        self.PHD.setValue(PHDangle)
        self.bfs.setValue(bfield_scale)
        self.trajl.setValue(sstp)
        self.trajs.setValue(s)
        

        for i in range(N_det):
            self.posTable.setItem(i, 0, QtWidgets.QTableWidgetItem())
            self.posTable.item(i, 0).setBackground(QtGui.QColor(colors[detector_id[i]-1]))
            
            self.posTable.setItem(i, 1, QtWidgets.QTableWidgetItem(
                                          str(detector_id[i])))
            self.posTable.setItem(i, 2,
                                  QtWidgets.QTableWidgetItem(str(channel_number[i])))
            self.posTable.setItem(i, 3,
                                  QtWidgets.QTableWidgetItem(str(ppb[i])))
            self.posTable.setItem(i, 4,
                                  QtWidgets.QTableWidgetItem(str(tpb[i])))
            self.posTable.setItem(i, 5,
                                  QtWidgets.QTableWidgetItem(str(dyo[i])))
            self.posTable.setItem(i, 6,
                                  QtWidgets.QTableWidgetItem(str(dro[i])))
            self.posTable.setItem(i, 7,
                                  QtWidgets.QTableWidgetItem(str(dzo[i])))
            self.posTable.setItem(i, 8,
                                  QtWidgets.QTableWidgetItem(det_type[i]))
            if detector_id[i] in det_use:
                self.chb[i].setChecked(True)

    def selecteFile(self):
        fileDialog = QtWidgets.QFileDialog(self.centralwidget)
        fileDialog.setDirectory('../MAST-U_efit')
        efitFile = fileDialog.getOpenFileName()
        fileDialog.destroy()
        if efitFile[0] != '':
            self.ifdir = os.path.relpath(os.path.dirname(efitFile[0])).replace(os.path.sep,"/")
            self.efitFile = efitFile[0].rsplit('g', 1)[-1]
            self.efitDisp.setText(os.path.splitext(self.efitFile)[0])
            # create directories in input and output for future use
            if not os.path.exists('../MAST-U_input/g' +
                                  self.efitFile.rsplit('.')[0]):
                os.makedirs('../MAST-U_input/g' +
                            self.efitFile.rsplit('.')[0])
                os.makedirs('../MAST-U_output/g' +
                            self.efitFile.rsplit('.')[0])


    def selectdFile(self):
        if self.efitFile == '':
            self.errormsg('Please select efit file first')
            return
        fileDialog = QtWidgets.QFileDialog(self.centralwidget)
        fileDialog.setDirectory('../MAST-U_input')
        self.dFile = fileDialog.getOpenFileName()
        fileDialog.destroy()
        self.dFile = self.dFile[0]
        if self.dFile != '':
            self.populate()

    def saveInput(self):
        self.prepInput()
        fileDialog = QtWidgets.QFileDialog(self.centralwidget)
        fileDialog.setDirectory('../MAST-U_input/g' +
                                self.efitFile.rsplit('.')[0])
        directory = fileDialog.getExistingDirectory()
        fileDialog.destroy()
        if directory == '':
            return
        # copy files from temp folders to selected folder
        src_files = os.listdir('../MAST-U_input/temp')
        for file_name in src_files:
            full_file_name = os.path.join('../MAST-U_input/temp', file_name)
            if (os.path.isfile(full_file_name)) and (file_name != '.gitignore'):
                shutil.copy(full_file_name, directory)
        print 'Input files were copied to ', directory

    def saveOutput(self):
        fileDialog = QtWidgets.QFileDialog(self.centralwidget)
        fileDialog.setDirectory('../MAST-U_output/g' +
                                self.efitFile.rsplit('.')[0])
        directory = fileDialog.getExistingDirectory()
        fileDialog.destroy()
        if directory == '':
            return
        src_files = os.listdir('../MAST-U_output/temp')
        for file_name in src_files:
            full_file_name = os.path.join('../MAST-U_output/temp', file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, directory)
        print len(src_files), 'orbit output files were coppied to ', directory


    def errormsg(self, text):
        QtWidgets.QMessageBox.warning(self.centralwidget, 'Message', text)

    
    # this function prepares input files necessary to run orbit code based on inputs in GUI and put them in _input/temp folder
    def prepInput(self):
        if self.efitFile != '' and self.dFile != '':
            efile = self.efitFile
            dfile = self.dFile
        else:
            self.errormsg('Please Select EFIT file and Dynamic file')
            return

       

        # make new control file based sample and GUI inputs
        cfile_new = ('../MAST-U_input/temp/control_file.data')
        cfile = ['../MAST-U_input/g' + self.efitFile.rsplit('.')[0] + '/control_file.data', cfile_new, 
                 os.path.dirname(self.dFile) + '/control_file.data', '../MAST-U_input/sample_input_files/control_file.data']
        for cfile in cfile:
            try: 
                controlf = open(cfile).readlines()
                print 'Using %s for new input files preparation' %cfile
            except:
                print "No control file in %s" %os.path.dirname(cfile)

        ncontrol = open(cfile_new, 'w+')
        
        # write new control file
        try:
            for line in controlf:
    #            if 'N_det =' in line:
    #                ncontrol.write('N_det = ' + str(det) +
    #                               '\n')
    #                continue
                ncontrol.write(line)
        except:
            print "Couldn't prepare control file"
            return
        ncontrol.close()

         # checking for completeley filled raws in the table
        tab_lines = []
        for i in range(n_prob):
            for j in range(1,8):
                if not self.posTable.item(i, j):
                    break
                else:
                    if self.posTable.item(i, j).text() == '':
                        break
            if j == 7:
                tab_lines.append(i)

        # check which of those selected for calculations
        selected = []
        for i in tab_lines:
            if self.chb[i].isChecked():
                selected.append(int(self.posTable.item(i, 1).text()))
                
        # write new dynamic file with parameters from GUI inputs
        dfile_new = ('../MAST-U_input/temp/dynamic_file.data')
        try:
            dynamicf = open(dfile).readlines()
        except:
            self.errormsg("Something went wrong with dynamic file")
            return
        
        ndynamic = open(dfile_new, 'w+')

        for line in dynamicf:
            if '#\\' in line:
                if 'detector_to_use' in line:
                    ndynamic.write('#\ detector_to_use = ' + str(selected)[1:-1] +
                                   '\n')
                    continue
                if 'RDist' in line and 'offset' not in line:
                    ndynamic.write('#\ RDist = ' + str(self.Rdist.value()) + '\n')
                    continue
                if 'ZDist' in line:
                    ndynamic.write('#\ ZDist = ' + str(self.Zdist.value()) + '\n')
                    continue
                if 'PHDangle' in line:
                    ndynamic.write('#\ PHDangle = ' + str(self.PHD.value()) + '\n')
                    continue
                if 'RP_rotation' in line:
                    ndynamic.write('#\ RP_rotation = ' + str(self.RProt.value()) +
                                   '\n')
                    continue
                
            if '#!' in line and 'detector_id' in line:
                ndynamic.write(line)
                for i in tab_lines:
                    ndynamic.write(''.join([(self.posTable.item(i, j).text().ljust(6) + ' ' ) for j in range(1,9)]) + '\n') 
                break
            ndynamic.write(line)
        ndynamic.close()


        # open static file and save new one with changes
        sfile_new = ('../MAST-U_input/temp/static_file.nml')
        try:
            staticf = open(self.static_file).readlines()
        except:
            print 'Something went wrong with static file'
            
        nstatic = open(sfile_new, 'w+')
        for line in staticf:
            if 'ifname =' in line:
                nstatic.write(("    ifname = '%s'" %efile).ljust(40) + "! efit file name (letter 'g' omitted at the begining of the file name)\n")
                continue
            if 'ifdir =' in line:
                nstatic.write(("    ifdir = '%s'" %self.ifdir).ljust(40)  + "! directory for efit files\n")
                continue
            if 'bfield_scale =' in line:
                nstatic.write(('    bfield_scale = ' + str(self.bfs.value())).ljust(40) + '! scale factor for B-field\n')
                continue
            if 'IPOLDIR =' in line:
                nstatic.write(('    IPOLDIR = ' +
                              str(int(self.poldir.isChecked()))).ljust(40) +'! 0 do not reverse pol. field, 1 reverse poloidal field\n')
                continue
            if 'SSTP =' in line:
                nstatic.write(('    SSTP = ' + str(self.trajl.value())).ljust(40) + '! maximum orbit length in m\n')
                continue
            if ' S = ' in line:
                nstatic.write(('    S = ' + str(self.trajs.value())).ljust(40) + '! step length in m\n')
                continue
            nstatic.write(line)
        nstatic.close()
        self.cfile = cfile_new

    def Execute(self):
        try:
            self.prepInput()
        except:
            self.errormsg('Input file preparation faild.')
        try:
            rap.main(self.cfile)
        except:
            self.errormsg('Orbit execution faild.')
        try:
            pocp.main(self.cfile)
        except:
            self.errormsg('Plotting faild.')


if __name__ == "__main__":
    import sys
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
#    ui.selectFile()
#    ui.Execut()
#    ui.plotTraj()
#    ui.populate()
    sys.exit(app.exec_())
