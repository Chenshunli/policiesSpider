import scrapy
import copy
import time
import re
from dataFilter import Cleaning_data
from zrzyPolicies.items import ZrzypoliciesItem
from selenium import webdriver
from time import sleep

# punctuation_str = punctuation
# print("中文标点符合：", punctuation_str)

class zrzybZcSpider(scrapy.Spider):
    name = 'zrzybZc'
    allowed_domains = ['gi.mnr.gov.cn']
    start_urls = ['http://gi.mnr.gov.cn/']

    def __init__(self, keyword = "", repeat=0):
        super(zrzybZcSpider, self).__init__()
        self.conflict_count = 0
        self.keyword = keyword
        self.repeat = int(repeat)
        self.page = 1
        self.count = 0
        self.t1 = time.time()

    def parse(self, response):
        # dirList = response.xpath("/html/body/div[4]/div/div[3]/div[1]/div/span/a")
        dirList = response.xpath("//div[contains( @class ,'listd')]/span")
        # dirList = response.xpath("//div[contains( @class ,'listd')]/span[contains( @class ,'theme_parent')]")
        # contList = response.xpath("//div[contains( @ class, 'listd')]/ul")
        driver = webdriver.Chrome(executable_path="D:\\chromedriver_win32\\chromedriver.exe")
        item = ZrzypoliciesItem()
        dirs = []
        durls = []
        for j in range(len(dirList)):
            dir = dirList[j]
            # 获取一级目录名称及地址
            if dir.xpath(".//a/text()").extract_first() is not None:
                dirName =  dir.xpath(".//a/text()").extract_first().replace('（','')
                dirUrl = dir.css("a::attr(href)").get()
                dirUrl = dirUrl.replace('./gkml2018','http://gi.mnr.gov.cn')
                dirs.append(dirName)
                durls.append(dirUrl)
        if(len(dirs)==len(durls)):
            urls = []
            titleList = []
            fabuDateList = []
            chengwenDateList = []
            # 循环获取每个一级目录下对应的内容
            for k in range(3,24):
                startUrl =  durls[k]
                print(startUrl)
                driver.get(startUrl)
                # driver.get(startUrl)

                print('Before search================')
                # 打印当前页面title
                title = driver.title
                print(title)

                # 打印当前页面URL
                now_url = driver.current_url
                print(now_url)
                # 获取当前分类总页数
                sleep(1)
                # pageNation = driver.find_elements_by_xpath("//div[@class='page-bottom']")
                flag = True
                # if len(urls)>10:
                #     break
                while flag:
                    sleep(3)
                    # floderurls = driver.find_elements_by_xpath("//div[contains( @class ,'listfr')]/table/tr/td[@class='oo']//a")
                    # content = driver.find_element_by_class_name("table-content").text
                    # contentList = driver.find_elements_by_xpath("//div[contains( @class ,'listfr')]/table/tr/td[@class='oo']")
                    contentList = driver.find_elements_by_xpath("//td[@class='oo']")
                    floderurls = driver.find_elements_by_xpath("//td[@class='oo']/a")
                    # faWenHaoList = response.xpath("//div[contains( @class ,'listfr')]/table/tr/td[3]")
                    sleep(3)
                    for i in range(len(contentList)):
                        content = contentList[i]
                        url = floderurls[i].get_attribute("href")
                        urls.append(url)
                        title = content.text
                        titleList.append(title)
                        # 不再获取发文号
                        # faWenHao = faWenHaoList[i]
                        # fawen = faWenHao.xpath(".//text()").extract_first()
                        # for info in contentList:
                    try:
                        next = driver.find_element_by_link_text("下一页")
                        if next:
                            new = next.click()
                        else:
                            flag = False
                    except Exception as e:
                        flag = False
                        print(driver.page_source[0])

            print('After search================')
            print("即将爬取" + str(len(urls)) + "条数据...")
            # 关闭所有窗口
            # driver.quit()
            for i in range(len(urls)):
                url0 = urls[i]
                item['url'] = url0
                yield scrapy.http.Request(url=url0, meta={'item': copy.deepcopy(item)},
                                          callback=self.parse_detail, errback=self.errback)



    def errback(self, failure):
        self.logger.error(repr(failure))

    def parseInfo(self, response):
        item = response.meta['item']
        # print("item:"+item)
        # contentList = response.xpath("//div[contains( @class ,'listfr')]/table/tr")
        contentList = response.xpath("//div[contains( @class ,'listfr')]/table/tr/td[contains( @class ,'oo')]")
        faWenHaoList = response.xpath("//div[contains( @class ,'listfr')]/table/tr/td[3]")
        a = response.xpath("//div[contains( @class ,'listfr')]/table/tr/td[3]/text()").extract_first()
        for i in range(len(contentList)):
        # for faWenHao in faWenHaoList:
            faWenHao = faWenHaoList[i]
            fawen = faWenHao.xpath(".//text()").extract_first()
            b = faWenHao.xpath("/text()").extract_first()
            c = faWenHao.xpath("text()").extract_first()
            # 如果发文号为空，无需爬取
            if fawen is None:
                continue
            else:
        # for info in contentList:
                info = contentList[i]
                title = info.xpath(".//a/text()").extract_first()
                detailUrl = info.css("a::attr(href)").get()
                detailUrl = detailUrl.replace('../../../../','http://gi.mnr.gov.cn/')
                item['title'] = title
                item['url'] = detailUrl
                yield scrapy.http.Request(url=detailUrl, meta={'item': copy.deepcopy(item)}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        # infos = response.css("div.xiaoquInfoItem")[:-1]
        # infos = response.xpath("//div[contains( @class ,'box')]/table/tr/td[2]")
        infos = response.xpath("//div[contains( @class ,'box')]/table/tr/td")
        ds = response.xpath("//div[contains( @class ,'xx')]/text").extract()
        details = response.xpath("//div[contains( @class ,'xx')]").extract()
        infoList = []
        for info in infos:
            textInfo = info.xpath(".//text()").extract()
            if textInfo:
                text0 = info.xpath(".//text()").extract()
                text1 = "".join(text0)
                infoList.append(text1)
            else:infoList.append("")
        # tiCai = infoList[13][0]
        # 体裁为“决定、公告、通报、公示、批复“
        # if '决定' not in tiCai and '公告' not in tiCai and '通报' not in tiCai and '公示' not in tiCai and '批复' not in tiCai:
        if(len(infoList)>8):
            # if len(item['title']) < 1 and len(infoList[1]) > 0:
            if len(infoList[1]) > 0:
                if isinstance(infoList[1],list):
                    item['title'] = infoList[1][0]
                elif isinstance(infoList[1],str):
                    item['title'] = infoList[1]
            if isinstance((infoList[3]),list):
                item['index'] = infoList[3][0]
            elif isinstance((infoList[3]),str):
                item['index'] = infoList[3]
            if isinstance((infoList[5]), list):
                item['topic'] = infoList[5][0]
            elif isinstance((infoList[5]), str):
                item['topic'] = infoList[5]
            if isinstance((infoList[7]), list):
                item['id'] = infoList[7][0]
            elif isinstance((infoList[7]), str):
                item['id'] = infoList[7]
            if isinstance((infoList[9]), list):
                item['organization'] = infoList[9][0]
            elif isinstance(infoList[9],str):
                item['organization'] = infoList[9]
            if isinstance((infoList[11]), list):
                item['createDate'] = infoList[11][0]
            elif isinstance(infoList[11],str):
                item['createDate'] = infoList[11]
            if isinstance((infoList[13]), str):
                item['tiCai'] = infoList[13]
            if isinstance((infoList[15]), list):
                item['impDate'] = infoList[15][0]
            elif isinstance(infoList[15],str):
                item['impDate'] = infoList[15]
            if isinstance((infoList[17]), list):
                item['abolitionDate'] = infoList[17][0]
            elif isinstance(infoList[17],str):
                item['abolitionDate'] = infoList[17]
            if(len(details)>0):
                detailInfo = Cleaning_data(details[0])
                # newInfo = self.clean_sentence(detailInfo)
            # ii = detailInfo.css("span::text").get()
            # ii2 = detailInfo.xpath("/text").get()
                content = detailInfo.replace(',', '，')
                if isinstance(content, str):
                    item['detailInfo'] = content
                elif isinstance(content, list):
                    item['detailInfo'] = " ".join(content)
                else:
                    item['detailInfo'] = ""
                # 如果存在附件，进行附件下载
                if "附件" in content:
                    driver2 = webdriver.Chrome(executable_path="D:\\chromedriver_win32\\chromedriver.exe")
                    # u = response.url
                    driver2.get(response.url)
                    contList = driver2.find_elements_by_xpath("//div[@class='xx']/ul/li")
                    urls = driver2.find_elements_by_xpath("//div[@class='xx']/ul/li/a")
                    # contList = response.xpath("//div[@class='xx']/ul[@id = 'xxgk_fj']")
                    # 可能有多个附件
                    file_list = []
                    nameList = []
                    for fujianUrl in urls:
                        # fujianUrl = contList[-1]
                        u = fujianUrl.get_attribute("href")
                        t = fujianUrl.text
                        # f_list = fujianUrl.css("a::attr(href)").get()
                        if isinstance(u, str):
                            file_list.append(u)
                            # fName = fujianUrl.xpath(".//a/text()").extract()
                            fName = t
                            nameList.append(fName)

                    item['file_urls'] = ';'.join(file_list)
                    item['files'] = ';'.join(nameList)
                else:
                    item['file_urls'] = ""
                    item['files'] = ""
            yield item
