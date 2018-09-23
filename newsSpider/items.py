# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 新闻中心
class NewsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 消息id
    news_id = scrapy.Field()

    # 消息标题
    news_title = scrapy.Field()

    # 消息内容
    news_content = scrapy.Field()

    # 消息源
    news_source = scrapy.Field()

    # 消息原始链接
    news_link = scrapy.Field()

    # 消息发布时间
    news_release_time = scrapy.Field()

    # 消息阅读状态，1未阅读，2已阅读
    news_read_status = scrapy.Field()

    # 消息获取时间
    news_get_time = scrapy.Field()

    # 消息包含图片 多张图片地址用';'隔开
    news_imgs = scrapy.Field()

# 教务处
class jwcNewsspiderItem(scrapy.Item):
    # 消息id
    news_id = scrapy.Field()

    # 消息标题
    news_title = scrapy.Field()

    # 消息内容
    news_content = scrapy.Field()

    # 消息源
    news_source = scrapy.Field()

    # 消息原始链接
    news_link = scrapy.Field()

    # 消息发布时间
    news_release_time = scrapy.Field()

    # 消息阅读状态，1未阅读，2已阅读
    news_read_status = scrapy.Field()

    # 消息获取时间
    news_get_time = scrapy.Field()

    # 消息包含图片 多张图片地址用';'隔开
    news_imgs = scrapy.Field()

# 学生处消息
class xscNewsspiderItem(scrapy.Item):
    # 消息id
    news_id = scrapy.Field()

    # 消息标题
    news_title = scrapy.Field()

    # 消息内容
    news_content = scrapy.Field()

    # 消息源
    news_source = scrapy.Field()

    # 消息原始链接
    news_link = scrapy.Field()

    # 消息发布时间
    news_release_time = scrapy.Field()

    # 消息阅读状态，1未阅读，2已阅读
    news_read_status = scrapy.Field()

    # 消息获取时间
    news_get_time = scrapy.Field()

    # 消息包含图片 多张图片地址用';'隔开
    news_imgs = scrapy.Field()
