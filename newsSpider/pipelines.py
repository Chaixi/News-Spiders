# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql.cursors
from newsSpider.items import NewsspiderItem
from newsSpider.items import jwcNewsspiderItem
from newsSpider.items import xscNewsspiderItem
import time

class NewsspiderPipeline(object):
    """
        功能：保存item数据
    """
    def __init__(self):
        # 若打开方式为"w"，则会出现错误TypeError: write() argument must be str, not bytes
        # self.filename_xmu_news = open("xmu_news.json", "wb+")
        # self.filename_jwc_news = open("jwc_news.json", "wb+")
        # self.filename_xsc_news = open("xsc_news.json", "wb+")

        # 创建数据库连接
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='mydemo', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        # 创建操作游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, NewsspiderItem):
            # text = "From xmu_news:" + json.dumps(dict(item), ensure_ascii=False) + ",\n"
            # self.filename_xmu_news.write(text.encode("utf-8"))
            #
            sql="INSERT INTO web_news(title, content, source, link, release_time, read_status, get_time, imgs) VALUE('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(item["news_title"], item["news_content"], item["news_source"], item["news_link"], item["news_release_time"], item["news_read_status"], item["news_get_time"], item["news_imgs"])

        elif isinstance(item, jwcNewsspiderItem):
            # text = "From jwc_news:" + json.dumps(dict(item), ensure_ascii=False) + ",\n"
            # self.filename_jwc_news.write(text.encode("utf-8"))
            #
            sql="INSERT INTO web_jwc_news(title, content, source, link, release_time, read_status, get_time, imgs) VALUE('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(item["news_title"], item["news_content"], item["news_source"], item["news_link"], item["news_release_time"], item["news_read_status"], item["news_get_time"], item["news_imgs"])

        elif isinstance(item, xscNewsspiderItem):
            # text = "From xsc_news:" + json.dumps(dict(item), ensure_ascii=False) + ",\n"
            # self.filename_xsc_news.write(text.encode("utf-8"))
            #
            sql="INSERT INTO web_xsc_news(title, content, source, link, release_time, read_status, get_time, imgs) VALUE('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(item["news_title"], item["news_content"], item["news_source"], item["news_link"], item["news_release_time"], item["news_read_status"], item["news_get_time"], item["news_imgs"])

        self.cursor.execute(sql)
        # 提交数据库操作
        self.conn.commit()

        return item

    def close_spider(self, spider):
        # self.filename_xmu_news.close()
        # self.filename_jwc_news.close()
        # self.filename_xsc_news.close()
        # 提交数据库操作
        self.conn.commit()
        # 关闭数据库连接
        self.cursor.close()
