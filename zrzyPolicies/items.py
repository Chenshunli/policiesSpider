# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZrzypoliciesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classification = scrapy.Field() #分类
    topic = scrapy.Field()  #主题
    title = scrapy.Field()  #标题
    index = scrapy.Field()  #索引号
    id = scrapy.Field()   #发文字号
    organization = scrapy.Field()  #发布机构
    tiCai = scrapy.Field()   #体裁
    # date = scrapy.Field()
    createDate = scrapy.Field() ##生成日期
    impDate = scrapy.Field()  #实施日期
    abolitionDate = scrapy.Field()  #废止日期
    url = scrapy.Field()   #链接
    detailInfo = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    pass

class GdPoliciesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classification = scrapy.Field() #分类
    topic = scrapy.Field()  #主题
    title = scrapy.Field()  #标题
    index = scrapy.Field()  #索引号
    id = scrapy.Field()   #发文字号
    organization = scrapy.Field()  #发布机构
    # tiCai = scrapy.Field()   #体裁
    # date = scrapy.Field()
    createDate = scrapy.Field() ##生成日期
    # impDate = scrapy.Field()  #实施日期
    fabuDate = scrapy.Field()  #发布日期
    url = scrapy.Field()   #链接
    detailInfo = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    pass

class GzPoliciesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # classification = scrapy.Field() #分类
    # topic = scrapy.Field()  #主题
    title = scrapy.Field()  #标题
    index = scrapy.Field()  #索引号
    # id = scrapy.Field()   #发文字号
    source = scrapy.Field()  #来源
    # tiCai = scrapy.Field()   #体裁
    # date = scrapy.Field()
    createDate = scrapy.Field() ##发布日期
    # impDate = scrapy.Field()  #实施日期
    # abolitionDate = scrapy.Field()  #废止日期
    url = scrapy.Field()   #链接
    detailInfo = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    pass