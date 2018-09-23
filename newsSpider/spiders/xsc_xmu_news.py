# -*- coding: utf-8 -*-
import scrapy
from newsSpider.items import xscNewsspiderItem
from newsSpider.spiders import myMysql
import time

class XscNewsSpider(scrapy.Spider):
    name = 'xsc_xmu_news'
    allowed_domains = ['xsc.xmu.edu.cn']
    start_urls = ['http://xsc.xmu.edu.cn/3084/list.htm']
    latest_release_time = myMysql.myMysql().getLatestTime(tableName="web_xsc_news")

    def parse(self, response):
        for each in response.xpath('//div[@id="wp_news_w4"]/table/tr'):
            # item = xscNewsspiderItem()
            # title = each.xpath('./td[2]/table/tr/td[1]/a/@title').extract()[0]
            # release_time = each.xpath('./td[2]/table/tr/td[2]//text()').extract()[0]
            detail_url = "http://xsc.xmu.edu.cn" + each.xpath('.//td[2]/table/tr/td[1]/a/@href').extract()[0]
            print("详情地址：{0}".format(detail_url))
            # print("title: {0} \n release_time: {1} \n link: {2}".format(title, release_time, link))
            # item['news_title'] = title
            # item['news_content'] = '暂无内容'
            # item['news_source'] = '厦门大学学生处'
            # item['news_link'] = link
            # item['news_release_time'] = release_time
            # item['news_read_status'] = '1'
            # item['news_get_time'] = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            # item['news_imgs'] = ''

            yield scrapy.Request(url=detail_url, callback=self.news_detail, dont_filter=False)

            # str1 = time.mktime(time.strptime(release_time, "%Y-%m-%d"))
            # str2 = time.mktime(time.strptime("2017-01-01", "%Y-%m-%d"))
            # result = int(str1)-int(str2)
            # if result<0:
            #     self.crawler.engine.close_spider(self, "学生处消息爬取完成！")

        url = response.xpath('//a[@class="next"]/@href').extract()
        if url:
            next_page = "http://xsc.xmu.edu.cn" + url[0]
            print("next page: {0}".format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=False)

    def news_detail(self, response):
        news_content = ''
        news_imgs = ''
        for p in response.xpath('//div[@class="Article_Content"]/p'):
            content = p.xpath(".//text()").extract()
            img = p.xpath("./img/@src").extract()
            if content:
                news_content += content[0] + "\r\n"
            if img:
                news_imgs += "http://xsc.xmu.edu.cn" + img[0] + ";"

        item = xscNewsspiderItem()
        item["news_title"] = response.xpath('//span[@class="Article_Title"]/text()').extract()[0]
        item["news_content"] = news_content
        item["news_source"] = '厦门大学学生处'
        item["news_link"] = response.url
        item["news_release_time"] = response.xpath('//span[@class="Article_PublishDate"]/text()').extract()[0]
        item["news_read_status"] = '1'
        item["news_get_time"] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item["news_imgs"] = news_imgs

        release_time = item["news_release_time"]
        print("the latest_release_time from web_xsc_news is {0}".format(self.latest_release_time))

        str1 = time.mktime(time.strptime(release_time, "%Y-%m-%d"))
        # str2 = time.mktime(time.strptime("2017-01-01", "%Y-%m-%d"))
        str2 = time.mktime(time.strptime(self.latest_release_time, "%Y-%m-%d"))

        result = int(str1) - int(str2)
        print("发布时间：{0} 是否继续：{1}".format(release_time, result))
        if result < 0:
            self.crawler.engine.close_spider(self, "学生处消息爬取完成！")
        elif myMysql.myMysql().columnExist(tableName="web_xsc_news", columnValue=item['news_link']):
            return
        else:
            yield item