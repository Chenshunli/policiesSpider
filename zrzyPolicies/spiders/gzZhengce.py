import scrapy
import copy
import time
import re
from selenium import webdriver
from time import sleep

from zrzyPolicies.items import GzPoliciesItem
from dataFilter import Cleaning_data

# punctuation_str = punctuation
# print("中文标点符合：", punctuation_str)

class GzZhengceSpider(scrapy.Spider):
    name = 'gzZhengce'
    allowed_domains = ['ghzyj.gz.gov.cn']
    start_urls = ['http://ghzyj.gz.gov.cn/zwgk/zcfg/']

    def __init__(self, keyword = "", repeat=0):
        super(GzZhengceSpider, self).__init__()
        self.conflict_count = 0
        self.keyword = keyword
        self.repeat = int(repeat)
        self.page = 1
        self.count = 0
        self.t1 = time.time()

    def parse(self, response):
        startUrls = ["http://ghzyj.gz.gov.cn/zwgk/zcfg/"]
        driver = webdriver.Chrome(executable_path="D:\\chromedriver_win32\\chromedriver.exe")
        item = GzPoliciesItem()
        for startUrl in startUrls:
            driver.get(startUrl)
            print('Before search================')

            # 打印当前页面title
            title = driver.title
            print(title)

            # 打印当前页面URL
            now_url = driver.current_url
            print(now_url)
            # 获取当前分类总页数
            sleep(1)
            pageNation = driver.find_elements_by_xpath("//div[@class='pagediv']")
            pages = pageNation[0].text
            # pages = driver.find_element_by_class_name('pagination').text
            # pList = driver.find_elements_by_xpath("//div[@class='pagination']//a")
            # pList1 = str(pages).split("\n")
            urls = []
            titleList = []
            fabuDateList = []
            chengwenDateList = []
            pList = driver.find_elements_by_xpath("//div[@class='pagediv']//span")
            # while nowPage < lastP:
            flag = True
            while flag:
                sleep(3)
                content = driver.find_element_by_class_name("news_list").text
                url = driver.find_element_by_class_name("news_list").text
                contentList = str(content).split("\n")
                floderurls = driver.find_elements_by_xpath("//div[@ class = 'mainContent']/ul/li//a")
                sleep(5)
                try:
                    for floderurl in floderurls:
                        result = floderurl.get_attribute("href")
                        urls.append(result)
                        # FLODERURLSLIST.append(result)
                        # print(result)

                    for i in range(len(contentList)):
                        cont = contentList[i]
                        if i % 2 == 0:
                            titleList.append(cont)
                        else:
                            date1 = cont.split(" ")[0]
                            # date2 = cont.split(" ")[1]
                            fabuDateList.append(date1)
                            # chengwenDateList.append(date2)
                    try:
                        # elem1=driver.find_element_by_link_text("下一页")
                        next = driver.find_elements_by_xpath("//div[@class='pagediv']//a[@class='next']")
                        # nextDisable = driver.find_elements_by_xpath("//div[@class='pagination']//a[@class='next disabled']")
                        if len(next) > 0:
                            new = next[0].click()
                        else:
                            flag = False
                    except Exception as e:
                        flag = False
                        continue
                        # print(driver.page_source[0])
                except Exception as e:
                    print(e)

        print('After search================')
        print("即将爬取"+str(len(urls))+"条数据...")
        # 关闭所有窗口
        # driver.quit()
        for i in range(len(urls)):
            url0 = urls[i]
            start = str(url0).find("_") + 1
            index = str(url0)[start:-5]
            item['url'] = url0
            item['index'] = index
            # item['title'] = titleList[i]
            # item['createDate'] = fabuDateList[i]
            # item['impDate'] = chengwenDateList[i]
            # yield item

            yield scrapy.http.Request(url=url0, meta={'item': copy.deepcopy(item)}, callback=self.parse_detail,
                                      errback=self.errback)

    def errback(self, failure):
        self.logger.error(repr(failure))


    def parse_detail(self, response):
            item = response.meta['item']
            # print("item:"+item)
            # contentList = response.xpath("//div[contains( @class ,'listfr')]/table/tr")
            contentInfo = response.xpath("//div[@class='content']/div[@class='content_article']").extract()
            # 来源、日期等信息
            tipsInfo = response.xpath("//div[@class='content']/div[contains(@class,'content_attr')]/span")
            if (len(tipsInfo) > 0):
                for tip in tipsInfo:
                    # text = tip.xpath("//text()").extract_first()
                    textSel = tip.xpath("string(.)")
                    text = tip.xpath("string(.)").extract()[0]
                    if("来源" in text):
                        # source = tip.xpath("//b/text()").extract_first()
                        source = text.split("：")[1]
                        item['source'] = source
                    if("发布时间" in text):
                        # date = tip.xpath("//b/text()").extract_first()
                        date = text.split("：")[1]
                        item['createDate'] = date

            if(len(contentInfo)>0):
                content = Cleaning_data(contentInfo[0])
                # 解决因英文逗号导致写入行时内容被写到两个单元格问题
                content = content.replace(',', '，')
                # item['detailInfo'] = content
                if isinstance(content,str):
                    item['detailInfo'] = content
                elif isinstance(content,list):
                    item['detailInfo'] = " ".join(content)
                else:
                    item['detailInfo'] = ""
                if "附件" in content:
                    contList = response.xpath("//div[@class ='article-content']/p[contains(@style,'margin-bottom')]")
                    # 可能有多个附件
                    file_list = []
                    nameList =[]
                    for fujianUrl in contList:
                        # fujianUrl = contList[-1]
                        # f_list = fujianUrl.xpath("//a/@href").extract()
                        f_list = fujianUrl.css("a::attr(href)").get()
                        if isinstance(f_list,str):
                            file_list.append("http:" + f_list)
                            # fName = fujianUrl.xpath(".//a/text()").extract()
                            fName = fujianUrl.xpath("string(.//a)").extract()[0]
                            # f = fujianUrl.xpath("./a/text()")
                            # name = fName[0].replace("：", "")
                            nameList.append(fName)
                    # item['file_urls'] = file_list
                    # item['files'] = nameList
                    item['file_urls'] = ';'.join(file_list)
                    item['files'] = ';'.join(nameList)
                else:
                    item['file_urls'] = ""
                    item['files'] = ""
            yield item

