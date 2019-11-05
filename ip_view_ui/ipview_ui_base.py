# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ipview_base.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(826, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.directory_input = QtWidgets.QTextEdit(self.centralwidget)
        self.directory_input.setGeometry(QtCore.QRect(530, 30, 256, 41))
        self.directory_input.setObjectName("directory_input")
        self.directory_load_push = QtWidgets.QPushButton(self.centralwidget)
        self.directory_load_push.setGeometry(QtCore.QRect(710, 90, 75, 23))
        self.directory_load_push.setObjectName("directory_load_push")
        self.clear_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_push_button.setGeometry(QtCore.QRect(710, 340, 75, 23))
        self.clear_push_button.setObjectName("clear_push_button")
        self.image_display = QtWidgets.QGraphicsView(self.centralwidget)
        self.image_display.setGeometry(QtCore.QRect(20, 30, 471, 441))
        self.image_display.setObjectName("image_display")
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(620, 90, 75, 23))
        self.next_button.setObjectName("next_button")
        self.previous_button = QtWidgets.QPushButton(self.centralwidget)
        self.previous_button.setGeometry(QtCore.QRect(530, 90, 75, 23))
        self.previous_button.setObjectName("previous_button")
        self.text_list_display = QtWidgets.QListView(self.centralwidget)
        self.text_list_display.setGeometry(QtCore.QRect(530, 130, 256, 192))
        self.text_list_display.setObjectName("text_list_display")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.directory_input.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.directory_load_push.setText(_translate("MainWindow", "Load"))
        self.clear_push_button.setText(_translate("MainWindow", "Clear"))
        self.next_button.setText(_translate("MainWindow", "next"))
        self.previous_button.setText(_translate("MainWindow", "previous"))
