# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UISettings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(607, 731)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #Form.setStyleSheet("background-color: white")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_8.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 0, 0, 1, 1)
        self.sb_epsilon_x = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sb_epsilon_x.setFont(font)
        self.sb_epsilon_x.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sb_epsilon_x.setDecimals(3)
        self.sb_epsilon_x.setMaximum(1.0)
        self.sb_epsilon_x.setSingleStep(0.001)
        self.sb_epsilon_x.setProperty("value", 0.01)
        self.sb_epsilon_x.setObjectName("sb_epsilon_x")
        self.gridLayout_8.addWidget(self.sb_epsilon_x, 0, 2, 1, 1)
        self.sb_epsilon_y = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sb_epsilon_y.setFont(font)
        self.sb_epsilon_y.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sb_epsilon_y.setDecimals(3)
        self.sb_epsilon_y.setMaximum(1.0)
        self.sb_epsilon_y.setSingleStep(0.001)
        self.sb_epsilon_y.setProperty("value", 0.01)
        self.sb_epsilon_y.setObjectName("sb_epsilon_y")
        self.gridLayout_8.addWidget(self.sb_epsilon_y, 1, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_8, 0, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.label_12 = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_17.addWidget(self.label_12, 0, 0, 1, 1)
        self.sb_co_nlast = QtWidgets.QSpinBox(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sb_co_nlast.sizePolicy().hasHeightForWidth())
        self.sb_co_nlast.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sb_co_nlast.setFont(font)
        self.sb_co_nlast.setMaximum(20)
        self.sb_co_nlast.setSingleStep(1)
        self.sb_co_nlast.setProperty("value", 5)
        self.sb_co_nlast.setObjectName("sb_co_nlast")
        self.gridLayout_17.addWidget(self.sb_co_nlast, 0, 1, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_17, 0, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_6, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 2, 0, 1, 1)
        self.sb_nreadings = QtWidgets.QSpinBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sb_nreadings.sizePolicy().hasHeightForWidth())
        self.sb_nreadings.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sb_nreadings.setFont(font)
        self.sb_nreadings.setMaximum(100)
        self.sb_nreadings.setSingleStep(1)
        self.sb_nreadings.setProperty("value", 15)
        self.sb_nreadings.setObjectName("sb_nreadings")
        self.gridLayout_5.addWidget(self.sb_nreadings, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)
        self.sb_nlast = QtWidgets.QSpinBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sb_nlast.sizePolicy().hasHeightForWidth())
        self.sb_nlast.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sb_nlast.setFont(font)
        self.sb_nlast.setMaximum(100)
        self.sb_nlast.setSingleStep(1)
        self.sb_nlast.setProperty("value", 5)
        self.sb_nlast.setObjectName("sb_nlast")
        self.gridLayout_5.addWidget(self.sb_nlast, 2, 1, 1, 1)
        self.cb_single_shot = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_single_shot.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cb_single_shot.setFont(font)
        self.cb_single_shot.setObjectName("cb_single_shot")
        self.gridLayout_5.addWidget(self.cb_single_shot, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 6, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 4, 0, 1, 1)
        self.le_logbook = QtWidgets.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_logbook.setFont(font)
        self.le_logbook.setObjectName("le_logbook")
        self.gridLayout_4.addWidget(self.le_logbook, 4, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 3, 1, 1, 1)
        self.le_lattice = QtWidgets.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_lattice.setFont(font)
        self.le_lattice.setObjectName("le_lattice")
        self.gridLayout_4.addWidget(self.le_lattice, 3, 2, 1, 1)
        self.cb_show_correction_result = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cb_show_correction_result.setFont(font)
        self.cb_show_correction_result.setObjectName("cb_show_correction_result")
        self.gridLayout_4.addWidget(self.cb_show_correction_result, 2, 0, 1, 3)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 5, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 6, 0, 1, 1)
        self.combo_subtrain = QtWidgets.QComboBox(self.groupBox)
        self.combo_subtrain.setObjectName("combo_subtrain")
        self.gridLayout_4.addWidget(self.combo_subtrain, 6, 1, 1, 1)
        self.combo_server = QtWidgets.QComboBox(self.groupBox)
        self.combo_server.setObjectName("combo_server")
        self.gridLayout_4.addWidget(self.combo_server, 5, 1, 1, 1)
        self.le_server = QtWidgets.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_server.setFont(font)
        self.le_server.setObjectName("le_server")
        self.gridLayout_4.addWidget(self.le_server, 5, 2, 1, 1)
        self.le_subtrain = QtWidgets.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.le_subtrain.setFont(font)
        self.le_subtrain.setObjectName("le_subtrain")
        self.gridLayout_4.addWidget(self.le_subtrain, 6, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 2)
        self.gridLayout_11.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem2, 4, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.sb_charge_tol = QtWidgets.QSpinBox(self.groupBox_4)
        self.sb_charge_tol.setSingleStep(5)
        self.sb_charge_tol.setProperty("value", 50)
        self.sb_charge_tol.setObjectName("sb_charge_tol")
        self.gridLayout_3.addWidget(self.sb_charge_tol, 0, 1, 1, 1)
        self.cb_charge_doocs = QtWidgets.QCheckBox(self.groupBox_4)
        self.cb_charge_doocs.setChecked(True)
        self.cb_charge_doocs.setObjectName("cb_charge_doocs")
        self.gridLayout_3.addWidget(self.cb_charge_doocs, 1, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox_4)
        self.label_17.setEnabled(False)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 2, 0, 1, 1)
        self.sb_bunch_charge = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.sb_bunch_charge.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.sb_bunch_charge.setFont(font)
        self.sb_bunch_charge.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sb_bunch_charge.setDecimals(2)
        self.sb_bunch_charge.setMaximum(2.0)
        self.sb_bunch_charge.setSingleStep(0.05)
        self.sb_bunch_charge.setProperty("value", 0.5)
        self.sb_bunch_charge.setObjectName("sb_bunch_charge")
        self.gridLayout_3.addWidget(self.sb_bunch_charge, 2, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_4, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_13.addWidget(self.label_7, 1, 0, 1, 1)
        self.le_cl_energy = QtWidgets.QLineEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_cl_energy.setFont(font)
        self.le_cl_energy.setObjectName("le_cl_energy")
        self.gridLayout_13.addWidget(self.le_cl_energy, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_13.addWidget(self.label_6, 0, 0, 1, 1)
        self.le_b2_energy = QtWidgets.QLineEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_b2_energy.setFont(font)
        self.le_b2_energy.setObjectName("le_b2_energy")
        self.gridLayout_13.addWidget(self.le_b2_energy, 1, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_13.addWidget(self.label_9, 2, 0, 1, 1)
        self.le_b1_energy = QtWidgets.QLineEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_b1_energy.setFont(font)
        self.le_b1_energy.setObjectName("le_b1_energy")
        self.gridLayout_13.addWidget(self.le_b1_energy, 2, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_13.addWidget(self.label_11, 3, 0, 1, 1)
        self.le_i1_energy = QtWidgets.QLineEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_i1_energy.setFont(font)
        self.le_i1_energy.setObjectName("le_i1_energy")
        self.gridLayout_13.addWidget(self.le_i1_energy, 3, 2, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_13, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem3, 5, 0, 1, 1)
        self.gridLayout_14.addWidget(self.groupBox_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.cb_couplerkick = QtWidgets.QCheckBox(self.tab_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cb_couplerkick.setFont(font)
        self.cb_couplerkick.setObjectName("cb_couplerkick")
        self.gridLayout_15.addWidget(self.cb_couplerkick, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_15.addItem(spacerItem4, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.groupBox_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.te_bpms = QtWidgets.QTextEdit(self.groupBox_7)
        self.te_bpms.setMaximumSize(QtCore.QSize(16777215, 100))
        self.te_bpms.setObjectName("te_bpms")
        self.gridLayout_19.addWidget(self.te_bpms, 3, 0, 1, 1)
        self.te_corrs = QtWidgets.QTextEdit(self.groupBox_7)
        self.te_corrs.setMaximumSize(QtCore.QSize(16777215, 100))
        self.te_corrs.setObjectName("te_corrs")
        self.gridLayout_19.addWidget(self.te_corrs, 1, 0, 1, 1)
        self.pb_check = QtWidgets.QPushButton(self.groupBox_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pb_check.setFont(font)
        self.pb_check.setObjectName("pb_check")
        self.gridLayout_19.addWidget(self.pb_check, 4, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout_19.addWidget(self.label_13, 2, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridLayout_19.addWidget(self.label_14, 0, 0, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_19, 0, 1, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox_7, 0, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem5, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_18 = QtWidgets.QLabel(self.tab_5)
        self.label_18.setObjectName("label_18")
        self.gridLayout_10.addWidget(self.label_18, 1, 0, 1, 1)
        self.cb_style_def = QtWidgets.QComboBox(self.tab_5)
        self.cb_style_def.setObjectName("cb_style_def")
        self.gridLayout_10.addWidget(self.cb_style_def, 1, 1, 1, 1)
        self.cb_show_cor_panel = QtWidgets.QCheckBox(self.tab_5)
        self.cb_show_cor_panel.setObjectName("cb_show_cor_panel")
        self.gridLayout_10.addWidget(self.cb_show_cor_panel, 0, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem6, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.pb_apply = QtWidgets.QPushButton(Form)
        self.pb_apply.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pb_apply.setFont(font)
        self.pb_apply.setObjectName("pb_apply")
        self.horizontalLayout.addWidget(self.pb_apply)
        self.pb_cancel = QtWidgets.QPushButton(Form)
        self.pb_cancel.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pb_cancel.setFont(font)
        self.pb_cancel.setObjectName("pb_cancel")
        self.horizontalLayout.addWidget(self.pb_cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Ocelot Interface"))
        self.groupBox_3.setTitle(_translate("Form", "SVD"))
        self.label_10.setText(_translate("Form", "Y plane"))
        self.label_3.setText(_translate("Form", "X plane"))
        self.groupBox_6.setTitle(_translate("Form", "Close Orbit "))
        self.label_12.setText(_translate("Form", "Number last BPMs for orbit closure"))
        self.groupBox_2.setTitle(_translate("Form", "Gentle Correction "))
        self.label_8.setText(_translate("Form", "Average Over Last (X) Readings"))
        self.label_2.setText(_translate("Form", "Number of Orbit Readings"))
        self.cb_single_shot.setText(_translate("Form", "Single-Shot measurement"))
        self.groupBox.setTitle(_translate("Form", "General"))
        self.label_4.setText(_translate("Form", "Lattice    "))
        self.label_5.setText(_translate("Form", "LogBook"))
        self.le_logbook.setText(_translate("Form", "xfellog"))
        self.le_lattice.setText(_translate("Form", "phase_advance_5pi"))
        self.cb_show_correction_result.setText(_translate("Form", "Show Correction Result (otherwise Changes)"))
        self.label_15.setText(_translate("Form", "Server"))
        self.label_16.setText(_translate("Form", "Subtrain def"))
        self.le_server.setText(_translate("Form", "XFEL, XFEL_SIM"))
        self.le_subtrain.setText(_translate("Form", "ALL, SA1, SA2, SA3, DUD"))
        self.groupBox_4.setTitle(_translate("Form", "Charge tolerance"))
        self.label.setText(_translate("Form", "Charge tolerance [%]"))
        self.cb_charge_doocs.setText(_translate("Form", "take bunch charge from DOOCS"))
        self.label_17.setText(_translate("Form", "Set bunch charge [nC]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "General"))
        self.groupBox_5.setTitle(_translate("Form", "Energy Readings"))
        self.label_7.setText(_translate("Form", "B2    "))
        self.label_6.setText(_translate("Form", "CL,..."))
        self.label_9.setText(_translate("Form", "B1    "))
        self.label_11.setText(_translate("Form", "I1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Dispersion"))
        self.cb_couplerkick.setText(_translate("Form", "CouplerKick"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Optics"))
        self.groupBox_7.setTitle(_translate("Form", "Uncheck Devices by Default"))
        self.pb_check.setText(_translate("Form", "Check"))
        self.label_13.setText(_translate("Form", "BPMs (must be divided by comma \",\" without quotes)"))
        self.label_14.setText(_translate("Form", "Corrs (must be divided by comma \",\" without quotes)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "Unchecked Devices"))
        self.label_18.setText(_translate("Form", "Chose style by default"))
        self.cb_show_cor_panel.setText(_translate("Form", "Show cor/BPM panel by default"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Form", "Appearance"))
        self.pb_apply.setText(_translate("Form", "Apply"))
        self.pb_cancel.setText(_translate("Form", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

