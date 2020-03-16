import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from view import MainWindow
from utils import dialog_savefile, InformationBox, breakdown_filename
# do not change the module structure for ds_jcpds and ds_powdiff for
# retro compatibility
from ds_jcpds import JCPDS
import pymatgen as mg
import datetime
#from utils import readchi, make_filename, writechi


class MainController(object):

    def __init__(self):

        self.widget = MainWindow()
        self.model = JCPDS()
        # self.obj_color = 'white'
        self.read_setting()
        self.connect_channel()
        self.file_name = ''
        self.file_path = ''
        #
        self.clip = QtWidgets.QApplication.clipboard()
        # no more stuff can be added below

    def show_window(self):
        self.widget.show()

    def connect_channel(self):
        # connecting events
        self.widget.pushButton_ImportCIF.clicked.connect(self.import_cif)
        self.widget.pushButton_ImportJCPDS.clicked.connect(self.import_jcpds)
        self.widget.pushButton_CalculateJCPDS.clicked.connect(
            self.calculate_jcpds)
        self.widget.pushButton_WriteJCPDS.clicked.connect(self.write_jcpds)
        self.widget.pushButton_WriteDioptasJCPDS.clicked.connect(
            self.write_dioptas_jcpds)
        self.widget.pushButton_ViewInputFile.clicked.connect(
            self.view_inputfile)


    def calculate_jcpds(self):
        if self.file_name == '':
            QtWidgets.QMessageBox.warning(self.widget, "Warning",
                              "Input filename is not given.")
            return
        comment = str(self.widget.lineEdit_Comment.text())
        int_min = self.widget.doubleSpinBox_MinDsp.value()
        dsp_min = self.widget.doubleSpinBox_MinInt.value()
        self.model.version = 4
        self.read_jcpds_values()
        textoutput = self.model.write_to_string(comments = comment, \
                                 int_min = int_min, dsp_min=dsp_min, \
                                 calculate_1bar_table = True)
        infobox = InformationBox()
        infobox.setText(textoutput)
        infobox.exec_()

    def write_dioptas_jcpds(self):
        QtWidgets.QMessageBox.warning(self.widget, "Warning",
                  "This function is not yet supported.")
        return

        if self.file_name == '':
            QtWidgets.QMessageBox.warning(self.widget, "Warning",
                              "Input filename is not given.")
            return
        path, filen, ext = breakdown_filename(self.file_name)
        stamp = '-dioptas-jt'
        filen_default = os.path.join(path, filen + stamp + '.jcpds')
        filen = dialog_savefile(self.widget, filen_default)
        if filen == '':
            return
        self.model.comments = str(self.widget.lineEdit_Comment.text())
        int_min = self.widget.doubleSpinBox_MinDsp.value()
        dsp_min = self.widget.doubleSpinBox_MinInt.value()
        self.read_jcpds_values()
        self.model.write_to_dioptas_jcpds(filen, int_min=int_min, \
                                          dsp_min=dsp_min)


    def write_jcpds(self):
        if self.file_name == '':
            QtWidgets.QMessageBox.warning(self.widget, "Warning",
                              "Input filename is not given.")
            return
        path, filen, ext = breakdown_filename(self.file_name)
        if ext == '.cif':
            stamp = '-cif-jt'
        else:
            stamp = '-jt'
        filen_default = os.path.join(path, filen + stamp + '.jcpds')
        filen = dialog_savefile(self.widget, filen_default)
        if filen == '':
            return
        comment = str(self.widget.lineEdit_Comment.text())
        int_min = self.widget.doubleSpinBox_MinDsp.value()
        dsp_min = self.widget.doubleSpinBox_MinInt.value()
        self.read_jcpds_values()
        textoutput = self.model.write_to_file(filen, comments = comment, \
                                 int_min = int_min, dsp_min=dsp_min, \
                                 calculate_1bar_table = True)

    def _check_P1_in_cif(self, file):
        with open(file, 'r') as f:
            cif_data = f.readlines()
        for line in cif_data:
            if '_symmetry_space_group_name_H-M' in line:
                a = line.replace('_symmetry_space_group_name_H-M', '')
                if 'P 1' in a:
                    return False
                else:
                    return True
        return False

    def import_cif(self):
        # pymatgen version check
        mg_version = mg.__version__
        mg_version_split = mg_version.split('.')
        d_current_version = datetime.datetime(int(mg_version_split[0]),
                                              int(mg_version_split[1]),
                                              int(mg_version_split[2]))
        d_work = datetime.datetime(2019, 4, 11)

        if d_current_version < d_work:
            QtWidgets.QMessageBox.warning(
                self.widget, "Warning",
                "Update your pymatgen to newer than 2019.4.11.")
            return
        # get cif file
        file = QtWidgets.QFileDialog.getOpenFileName(
            self.widget, "Choose a CIF File", self.file_path,
            "(*.cif)")[0]
        if file == '':
            return
        self._quick_input_view(filename=file)
        not_P1 = self._check_P1_in_cif(file)
        if not not_P1:
            QtWidgets.QMessageBox.warning(
                self.widget, "Warning",
                "The CIF file is for P1 structure which cannot be processed.")
            return
        jcpds_from_cif = JCPDS()
        success = jcpds_from_cif.set_from_cif(file, 200., 4., \
                      thermal_expansion=1e-5)
        if not success:
            QtWidgets.QMessageBox.warning(
                self.widget, "Warning",
                "Conversion of your cif was not successful.\n" +  \
                "Check the cif file for space group.  It should not be P1.")
            return
        self.model = jcpds_from_cif
        self.file_path, fn, ext = breakdown_filename(file)
        self.model.comments = 'from ' + fn + ext
        self.file_name = file
        self._update_filename()
        # populate double spin boxes
        self._populate_parameters()

    def _quick_input_view(self, filename=None):
        infobox = InformationBox()
        infobox.setText(self._get_text_content(filename=filename))
        infobox.exec_()

    def view_inputfile(self):
        if self.file_name == '':
            QtWidgets.QMessageBox.warning(
                self.widget, "Warning",
                "There is no input file to show.")
            return
        self._quick_input_view()

    def _get_text_content(self, filename=None):
        if filename == None:
            filename = self.file_name
        f = open(filename, 'r')
        text = f.read()
        f.close()
        return text

    def _update_filename(self):
        self.widget.lineEdit_SourceFile.setText(self.file_name)

    def import_jcpds(self):
        file = QtWidgets.QFileDialog.getOpenFileName(
            self.widget, "Choose JPCDS Files", self.file_path,
            "(*.jcpds)")[0]
        if file == '':
            return
        self._quick_input_view(filename=file)
        jcpds = JCPDS()
        try:
            jcpds.read_file(file)
        except:
            QtWidgets.QMessageBox.warning(
                self.widget, "Warning", "JCPDS read failed.")
            return
        self.model = jcpds
        self.file_path, _, _ = breakdown_filename(file)
        self.file_name = file
        self._update_filename()
        # populate double spin boxes
        self._populate_parameters()
        # somethings to say about potential problems
        if self.model.k0 > 600.:
            QtWidgets.QMessageBox.warning(
                self.widget, "Warning",
                "K0 value of this JCPDS is abnormally high and could crash PeakPo.")
        if self.model.k0p < 1.:
            QtWidgets.QMessageBox.warning(
                self.widget, "Warning",
                "K0p value of this JCPDS is abnormally low and could crash PeakPo.")


    def _populate_parameters(self):
        self.widget.doubleSpinBox_CellParamA.setValue(self.model.a0)
        self.widget.doubleSpinBox_CellParamB.setValue(self.model.b0)
        self.widget.doubleSpinBox_CellParamC.setValue(self.model.c0)
        self.widget.doubleSpinBox_CellParamAlpha.setValue(self.model.alpha0)
        self.widget.doubleSpinBox_CellParamBeta.setValue(self.model.beta0)
        self.widget.doubleSpinBox_CellParamGamma.setValue(self.model.gamma0)
        self.widget.doubleSpinBox_K0.setValue(self.model.k0)
        self.widget.doubleSpinBox_K0p.setValue(self.model.k0p)
        self.widget.doubleSpinBox_ThermExpan.setValue(
            self.model.thermal_expansion * 1.e5)

        self.widget.lineEdit_CrystalSystem.setText(self.model.symmetry)
        self.widget.lineEdit_CrystalSystem.setReadOnly(True)
        self.widget.lineEdit_Comment.setText(self.model.comments.rstrip())
        if self.model.symmetry == 'cubic':  # cubic
            self.widget.doubleSpinBox_CellParamA.setDisabled(False)
            self.widget.doubleSpinBox_CellParamB.setDisabled(True)
            self.widget.doubleSpinBox_CellParamC.setDisabled(True)
            self.widget.doubleSpinBox_CellParamAlpha.setDisabled(True)
            self.widget.doubleSpinBox_CellParamBeta.setDisabled(True)
            self.widget.doubleSpinBox_CellParamGamma.setDisabled(True)
        elif self.model.symmetry == 'nosymmetry':  # P, d-sp input
            pass
        elif self.model.symmetry == 'hexagonal' or \
            self.model.symmetry == 'trigonal':
            self.widget.doubleSpinBox_CellParamA.setDisabled(False)
            self.widget.doubleSpinBox_CellParamB.setDisabled(True)
            self.widget.doubleSpinBox_CellParamC.setDisabled(False)
            self.widget.doubleSpinBox_CellParamAlpha.setDisabled(True)
            self.widget.doubleSpinBox_CellParamBeta.setDisabled(True)
            self.widget.doubleSpinBox_CellParamGamma.setDisabled(True)
        elif self.model.symmetry == 'tetragonal':  # tetragonal
            self.widget.doubleSpinBox_CellParamA.setDisabled(False)
            self.widget.doubleSpinBox_CellParamB.setDisabled(True)
            self.widget.doubleSpinBox_CellParamC.setDisabled(False)
            self.widget.doubleSpinBox_CellParamAlpha.setDisabled(True)
            self.widget.doubleSpinBox_CellParamBeta.setDisabled(True)
            self.widget.doubleSpinBox_CellParamGamma.setDisabled(True)
        elif self.model.symmetry == 'orthorhombic':  # orthorhombic
            self.widget.doubleSpinBox_CellParamA.setDisabled(False)
            self.widget.doubleSpinBox_CellParamB.setDisabled(False)
            self.widget.doubleSpinBox_CellParamC.setDisabled(False)
            self.widget.doubleSpinBox_CellParamAlpha.setDisabled(True)
            self.widget.doubleSpinBox_CellParamBeta.setDisabled(True)
            self.widget.doubleSpinBox_CellParamGamma.setDisabled(True)
        elif self.model.symmetry == 'monoclinic':  # monoclinic
            self.widget.doubleSpinBox_CellParamA.setDisabled(False)
            self.widget.doubleSpinBox_CellParamB.setDisabled(False)
            self.widget.doubleSpinBox_CellParamC.setDisabled(False)
            self.widget.doubleSpinBox_CellParamAlpha.setDisabled(True)
            self.widget.doubleSpinBox_CellParamBeta.setDisabled(False)
            self.widget.doubleSpinBox_CellParamGamma.setDisabled(True)
        elif self.model.symmetry == 'triclinic':  # triclinic
            self.widget.doubleSpinBox_CellParamA.setDisabled(False)
            self.widget.doubleSpinBox_CellParamB.setDisabled(False)
            self.widget.doubleSpinBox_CellParamC.setDisabled(False)
            self.widget.doubleSpinBox_CellParamAlpha.setDisabled(False)
            self.widget.doubleSpinBox_CellParamBeta.setDisabled(False)
            self.widget.doubleSpinBox_CellParamGamma.setDisabled(False)
        # disable edit depending on symmetry

    def read_jcpds_values(self):
        self.model.k0 = self.model.k0 = self.widget.doubleSpinBox_K0.value()
        self.model.k0p = self.widget.doubleSpinBox_K0p.value()
        self.model.thermal_expansion = \
            self.widget.doubleSpinBox_ThermExpan.value() * 1.e-5

        if self.model.symmetry == 'cubic':  # cubic
            self.model.a0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.b0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.c0 = self.widget.doubleSpinBox_CellParamA.value()
        elif self.model.symmetry == 'nosymmetry':  # P, d-sp input
            pass
        elif self.model.symmetry == 'hexagonal' or \
            self.model.symmetry == 'trigonal':
            self.model.a0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.b0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.c0 = self.widget.doubleSpinBox_CellParamC.value()
        elif self.model.symmetry == 'tetragonal':  # tetragonal
            self.model.a0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.b0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.c0 = self.widget.doubleSpinBox_CellParamC.value()
        elif self.model.symmetry == 'orthorhombic':  # orthorhombic
            self.model.a0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.b0 = self.widget.doubleSpinBox_CellParamB.value()
            self.model.c0 = self.widget.doubleSpinBox_CellParamC.value()
        elif self.model.symmetry == 'monoclinic':  # monoclinic
            self.model.a0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.b0 = self.widget.doubleSpinBox_CellParamB.value()
            self.model.c0 = self.widget.doubleSpinBox_CellParamC.value()
            self.model.beta0 = self.widget.doubleSpinBox_CellParamBeta.value()
        elif self.model.symmetry == 'triclinic':  # triclinic
            self.model.a0 = self.widget.doubleSpinBox_CellParamA.value()
            self.model.b0 = self.widget.doubleSpinBox_CellParamB.value()
            self.model.c0 = self.widget.doubleSpinBox_CellParamC.value()
            self.model.alpha0 = \
                self.widget.doubleSpinBox_CellParamAlpha.value()
            self.model.beta0 = self.widget.doubleSpinBox_CellParamBeta.value()
            self.model.gamma0 = \
                self.widget.doubleSpinBox_CellParamGamma.value()

    def write_setting(self):
        """
        Write default setting
        """
        # self.settings = QtCore.QSettings('DS', 'PeakPo')
        self.settings = QtCore.QSettings('DS', 'JCPDSTools')
        # print('write:' + self.model.chi_path)
        self.settings.setValue('jcpds_path', self.file_path)

    def read_setting(self):
        """
        Read default setting
        """
        self.settings = QtCore.QSettings('DS', 'JCPDSTools')
        # self.settings.setFallbacksEnabled(False)
        self.file_path = self.settings.value('file_path')
