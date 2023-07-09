from mainCode.UI2py.login import Ui_MainWindow as login_ui
from mainCode.UIgo.registerClass import register
from mainCode.tools.MySQLTools import MySqlTools
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from mainCode.UIgo.queryClass import query
from mainCode.UIgo.changeClass import change

class login(QMainWindow, login_ui):
    sig_user = pyqtSignal(str)

    def __init__(self):
        super(login, self).__init__()
        self.setupUi(self)
        self.query_window = query()
        self.pushButton_register.clicked.connect(self.to_register)
        self.pushButton_login.clicked.connect(self.login_check)
        self.pushButton_change_ps.clicked.connect(self.change_password)

    def login_check(self):
        """
        check账号和密码是否正确
        :return: 无返回值
        """
        user = MySqlTools("user")
        account = self.plainTextEdit_account.toPlainText()
        password = self.plainTextEdit_password.text()
        if account == '' or password == '':
            QMessageBox.warning(None, 'warning!', '账号或密码不得为空值！')
            return
        user_pass = user.query(column='password', condition='user_id="{}"'.format(account))[0][0]
        if password != user_pass:
            QMessageBox.warning(None, 'warning!', "账号或密码错误")
            return
        else:
            self.sig_user.connect(self.query_window.receive_user_id)
            self.send_signal()
            self.query_window.show()
            self.close()

    def send_signal(self):
        """
        发送账号信息至其他界面
        :return: 无返回值
        """
        user_id = self.plainTextEdit_account.toPlainText()
        self.sig_user.emit(user_id)

    def to_register(self):
        """
        跳转至注册界面
        :return: 无返回值
        """
        self.register_window = register()
        self.register_window.show()
        self.close()

    def change_password(self):
        '''

        '''
        self.change_window = change()
        self.change_window.show()
        self.close()



