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
        MainWindow.resize(819, 542)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(15, 15, 15);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.directory_load_push = QtWidgets.QPushButton(self.centralwidget)
        self.directory_load_push.setGeometry(QtCore.QRect(700, 50, 75, 23))
        self.directory_load_push.setStyleSheet("background-color: rgb(96, 181, 255);")
        self.directory_load_push.setObjectName("directory_load_push")
        self.clear_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_push_button.setGeometry(QtCore.QRect(520, 280, 75, 23))
        self.clear_push_button.setStyleSheet("background-color: rgb(96, 181, 255);")
        self.clear_push_button.setObjectName("clear_push_button")
        self.image_display = QtWidgets.QGraphicsView(self.centralwidget)
        self.image_display.setGeometry(QtCore.QRect(20, 50, 471, 441))
        self.image_display.setStyleSheet("border: rgb(15, 15, 15);")
        self.image_display.setObjectName("image_display")
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(610, 50, 75, 23))
        self.next_button.setStyleSheet("background-color: rgb(96, 181, 255);")
        self.next_button.setObjectName("next_button")
        self.previous_button = QtWidgets.QPushButton(self.centralwidget)
        self.previous_button.setGeometry(QtCore.QRect(520, 50, 75, 23))
        self.previous_button.setStyleSheet("background-color: rgb(96, 181, 255);")
        self.previous_button.setObjectName("previous_button")
        self.text_list_display = QtWidgets.QListView(self.centralwidget)
        self.text_list_display.setGeometry(QtCore.QRect(520, 80, 281, 192))
        self.text_list_display.setAutoFillBackground(True)
        self.text_list_display.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-color: rgb(96, 181, 255);")
        self.text_list_display.setObjectName("text_list_display")
        self.directory_search_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.directory_search_push_button.setGeometry(QtCore.QRect(90, 20, 23, 21))
        self.directory_search_push_button.setStyleSheet("background-color: rgb(96, 181, 255);")
        self.directory_search_push_button.setObjectName("directory_search_push_button")
        self.directory_display = QtWidgets.QTextEdit(self.centralwidget)
        self.directory_display.setEnabled(False)
        self.directory_display.setGeometry(QtCore.QRect(120, 10, 681, 31))
        font = QtGui.QFont()
        font.setKerning(False)
        self.directory_display.setFont(font)
        self.directory_display.setAutoFillBackground(True)
        self.directory_display.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-color: rgb(96, 181, 255);")
        self.directory_display.setObjectName("directory_display")
        self.save_push_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_push_button.setGeometry(QtCore.QRect(10, 20, 61, 23))
        self.save_push_button.setStyleSheet("background-color: rgb(96, 181, 255);")
        self.save_push_button.setObjectName("save_push_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 819, 21))
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
        self.directory_load_push.setText(_translate("MainWindow", "Load"))
        self.clear_push_button.setText(_translate("MainWindow", "Clear"))
        self.next_button.setText(_translate("MainWindow", "next"))
        self.previous_button.setText(_translate("MainWindow", "previous"))
        self.directory_search_push_button.setText(_translate("MainWindow", "..."))
        self.directory_display.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.save_push_button.setText(_translate("MainWindow", "Save"))
