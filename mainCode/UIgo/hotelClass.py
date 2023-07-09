import datetime
from mainCode.UI2py.hotel import Ui_MainWindow as hotel_ui
from mainCode.tools.MySQLTools import MySqlTools
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets

"""
该类为对hotel界面类的重写以实现相关功能
"""


class hotel(QMainWindow, hotel_ui):
    sig = pyqtSignal(dict)
    sig_user = pyqtSignal(str)

    def __init__(self):
        super(hotel, self).__init__()
        self.setupUi(self)
        self.user_id = None
        from mainCode.UIgo.reservationClass import reservation
        self.reservation_window = reservation()

        self.pushButton_res.clicked.connect(self.reservation_check)
        self.pushButton_room.clicked.connect(self.show_room)
        self.pushButton_hotel.clicked.connect(self.show_hotel)
        self.pushButton_back.clicked.connect(self.toquery)

        for city in self.city_list():
            self.comboBox.addItem(city[0])

    def receive_user_id(self, user):
        """
        用于接收用户信息
        :param user: 接收的用户名
        :return: 无返回值
        """
        self.user_id = user

    def send_signal(self):
        """
        用于发送信号的，将酒店名，房间类型，酒店id，用户id等信号发送出去
        :return: 无返回值
        """
        hotel = self.plainTextEdit_res_hotel.toPlainText()
        room = self.plainTextEdit_res_room.toPlainText()
        hotel_name = MySqlTools('hotel').query(column='hotel_name', condition='hotel_id={}'.format(hotel))
        dic = {
            'hotel': hotel_name[0][0],
            'room': room,
            'hotel_id': hotel,
            'user_id': self.user_id
        }
        self.sig.emit(dic)

    def reservation_check(self):
        """
        用于对预订信息做check的，保证输入的酒店id和房间类型是有效的并跳转至下一界面
        :return: 无返回值
        """
        hotel = self.plainTextEdit_res_hotel.toPlainText()
        room = self.plainTextEdit_res_room.toPlainText()
        if hotel == '' or room == '':
            QMessageBox.warning(None, "warning!", "酒店id或房间类型不能为空！")
            return
        hotel_check = MySqlTools("hotel").query(condition='hotel_id="{}"'.format(hotel))
        room_check = MySqlTools("room").query(condition='hotel_id={} and room_type="{}"'.format(hotel, room))
        if len(hotel_check) == 0 or len(room_check) == 0:
            QMessageBox.warning(None, "warning!", "酒店id或房间类型填写错误！")
            return
        else:
            self.sig.connect(self.reservation_window.receive)
            self.send_signal()
            self.reservation_window.show()
            self.close()

    def hotel_query(self):
        """
        用于酒店查询的
        :return: 酒店列表
        """
        hotel = MySqlTools("hotel")
        city = self.comboBox.currentText()
        hotel_list = hotel.query(condition='hotel_city="{}"'.format(city))
        hotel.close()
        return hotel_list

    def city_list(self):
        """
        用于查询城市的
        :return: 城市列表
        """
        self.sql = MySqlTools("hotel")
        city_list = self.sql.query(column='distinct(hotel_city)')
        self.sql.close()
        return city_list

    def show_hotel(self):
        """
        将查询到的酒店列表展示出来
        :return: 无返回值
        """
        i = 0
        hotel_list = self.hotel_query()
        self.tableWidget_hotel.setRowCount(len(hotel_list))
        for hotel in hotel_list:
            hotel_id = hotel[0]
            hotel_name = hotel[1]
            hotel_address = hotel[2]
            hotel_introduce = hotel[-1]
            self.tableWidget_hotel.setItem(i, 0, QtWidgets.QTableWidgetItem(str(hotel_id)))
            self.tableWidget_hotel.setItem(i, 1, QtWidgets.QTableWidgetItem(str(hotel_name)))
            self.tableWidget_hotel.setItem(i, 2, QtWidgets.QTableWidgetItem(hotel_address))
            self.tableWidget_hotel.setItem(i, 3, QtWidgets.QTableWidgetItem(hotel_introduce))
            i = i + 1

    def room_query(self):
        """
        用于房间查询的
        :return: 房间信息字典
        """
        room = MySqlTools("room")
        hotel_id = self.lineEdit_room.text()
        try:
            room_type = room.query(column='distinct(room_type)', condition='hotel_id={}'.format(hotel_id))
        except:
            QMessageBox.warning(None, 'warning!', '请输入正确的酒店ID!')
            return
        room_price = []
        room_cap = []
        room_num = []
        for type in room_type:
            room_price.append(room.query(column='distinct(room_price)',
                                         condition='hotel_id={} and room_type="{}"'.format(hotel_id, type[0])))
            room_cap.append(room.query(column='distinct(room_cap)',
                                       condition='hotel_id={} and room_type="{}"'.format(hotel_id, type[0])))
            # 计算还剩多少房间
            reservation = MySqlTools("reservation")
            room = MySqlTools("room")
            date_list = reservation.query(column='order_id,check_in,check_out,room_id',
                                          condition='order_status!=-1 and order_status!=2 and hotel_id={}'.format(hotel_id))
            checkin = self.dateEdit_check_in.date().toString("yyyy-MM-dd")
            checkout = self.dateEdit_check_out.date().toString("yyyy-MM-dd")
            for d in date_list:
                order_id = d[0]
                check_in_re = d[1]
                check_out_re = d[2]
                room_id = d[3]
                if check_in_re <= datetime.date(*map(int, checkin.split('-'))) <= check_out_re or check_in_re <= datetime.date(*map(int, checkout.split('-'))) <= check_out_re:
                    room.update(condition='room_status=0 where hotel_id={} and room_number={}'.format(hotel_id, room_id))
            room_1 = room.query(column='room_number',
                                condition='hotel_id={} and room_type="{}" and room_status!=0'.format(hotel_id, type[0]))

            room_num.append(len(room_1))
        room.update(condition='room_status=1 where room_status=0 and hotel_id={} '.format(hotel_id))
        room.close()
        room_dict = {
            'room_type': room_type,
            'room_price': room_price,
            'room_cap': room_cap,
            'room_num': room_num
        }
        return room_dict

    def show_room(self):
        """
        将房间信息展示出来
        :return: 无返回值
        """
        room_type_dict = self.room_query()
        if room_type_dict is None:
            return
        room_type_list = room_type_dict['room_type']
        room_price_list = room_type_dict['room_price']
        room_cap_list = room_type_dict['room_cap']
        room_num_list = room_type_dict['room_num']
        self.tableWidget_room.setRowCount(len(room_type_list))

        for i in range(len(room_type_list)):
            room_type = room_type_list[i][0]
            room_price = room_price_list[i][0][0]
            room_cap = room_cap_list[i][0][0]
            room_num = room_num_list[i]
            self.tableWidget_room.setItem(i, 0, QtWidgets.QTableWidgetItem(str(room_type)))
            self.tableWidget_room.setItem(i, 1, QtWidgets.QTableWidgetItem(str(room_price)))
            self.tableWidget_room.setItem(i, 2, QtWidgets.QTableWidgetItem(str(room_cap)))
            self.tableWidget_room.setItem(i, 3, QtWidgets.QTableWidgetItem(str(room_num)))
    def send_signal_id(self):
        """
        发送账号信息
        :return: 无返回值
        """
        user_id = self.user_id
        self.sig_user.emit(user_id)

    def toquery(self):
        from mainCode.UIgo.queryClass import query
        self.query_window = query()
        self.sig_user.connect(self.query_window.receive_user_id)
        self.send_signal_id()
        self.query_window.show()
        self.close()
