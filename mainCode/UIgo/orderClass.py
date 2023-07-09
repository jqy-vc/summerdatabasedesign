from mainCode.UI2py.order import Ui_MainWindow as order_ui
from mainCode.tools.MySQLTools import MySqlTools
from mainCode.UIgo.order_alterClass import order_alter
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
import datetime


class order(QMainWindow, order_ui):
    sig_user = pyqtSignal(str)
    sig_order = pyqtSignal(str)

    def __init__(self):
        super(order, self).__init__()
        self.query_window = None
        self.setupUi(self)
        self.user_id = None
        self.pushButton_back.clicked.connect(self.back_to_query)
        self.pushButton_alter.clicked.connect(self.to_order_alter)
        self.pushButton_login.clicked.connect(self.back_to_login)
        self.pushButton_cancel.clicked.connect(self.cancel)

    def receive(self, user):
        """
        接收账号信息并展示
        :param user:账号
        :return: 无返回值
        """
        self.user_id = user
        self.label.setText(user)
        self.reservation_show()

    def send_signal(self):
        """
        发送账号信息
        :return: 无返回值
        """
        user_id = self.user_id
        self.sig_user.emit(user_id)

    def back_to_query(self):
        """
        返回query界面
        :return: 无返回值
        """
        from mainCode.UIgo.queryClass import query
        self.query_window = query()
        self.sig_user.connect(self.query_window.receive_user_id)
        self.send_signal()
        self.query_window.show()
        self.close()

    def to_order_alter(self):
        """
        跳转至order_alter界面并check订单号是否有效
        :return: 无返回值
        """
        if self.comboBox.currentText() == '请选择订单号':
            QMessageBox.warning(None, 'warning!', '请选择订单号！')
            return
        self.order_alter_window = order_alter()
        self.sig_order.connect(self.order_alter_window.receive_order)
        self.send_signal_alter()
        self.sig_user.connect(self.order_alter_window.receive_user)
        self.send_signal()
        self.order_alter_window.show()
        self.close()

    def send_signal_alter(self):
        """
        发送订单号信号
        :return: 无返回值
        """
        order_id = self.comboBox.currentText()
        self.sig_order.emit(order_id)

    def back_to_login(self):
        """
        切换账号跳转至登录界面
        :return: 无返回值
        """
        from mainCode.UIgo.loginClass import login
        self.login_window = login()
        self.login_window.show()
        self.close()

    def reservation_query(self):
        """
        查询订单
        :return:所有符合条件的订单
        """
        reservation = MySqlTools('reservation')
        user = MySqlTools('user')
        user_id = self.user_id
        try:
            is_admin = user.query(column='is_admin', condition='user_id="{}"'.format(user_id))[0][0]
            if is_admin:
                orders = reservation.query()
            else:
                orders = reservation.query(condition='user_id="{}"'.format(user_id))
            return orders
        except Exception as e:
            QMessageBox.warning(None, 'warning!', '查询失败！')
            return
        finally:
            reservation.close()

    def reservation_show(self):
        """
        展示订单
        :return:无返回值
        """
        hotel = MySqlTools('hotel')
        reservation = MySqlTools('reservation')
        order_list = self.reservation_query()
        if order_list is None:
            return
        self.tableWidget.setRowCount(len(order_list))
        for i in range(len(order_list)):
            order_id = order_list[i][0]
            hotel_id = order_list[i][2]
            room_id = order_list[i][3]
            name = order_list[i][4]
            checkin = order_list[i][10]
            checkout = order_list[i][11]

            import datetime
            interval = checkout - checkin  # 两日期差距
            payment = interval.days*order_list[i][14]
            status_int = order_list[i][13]

            if checkin < datetime.datetime.today().date() and status_int not in [-1, 2]:
                status_int = 2
                reservation.update(condition='order_status=2 where order_id={}'.format(order_id))

            hotel_name = hotel.query(column='hotel_name', condition='hotel_id={}'.format(hotel_id))[0][0]
            status = self.status_change(status_int)

            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(order_id)))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(hotel_name)))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(room_id)))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(name)))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(checkin)))
            self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(checkout)))
            self.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(str(payment)))
            self.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(status)))
            self.comboBox.addItem("{}".format(order_id))

        hotel.close()
        reservation.close()

    @staticmethod
    def status_change(status: int):
        """
        状态展示转换函数
        :param status:数据库中存的状态值
        :return: 展示的状态值
        """
        if status == 1:
            return "已提交"
        if status == 0:
            return "已修改"
        if status == -1:
            return "已取消"
        if status == 2:
            return "已完成"

    def cancel(self):
        """
        取消订单并修改订单状态
        :return: 无返回值
        """
        reservation = MySqlTools('reservation')
        order_id = self.comboBox.currentText()
        if order_id == '请选择订单号':
            QMessageBox.warning(None, 'warning!', '请选择订单号!')
            return
        status = self.status_change(-1)
        try:
            reservation.update(condition='order_status=-1 where order_id={}'.format(order_id))
            self.tableWidget.setItem(self.find_row_table(), 7, QtWidgets.QTableWidgetItem(str(status)))
            QMessageBox.information(None, 'msg', '操作成功!')
        except:
            QMessageBox.warning(None, 'warning!', '操作失败！')

        reservation.close()

    def find_row_table(self):
        """
        查找取消的订单号
        :return: 订单所在行
        """
        row_count = self.tableWidget.rowCount()
        for row in range(row_count):
            item = self.tableWidget.item(row, 0)
            if item is not None and item.text() == self.comboBox.currentText():
                return row






'''from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = order()
    window.show()
    sys.exit(app.exec_())'''