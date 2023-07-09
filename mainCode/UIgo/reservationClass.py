from mainCode.UI2py.reservation import Ui_MainWindow as reservation_ui
from mainCode.tools.MySQLTools import MySqlTools
from mainCode.UIgo.orderClass import order
from mainCode.UIgo.hotelClass import hotel
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
import datetime


class reservation(QMainWindow, reservation_ui):
    sig_user = pyqtSignal(str)

    def __init__(self):
        super(reservation, self).__init__()
        self.setupUi(self)
        self.sig = None
        self.hotel_id = None
        self.user_id = None
        self.order_window = order()
        self.pushButton_cancel.clicked.connect(self.back_to_hotel)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_commit.clicked.connect(self.commit_check)
        self.sig_user.connect(self.order_window.receive)
        self.pushButton_commit.clicked.connect(self.send_signal)

    def back_to_hotel(self):
        """
        返回hotel界面
        :return: 无返回值
        """
        self.hotel_window = hotel()
        self.sig_user.connect(self.hotel_window.receive_user_id)
        self.send_signal()
        self.hotel_window.show()

    def receive(self, dic):
        """
        接收信息
        :param dic:信息字典
        :return: 无返回值
        """
        self.sig = dic
        print(dic)
        self.label_hotel.setText(dic['hotel'])
        self.label_room.setText(dic['room'])
        self.hotel_id = dic['hotel_id']
        self.user_id = dic['user_id']

    def commit_check(self):
        """
        check提交的信息是否有效并提交
        :return: 无返回值
        """

        name = self.plainTextEdit_name.toPlainText()
        if name == '':
            QMessageBox.warning(None, 'warning!', "姓名不能为空！")
            return
        sex = self.comboBox_sex.currentText()
        if sex == '女':
            sex = 0
        else:
            sex = 1
        id_num = self.plainTextEdit_idNum.toPlainText()
        id_num_list = list(id_num)
        if len(id_num_list) != 18:
            QMessageBox.warning(None, 'warning!', "请输入18位身份证号")
            return
        telephone = self.plainTextEdit_telephone.toPlainText()
        telephone_list = list(telephone)
        if len(telephone_list) != 11 or telephone.isdigit() is False:
            QMessageBox.warning(None, 'warning!', "请输入11位手机号")
            return

        email = self.plainTextEdit_email.toPlainText()
        customers = self.comboBox_customers.currentText()
        if customers == '入住人数':
            QMessageBox.warning(None, 'warning!', '请选择入住人数！')
            return

        checkin = self.dateEdit_in.date().toString("yyyy-MM-dd")
        checkout = self.dateEdit_out.date().toString("yyyy-MM-dd")
        self.days_1=self.dateEdit_in.date().year()*365+self.dateEdit_in.date().month()*30+self.dateEdit_in.date().day()
        self.days_2 = self.dateEdit_out.date().year() * 365 + self.dateEdit_out.date().month() * 30 + self.dateEdit_out.date().day()
        if self.dateEdit_in.date() > self.dateEdit_out.date():
            QMessageBox.warning(None, 'warning!', '入住时间应当早于离开时间')
            return

        remarks = self.plainTextEdit_remarks.toPlainText()
        hotel_id = self.hotel_id
        room_type = self.label_room.text()

        reservation = MySqlTools("reservation")
        room = MySqlTools("room")
        date_list = reservation.query(column='order_id,check_in,check_out,room_id',
                                      condition='order_status!=-1 and order_status!=2 and hotel_id={}'.format(hotel_id))

        for d in date_list:
            order_id = d[0]
            check_in_re = d[1]
            check_out_re = d[2]
            room_id = d[3]
            if check_in_re <= datetime.date(
                    *map(int, checkin.split('-'))) <= check_out_re or check_in_re <= datetime.date(*map(int, checkout.split('-'))) <= check_out_re:
                room.update(condition='room_status=0 where hotel_id={} and room_number={}'.format(hotel_id, room_id))
        room_1 = room.query(column='room_number',
                            condition='hotel_id={} and room_type="{}" and room_status!=0'.format(hotel_id, room_type))
        if len(room_1) == 0:
            QMessageBox.information(None, 'msg', '该时间段该房型已无剩余')
        else:
            room_num = room_1[0][0]
            if reservation.query(column='max(order_id)')[0][0] is not None:
                order_id_max = reservation.query(column='max(order_id)')[0][0] + 1
            else:
                order_id_max = 1
            room_price = room.query(column='room_price',
                                    condition='hotel_id={} and room_number={}'.format(hotel_id, room_num))[0][0]
            params = {
                'order_id': str(order_id_max),
                'user_id': "\"" + self.user_id + "\"",
                'hotel_id': str(hotel_id),
                'room_id': str(room_num),
                'customer_name': "\"" + name + "\"",
                'customer_sex': str(sex),
                'id_number': "\"" + id_num + "\"",
                'telephone_number': str(telephone),
                'email': "\"" + email + "\"",
                'customer_number': str(customers),
                'check_in': "\"" + checkin + "\"",
                'check_out': "\"" + checkout + "\"",
                'remarks': "\"" + remarks + "\"",
                'order_status': '1',
                'room_price_onenight': str(room_price)
            }
            reservation.insert(params)
            room.update(condition='room_status=1 where room_status=0 and hotel_id={} '.format(hotel_id))
            QMessageBox.information(None, 'msg', '预订成功！')
            self.order_window.show()
            self.close()
        reservation.close()
        room.close()

    def send_signal(self):
        """
        发送账号信号
        :return: 无返回值
        """
        user_id = self.user_id
        self.sig_user.emit(user_id)

from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = reservation()
    window.show()
    sys.exit(app.exec_())