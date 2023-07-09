import pymysql
from testCode.settings import DATABASES
import logging

logging.getLogger().setLevel(logging.INFO)

"""
author:zhuguixin
date:2023/6/27 14/07
"""

"""
该类是用于对Mysql数据库做增删查改操作的
"""


class MySqlTools:
    """
    配置数据库信息，通过输入表名指定操作表
    """

    def __init__(self, table_name: str):
        connect = pymysql.connect(host=DATABASES.get("hostname"), user=DATABASES.get("username"),
                                  password=DATABASES.get("password"), database=DATABASES.get("name"),
                                  port=DATABASES.get("port"), charset='utf8')
        self.connect = connect
        self.table_name = table_name
        self.cursor = connect.cursor()

    def query(self, column="*", condition=None, limit=None):
        """
        该函数是用于查询数据库数据的
        :param column: 需要查找的列，或基于distinct之类操作的数据，例如distinct(id)，默认为*
        :param condition: 查询条件，例如id=1，默认为None
        :param limit: 限制数据，例如1000，默认为None
        :return: 返回查询数据的列表，例如[[1],[2]]
        """
        sql = 'select {} from {} '.format(column, self.table_name)
        if condition:
            sql = sql + ' where ' + condition
            if limit:
                sql = sql + ' limit ' + str(limit)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        table_list = []
        for r in result:
            table_list.append(list(r))
        if table_list is None:
            logging.info("{} don't have data".format(self.table_name))
        else:
            print(result)
        return table_list

    def insert(self, params: dict):
        """
        该函数是用于向数据库插入数据的
        :param params: 参数的字典，例如{'id':1,'name':'lihua'}，注意字典顺序必须与数据库字段顺序对应
        :return: 无返回值
        """
        params_values = []
        for p in params:
            params_values.append(params[p])
        params_str = ",".join(params_values)
        sql = 'insert into ' + self.table_name + ' values({})'.format(params_str)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            logging.info("insert successfully!")
        except Exception as e:
            logging.error("insert fail! with {}".format(e))

    def update(self, condition: str):
        """
        该函数是用于更新数据库数据的
        :param condition: 需要更新的字段值和条件，例如'id=3 where id=2'
        :return: 无返回值
        """
        sql = 'update ' + self.table_name + ' set ' + condition
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            logging.info("update successfully!")
        except Exception as e:
            logging.error("update fail! with {}".format(e))

    def delete(self, condition: str):
        """
        该函数是用于删除数据库数据的
        :param condition: 要删除的数据符合的条件，例如'id=1'
        :return: 无返回值
        """
        sql = 'delete from ' + self.table_name + ' where ' + condition
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            logging.info("delete successfully!")
        except Exception as e:
            logging.error("delete fail! with {}".format(e))

    def close(self):
        """
        该函数是用于关闭数据库游标和连接的，防止阻塞，每开一个必关一个
        :return: 无返回值
        """
        self.cursor.close()
        self.connect.close()
        logging.info("connection is closed!")


if __name__ == "__main__":
    # mysql_test = MySqlTools("spider_hotel")
    # mysql_test.insert({"id":'"12245"',"url":'"testtesttest"',"sourceCode":'"ttttt"',"city":'"杭州"'})
    # mysql_test.update('id=12121 where id=12245')
    # mysql_test.delete('city="宁波"')
    # mysql_test.query()
    # x = mysql_test.query()
    hotel = MySqlTools("hotel")
    hotel.query()
    # hotel.delete('hotel_city="杭州"')
    # mysql_test.close()
    hotel.close()
    room = MySqlTools("room")
    room.query()
    room.close()
