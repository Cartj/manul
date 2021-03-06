#!/opt/anaconda4/bin/python
"""
Sergey Tomin. XFEL/DESY, 2017.
"""
#QT imports
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox, QMainWindow, QDialog
import numpy as np
import sys
import os
import time
import pyqtgraph as pg
from copy import deepcopy
from scipy import optimize
import json
import importlib
import logging

# filename="logs/afb.log",
#filename="logs/manul.log"
#logging.basicConfig(filename="logs/manul.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(level=logging.INFO)
path = os.path.realpath(__file__)
indx = path.find("manul")
print("PATH to main file: " + os.path.realpath(__file__) + " path to folder"+ path[:indx])
sys.path.append(path[:indx])
sys.path.append("C:/Users/tomins/Documents/Dropbox/DESY/repository/ocelot")


from ocelot import *
#from ocelot.gui.accelerator import *
from ocelot.cpbd.track import *

#from ocelot.optimizer.mint.opt_objects import Device
from ocelot.optimizer.mint.xfel_interface import *


from orbit import OrbitInterface
from mint.devices import *
from dispersion import *
from gui.gui_main import *
from gui.settings_gui import *
from ml.adviser_gui import *
from lattices import lattice_manager
logger = logging.getLogger(__name__)



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
        #self.load_lattice_files()

        path = os.path.realpath(__file__)
        indx = path.find("ocelot" + os.sep + "optimizer")
        self.path2ocelot = path[:indx]
        self.path2manul = path[:path.find("manul")]

        self.optimizer_path = self.path2ocelot + "ocelot" + os.sep + "optimizer" + os.sep
        self.config_dir = self.path2manul + "manul" + os.sep + "configs" + os.sep
        self.config_file = self.config_dir + "settings.json"
        self.gui_dir = self.path2manul + "manul" + os.sep + "gui" + os.sep
        self.gold_orbits_dir = "/home/xfeloper/data/golden_orbits/" # self.path2manul + "manul" + os.sep + "golden_orbits" + os.sep
        self.gold_orbits_from_OD_dir = "/home/xfeloper/data/orbit_display/"#self.path2manul + "manul" + os.sep + "golden_orbits" + os.sep
        self.rm_files_dir_root = self.path2manul + "manul" + os.sep + "rm_files" + os.sep
        self.set_file = self.config_dir + "default.json" # ./parameters/default.json"
        self.obj_func_path = self.optimizer_path + "mint" + os.sep + "obj_function.py"
        self.obj_save_path = self.config_dir +  "obj_funcs" + os.sep
        # initialize
        QFrame.__init__(self)

        #self.logbook = "xfellog"
        self.settings = None
        self.adviser = None
        self.mi = XFELMachineInterface()
        #self.mi = TestMachineInterface()
        self.debug_mode = False
        if self.mi.__class__ == TestMachineInterface:
            self.debug_mode = True
        self.ui = MainWindow(self)

        self.show_correction_result = True


        self.subtrain = self.ui.combo_subtrain.currentText()
        self.load_settings()
        #self.server = "XFEL"
        #self.subtrain = "SA1"

        self.orbit = OrbitInterface(parent=self)
        self.dispersion = DispersionInterface(parent=self)

        self.ui.action_Parameters.triggered.connect(self.run_settings_window)

        try:
            self.xfel_lattice = lattice_manager.XFELLattice(path="lattices." + self.path2lattice)
        except:
            self.error_box("Could not load lattice files. Check the path in settings and try again. Path: " + "lattices." + self.path2lattice)
            return

        self.online_calc = True

        #QFrame.__init__(self)
        #self.ui = UiS_Form()
        #self.ui.setupUi(self)


        #load in the dark theme style sheet
        self.loadStyleSheet()


        #timer for plots, starts when scan starts
        self.multiPvTimer = QtCore.QTimer()
        #self.multiPvTimer.timeout.connect(self.getPlotData)
        #self.initTable()
        #print("quads", self.quads)
        self.add_plot()


        #self.ui.cb_lattice.setCurrentIndex(0)

        #self.correctors_list(seq=self.big_sequence, energy=130)
        #self.change_subtrain()
        self.timer_live = pg.QtCore.QTimer()
        self.timer_live.timeout.connect(self.orbit.live_orbit)

        self.feedback_timer = pg.QtCore.QTimer()
        self.feedback_timer.timeout.connect(self.orbit.auto_correction)

        self.load_lattice_files()
        self.lat = self.return_lat()
        #self.tws0 = self.return_tws()
        #self.load_lattice()

        self.ui.pb_write.clicked.connect(self.calc_twiss)
        self.ui.pb_read.clicked.connect(self.read_quads)
        self.ui.pb_reset.clicked.connect(self.reset_quads)

        #self.ui.cb_lattice.currentIndexChanged.connect(self.return_lat)
        self.ui.cb_otr55.setChecked(True)
        self.ui.cb_coupler_kick.stateChanged.connect(self.apply_coupler_kick)
        self.ui.cb_sec_order.stateChanged.connect(self.apply_second_order)
        #self.ui.pb_write.clicked.connect(self.match)
        #self.ui.pb_reload.clicked.connect(self.reload_lat)

        self.ui.pb_set_pos.clicked.connect(self.arbitrary_lattice)


        self.ui.actionGO_Adviser.triggered.connect(self.run_adviser_window)
        self.ui.combo_subtrain.currentIndexChanged.connect(self.change_subtrain)


    def get_charge_bunch(self):
        if self.charge_from_doocs:
            charge = ChargeDoocs()
            charge.mi = self.mi
            self.bunch_charge = charge.get_value()

    def change_subtrain(self):

        self.subtrain = self.ui.combo_subtrain.currentText()

        self.arbitrary_lattice()

    def load_lattice_files(self):
        names = [sec.name for sec in self.xfel_lattice.sections]
        for name in names:
            self.ui.cb_lattice.addItem(name)
        self.ui.cb_lattice.setCurrentIndex(1)

        self.ui.cb_lattice.currentIndexChanged.connect(self.return_lat)
        current_lat = self.ui.cb_lattice.currentText()
        section = self.xfel_lattice.get_section(current_lat)
        self.big_sequence = self.xfel_lattice.get_sequence(section)
        self.correctors_list(seq=self.big_sequence, energy=130)

    def run_settings_window(self):
        if self.settings is None:
            self.settings = ManulSettings(parent=self)
        self.settings.show()

    def run_adviser_window(self):
        if self.adviser is None:
            self.adviser = ManulAdviser(parent=self)
        self.adviser.show()

    def load_settings(self):
        logger.debug("load settings ... ")
        with open(self.config_file, 'r') as f:
            table = json.load(f)

        self.show_correction_result = table["show_correction_result"]
        self.gc_nlast = table["nlast"]
        self.gc_nreadings = table["nreadings"]
        #self.lattice_settings = table["lattice"]
        self.svd_epsilon_x = table["epsilon_x"]
        self.svd_epsilon_y = table["epsilon_y"]
        self.uncheck_corrs = table["uncheck_corrs"]
        self.uncheck_bpms = table["uncheck_bpms"]

        self.le_cl_energy = table["le_cl_energy"]
        self.le_b2_energy = table["le_b2_energy"]
        self.le_b1_energy = table["le_b1_energy"]
        self.le_i1_energy = table["le_i1_energy"]

        self.single_shot_flag = table["single_shot"]

        self.co_nlast_bpms = table["co_nlast"]
        self.logbook = table["logbook"]
        self.path2lattice = table["lattice"]
        self.rm_files_dir = self.rm_files_dir_root + self.path2lattice + os.sep

        if "subtrain_list" in table.keys():
            subtrain_list = table["subtrain_list"]
        else:
            subtrain_list = ["ALL"]
            
        for name in subtrain_list:
            self.ui.combo_subtrain.addItem(name)
        
        if "subtrain" in table.keys() and table["subtrain"] in subtrain_list:
            indx = subtrain_list.index(table["subtrain"])
        else:
            indx = 0
            logger.warning("load_settings: 'subtrain' not in table.keys() or table['subtrain'] not in subtrain_list")

        if "charge_tol" in table.keys():
            self.charge_tol = table["charge_tol"]
        else:
            self.charge_tol = 0.

        if "bunch_charge" in table.keys():
            self.bunch_charge = table["bunch_charge"]
        else:
            self.bunch_charge = 0.5 #nC

        if "charge_doocs" in table.keys():
            self.charge_from_doocs = table["charge_doocs"]
        else:
            self.charge_from_doocs = False

        self.ui.combo_subtrain.setCurrentIndex(indx)
        self.subtrain = self.ui.combo_subtrain.currentText()
        
        if "server" in table.keys():
            self.server = table["server"]
        else:
            self.server = "XFEL"

        if "beta" in table.keys():
            self.svd_beta = table["beta"]
        else:
            self.svd_beta = 0

        logger.debug("load settings ... OK")

    def update_table(self):
        for quad in self.quads:
            quad.ui.set_init_value(quad.kick_mrad)
            quad.ui.set_value(quad.kick_mrad)


    def reset_quads(self):
        for quad in self.quads:
            #print(quad.i_kick)
            quad.ui.set_value(quad.i_kick)
        #self.calc()

    def correctors_list(self, seq, start_pos=23.2, energy=130.):

        self.corr_list = []
        L = start_pos
        E = energy
        for elem in seq:
            L += elem.l
            if elem.__class__ in [Hcor, Vcor]:
                elem.s_pos = L - elem.l/2.
                elem.E = E
                self.corr_list.append(elem)
            if elem.__class__ == Cavity:
                E += elem.v*np.cos(elem.phi*np.pi/180.)
        return self.corr_list

    def read_quads(self):

        self.online_calc = False
        for elem in self.quads:
            elem.kick_mrad = elem.mi.get_value()
            logger.debug("Quad."+elem.id + " updated. k1 = "+str(elem.kick_mrad)+ " mrad")
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
                logger.warning("Could not read cavity voltage: " +cav.id)
            #print("Volt = ", v, cav.mi)
            cav.v = v*0.001
            logger.debug("Cavity: " + cav.id + ":" + str(cav.v))
        self.online_calc = True
        self.lat.update_transfer_maps()
        self.tws0 = self.back_tracking()
        logger.debug("back_tracking result: " + str(self.tws0))
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

    def back_tracking(self):
        logger.debug("back_tracking: ... ")
        tws0 = self.read_twiss()

        section = self.xfel_lattice.return_lat_section("up to TL")
        cell_back_track = section.seq

        if self.ui.cb_design_tws.isChecked():
            return self.tws_des

        if self.ui.cb_otr218.isChecked():
            stop = 'OTRB.218.B1'

        elif self.ui.cb_otr450.isChecked():
            stop = 'OTRB.450.B2'

        else:
            stop = 'OTRC.55.I1'

        stop_elem = cell_back_track[[elem.id for elem in cell_back_track].index(stop)]

        lat_tmp = MagneticLattice(cell_back_track, stop=stop_elem)
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
        logger.debug("back_tracking: ... OK")
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
        mi_tws = MITwiss(server=self.server, subtrain=self.subtrain)
        mi_tws.mi = self.mi
        tws_dict = mi_tws.get_tws(section=section)
        for key in tws_dict.keys():
            tws.__dict__[key] = tws_dict[key]

        #ch_beta_x = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_X.BETA.SA1"
        #ch_alpha_x = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_X.ALPHA.SA1"
        #ch_beta_y = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_Y.BETA.SA1"
        #ch_alpha_y = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_Y.ALPHA.SA1"
        #ch_energy = "XFEL.UTIL/BEAM_PARAMETER/" + section + "/PROJECTED_X.ENERGY.SA1"

        #tws.beta_x = self.mi.get_value(ch_beta_x)
        #tws.beta_y = self.mi.get_value(ch_beta_y)
        #tws.alpha_x = self.mi.get_value(ch_alpha_x)
        #tws.alpha_y = self.mi.get_value(ch_alpha_y)
        ##tws.E = self.mi.get_value(ch_energy)*0.001
        logger.debug(tws)
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
            logger.debug("match -> error_func -> err = " + str(err))
            return err


        res = optimize.fmin(error_func, x, xtol=0.1)
        logger.debug(res)
        for i, quad in enumerate(quads):
            quad.kick_mrad = res[i]
            quad.k1 = res[i]/quad.l/1000.
            quad.ui.set_value(quad.kick_mrad)



    def apply_coupler_kick(self):
        logger.debug("apply_coupler_kick: checkbox:" +str(self.ui.cb_coupler_kick.isChecked()))
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
        logger.debug("apply_coupler_kick: OK")


    def apply_second_order(self):
        logger.debug("apply_second_order: checkbox:" +str(self.ui.cb_sec_order.isChecked()))
        method = MethodTM()
        if self.ui.cb_sec_order.isChecked():
            method.global_method = SecondTM
        else:
            method.global_method = TransferMap
        self.lat = MagneticLattice(self.lat.sequence, method=method)

        # calc orbit
        self.orbit.calc_orbit()
        logger.debug("apply_second_order: OK")

    def arbitrary_lattice(self):
        #current_lat = self.ui.cb_lattice.currentText()
        #if current_lat != "Arbitrary":
        #    return 0

        lat_from = self.ui.sb_lat_from.value()
        lat_to = self.ui.sb_lat_to.value()
        if lat_to - 30 < lat_from:
            self.ui.sb_lat_to.setValue(lat_from+30)

        lat_from = self.ui.sb_lat_from.value()
        lat_to = self.ui.sb_lat_to.value()
        s_poss = np.array([cor.s_pos for cor in self.corr_list])
        idx_frm = (np.abs(s_poss - lat_from)).argmin()
        idx_to = (np.abs(s_poss - lat_to)).argmin()
        if idx_frm == idx_to:
            idx_to += 1
            self.ui.sb_lat_to.setValue(self.corr_list[idx_to].s_pos)
        
        # end changing of the code
        # start /stop elements should be correctors !!!
        self.return_lat(start=self.corr_list[idx_frm], stop=self.corr_list[idx_to])

        #self.orbit.choose_plane()
        #self.orbit.uncheck_aircols()

    def return_lat(self, qt_currentIndex=None, start=None, stop=None):
        self.get_charge_bunch()
        logger.debug("return_lat: ... ")
        self.orbit.reset_undo_database()
        current_lat = self.ui.cb_lattice.currentText()
        if current_lat == "Arbitrary" and start == None and stop == None:
            section = self.xfel_lattice.get_section(current_lat)
            cell = self.xfel_lattice.lats[section.str_cells[0]].cell
            start = cell[0]
            stop = cell[-1]
            
        try:
            section = self.xfel_lattice.return_lat_section(current_lat, start=start, stop=stop)
        except Exception as e:
            logger.error("return_lat: xfel_lattice.return_lat()" +str(e))
            raise
            
        self.seq = section.seq
        total_len = np.sum([elem.l for elem in section.seq])
        self.lat_zi = section.z0
        self.tws_des = section.tws_des


        self.corr_list = self.correctors_list(seq=self.seq, start_pos=self.lat_zi, energy=self.tws_des.E)
        self.ui.sb_lat_from.setMinimum(self.lat_zi)
        # self.ui.sb_lat_from.setValue(self.lat_zi)
        self.ui.sb_lat_from.setMaximum(self.lat_zi + total_len - 30)
        self.ui.sb_lat_to.setMaximum(self.lat_zi + total_len)
        self.ui.sb_lat_to.setMinimum(self.lat_zi + 30)
        if start == None and stop == None:
            self.ui.sb_lat_to.setValue(self.lat_zi + total_len)
            self.ui.sb_lat_from.setValue(self.lat_zi)


        self.lat = section.lat #MagneticLattice(self.get_slice_sequence(self.seq, start=start, stop=stop), method=method)


        self.lat_zi = self.ui.sb_lat_from.value()
        # tws0 is used in match in backtracking
        self.tws0 = deepcopy(self.tws_des)

        # self.lat = shrinker(self.lat, remaining_types=[Quadrupole, Hcor, Vcor,
        #                                               Monitor, Bend, SBend, RBend, Sextupole, Octupole],
        #                    init_energy=self.tws0.E)
        try:
            self.plot_design_twiss()
        except Exception as e:
            logger.error("return_lat: plot_design_twiss: " + str(e))

        self.load_lattice()

        try:
            #self.lat4twiss = MagneticLattice(self.seq)
            self.calc_twiss()
        except Exception as e:
            logger.error("return_lat: calc_twiss: " + str(e))

        # for orbit
        # self.orbit.load_orbit_devs()
        self.orbit.calc_orbit()
        logger.debug("return_lat: ... OK")

        self.orbit.choose_plane()
        self.orbit.uncheck_aircols()

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
                mi_dev = Device(eid=self.server + ".MAGNETS/MAGNET.ML/" + elem.id + "/KICK_MRAD.SP")
                mi_dev.mi = self.mi
                elem.mi = mi_dev
        return devices

    def load_cavs(self):
        devices = []
        for elem in self.lat.sequence:
            if elem.__class__ == Cavity and ("L1" in elem.id or "L2" in elem.id or "L3" in elem.id):
                mi_dev = MICavity(eid=elem.id, server=self.server, subtrain=self.subtrain)

                mi_dev.mi = self.mi
                elem.mi = mi_dev
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

        try:
            self.r_items = self.plot_lat(plot_wdg=self.plot2, types=[Quadrupole])
        except Exception as e:
            logger.error("load_lattice: error in r_items" + str(e))


    def plot_design_twiss(self):
        tws = twiss(self.lat, self.tws_des)

        s = np.array([tw.s for tw in tws]) + self.lat_zi
        bx = np.array([tw.beta_x for tw in tws])
        by = np.array([tw.beta_y for tw in tws])
        #self.s_des + self.lat_zi
        self.beta_x_des.setData(x=s, y=bx)
        self.beta_y_des.setData(x=s, y=by)
    #    self.r_items = self.plot_lat(plot_wdg=self.plot2, types=[Quadrupole])

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
        if reply == QtGui.QMessageBox.Yes:
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
            logger.error('No style sheet found!')




def main():


    #make pyqt threadsafe
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    #create the application
    app    = QApplication(sys.argv)


    window = ManulInterfaceWindow()


    #show app
    #window.setWindowIcon(QtGui.QIcon('gui/angry_manul.png'))
    # setting the path variable for icon
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'gui/manul.png')
    app.setWindowIcon(QtGui.QIcon(path))
    window.show()
    window.raise_()
    #Build documentaiton if source files have changed
    # TODO: make more universal
    #os.system("cd ./docs && xterm -T 'Ocelot Doc Builder' -e 'bash checkDocBuild.sh' &")
    #exit script
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

