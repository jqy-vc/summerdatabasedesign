from mainCode.UI2py.order_alter import Ui_MainWindow as order_alter_ui
from mainCode.tools.MySQLTools import MySqlTools
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
import datetime


class order_alter(QMainWindow, order_alter_ui):
    sig_userId = pyqtSignal(str)

    def __init__(self):
        super(order_alter, self).__init__()
        self.setupUi(self)
        self.order_id = None
        self.user_id = None
        self.pushButton_back.clicked.connect(self.back_to_order)
        self.pushButton_alter.clicked.connect(self.alter_check)

    def receive_order(self, order):
        """
        接收订单信息，并展示
        :param order:订单号
        :return: 无返回值
        """
        self.order_id = order
        self.label_orderId.setText(order)
        self.order_show()

    def receive_user(self, user):
        """
        接收用户账号信息
        :param user: 账号信息
        :return: 无返回值
        """
        self.user_id = user

    def back_to_order(self):
        """
        返回order界面
        :return: 无返回值
        """
        from mainCode.UIgo.orderClass import order
        self.order_window = order()
        self.sig_userId.connect(self.order_window.receive)
        self.send_signal()
        self.order_window.show()
        self.close()

    def send_signal(self):
        """
        发送账号信息
        :return: 无返回值
        """
        user_id = self.user_id
        self.sig_userId.emit(user_id)

    def alter_check(self):
        """
        check订单是否可修改以及修改的信息是否有效
        :return: 无返回值
        """
        if self.status in [-1, 2]:
            QMessageBox.warning(None, 'warning', '该订单已取消或已完成，不可修改！')
            return
        reservation = MySqlTools('reservation')
        order_id = self.order_id
        name = self.plainTextEdit_name.toPlainText()
        sex = self.comboBox_sex.currentText()
        id_num = self.plainTextEdit_idNum.toPlainText()
        telephone = self.plainTextEdit_telephone.toPlainText()
        email = self.plainTextEdit_email.toPlainText()
        customers = self.comboBox_customers.currentText()
        check_in = datetime.date(*map(int, self.dateEdit_in.date().toString("yyyy-MM-dd").split('-')))
        check_out = datetime.date(*map(int, self.dateEdit_out.date().toString("yyyy-MM-dd").split('-')))
        remarks = self.plainTextEdit_remarks.toPlainText()

        if sex == '男':
            sex = 1
        else:
            sex = 0

        if len(list(id_num)) != 18:
            QMessageBox.warning(None, 'waring!', '请输入18位身份证号！')
            return

        if len(list(telephone)) != 11 or telephone.isdigit() is False:
            QMessageBox.warning(None, 'warning', '请输入11位手机号！')
            return

        reservation.update(
            condition='customer_name="{}",customer_sex={},id_number="{}",telephone_number={},email="{}",customer_number={},check_in="{}",check_out="{}",remarks="{}",order_status=0 where order_id={}'
            .format(name, sex, id_num, telephone, email, customers, check_in, check_out, remarks, order_id))
        QMessageBox.information(None, 'msg', '修改成功！')

        reservation.close()
        self.back_to_order()

    def order_query(self):
        """
        根据接收的订单号查询订单信息
        :return: 订单信息列表
        """
        order_id = self.order_id
        reservation = MySqlTools('reservation')
        order = reservation.query(condition='order_id={}'.format(order_id))
        reservation.close()
        return order[0]

    def order_show(self):
        """
        展示订单信息
        :return: 无返回值
        """
        order = self.order_query()
        user_id = order[1]
        hotel_id = order[2]
        room_id = order[3]
        name = order[4]
        sex = order[5]
        id_number = order[6]
        telephone = order[7]
        email = order[8]
        customers = order[9]
        check_in = order[10]
        check_out = order[11]
        remarks = order[12]
        self.status = order[13]

        hotel = MySqlTools('hotel')
        hotel_name = hotel.query(column='hotel_name', condition='hotel_id={}'.format(hotel_id))[0][0]
        hotel.close()
        if sex == 1:
            sex = "男"
        else:
            sex = "女"

        self.label_userId.setText(user_id)
        self.label_hotel.setText(hotel_name)
        self.label_room.setText(str(room_id))
        self.plainTextEdit_name.setPlainText(name)
        self.comboBox_sex.setCurrentText(sex)
        self.plainTextEdit_idNum.setPlainText(id_number)
        self.plainTextEdit_telephone.setPlainText(str(telephone))
        self.plainTextEdit_email.setPlainText(email)
        self.comboBox_customers.setCurrentText(str(customers))
        self.dateEdit_in.setDate(check_in)
        self.dateEdit_out.setDate(check_out)
        self.plainTextEdit_remarks.setPlainText(remarks)
