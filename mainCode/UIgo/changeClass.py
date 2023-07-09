from mainCode.UI2py.change_pass import Ui_mainWindow as change_ui
from mainCode.tools.MySQLTools import MySqlTools
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
"""
该类为对change_password界面类的重写以实现相关功能
"""


class change(QMainWindow, change_ui):

    def __init__(self):
        super(change, self).__init__()
        self.setupUi(self)
        self.pushButton_back.clicked.connect(self.backtologin)
        self.pushButton_modify.clicked.connect(self.changepass)

    def backtologin(self):
        """
        返回登录界面
        :return: 无返回值
        """
        from mainCode.UIgo.loginClass import login
        self.login_window = login()
        self.login_window.show()
        self.close()


    def changepass(self):
        user = MySqlTools("user")
        userid = self.lineEdit_id.text()
        initial = self.lineEdit_initial.text()
        new_pass_1 = self.lineEdit_new1.text()
        new_pass_2 = self.lineEdit_new2.text()
        if userid == '' or initial == '':
            QMessageBox.warning(None, "warning!", "账号与密码不得为空值")
            return
        if new_pass_1 != new_pass_2:
            QMessageBox.warning(None, "warning!", "两次输入的密码需一致")
            return
        if new_pass_1 == initial:
            QMessageBox.warning(None, "warning!", "新旧密码不能相同")
            return
        if initial != user.query(column='password', condition='user_id="{}"'.format(userid))[0][0]:
            QMessageBox.warning(None, "warning!", "密码不正确")
            return
        if [userid] not in user.query(column='user_id'):
            QMessageBox.warning(None, "warning!", "账号不存在")
            return
        else:
            try:
                params = {
                    'user_id': "\"" + userid + "\"",
                    'password': "\"" + new_pass_1 + "\"",
                    'is_admin': '0'
                }
                user.update(condition='password="{}" where user_id="{}"'.format(new_pass_1, userid))
                QMessageBox.information(None, "msg", "修改成功")
                self.backtologin()
            except Exception as e:
                QMessageBox.information(None, "error", "出错了")
                print(e)
            finally:
                user.close()
