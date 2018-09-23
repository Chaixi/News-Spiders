# -*- coding: utf-8 -*-
import scrapy
from newsSpider.items import jwcNewsspiderItem
from newsSpider.spiders import myMysql
import time

class JwcXmuSpider(scrapy.Spider):
    name = 'jwc_xmu_news'
    allowed_domains = ['jwc.xmu.edu.cn']
    start_urls = ['http://jwc.xmu.edu.cn/2194/list.htm']
    latest_release_time = myMysql.myMysql().getLatestTime(tableName="web_jwc_news")

    def parse(self, response):
        for each in response.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/table/tr"):
            detail_url = "http://jwc.xmu.edu.cn" + each.xpath("./td[2]/table/tr/td[1]/a/@href").extract()[0]
            print("详情地址："+detail_url)
            yield scrapy.Request(url=detail_url, callback=self.news_detail)

        # url跟进
        # 下一页的url
        url = response.xpath('//a[@class="next"]/@href').extract()
        if url:
            next_page = "http://jwc.xmu.edu.cn" + url[0]
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=False)
        # url跟进结束

    def news_detail(self, response):
        news_content = ''
        news_imgs = ''
        for p in response.xpath("/html/body/div[3]/div[2]/div/div/div/div/p"):
            content = p.xpath(".//text()").extract()
            img = p.xpath("./img/@src").extract()
            if content:
                news_content += content[0] + "\r\n"
            if img:
                news_imgs += "http://jwc.xmu.edu.cn" + img[0] + ";"

        item = jwcNewsspiderItem()
        item["news_title"] = response.xpath("/html/body/div[3]/div[1]/h1/span/span/span/text()").extract()[0]
        item["news_content"] = news_content
        item["news_source"] = '厦门大学教务处'
        item["news_link"] = response.url
        item["news_release_time"] = response.xpath("/html/body/div[3]/div[1]/h2/span/span/span/text()").extract()[0]
        item["news_read_status"] = '1'
        item["news_get_time"] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item["news_imgs"] = news_imgs

        release_time = item["news_release_time"]
        print("the latest_release_time from web_jwc_news is {0}".format(self.latest_release_time))

        str1 = time.mktime(time.strptime(release_time, "%Y-%m-%d"))
        str2 = time.mktime(time.strptime(self.latest_release_time, "%Y-%m-%d"))
        result = int(str1) - int(str2)
        print("发布时间：{0} 是否继续：{1}".format(release_time, result))
        if result < 0:
            self.crawler.engine.close_spider(self, "教务处消息爬取完成！")
        elif myMysql.myMysql().columnExist(tableName="web_jwc_news", columnValue=item['news_link']):
            return
        else:
            yield item