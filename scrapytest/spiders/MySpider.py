# -*- coding:utf8-*-
import scrapy
import sys
import time
from ..items import ScrapytestItem
from scrapy.selector import Selector

sys.stdout = open('output.txt', 'w')
pageIndex = 0


class MySpider(scrapy.Spider):
    # 用于区别Spider
    name = "MySpider"
    # 允许访问的域
    allowed_domains = ['imooc.com']
    # 爬取的地址
    start_urls = ["http://www.imooc.com/course/list"]

    # 爬取方法
    def parse(self, response):

        # 实例一个容器保存爬取的信息
        item = ScrapytestItem()
        # 这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        # 先获取每个课程的div
        sel = Selector(response)
        title = sel.xpath('/html/head/title/text()').extract()  # 标题
        print(title[0])
        sels = sel.xpath('//div[@class="course-card-container"]')
        index = 0
        global pageIndex
        pageIndex += 1
        print(u'%s' % (time.strftime('%Y-%m-%d %H-%M-%S')))
        print('第' + str(pageIndex) + '页 ')
        print('----------------------------------------------')

        for box in sels:
            print(' ')
            # 获取div中的课程标题
            item['title'] = box.xpath('.//h3[@class="course-card-name"]/text()').extract()[0].strip()
            item['url'] = 'http://www.imooc.com' + box.xpath('.//a[@class="course-card"]/@href').extract()[0].strip()
            item['image_url'] = 'http:' + box.xpath('.//img[@class="course-banner lazy"]/@src').extract()[0].strip()
            item['introduction'] = box.xpath('.//p[@class="course-card-desc"]/text()').extract()[0].strip()
            item['student'] = box.xpath('.//div[@class="course-card-info"]/span[2]/text()').extract()[0].strip()
            item['difficulty'] = box.xpath('.//div[@class="course-card-info"]/span[1]/text()').extract()[0].strip()
            item['category'] = box.xpath('.//div[@class="course-label"]/label/text()').extract()[0].strip()

            index += 1
            yield item

        time.sleep(1)
        print(u'%s' % (time.strftime('%Y-%m-%d %H-%M-%S')))
        next = u'下一页'
        url = response.xpath("//a[contains(text(),'" + next + "')]/@href").extract()
        if url:
            # 将信息组合成下一页的url
            page = 'http://www.imooc.com' + url[0]
            # 返回url
            yield scrapy.Request(page, callback=self.parse)
