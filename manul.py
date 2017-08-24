#!/opt/anaconda4/bin/python
"""
Sergey Tomin. XFEL/DESY, 2017.
"""
#QT imports
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox, QMainWindow, QDialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
#normal imports
import numpy as np
#import epics
import sys
import os


path = os.path.realpath(__file__)
indx = path.find("manul")
print("PATH", os.path.realpath(__file__), path[:indx])
sys.path.append(path[:indx])
if sys.version_info[0] == 2:
    from imp import reload
else:
    from importlib import reload
import time
import pyqtgraph as pg
from gui.gui_main import *
from orbit import OrbitInterface
from lattices.xfel_i1_mad import *
from lattices.xfel_l1_mad import *
from lattices.xfel_l2_mad import *
#from lattices.xfel_l3_mad import *
from lattices.xfel_l3_no_cl import *
from lattices.xfel_cl import *
from lattices.xfel_tld_892 import *
from lattices.xfel_sase1_mad import *
from lattices.xfel_sase3_mad import *
from ocelot import *
from ocelot.gui.accelerator import *
from ocelot.cpbd.track import *
from ocelot.optimizer.mint.xfel_interface import *

from ocelot.optimizer.mint.opt_objects import Device
from ocelot.optimizer.mint.xfel_interface import *
import copy
from scipy import optimize
from devices import *
from dispersion import *

