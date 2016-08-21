# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './shot_time_tracker.ui'
#
# Created: Sun Aug 21 11:56:59 2016
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(394, 220)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.process_label = QtGui.QLabel(self.centralwidget)
        self.process_label.setGeometry(QtCore.QRect(10, 20, 101, 18))
        self.process_label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.process_label.setObjectName("process_label")
        self.process_editline = QtGui.QLineEdit(self.centralwidget)
        self.process_editline.setGeometry(QtCore.QRect(100, 20, 281, 28))
        self.process_editline.setObjectName("process_editline")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 130, 351, 61))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.action_status_label = QtGui.QLabel(self.frame)
        self.action_status_label.setGeometry(QtCore.QRect(70, 20, 211, 20))
        self.action_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.action_status_label.setObjectName("action_status_label")
        self.start_button = QtGui.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(30, 80, 351, 31))
        self.start_button.setDefault(False)
        self.start_button.setFlat(True)
        self.start_button.setObjectName("start_button")
        self.asset_label = QtGui.QLabel(self.centralwidget)
        self.asset_label.setGeometry(QtCore.QRect(0, 50, 101, 18))
        self.asset_label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.asset_label.setObjectName("asset_label")
        self.asset_editline = QtGui.QLineEdit(self.centralwidget)
        self.asset_editline.setGeometry(QtCore.QRect(100, 50, 281, 28))
        self.asset_editline.setObjectName("asset_editline")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.process_label.setText(QtGui.QApplication.translate("MainWindow", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.action_status_label.setText(QtGui.QApplication.translate("MainWindow", "Not Running", None, QtGui.QApplication.UnicodeUTF8))
        self.start_button.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_label.setText(QtGui.QApplication.translate("MainWindow", "Asset", None, QtGui.QApplication.UnicodeUTF8))      

