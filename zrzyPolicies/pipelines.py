# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# class ZrzypoliciesPipeline:
#     def process_item(self, item, spider):
#         return item

import json
import csv
import scrapy
from zrzyPolicies.items import GdPoliciesItem
from scrapy.pipelines.files import FilesPipeline,BytesIO,md5sum  #这些都要导入
from urllib import parse
import re
from urllib.parse import urlparse
from os.path import basename,dirname,join

# 文件下载类
class MyFilesPipeline(FilesPipeline):  #在FilesPipeline的基础上创建了自己的pipeline
    # def file_path(self, request, response=None, info=None):
    #     path = urlparse(request.url).path
    #     return join(basename(dirname(path)), basename(path))


    def get_media_requests(self, item, info):
        # item = GdPoliciesItem()
        if len(item['file_urls'])>2:
            urls = item['file_urls'].split(';')
            names = item['files'].split(';')
            if(len(str(item['index']).split("/")))>1:
                path = str(item['index']).split("/")[1]
            elif (len(str(item['index']).split("/"))) >0:
                path = str(item['index'])
            for i in range(len(urls)):
                file_url = urls[i]
                file_name = path+'_'+names[i]
            # for file_url, file_name in zip(item['file_urls'], item['files']):
                yield scrapy.Request(file_url, meta={'file_name': file_name})

    def file_path(self, request, response=None, info=None):
        file_name = request.meta['file_name']
        # return 'gd/%s' % (file_name)
        # return 'gz/%s' % (file_name)
        # return 'zrzy/%s' % (file_name)

    # def file_downloaded(self, response, request, info):  #函数名称和原FilesPipeline中的一样
    #     pattern = re.compile(r'filename=(.*)')    #文件名就是filename后面的字符串
    #
    #     #利用Content-Disposition获取文件类型，
    #     containFileName = response.headers.get('Content-Disposition').decode('utf-8')
    #     if not containFileName:
    #         containFileName = response.headers.get('content-disposition').decode('utf-8')
    #
    #     #根据pattern在containFileName中找对应的字符串
    #     file_name1 = pattern.search(containFileName).group(1)
    #
    #     #解码，例如文件名里边带有的%20，通过解码可以转换成空格，如果没有这步，生成的文件名称则带有%20，这行可以删掉自己试试
    #     file_name2 = parse.unquote(file_name1)
    #     path = 'full/%s' % (file_name2)  #新的path在full文件夹中
    #
    #     buf = BytesIO(response.body)  #以下这些照写
    #     checksum = md5sum(buf)
    #     buf.seek(0)
    #     self.store.persist_file(path, buf, info)
    #     return checksum
    #
    #
    # def file_path(self, request, response=None, info=None):
    #     path = urlparse(request.url).path
    #     return join(basename(dirname(path)), basename(path))


class ZrzypoliciesPipeline:

    def open_spider(self, spider):
        if spider.name == "zrzybZc":
            self.file = open(spider.name + '.csv', 'a+', encoding='utf_8_sig')
        elif spider.name == "gdZhengce":
            self.file = open(spider.name + '.csv', 'a+', encoding='utf_8_sig')
        elif spider.name == "gzZhengce":
            self.file = open(spider.name + '.csv', 'a+', encoding='utf_8_sig')


    def close_spider(self, spider):
        self.file.close()
    #
    # def process_item(self, item, spider):
    #     # content = dict(item)
    #     # content = json.dumps(content, ensure_ascii=False)
    #     # self.file.write(content + "\n")
    #     writer = csv.writer(self.file)
    #     fieldnames = ['classification','title', 'index', 'topic','id' ,'organization' ,'createDate','tiCai','impDate','abolitionDate''detailInfo']
    #     # writer = csv.DictWriter(self.file, fieldnames=fieldnames)
    #     writer.writerow(fieldnames)
    #     # writer.writerow(item)
    #     writer.writerow([item['classification'],item['title'], item['index'], item['topic'],item['id'] ,item['organization'] ,item['createDate'] ,
    #                      item['tiCai'],item['impDate'], item['abolitionDate'],item['detailInfo'],item['url']])
    #     return item

    def process_item(self, item, spider):
        content = dict(item)
        content = json.dumps(content, ensure_ascii=False)
        self.file.write(content + "\n")
        return item