class ManulInterfaceWindow(QMainWindow):
    """ Main class for the GUI application """
    def __init__(self):
        """
        Initialize the GUI and QT UI aspects of the application.
        Initialize the scan parameters.
        Connect start and logbook buttons on the scan panel.
        Initialize the plotting.
        Make the timer object that updates GUI on clock cycle during a scan.
        """
        # PATHS
        self.dev_mode = True

        path = os.path.realpath(__file__)
        indx = path.find("ocelot" + os.sep + "optimizer")
        self.path2ocelot = path[:indx]
        self.path2manul = path[:path.find("manul")]

        self.optimizer_path = self.path2ocelot + "ocelot" + os.sep + "optimizer" + os.sep
        self.config_dir = self.path2ocelot + "config_optim" +os.sep
        self.gold_orbits_dir = self.path2manul + "manul" + os.sep + "golden_orbits" + os.sep
        self.gold_orbits_from_OD_dir = "/home/xfeloper/data/orbit_display/"#self.path2manul + "manul" + os.sep + "golden_orbits" + os.sep
        self.rm_files_dir = self.path2manul + "manul" + os.sep + "rm_files" + os.sep
        self.set_file = self.config_dir + "default.json" # ./parameters/default.json"
        self.obj_func_path = self.optimizer_path + "mint" + os.sep + "obj_function.py"
        self.obj_save_path = self.config_dir +  "obj_funcs" + os.sep
        # initialize
        QFrame.__init__(self)


        self.logbook = "xfellog"
        self.dev_mode = True

        #self.mi = XFELMachineInterface()
        self.mi = TestMachineInterface()

        self.ui = MainWindow(self)

        self.orbit = OrbitInterface(parent=self)
        self.dispersion = DispersionInterface(parent=self)
        self.cell_back_track = (cell_i1 + cell_l1 + cell_l2 + cell_l3_no_cl + cell_cl)

        lat = MagneticLattice(cell_l3_no_cl+cell_cl+cell_sase1, start=bpmr_1307_l3, stop=qa_2253_sa1)
        self.cl_copy = copy.deepcopy(lat.sequence)

        lat = MagneticLattice(cell_l2 + cell_l3_no_cl + cell_cl, start=engrd_419_b2, stop=mpbpmi_1693_cl)
        self.l3_copy = copy.deepcopy(lat.sequence)

        lat = MagneticLattice(cell_sase1+cell_t4, stop=ensub_2583_t4)
        self.sase1_copy = copy.deepcopy(lat.sequence)

        lat = MagneticLattice(cell_t4 + cell_sase3, start=ensub_2583_t4)
        self.sase3_copy = copy.deepcopy(lat.sequence)

        self.copy_cells = copy.deepcopy((cell_i1, cell_l1, cell_l2, cell_l3_no_cl, cell_cl,
                                         cell_i1d, cell_b1d, cell_b2d, cell_tld, cell_sase1, cell_sase3, cell_t4))

        self.big_sequence = list(flatten(cell_i1 + cell_l1 + cell_l2 + cell_l3_no_cl +
                                   cell_cl + cell_sase1 + cell_t4 + cell_sase3))

        self.online_calc = True

        #QFrame.__init__(self)
        #self.ui = UiS_Form()
        #self.ui.setupUi(self)


        #load in the dark theme style sheet
        self.loadStyleSheet()


        self.timer_live = pg.QtCore.QTimer()
        self.timer_live.timeout.connect(self.orbit.live_orbit)

        self.feedback_timer = pg.QtCore.QTimer()
        self.feedback_timer.timeout.connect(self.orbit.auto_correction)

        #timer for plots, starts when scan starts
        self.multiPvTimer = QtCore.QTimer()
        #self.multiPvTimer.timeout.connect(self.getPlotData)
        self.pvs = ["sdf","asdf"]
        #self.initTable()
        #print("quads", self.quads)
        self.add_plot()
        self.ui.cb_lattice.addItem("Arbitrary")
        self.ui.cb_lattice.addItem("I1D")
        self.ui.cb_lattice.addItem("B1D")
        self.ui.cb_lattice.addItem("B2D")
        self.ui.cb_lattice.addItem("TLD")
        self.ui.cb_lattice.addItem("I1")
        self.ui.cb_lattice.addItem("L1")
        self.ui.cb_lattice.addItem("L2")
        self.ui.cb_lattice.addItem("L3")
        self.ui.cb_lattice.addItem("CL")
        self.ui.cb_lattice.addItem("SASE1")
        self.ui.cb_lattice.addItem("T4")
        self.ui.cb_lattice.addItem("SASE3")
        self.ui.cb_lattice.addItem("up to B1")
        self.ui.cb_lattice.addItem("up to B2")
        self.ui.cb_lattice.addItem("up to TL")
        self.ui.cb_lattice.addItem("up to SASE3")
        self.ui.cb_lattice.setCurrentIndex(0)
        self.correctors_list()
        self.lat = self.return_lat()
        #self.tws0 = self.return_tws()
        #self.load_lattice()

        self.ui.pb_write.clicked.connect(self.calc_twiss)
        self.ui.pb_read.clicked.connect(self.read_quads)
        self.ui.pb_reset.clicked.connect(self.reset_quads)

        self.ui.cb_lattice.currentIndexChanged.connect(self.return_lat)
        self.ui.cb_otr55.setChecked(True)
        self.ui.cb_coupler_kick.stateChanged.connect(self.apply_coupler_kick)
        self.ui.cb_sec_order.stateChanged.connect(self.apply_second_order)
        #self.ui.pb_write.clicked.connect(self.match)
        #self.ui.pb_reload.clicked.connect(self.reload_lat)

        self.ui.sb_lat_from.editingFinished.connect(self.arbitrary_lattice)
        self.ui.sb_lat_to.editingFinished.connect(self.arbitrary_lattice)
        #self.ui.sb_lat_from.valueChanged.connect(self.arbitrary_lattice)
        #self.ui.sb_lat_to.valueChanged.connect(self.arbitrary_lattice)



    def update_table(self):
        for quad in self.quads:
            quad.ui.set_init_value(quad.kick_mrad)
            quad.ui.set_value(quad.kick_mrad)


    def reset_quads(self):
        for quad in self.quads:
            #print(quad.i_kick)
            quad.ui.set_value(quad.i_kick)
        #self.calc()

    def correctors_list(self):

        self.corr_list = []
        L = 23.2
        for elem in self.big_sequence:
            L += elem.l
            if elem.__class__ in [Hcor, Vcor]:
                elem.s_pos = L - elem.l/2.
                self.corr_list.append(elem)
        self.ui.sb_lat_from.setMaximum(L-30)
        self.ui.sb_lat_to.setMaximum(L)
        print("L_maximum", L)
        # self.lat = MagneticLattice(cell_i1 + cell_l1 + cell_l2 + cell_l3_no_cl +
        #                            cell_cl + cell_sase1 + cell_t4 + cell_sase3,
        #                            # start=start_elem, stop=stop_elem,
        #                            method=method)

    def read_quads(self):


        #if self.ui.cb_lattice.currentText() == "Arbitrary":
        #    lat_from = self.ui.sb_lat_from.value()
        #    lat_to = self.ui.sb_lat_to.value()
        #    self.ui.sb_lat_from.setValue(self.ui.sb_lat_from.minimum())
        #    self.ui.sb_lat_to.setValue(self.ui.sb_lat_to.maximum())
        #    self.arbitrary_lattice()


        self.online_calc = False
        for elem in self.quads:
            elem.kick_mrad = elem.mi.get_value()
            print("Quad."+elem.id," updated. ", "k1="+str(elem.kick_mrad)+ " mrad")
            k1 = elem.kick_mrad/elem.l*1e-3
            elem.k1 = k1
            elem.i_kick = elem.kick_mrad
            #print(elem.i_kick)
            elem.ui.set_init_value(elem.kick_mrad)
            elem.ui.set_value(elem.kick_mrad)

        for cav in self.cavs:
            try:
                v = cav.mi.get_value()
            except:
                v = 0.
            #print("Volt = ", v, cav.mi)
            cav.v = v*0.001

        self.online_calc = True
        self.lat.update_transfer_maps()
        #TODO: add in GUI option to return design twiss
        self.tws0 = self.back_tracking()
        print("back_tracking = ", self.tws0)
        tws = twiss(self.lat, self.tws0)
        beta_x = [tw.beta_x for tw in tws]
        beta_y = [tw.beta_y for tw in tws]
        dx = [tw.Dx for tw in tws]
        dy = [tw.Dy for tw in tws]
        s = [tw.s for tw in tws]

        self.update_plot(s, beta_x, beta_y, dx, dy)
        update = self.question_box("Reclculate ORM?")
        if update:
            self.orbit.calc_response_matrix(do_DRM_calc=False)
        #if self.ui.cb_lattice.currentText() == "Arbitrary":
        #    self.ui.sb_lat_from.setValue(lat_from)
        #    self.ui.sb_lat_to.setValue(lat_to)
        #    self.parent.arbitrary_lattice()
        #self.update_table()

    def back_tracking(self):
        tws0 = self.read_twiss()
        if self.ui.cb_design_tws.isChecked():
            return self.tws_des
        if self.ui.cb_otr218.isChecked():
            stop = otrb_218_b1

        elif self.ui.cb_otr450.isChecked():
            stop = otrb_450_b2

        else:
            stop = otrc_55_i1


        lat_tmp = MagneticLattice(self.cell_back_track, stop=stop)
        lat_tmp = MagneticLattice(lat_tmp.sequence[::-1])
        for elem in lat_tmp.sequence:
            if elem.__class__  == Cavity:
                elem.phi -= 180
                #print(elem.v, elem.phi)
        lat_tmp.update_transfer_maps()

        tws0.alpha_x = -tws0.alpha_x
        tws0.alpha_y = -tws0.alpha_y
        #print("start", tws0)
        tws = twiss(lat_tmp, tws0)
        #plot_opt_func(lat_tmp, tws)
        #plt.show()
        self.tws0 = Twiss()
        self.tws0.beta_x = tws[-1].beta_x
        self.tws0.beta_y = tws[-1].beta_y
        self.tws0.alpha_x = -tws[-1].alpha_x
        self.tws0.alpha_y = -tws[-1].alpha_y
        self.tws0.s = 0
        self.tws0.E = tws[-1].E
        for elem in lat_tmp.sequence:
            if elem.__class__  == Cavity:
                elem.phi += 180
        lat_tmp.update_transfer_maps()
        return self.tws0


    def read_twiss(self):
        tws = Twiss()
        if self.ui.cb_otr218.isChecked():
            section = "B1"
            tws.E = 0.7
        elif self.ui.cb_otr450.isChecked():
            section = "B2"
            tws.E = 2.4
        else:
            self.ui.cb_otr55.setChecked(True)
            section = "I1"
            tws.E = 0.130

        ch_beta_x = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_X.BETA.SA1"
        ch_alpha_x = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_X.ALPHA.SA1"
        ch_beta_y = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_Y.BETA.SA1"
        ch_alpha_y = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_Y.ALPHA.SA1"
        ch_energy = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_X.ENERGY.SA1"

        tws.beta_x = self.mi.get_value(ch_beta_x)
        tws.beta_y = self.mi.get_value(ch_beta_y)
        tws.alpha_x = self.mi.get_value(ch_alpha_x)
        tws.alpha_y = self.mi.get_value(ch_alpha_y)
        #tws.E = self.mi.get_value(ch_energy)*0.001
        print(tws)
        return tws

    def match(self):
        quads = [qi_46_i1, qi_47_i1, qi_50_i1, qi_52_i1, qi_53_i1, qi_54_i1]
        x = np.array([q.kick_mrad for q in quads])
        def error_func(x):
            #print(x)
            for i, quad in enumerate(quads):
                quad.kick_mrad = x[i]
                quad.k1 = x[i]/quad.l/1000.
            self.lat.update_transfer_maps()
            tws = twiss(self.lat, self.tws0)
            err = np.sqrt((tws[-1].beta_x - self.tws_end.beta_x)**2 +
            (tws[-1].beta_y - self.tws_end.beta_y)**2 +
            (tws[-1].alpha_x - self.tws_end.alpha_x)**2 +
            (tws[-1].alpha_y - self.tws_end.alpha_y)**2 )
            print(err)
            return err


        res = optimize.fmin(error_func, x, xtol=0.1)
        print(res)
        for i, quad in enumerate(quads):
            quad.kick_mrad = res[i]
            quad.k1 = res[i]/quad.l/1000.
            quad.ui.set_value(quad.kick_mrad)



    def apply_coupler_kick(self):
        print(self.ui.cb_coupler_kick.isChecked())
        if self.ui.cb_coupler_kick.isChecked():
            for elem in self.lat.sequence:
                if elem.__class__ == Cavity and not(".AH1." in elem.id):# and not(".A1." in elem.id):
                    elem.coupler_kick = True
                    elem.vx_up = -56.813 + 10.751j
                    elem.vy_up = -41.091 + 0.5739j
                    elem.vxx_up = 0.99943 - 0.81401j
                    elem.vxy_up = 3.4065 - 0.4146j
                    elem.vx_down = -24.014 + 12.492j
                    elem.vy_down = 36.481 +  7.9888j
                    elem.vxx_down = -4.057 - 0.1369j
                    elem.vxy_down = 2.9243 - 0.012891j
        else:
            for elem in self.lat.sequence:
                if elem.__class__ == Cavity and not(".AH1." in elem.id):# and not(".A1." in elem.id):
                    elem.coupler_kick = False
        self.lat.update_transfer_maps()
        self.calc_twiss()

        # calc orbit
        self.orbit.calc_orbit()

    def apply_second_order(self):
        print(self.ui.cb_sec_order.isChecked())
        method = MethodTM()
        if self.ui.cb_sec_order.isChecked():
            method.global_method = SecondTM
        else:
            method.global_method = TransferMap
        self.lat = MagneticLattice(self.lat.sequence, method=method)

        # calc orbit
        self.orbit.calc_orbit()

    def arbitrary_lattice(self):
        current_lat = self.ui.cb_lattice.currentText()
        if current_lat != "Arbitrary":
            return 0
        print("here")
        lat_from = self.ui.sb_lat_from.value()
        lat_to = self.ui.sb_lat_to.value()
        print("arbitrary_lattice", lat_from, lat_to)
        if lat_to - 20 < lat_from:
            self.ui.sb_lat_to.setValue(lat_from+20)
            print("set ", lat_from+20)
        self.return_lat()



    def return_lat(self):
        self.orbit.reset_undo_database()
        #self.lat = MagneticLattice(cell_i1+cell_l1)
        current_lat = self.ui.cb_lattice.currentText()
        method = MethodTM()
        method.global_method = TransferMap
        if current_lat == "B1D":
            self.lat = MagneticLattice(cell_i1 + cell_l1 + cell_b1d, method=method)

            self.tws_des = tws_i1

            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1] + self.copy_cells[5])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen + 23.2)

        elif current_lat == "Arbitrary":

            lat_from = self.ui.sb_lat_from.value()
            lat_to = self.ui.sb_lat_to.value()
            s_poss = np.array([cor.s_pos for cor in self.corr_list])
            idx_frm = (np.abs(s_poss - lat_from)).argmin()
            idx_to = (np.abs(s_poss - lat_to)).argmin()
            if idx_frm == idx_to:
                idx_to += 1
                self.ui.sb_lat_to.setValue(self.corr_list[idx_to].s_pos)
            print(lat_from, lat_to, idx_frm, idx_to)
            self.lat = MagneticLattice(self.big_sequence,
                                       start=self.corr_list[idx_frm], stop=self.corr_list[idx_to],
                                       method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2

        elif current_lat == "up to B1":
            self.lat = MagneticLattice(cell_i1 + cell_l1, method=method)

            self.tws_des = tws_i1

            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen + 23.2)

        elif current_lat == "L1":
            self.lat = MagneticLattice(cell_l1, method=method)
            self.tws_des = tws_l1

            tmp_lat = MagneticLattice(self.copy_cells[1] )
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 62.08894499999998
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "B2D":
            self.lat = MagneticLattice(cell_i1 + cell_l1 + cell_l2 + cell_b2d, method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1] + self.copy_cells[2]  + self.copy_cells[6])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "up to B2":
            self.lat = MagneticLattice(cell_i1 + cell_l1 + cell_l2 , method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1] + self.copy_cells[2] )
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "TLD":
            self.lat = MagneticLattice(cell_i1 + cell_l1 + cell_l2 + cell_l3_no_cl + cell_cl + cell_tld, method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1]
                                      + self.copy_cells[2] + self.copy_cells[3] + self.copy_cells[4]+ self.copy_cells[8])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "up to TL":
            self.lat = MagneticLattice(cell_i1 + cell_l1 + cell_l2 + cell_l3_no_cl + cell_cl, method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1]
                                      + self.copy_cells[2] + self.copy_cells[3] + self.copy_cells[4])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "up to SASE3":
            self.lat = MagneticLattice(cell_i1 + cell_l1 + cell_l2 + cell_l3_no_cl + cell_cl + cell_sase1 + cell_t4 + cell_sase3, method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[1]
                                      + self.copy_cells[2] + self.copy_cells[3] + self.copy_cells[4] + self.copy_cells[9] + self.copy_cells[11] + self.copy_cells[10])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "L2":
            self.lat = MagneticLattice(cell_l2 , method=method)
            self.tws_des = tws_l2
            tmp_lat = MagneticLattice( self.copy_cells[2])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 229.30069400000002
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "L3":
            self.lat = MagneticLattice(cell_l2 + cell_l3_no_cl + cell_cl,
                                       start = engrd_419_b2, stop=mpbpmi_1693_cl, method=method)

            #self.tws_des = tws_l3
            self.tws_des = Twiss()
            self.tws_des.beta_x = 20.6928140374
            self.tws_des.beta_y = 6.8214735433
            self.tws_des.alpha_x = 0.0332419824342
            self.tws_des.alpha_y = -0.869862984066
            self.tws_des.E = 2.39999998888

            tmp_lat = MagneticLattice(self.l3_copy)
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 396.2191659999965
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "CL":
            self.lat = MagneticLattice(cell_l3_no_cl + cell_cl + cell_sase1,
                                       start = bpmr_1307_l3, stop=qa_2253_sa1, method=method)

            self.tws_des = Twiss()
            #self.tws_des.beta_x = 21.6754251533
            #self.tws_des.beta_y = 44.5714136209
            #self.tws_des.alpha_x = -0.758842958261
            #self.tws_des.alpha_y = 1.42869027612
            #self.tws_des.E = 16.3674999889
            self.tws_des.beta_x = 20.8408455944
            self.tws_des.beta_y = 45.1306436718
            self.tws_des.alpha_x = -0.712872984902
            self.tws_des.alpha_y = 1.41986586551
            self.tws_des.E = 15.2349999889
            #self.tws_des.s = 1359.6367660000235
            #self.tws_des = tws_cl
            tmp_lat = MagneticLattice(self.cl_copy)
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            #self.lat_zi = 1629.7019660000299
            self.lat_zi = 1359.6367660000235 + 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "I1D":
            self.lat = MagneticLattice(cell_i1 + cell_i1d, method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0] + self.copy_cells[5])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "SASE1":
            self.lat = MagneticLattice(cell_sase1+cell_t4, stop=ensub_2583_t4, method=method)
            self.tws_des = tws_sase1
            tmp_lat = MagneticLattice( self.sase1_copy)
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 1957.1856390000232
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "T4":
            self.lat = MagneticLattice(cell_t4 , method=method)
            self.tws_des = tws_t4
            tmp_lat = MagneticLattice( self.copy_cells[11])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 2438.5169790000195
            print("totlaLen=", self.lat.totalLen+ 23.2)

        elif current_lat == "SASE3":
            self.lat = MagneticLattice(cell_t4 + cell_sase3, start=ensub_2583_t4, method=method)
            #self.tws_des = tws_sase3
            self.tws_des = Twiss()

            self.tws_des.beta_x = 13.6455956218
            self.tws_des.beta_y = 3.93176166974
            self.tws_des.alpha_x = 2.20226650304
            self.tws_des.alpha_y = -0.830611804908
            self.tws_des.E = 17.4999999889

            tmp_lat = MagneticLattice( self.sase3_copy)
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 2560.450479000018
            print("totlaLen=", self.lat.totalLen+ 23.2)
        else:
            self.lat = MagneticLattice(cell_i1, method=method)
            self.tws_des = tws_i1
            tmp_lat = MagneticLattice(self.copy_cells[0])
            tws = twiss(tmp_lat, self.tws_des)
            self.s_des = [tw.s for tw in tws]
            self.b_x_des = [tw.beta_x for tw in tws]
            self.b_y_des = [tw.beta_y for tw in tws]
            self.tws_end = tws[-1]
            self.lat_zi = 23.2
            print("totlaLen=", self.lat.totalLen+ 23.2)
        self.s_des = np.array(self.s_des)
        self.tws0 = copy.deepcopy(self.tws_des)

        #self.lat = shrinker(self.lat, remaining_types=[Quadrupole, Hcor, Vcor,
        #                                               Monitor, Bend, SBend, RBend, Sextupole, Octupole],
        #                    init_energy=self.tws0.E)
        self.load_lattice()
        self.calc_twiss()

        # for orbit
        #self.orbit.load_orbit_devs()
        self.orbit.calc_orbit()

        return self.lat

    def return_tws(self):
        tws0 = Twiss()
        tws0.E = 0.005
        tws0.beta_x = 55.7887190242
        tws0.beta_y = 55.7887190242
        tws0.alpha_x = 18.185436973
        tws0.alpha_y = 18.185436973
        return tws0

    def load_devices(self, types):
        devices = []
        mi_devs = {}

        L = 0
        for elem in self.lat.sequence:
            L += elem.l
            if elem.__class__ in types:
                elem.s_pos = L - elem.l/2.
                elem.k1_th = elem.k1
                elem.kick_mrad = elem.k1 * elem.l * 1000.
                elem.i_kick = elem.kick_mrad
                devices.append(elem)
                mi_dev = Device(eid="XFEL.MAGNETS/MAGNET.ML/" + elem.id + "/KICK_MRAD.SP")
                mi_dev.mi = self.mi
                elem.mi = mi_dev
        return devices

    def load_cavs(self):
        devices = []
        for elem in self.lat.sequence:
            if elem.__class__ == Cavity and ("L1" in elem.id or "L2" in elem.id or "L3" in elem.id):
                mi_dev = MICavity(eid=elem.id)

                mi_dev.mi = self.mi
                elem.mi = mi_dev
                #print(elem.mi)
                devices.append(elem)
        return devices


    def load_lattice(self):
        self.quads = self.load_devices(types=[Quadrupole])
        self.cavs = self.load_cavs()

        self.add_devs2table(self.quads, w_table=self.ui.tableWidget, calc_obj=self.calc_twiss)

        #self.init_kick_mrad = np.array([q.kick_mrad for q in self.quads])
        self.quad_ampl = np.max(np.abs(np.array([q.kick_mrad for q in self.quads])))
        # for orbit
        self.orbit.load_orbit_devs()

        tws = twiss(self.lat, self.tws_des)

        s = np.array([tw.s for tw in tws]) + self.lat_zi
        self.beta_x_des.setData(x=self.s_des + self.lat_zi, y=self.b_x_des)
        self.beta_y_des.setData(x=self.s_des + self.lat_zi, y=self.b_y_des)
        self.r_items = self.plot_lat(plot_wdg=self.plot2, types=[Quadrupole])

    def calc_twiss(self, calc=True):
        #lat = MagneticLattice(cell)
        if self.online_calc == False:
            return

        # L = 0
        for elem in self.lat.sequence:
            if elem.__class__ in [Quadrupole]:
                #print(elem.id, elem.row)
                elem.kick_mrad = elem.ui.get_value()
                elem.k1 = elem.kick_mrad/elem.l/1000.
                if np.abs(np.abs(elem.kick_mrad) - np.abs(elem.i_kick))> 1:
                    self.r_items[elem.ui.row].setBrush(pg.mkBrush("r"))
                    self.ui.tableWidget.item(elem.row, 1).setForeground(QtGui.QColor(255, 101, 101))  # red
                else:
                    self.ui.tableWidget.item(elem.row, 1).setForeground(QtGui.QColor(255, 255, 255))  # white
                    self.r_items[elem.ui.row].setBrush(pg.mkBrush("g"))
                r = self.r_items[elem.ui.row]
                sizes = r.init_params
                #sizes = list(r.boundingRect().getRect())
                sizes[3] = 10*elem.kick_mrad/self.quad_ampl
                r.setRect(sizes[0], sizes[1], sizes[2], sizes[3])

        self.lat.update_transfer_maps()

        tws = twiss(self.lat, self.tws0)

        beta_x = [tw.beta_x for tw in tws]
        beta_y = [tw.beta_y for tw in tws]
        dx = [tw.Dx for tw in tws]
        dy = [tw.Dy for tw in tws]
        s = [tw.s for tw in tws]

        self.update_plot(s, beta_x, beta_y, dx, dy)

    def add_devs2table(self, devs, w_table, calc_obj, spin_params=[-5000, 5000, 5], check_box=False):
        """ Initialize the UI table object """
        #spin_boxes = [QtGui.QDoubleSpinBox()]*
        self.spin_boxes = []
        w_table.setRowCount(0)
        for row in range(len(devs)):
            eng = QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates)
            w_table.setRowCount(row + 1)
            pv = devs[row].id
            # put PV in the table
            w_table.setItem(row, 0, QtGui.QTableWidgetItem(str(pv)))
            # put start val in
            val = np.round(devs[row].kick_mrad, 4)
            w_table.setItem(row, 1, QtGui.QTableWidgetItem(str(val)))
            spin_box = QtGui.QDoubleSpinBox()
            spin_box.setStyleSheet("color: #b1b1b1; font-size: 16px; background-color:#595959; border: 2px solid #b1b1b1")
            spin_box.setLocale(eng)
            spin_box.setDecimals(4)
            spin_box.setMaximum(spin_params[1])
            spin_box.setMinimum(spin_params[0])
            spin_box.setSingleStep(spin_params[2])
            spin_box.setValue(devs[row].kick_mrad)
            spin_box.setAccelerated(True)
            spin_box.valueChanged.connect(calc_obj)
            # spin_box.setFixedWidth(50)
            w_table.setCellWidget(row, 2, spin_box)
            #w_table.resizeColumnsToContents()
            self.spin_boxes.append(spin_box)

            if check_box:
                checkBoxItem = QtGui.QTableWidgetItem()
                # checkBoxItem.setBackgroundColor(QtGui.QColor(100,100,150))
                checkBoxItem.setCheckState(QtCore.Qt.Checked)
                flags = checkBoxItem.flags()
                # print("FLAG", flags)
                # flags != flags
                checkBoxItem.setFlags(flags)
                w_table.setItem(row, 3, checkBoxItem)

            devs[row].row = row

            ui = DeviceUI()
            ui.tableWidget = w_table
            ui.row = row
            ui.col = 2
            devs[row].ui = ui
        #w_table.repaint()


    def plot_lat(self, plot_wdg, types, x_scale=1):
        plot_wdg.clear()
        r_items = []
        L = self.lat_zi
        for elem in self.lat.sequence:
            a = 1
            L += elem.l
            if elem.__class__ in types:
                s = L - elem.l
                r1 = pg.QtGui.QGraphicsRectItem(s, 0, elem.l*x_scale, 1)#10*elem.k1/self.quad_ampl)
                r1.setPen(pg.mkPen(None))
                r1.setBrush(pg.mkBrush("g"))
                r1.init_params = [s, 0, elem.l*x_scale, 1] #*elem.k1/self.quad_ampl]
                r_items.append(r1)
                plot_wdg.addItem(r1)
        plot_wdg.update()
        return r_items

    def zoom_signal(self):
        #s = self.plot1.viewRange()[0][0]
        #s_pos = np.array([q.s_pos for q in self.quads])
        s_pos = np.array([q.s_pos for q in self.quads]) + self.lat_zi
        s_up = self.plot1.viewRange()[0][0]
        s_down = self.plot1.viewRange()[0][1]
        s_up = s_up if s_up <= s_pos[-1] else s_pos[-1]
        s_down = s_down if s_down >= s_pos[0] else s_pos[0]

        indexes = np.arange(np.argwhere(s_pos >= s_up)[0][0], np.argwhere(s_pos <= s_down)[-1][0] + 1)
        mask = np.ones(len(self.quads), np.bool)
        mask[indexes] = 0
        self.quads = np.array(self.quads)
        [q.ui.set_hide(hide=False) for q in self.quads[indexes]]
        [q.ui.set_hide(hide=True) for q in self.quads[mask]]


    def add_plot(self):

        win = pg.GraphicsLayoutWidget()

        self.plot3 = win.addPlot(row=0, col=0)
        win.ci.layout.setRowMaximumHeight(0, 200)

        self.plot3.showGrid(1, 1, 1)


        self.plot1 = win.addPlot(row=1, col=0)
        self.plot3.setXLink(self.plot1)

        self.plot1.showGrid(1, 1, 1)

        self.plot1.getAxis('left').enableAutoSIPrefix(enable=False)  # stop the auto unit scaling on y axes
        layout = QtGui.QGridLayout()
        self.ui.widget_2.setLayout(layout)
        layout.addWidget(win, 0, 0)

        self.plot1.setAutoVisible(y=True)

        self.plot1.addLegend()
        color = QtGui.QColor(0, 255, 255)
        pen = pg.mkPen(color, width=3)
        self.beta_x = pg.PlotCurveItem(x=[], y=[], pen=pen, name='beta_x', antialias=True)
        self.plot1.addItem(self.beta_x)

        pen = pg.mkPen(color, width=1)
        self.beta_x_des = pg.PlotCurveItem(x=[], y=[], pen=pen, name='beta_x', antialias=True)
        self.plot1.addItem(self.beta_x_des)

        color = QtGui.QColor(255, 0, 0)
        pen = pg.mkPen(color, width=3)
        self.beta_y = pg.PlotCurveItem(x=[], y=[], pen=pen, name='beta_y', antialias=True)
        self.plot1.addItem(self.beta_y)

        color = QtGui.QColor(255, 0, 0)
        pen = pg.mkPen(color, width=1)
        self.beta_y_des = pg.PlotCurveItem(x=[], y=[], pen=pen, name='beta_y', antialias=True)
        self.plot1.addItem(self.beta_y_des)

        self.plot2 = win.addPlot(row=2, col=0)
        win.ci.layout.setRowMaximumHeight(2, 150)

        self.plot2.setXLink(self.plot1)
        self.plot2.showGrid(1, 1, 1)

        self.plot3.addLegend()
        color = QtGui.QColor(0, 255, 255)
        pen = pg.mkPen(color, width=3)
        self.Dx = pg.PlotCurveItem(x=[], y=[], pen=pen, name='Dx', antialias=True)
        self.plot3.addItem(self.Dx)

        color = QtGui.QColor(255, 0, 0)
        pen = pg.mkPen(color, width=3)
        self.Dy = pg.PlotCurveItem(x=[], y=[], pen=pen, name='Dy', antialias=True)
        self.plot3.addItem(self.Dy)
        self.plot2.sigRangeChanged.connect(self.zoom_signal)

    def error_box(self, message):
        QtGui.QMessageBox.about(self, "Error box", message)

    def question_box(self, message):
        #QtGui.QMessageBox.question(self, "Question box", message)
        reply = QtGui.QMessageBox.question(self, "Recalculate ORM?",
                "Recalculate Orbit Response Matrix?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply==QtGui.QMessageBox.Yes:
            return True

        return False

    def update_plot(self, s, bx, by, dx, dy):
        # Line
        s = np.array(s) + self.lat_zi
        self.beta_x.setData(x=s, y=bx)
        self.beta_y.setData(x=s, y=by)
        self.plot1.update()
        #self.plot1.setYRange(-5, 200)
        self.plot2.update()
        self.Dx.setData(x=s, y=dx)
        self.Dy.setData(x=s, y=dy)
        self.plot3.update()


    def loadStyleSheet(self):
        """ Sets the dark GUI theme from a css file."""
        try:
            self.cssfile = "gui/style.css"
            with open(self.cssfile, "r") as f:
                self.setStyleSheet(f.read())
        except IOError:
            print ('No style sheet found!')




def main():


    #make pyqt threadsafe
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    #create the application
    app    = QApplication(sys.argv)


    window = ManulInterfaceWindow()


    #show app
    window.setWindowIcon(QtGui.QIcon('manul.png'))

    window.show()
    window.raise_()
    #Build documentaiton if source files have changed
    # TODO: make more universal
    #os.system("cd ./docs && xterm -T 'Ocelot Doc Builder' -e 'bash checkDocBuild.sh' &")
    #exit script
    sys.exit(app.exec_())

if __name__ == "__main__":

    main()
    #window = ManulInterfaceWindow()
    #window.read_quads()

