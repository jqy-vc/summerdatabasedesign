# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1111, 858)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit_account = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_account.setGeometry(QtCore.QRect(290, 230, 531, 101))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.plainTextEdit_account.setFont(font)
        self.plainTextEdit_account.setObjectName("plainTextEdit_account")
        self.plainTextEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.plainTextEdit_password.setEchoMode(QLineEdit.Password)
        self.plainTextEdit_password.setGeometry(QtCore.QRect(290, 400, 531, 101))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.plainTextEdit_password.setFont(font)
        self.plainTextEdit_password.setObjectName("plainTextEdit_password")
        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_login.setGeometry(QtCore.QRect(180, 580, 211, 101))
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_register = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_register.setGeometry(QtCore.QRect(470, 580, 211, 101))
        self.pushButton_register.setObjectName("pushButton_register")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(470, 90, 321, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 80, 131, 101))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:/Users/jqyyd/Desktop/屏幕截图 2023-06-26 230630.jpg"))
        self.label_2.setObjectName("label_2")
        self.pushButton_change_ps = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_change_ps.setGeometry(QtCore.QRect(760, 580, 211, 101))
        self.pushButton_change_ps.setObjectName("pushButton_change_ps")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1111, 33))
        self.menubar.setObjectName("menubar")
        self.menulogin = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menulogin.setFont(font)
        self.menulogin.setObjectName("menulogin")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menulogin.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python酒店预订系统"))
        self.plainTextEdit_account.setPlaceholderText(_translate("MainWindow", "请输入用户ID"))
        self.plainTextEdit_password.setPlaceholderText(_translate("MainWindow", "请输入用户密码"))
        self.pushButton_login.setText(_translate("MainWindow", "登录"))
        self.pushButton_register.setText(_translate("MainWindow", "注册"))
        self.label.setText(_translate("MainWindow", "酒店预订系统"))
        self.pushButton_change_ps.setText(_translate("MainWindow", "修改密码"))
        self.menulogin.setTitle(_translate("MainWindow", "login"))