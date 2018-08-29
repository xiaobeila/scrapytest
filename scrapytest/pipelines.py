# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql


class ScrapytestPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect("127.0.0.1", "root", "", "python", charset="utf8")
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'INSERT INTO imooc_course (title) VALUES ("{}")'.format(item['title'])
        self.cur.execute(sql)
        # 提交，不然无法保存新建或者修改的数据
        self.conn.commit()

        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cur.close()
        # 关闭连接
        self.conn.close()
