from mainCode.UI2py.query import Ui_MainWindow as query_ui
from mainCode.UIgo.hotelClass import hotel
from mainCode.UIgo.orderClass import order
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal


class query(QMainWindow, query_ui):
    sig_user = pyqtSignal(str)

    def __init__(self):
        super(query, self).__init__()
        self.setupUi(self)
        self.user_id = None
        self.hotel_window = hotel()
        self.order_window = order()

        self.pushButton_hotel.clicked.connect(self.send_signal)
        self.sig_user.connect(self.hotel_window.receive_user_id)
        self.pushButton_hotel.clicked.connect(self.close)
        self.pushButton_hotel.clicked.connect(self.hotel_window.show)
        self.sig_user.connect(self.order_window.receive)
        self.pushButton_reservation.clicked.connect(self.send_signal)
        self.pushButton_reservation.clicked.connect(self.close)
        self.pushButton_reservation.clicked.connect(self.order_window.show)
        self.pushButton_change.clicked.connect(self.back_to_login)

    def receive_user_id(self, user):
        """
        接收信息
        :param user:用户账号
        :return: 无返回值
        """
        self.user_id = user

    def send_signal(self):
        """
        发送信息
        :return:无返回值
        """
        user_id = self.user_id
        self.sig_user.emit(user_id)

    def back_to_login(self):
        """
        回到登陆界面
        :return:无返回值
        """
        from mainCode.UIgo.loginClass import login
        self.login_window = login()
        self.login_window.show()
        self.close()