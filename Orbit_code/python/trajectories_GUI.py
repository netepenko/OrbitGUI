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
n_prob = 8  # table size for probe detectors
n_stat = 2  # table size for fixed detectors
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
        self.efitButton.setGeometry(QtCore.QRect(240, 10, 120, 23))
        self.efitButton.clicked.connect(self.selecteFile)
        self.efitButton.setText('Select EFIT file')
        self.efitButton.setToolTip('Select geqdsk file (MHD equilibrium '
                                   ' magnetic field configuration)\nFile must'
                                   ' be located in MAST-U/efit folder')

        self.dynamicfButton = QtWidgets.QPushButton(self.tab)
        self.dynamicfButton.setGeometry(QtCore.QRect(440, 10, 120, 23))
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
        self.Rdist.setSingleStep(0.1)
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
        self.RProt.setGeometry(QtCore.QRect(210, 50, 150, 22))
        self.RProt.setMinimum(-180)
        self.RProt.setMaximum(180)
        self.RProt.setSingleStep(1)
        self.RProt.setPrefix("RP_rotation = ")
        self.RProt.setSuffix(" deg")
        self.RProt.setToolTip('Reciprocating probe rotation angle')

        self.PHD = QtWidgets.QDoubleSpinBox(self.tab)
        self.PHD.setGeometry(QtCore.QRect(210, 80, 150, 22))
        self.PHD.setMinimum(-180)
        self.PHD.setMaximum(180)
        self.PHD.setSingleStep(1)
        self.PHD.setPrefix("PHDangle = ")
        self.PHD.setSuffix(" deg")
        self.PHD.setToolTip('Toroidal angle of the port')

        self.bfs = QtWidgets.QDoubleSpinBox(self.tab)
        self.bfs.setGeometry(QtCore.QRect(380, 50, 150, 22))
        self.bfs.setMinimum(-100)
        self.bfs.setMaximum(100)
        self.bfs.setSingleStep(1)
        self.bfs.setPrefix("bfield_scale = ")
        self.bfs.setToolTip('Scaling coefficient applied to magnetic field')

        self.trajl = QtWidgets.QDoubleSpinBox(self.tab)
        self.trajl.setGeometry(QtCore.QRect(550, 50, 150, 22))
        self.trajl.setMinimum(0.01)
        self.trajl.setMaximum(10.0)
        self.trajl.setSingleStep(0.1)
        self.trajl.setPrefix("SSTP = ")
        self.trajl.setSuffix(" m")
        self.trajl.setToolTip('Maximum orbit length in meters')

        self.poldir = QtWidgets.QCheckBox(self.tab)
        self.poldir.setGeometry(QtCore.QRect(380, 84, 15, 15))

        self.poldirLabel = QtWidgets.QLabel(self.tab)
        self.poldirLabel.setGeometry(QtCore.QRect(395, 80, 150, 23))
        self.poldirLabel.setText('Invert B poloidal componet')
        self.poldirLabel.setToolTip('Inverse poloidal componet of magnetic '
                                    'field\nNecessary due to some '
                                    'inconsistencies in efit files formats')

        self.rpLabel = QtWidgets.QLabel(self.tab)
        self.rpLabel.setGeometry(QtCore.QRect(40, 110, 150, 23))
        self.rpLabel.setText('Probe detectors:')

        self.stLabel = QtWidgets.QLabel(self.tab)
        self.stLabel.setGeometry(QtCore.QRect(40, 390, 150, 23))
        self.stLabel.setText('Stationary detectors:')

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
        self.posTable.setColumnCount(8)
        self.posTable.setGeometry(QtCore.QRect(40, 130, 720, 265))
        TableHeader = ['Phi Port Base', 'Horizon. offset', 'Radial offset',
                       'Hight Offset', 'Theta Port', 'Ch', 'Det_id',
                       'Color']
        self.posTable.setHorizontalHeaderLabels(TableHeader)
        self.posTable.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)
        self.posTable.verticalHeader().setVisible(False)

        self.stTable = QtWidgets.QTableWidget(self.tab)
        self.stTable.setRowCount(n_stat)
        self.stTable.setColumnCount(8)
        self.stTable.setGeometry(QtCore.QRect(40, 410, 720, 85))
        stTableHeader = ['Rdist', 'Zdist', 'PHD angle', 'Phi Port',
                         'Theta Port', 'Ch', 'Det_id', 'Color']
        self.stTable.setHorizontalHeaderLabels(stTableHeader)
        self.stTable.verticalHeader().setVisible(False)
        self.stTable.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        # checkboxes
        self.chb = []
        for i in range(n_prob):
            self.chb.append(QtWidgets.QCheckBox(self.tab))
            self.chb[i].setGeometry(QtCore.QRect(20, 162 + 30*i, 15, 15))
        self.chb_st = []
        for i in range(n_stat):
            self.chb_st.append(QtWidgets.QCheckBox(self.tab))
            self.chb_st[i].setGeometry(QtCore.QRect(
                    20, 445 + 30*i, 15, 15))

        # declare some attributes
        self.efitFile = ''  # name of efit file without folder
        self.dFile = ''  # dynamic file name with full path

    def populate(self):
        # clear the tables and unselect checkboxes
        self.posTable.clearContents()
        self.stTable.clearContents()
        for i in self.chb:
            i.setChecked(False)
        for i in self.chb_st:
            i.setChecked(False)
        # open dynamic file and load parameters to fill in tables and controls
        dfile = self.dFile
        try:
            dd = B.get_file(dfile)
        except:
            print "Couldn't open dynamic file to load parameters inputs"

        dpar = dd.par

        # Number of detectors to be used in calculations
        detectors = dpar.get_value('detectors', var_type=int)

        # Which detectors are used in the calculations
        try:
            dn = np.array(dpar.get_value('detector_number').split(','),
                          dtype=int)
        except:
            dn = np.array(int(dpar.get_value('detector_number')))

        # Port angle of each detector when the Reciprocating probe arm
        # is at a rotation angle of 0 (in degrees)
        ppb = B.get_data(dd, 'phi_port_base')

        # Theta angle of each detector when the Reciprocating probe arm
        # is at a rotation angle of 0 (in degrees)
        tpb = B.get_data(dd, 'theta_port_base')

        # Horizontal offset of each detector (in mm)
        dxo = B.get_data(dd, 'detector_horizontal_offset')

        # Radial offset of each detector (measured from the base in mm)
        dro = B.get_data(dd, 'detector_radial_axis_offset')

        # Height offset of each detector (measured from the center in mm)
        dyo = B.get_data(dd, 'detector_height_offest')

        # Alpha is the rotational angle of the RP arm (in degrees)
        alpha = dpar.get_value('RP_rotation')

        # Radial position of the probe (in m)
        Rdist = dpar.get_value('RDist')

        # Radial position of the probe (in m)
        Zdist = dpar.get_value('ZDist')

        # Toroidal angle of the port
        PHDangle = dpar.get_value('PHDangle')

        # get the assigned channel numbers
        channel_number = B.get_data(dd, 'ch')

        # get the assigned channel numbers
        detector_id = B.get_data(dd, 'detector_id')

        # open static file to read some data
        sfile = dfile.rsplit('/', 1)[0] + '/static_file.nml'
        try:
            staticf = open(sfile).readlines()
        except:
            try:
                staticf = open('../MAST-U_input/temp/static_file.nml').readlines()
            except:
                staticf = open('../MAST-U_input/input_files_sample/static_file.nml').readlines()

        for line in staticf:
            if 'bfield_scale' in line:
                bfield_scale = float(line[line.find('=') + 1: line.find('!')])
            if 'IPOLDIR' in line:
                ipoldir = int(line[line.find('=') + 1: line.find('!')])
                self.poldir.setChecked(bool(ipoldir))
            if 'SSTP' in line:
                sstp = float(line[line.find('=') + 1: line.find('!')])

        # open file with fixed detectors positions
        try:
            st_dd = B.get_file(dfile.rsplit('/', 1)[0] +
                               '/fixed_detectors.data')
        except:
            try:
                st_dd = B.get_file('../MAST-U_input/temp/fixed_detectors.data')
            except:
                st_dd = B.get_file('../MAST-U_input/input_files_sample/fixed_detectors.data')

        st_rdist = B.get_data(st_dd, 'st_rdist')
        st_zdist = B.get_data(st_dd, 'st_zdist')
        st_phdangle = B.get_data(st_dd, 'st_phdangle')
        st_phi_port = B.get_data(st_dd, 'st_phi_port')
        st_theta_port = B.get_data(st_dd, 'st_theta_port')
        st_ch = B.get_data(st_dd, 'st_ch')
        st_detector_id = B.get_data(st_dd, 'st_detector_id')

        # push values to their indicators on GUI
        self.Rdist.setValue(Rdist)
        self.Zdist.setValue(Zdist)
        self.RProt.setValue(alpha)
        self.PHD.setValue(PHDangle)
        self.bfs.setValue(bfield_scale)
        self.trajl.setValue(sstp)

        for i in range(len(ppb)):
            self.posTable.setItem(i, 0,
                                  QtWidgets.QTableWidgetItem(str(ppb[i])))
            self.posTable.setItem(i, 1,
                                  QtWidgets.QTableWidgetItem(str(dxo[i])))
            self.posTable.setItem(i, 2,
                                  QtWidgets.QTableWidgetItem(str(dro[i])))
            self.posTable.setItem(i, 3,
                                  QtWidgets.QTableWidgetItem(str(dyo[i])))
            self.posTable.setItem(i, 4,
                                  QtWidgets.QTableWidgetItem(str(tpb[i])))
            self.posTable.setItem(i, 5,
                                  QtWidgets.QTableWidgetItem(
                                          str(channel_number[i])))
            self.posTable.setItem(i, 6,
                                  QtWidgets.QTableWidgetItem(
                                          str(detector_id[i])))
            self.posTable.setItem(i, 7, QtWidgets.QTableWidgetItem())
            self.posTable.item(i, 7).setBackground(
                    QtGui.QColor(colors[i]))
            if i + 1 in dn[0: detectors]:
                self.chb[i].setChecked(True)

        for j in range(len(st_rdist)):
            self.stTable.setItem(j, 0,
                                 QtWidgets.QTableWidgetItem(str(st_rdist[j])))
            self.stTable.setItem(j, 1,
                                 QtWidgets.QTableWidgetItem(str(st_zdist[j])))
            self.stTable.setItem(j, 2,
                                 QtWidgets.QTableWidgetItem(
                                         str(st_phdangle[j])))
            self.stTable.setItem(j, 3,
                                 QtWidgets.QTableWidgetItem(
                                         str(st_phi_port[j])))
            self.stTable.setItem(j, 4,
                                 QtWidgets.QTableWidgetItem(
                                         str(st_theta_port[j])))
            self.stTable.setItem(j, 5,
                                 QtWidgets.QTableWidgetItem(str(st_ch[j])))
            self.stTable.setItem(j, 6,
                                 QtWidgets.QTableWidgetItem(
                                         str(st_detector_id[j])))
            self.stTable.setItem(j, 7, QtWidgets.QTableWidgetItem())
            self.stTable.item(j, 7).setBackground(
                    QtGui.QColor(colors[j + len(ppb)]))
            if j + 1 + len(ppb) in dn[0: detectors]:
                self.chb_st[j].setChecked(True)

    def selecteFile(self):

        fileDialog = QtWidgets.QFileDialog(self.centralwidget)
        fileDialog.setDirectory('../MAST-U_efit')
        self.efitFile = fileDialog.getOpenFileName()
        fileDialog.destroy()
        if self.efitFile[0] != '':
            self.efitFile = self.efitFile[0].rsplit('g', 1)[-1]
            self.efitDisp.setText(os.path.splitext(self.efitFile)[0])
            if not os.path.exists('../MAST-U_input/g' +
                                  self.efitFile.rsplit('.')[0]):
                os.makedirs('../MAST-U_input/g' +
                            self.efitFile.rsplit('.')[0])
                os.makedirs('../MAST-U_output/g' +
                            self.efitFile.rsplit('.')[0])

        else:
            self.efitFile = ''

    def selectdFile(self):

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
            if (os.path.isfile(full_file_name)):
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

    def plotTraj(self):
        try:
            pocp.main(self.cfile)
        except:
            self.errormsg('Please Run Orbit first')

    def errormsg(self, text):
        QtWidgets.QMessageBox.warning(self.centralwidget, 'Message', text)

    # this procedure prepares input files to run orbit code based on inputs
    # in GUI
    def prepInput(self):
        if self.efitFile != '' and self.dFile != '':
            efile = self.efitFile
            dfile = self.dFile
        else:
            self.errormsg('Please Select EFIT file and Dynamic file')
            return

        # checking how many completeley filled raws in eahc table
        pdet = 0
        fdet = 0
        for i in range(n_prob):
            for j in range(7):
                if not self.posTable.item(i, j):
                    break
                else:
                    if self.posTable.item(i, j).text() == '':
                        break
            if j == 6:
                pdet += 1

        for i in range(n_stat):
            for j in range(7):
                if not self.stTable.item(i, j):
                    break
                else:
                    if self.stTable.item(i, j).text() == '':
                        break
            if j == 6:
                fdet += 1
        det = pdet + fdet
        selected = []
        # check which of those selected for calculations
        for i in range(pdet):
            if self.chb[i].isChecked():
                selected.append(i + 1)
        for i in range(fdet):
            if self.chb_st[i].isChecked():
                selected.append(i + 1 + pdet)
        detectors = len(selected)
        # add the rest to the list, necessary due to the orbit input structure
        for i in range(det):
            if i + 1 not in selected:
                selected.append(i + 1)

        # open control_file_sample and fill in necessary inputs
        cfile_new = ('../MAST-U_input/temp/control_file.data')
        try:
            controlf = open(os.path.dirname(self.dFile) +
                           '/control_file.data').readlines()
        except:
            try:
                controlf = open(cfile_new).readlines()
            except:
                controlf = open('../MAST-U_input/input_files_sample/control_file.data').readlines()

        ncontrol = open(cfile_new, 'w+')
        for line in controlf:
            if 'N_det =' in line:
                ncontrol.write('N_det = ' + str(det) +
                               '\n')
                continue
            ncontrol.write(line)
        ncontrol.close()

        # write new dynamic file with parameters from GUI inputs
        dfile_new = ('../MAST-U_input/temp/dynamic_file.data')
        try:
            dynamicf = open(dfile).readlines()
        except:
            try:
                dynamicf = open(dfile_new).readlines()
            except:
                dynamicf = open('../MAST-U_input/input_files_sample/dynamic_file.data').readlines()
        ndynamic = open(dfile_new, 'w+')

        for line in dynamicf:
            if '#\detectors =' in line:
                ndynamic.write('#\detectors = ' +
                               str(detectors) + '\n')
                continue
            if '#\detector_number =' in line:
                ndynamic.write('#\detector_number = ' + str(selected)[1:-1] +
                               '\n')
                continue
            if '#\RDist =' in line:
                ndynamic.write('#\RDist = ' + str(self.Rdist.value()) + '\n')
                continue
            if '#\ZDist =' in line:
                ndynamic.write('#\ZDist = ' + str(self.Zdist.value()) + '\n')
                continue
            if '#\PHDangle =' in line:
                ndynamic.write('#\PHDangle = ' + str(self.PHD.value()) + '\n')
                continue
            if '#\RP_rotation =' in line:
                ndynamic.write('#\RP_rotation = ' + str(self.RProt.value()) +
                               '\n')
                continue
            if '#! phi_port_base[f,0]/' in line:
                ndynamic.write(line)
                for i in range(pdet):
                    ndynamic.write(self.posTable.item(i, 0).text() + ' ' +
                                   self.posTable.item(i, 1).text() + ' ' +
                                   self.posTable.item(i, 2).text() + ' ' +
                                   self.posTable.item(i, 3).text() + ' ' +
                                   self.posTable.item(i, 4).text() + ' ' +
                                   self.posTable.item(i, 5).text() + ' ' +
                                   self.posTable.item(i, 6).text() + '\n')

                break
            ndynamic.write(line)
        ndynamic.close()

        # write new fixed detectors file
        fdf = open('../MAST-U_input/temp/fixed_detectors.data', 'w+')
        fdf.write('#! st_rdist[f,0]/ st_zdist[f,1]/ st_phdangle[f,2]/'
                  ' st_phi_port[f,3]/ st_theta_port[f,4]/ st_ch[i,5]/'
                  ' st_detector_id[i,6]/\n')

        for i in range(fdet):
            fdf.write(self.stTable.item(i, 0).text() + ' ' +
                      self.stTable.item(i, 1).text() + ' ' +
                      self.stTable.item(i, 2).text() + ' ' +
                      self.stTable.item(i, 3).text() + ' ' +
                      self.stTable.item(i, 4).text() + ' ' +
                      self.stTable.item(i, 5).text() + ' ' +
                      self.stTable.item(i, 6).text() + '\n')
        fdf.close()
        # open static file and save new one with changes

        sfile_new = ('../MAST-U_input/temp/static_file.nml')
        try:
            staticf = open(os.path.dirname(self.dFile) +
                           '/static_file.nml').readlines()
        except:
            try:
                staticf = open(sfile_new).readlines()
            except:
                staticf = open('../MAST-U_input/input_files_sample/static_file.nml').readlines()

        nstatic = open(sfile_new, 'w+')
        for line in staticf:
            if 'ifname =' in line:
                nstatic.write("    ifname = '" + efile + "'\n")
                continue
            if 'bfield_scale =' in line:
                nstatic.write('    bfield_scale = ' + str(self.bfs.value()) +
                              '                 ! scale factor for B-field\n')
                continue
            if 'IPOLDIR =' in line:
                nstatic.write(' IPOLDIR = ' +
                              str(int(self.poldir.isChecked())) +
                              '                    ! 0 do not reverse pol.' +
                              'field, 1 reverse poloidal field\n')
                continue
            if 'SSTP =' in line:
                nstatic.write('SSTP = ' + str(self.trajl.value()) +
                              '                     ! maximum orbit length' +
                              ' in meters\n')
                continue
            nstatic.write(line)
        nstatic.close()
        self.cfile = cfile_new

    def Execute(self):
        self.prepInput()
        rap.main(self.cfile)
        self.plotTraj()


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
