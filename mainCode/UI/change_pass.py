# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_pass.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 90, 101, 101))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/Users/jqyyd/Desktop/屏幕截图 2023-06-26 230630.jpg"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(340, 70, 301, 141))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_id = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_id.setGeometry(QtCore.QRect(100, 220, 291, 61))
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.lineEdit_initial = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_initial.setEchoMode(QLineEdit.Password)
        self.lineEdit_initial.setGeometry(QtCore.QRect(420, 220, 291, 61))
        self.lineEdit_initial.setObjectName("lineEdit_initial")
        self.lineEdit_new1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_new1.setGeometry(QtCore.QRect(100, 330, 291, 61))
        self.lineEdit_new1.setObjectName("lineEdit_new1")
        self.lineEdit_new1.setEchoMode(QLineEdit.Password)
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(200, 430, 141, 81))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(24)
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_modify = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_modify.setGeometry(QtCore.QRect(480, 430, 141, 81))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(24)
        self.pushButton_modify.setFont(font)
        self.pushButton_modify.setObjectName("pushButton_modify")
        self.lineEdit_new2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_new2.setGeometry(QtCore.QRect(420, 330, 291, 61))
        self.lineEdit_new2.setObjectName("lineEdit_new2")
        self.lineEdit_new2.setEchoMode(QLineEdit.Password)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menuchange_paswwrod = QtWidgets.QMenu(self.menubar)
        self.menuchange_paswwrod.setObjectName("menuchange_paswwrod")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuchange_paswwrod.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Python酒店预定系统"))
        self.label_2.setText(_translate("mainWindow", "酒店预定系统"))
        self.lineEdit_id.setPlaceholderText(_translate("mainWindow", "请输入用户ID"))
        self.lineEdit_initial.setPlaceholderText(_translate("mainWindow", "请输入原始密码"))
        self.lineEdit_new1.setPlaceholderText(_translate("mainWindow", "请输入新密码"))
        self.pushButton_back.setText(_translate("mainWindow", "返回"))
        self.pushButton_modify.setText(_translate("mainWindow", "修改"))
        self.lineEdit_new2.setPlaceholderText(_translate("mainWindow", "请再次输入新密码"))
        self.menuchange_paswwrod.setTitle(_translate("mainWindow", "change_password"))