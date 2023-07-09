import logging
from PageDownload import PageDownload
import pymysql
from tools.MySQLTools import MySqlTools
from lxml import etree
import random

"""
author:zhuguixin
date:2023/6/27 21:17
"""


def spider2hotel():
    spider = MySqlTools("spider_hotel")
    hotel = MySqlTools("hotel")

    spider_list = spider.query(condition='sourceCode!="暂无"')
    i = 1
    for s in spider_list:
        uid = i
        url = s[1]
        name = s[2]
        city = s[3]
        html = etree.HTML(s[-1])
        try:
            address = html.xpath("//p[@id='showMap2']/span/text()")[0].replace("\n", "")
            introduce = html.xpath("//div[@id='property_description_content']//p[@class]/text()")[0].replace("\n", "")
        except:
            continue
        syh = "\""
        params_hotel = {
            'hotel_id': syh + str(uid) + syh,
            'hotel_name': syh + name + syh,
            'hotel_address': syh + address + syh,
            'hotel_city': syh + city + syh,
            'hotel_introduce': syh + introduce + syh
        }
        if len(hotel.query(condition='hotel_name=' + syh + name + syh)) > 0:
            logging.info("exists!{}".format(name))
            i = i + 1
            continue
        try:
            hotel.insert(params_hotel)
            logging.info(params_hotel)
            i = i + 1
        except Exception as e:
            logging.info("fail:{} with {}".format(params_hotel["hotel_id"], e))
    spider.close()
    hotel.close()


def spider2room():
    spider = MySqlTools("spider_hotel")
    spider_list = spider.query(condition='sourceCode!="暂无"', limit=400)
    hotel = MySqlTools("hotel")
    room = MySqlTools("room")

    for s in spider_list:
        html = etree.HTML(s[-1])
        try:
            room_type_list = html.xpath("//section[@class='roomstable']//a/span/text()")
        except:
            continue
        name = "\"" + s[2] + "\""
        try:
            uid = "\"" + hotel.query(condition='hotel_name=' + name)[0][0] + "\""
        except:
            continue
        for i in range(len(room_type_list)):
            floor = (i + 2) * 100
            for j in range(1, 16):
                room_num = floor + j
                params = {
                    'room_type': "\"" + room_type_list[i] + "\"",
                    'hotel_id': uid,
                    'hotel_name': name,
                    'room_num': str(room_num),
                    'room_price': str(float(random.randint(300, 800))),
                    'room_cap': str(random.randint(1, 3)),
                    'room_status': str(1)
                }
                try:
                    room.insert(params)
                except Exception as e:
                    logging.info("fail:{} with {}".format(params["hotel_id"], e))

    spider.close()
    hotel.close()
    room.close()


if __name__ == "__main__":
    spider2room()
