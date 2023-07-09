from mainCode.UI2py.register import Ui_MainWindow as register_ui
from mainCode.tools.MySQLTools import MySqlTools
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class register(QMainWindow, register_ui):
    def __init__(self):
        super(register, self).__init__()
        self.setupUi(self)
        self.pushButton_register.clicked.connect(self.show_massage)
        self.pushButton_cancel.clicked.connect(self.to_login)

    def show_massage(self):
        """
        check输入的账号密码并弹出提示框
        :return: 无返回值
        """
        user = MySqlTools("user")
        account = self.plainTextEdit_account.toPlainText()
        password = self.plainTextEdit_password.text()
        password2 = self.plainTextEdit_password_2.text()
        if account == '' or password == '':
            QMessageBox.warning(None, "warning!", "账号与密码不得为空值")
            return
        if password2 != password:
            QMessageBox.warning(None, "warning!", "两次输入的密码需一致")
            return
        if len(user.query(condition='user_id="{}"'.format(account))) > 0:
            QMessageBox.warning(None, "warning!", "账号已存在")
            return
        else:
            try:
                params = {
                    'user_id': "\""+ account+"\"",
                    'password': "\""+password+"\"",
                    'is_admin': '0'
                }
                user.insert(params=params)
                QMessageBox.information(None, "msg", "注册成功")
                self.to_login()
            except Exception as e:
                QMessageBox.information(None, "error", "出错了")
            finally:
                user.close()

    def to_login(self):
        """
        返回登录界面
        :return: 无返回值
        """
        from mainCode.UIgo.loginClass import login
        self.login_window = login()
        self.login_window.show()
        self.close()
