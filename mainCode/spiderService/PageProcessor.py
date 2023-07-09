import logging

from PageDownload import PageDownload
import uuid
from tools.MySQLTools import MySqlTools
from pymysql.converters import escape_str

"""
author:zhuguixin
date:2023/6/27 15:55
"""


def hangzhou():
    # "https://www.booking.cn/searchresults.zh-cn.html?sid=e02808502ac39012238a253d04e30657&aid=1662037&city=-1908366&offset=25"

    url_pre = "https://www.booking.cn/searchresults.zh-cn.html?sid=e02808502ac39012238a253d04e30657&aid=1662037&city=-1908366&offset="
    mysql_table = MySqlTools("spider_hotel")
    for i in range(8):
        url = url_pre + str(i * 25)
        page_download = PageDownload(url)
        html = page_download.get_html_chrome()
        hotel_url_list = html.xpath("//a[@data-testid='title-link']/@href")
        hotel_title_list = html.xpath("//a[@data-testid='title-link']/div[1]/text()")

        for j in range(len(hotel_url_list)):
            syh = "\""
            uid = syh + str(uuid.uuid1()).replace("-", "") + syh
            hotel_url = syh + hotel_url_list[j] + syh
            hotel_title = syh + hotel_title_list[j].replace("\n", "") + syh
            if len(mysql_table.query(condition='name=' + hotel_title)) > 0:
                logging.info("exists,id={}".format(mysql_table.query(condition='name=' + hotel_title)[0][0]))
                continue
            sourceCode = '"暂无"'
            params = {
                'id': uid,
                'url': hotel_url,
                'name': hotel_title,
                'city': '\"杭州\"',
                'sourceCode': sourceCode
            }
            mysql_table.insert(params)
    mysql_table.close()


def shanghai():
    url_pre = "https://www.booking.cn/searchresults.zh-cn.html?sid=e02808502ac39012238a253d04e30657&aid=1662037&city=-1924465&offset="
    mysql_table = MySqlTools("spider_hotel")
    for i in range(19):
        url = url_pre + str(i * 25)
        page_download = PageDownload(url)
        html = page_download.get_html_chrome()
        hotel_url_list = html.xpath("//a[@data-testid='title-link']/@href")
        hotel_title_list = html.xpath("//a[@data-testid='title-link']/div[1]/text()")

        for j in range(len(hotel_url_list)):
            syh = "\""
            uid = syh + str(uuid.uuid1()).replace("-", "") + syh
            hotel_url = syh + hotel_url_list[j] + syh
            hotel_title = syh + hotel_title_list[j].replace("\n", "") + syh
            if len(mysql_table.query(condition='name=' + hotel_title)) > 0:
                logging.info("exists,id={}".format(mysql_table.query(condition='name=' + hotel_title)[0][0]))
                continue
            sourceCode = '"暂无"'
            params = {
                'id': uid,
                'url': hotel_url,
                'name': hotel_title,
                'city': '\"上海\"',
                'sourceCode': sourceCode
            }
            mysql_table.insert(params)
    mysql_table.close()

def beijing():
    url_pre = "https://www.booking.cn/searchresults.zh-cn.html?sid=e02808502ac39012238a253d04e30657&aid=1662037&city=-1898541&offset="
    mysql_table = MySqlTools("spider_hotel")
    for i in range(16):
        url = url_pre + str(i * 25)
        page_download = PageDownload(url)
        html = page_download.get_html_chrome()
        hotel_url_list = html.xpath("//a[@data-testid='title-link']/@href")
        hotel_title_list = html.xpath("//a[@data-testid='title-link']/div[1]/text()")

        for j in range(len(hotel_url_list)):
            syh = "\""
            uid = syh + str(uuid.uuid1()).replace("-", "") + syh
            hotel_url = syh + hotel_url_list[j] + syh
            hotel_title = syh + hotel_title_list[j].replace("\n", "") + syh
            if len(mysql_table.query(condition='name=' + hotel_title)) > 0:
                logging.info("exists,id={}".format(mysql_table.query(condition='name=' + hotel_title)[0][0]))
                continue
            sourceCode = '"暂无"'
            params = {
                'id': uid,
                'url': hotel_url,
                'name': hotel_title,
                'city': '\"北京\"',
                'sourceCode': sourceCode
            }
            mysql_table.insert(params)
    mysql_table.close()


def ningbo():
    url_pre = "https://www.booking.cn/searchresults.zh-cn.html?sid=e02808502ac39012238a253d04e30657&aid=1662037&city=-1920233&offset="
    mysql_table = MySqlTools("spider_hotel")
    for i in range(3):
        url = url_pre + str(i * 25)
        page_download = PageDownload(url)
        html = page_download.get_html_chrome()
        hotel_url_list = html.xpath("//a[@data-testid='title-link']/@href")
        hotel_title_list = html.xpath("//a[@data-testid='title-link']/div[1]/text()")

        for j in range(len(hotel_url_list)):
            syh = "\""
            uid = syh + str(uuid.uuid1()).replace("-", "") + syh
            hotel_url = syh + hotel_url_list[j] + syh
            hotel_title = syh + hotel_title_list[j].replace("\n", "") + syh
            if len(mysql_table.query(condition='name=' + hotel_title)) > 0:
                logging.info("exists,id={}".format(mysql_table.query(condition='name=' + hotel_title)[0][0]))
                continue
            sourceCode = '"暂无"'
            params = {
                'id': uid,
                'url': hotel_url,
                'name': hotel_title,
                'city': '\"宁波\"',
                'sourceCode': sourceCode
            }
            mysql_table.insert(params)
    mysql_table.close()


def update_sourcecode():
    mysql = MySqlTools("spider_hotel")
    data_tuple = mysql.query(condition='sourceCode="暂无"')
    for data in data_tuple:
        uid = data[0]
        url = data[1]
        html = escape_str(PageDownload(url).get_page_chrome())
        condition = 'sourceCode=' + "\"" + html + "\"" + ' where id=' + "\"" + uid + "\""
        mysql.update(condition=condition)

    mysql.close()


if __name__ == "__main__":
    update_sourcecode()
