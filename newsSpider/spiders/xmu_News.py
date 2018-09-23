# -*- coding: utf-8 -*-
import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.spiders import myMysql
import time

class GetnewsSpider(scrapy.Spider):

    # 爬虫名
    name = 'xmu_news'
    # 爬虫作用范围
    allowed_domains = ['news.xmu.edu.cn']
    start_urls = ['http://news.xmu.edu.cn/1552/list.htm']
    # 作用类似静态变量属性
    latest_release_time = myMysql.myMysql().getLatestTime(tableName="web_news")

    def parse(self, response):
        for each in response.xpath("/html/body/div/div[4]/div[3]/table/tr/td/div/div/div[1]/table/tr"):
            detail_url = 'http://news.xmu.edu.cn' + each.xpath("./td/table/tr/td[1]/a/@href").extract()[0]
            print("详情地址："+detail_url)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, dont_filter=False)

        # url跟进开始，翻页
        # 获取下一页的url信息
        url = response.xpath('//a[@class="next"]/@href').extract()
        if url:
        #     # 将信息组合成下一页的url
            next_page = 'http://news.xmu.edu.cn' + url[0]
            print("下一页地址：" + next_page)
        #     # 返回url
            yield scrapy.Request(url=next_page, callback = self.parse)
        # url跟进结束

    # 获取消息详情
    def parse_detail(self, response):
        news_content = ''
        news_img = ''
        for p in response.xpath('//*[@id="newscontent"]/div/div[1]/div/div/p'):
            content = p.xpath('.//text()').extract()
            img = p.xpath('./img/@src').extract()
            # 要先判断是否为空，不然可能会出现indexError
            if content:
                # print("正文："+temp[0])
                news_content += content[0] + "\r\n"
            if img:
                # print("图片："+img[0])
                news_img += "http://news.xmu.edu.cn" + img[0] + ";"

        item = NewsspiderItem()
        item["news_title"] = response.xpath('//*[@id="mainContainer"]/div[3]/table/tr/td/span/span/span/text()').extract()[0]
        item["news_content"] = news_content
        item["news_source"] = '厦门大学新闻网'
        item["news_link"] = response.url
        item["news_release_time"] = response.xpath('//*[@id="mainContainer"]/div[4]/table/tr[2]/td/span[1]/span/span/text()').extract()[0]
        item["news_read_status"] = '1'
        item["news_get_time"] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item["news_imgs"] = news_img

        release_time = item['news_release_time']
        print("the latest_release_time from web_xmu_news is {0}".format(self.latest_release_time))

        st1 = time.mktime(time.strptime(release_time, "%Y-%m-%d"))
        st2 = time.mktime(time.strptime(self.latest_release_time, "%Y-%m-%d"))
        result = int(st1) - int(st2)
        print("发布时间：{0} 是否继续：{1}".format(release_time, result))

        # 发布时间小于数据库最新时间则停止爬取，且数据若已存在则不保存到数据库
        if result <= 0:
            self.crawler.engine.close_spider(self, '厦门大学新闻网消息爬取完成!')
        elif myMysql.myMysql().columnExist(tableName="web_news", columnValue=item['news_link']):
            return
        else:
            yield item