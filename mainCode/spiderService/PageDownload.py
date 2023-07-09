import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from lxml import etree

logging.getLogger().setLevel(logging.INFO)

"""
author:zhuguixin
date:2023/6/17 13:20
"""

"""
网页爬取类
输入url爬取网页
"""


class PageDownload:

    def __init__(self, url: str):
        self.url = url

    def get_page(self):
        global page
        try:
            page = requests.get(self.url)
            page.encoding = page.apparent_encoding
            page_code = page.status_code
            logging.info("page downloaded! {}".format(self.url))
            logging.info("page_code:{}".format(page_code))
        except Exception as e:
            logging.info("fail! {}".format(self.url))
            logging.info(e)
        return page.text

    def get_html(self):
        html = etree.HTML(self.get_page())
        return html

    def get_page_chrome(self):
        global page
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument("--blink-settings=imagesEnabled=false")
        chrome_option.add_argument("--disable-infobars")
        chrome_option.page_load_strategy = "eager"
        # chrome_option.add_argument("--headless")

        driver = webdriver.Chrome(chrome_option)
        try:
            driver.get(self.url)
            driver.find_element(By.XPATH, "//button[@class='bui-button js-accept-continue']").click()
            time.sleep(3)
            page = driver.page_source
        except Exception as e:
            logging.info("fail! {}".format(self.url))
            logging.info(e)
        finally:
            driver.quit()

        return page

    def get_html_chrome(self):
        html = etree.HTML(self.get_page_chrome())
        return html


if __name__ == "__main__":
    page_download = PageDownload("https://www.booking.cn/hotel/cn/atour-x-ningbo-railway-station-liuting-street.zh-cn.html?sid=e02808502ac39012238a253d04e30657&aid=1662037&ucfs=1&arphpl=1&dest_id=-1920233&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=19&hapos=19&sr_order=popularity&srpvid=91284e1eaaf30006&srepoch=1687950398&from=searchresults#hotelTmpl")
    # page_download.get_page()
    page_download.get_html_chrome()
