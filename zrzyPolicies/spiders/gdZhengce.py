import scrapy
import copy
import time
from selenium import webdriver
from time import sleep
from zrzyPolicies.items import GdPoliciesItem
from dataFilter import Cleaning_data

class GdZhengceSpider(scrapy.Spider):
    name = 'gdZhengce'
    allowed_domains = ['nr.gd.gov.cn']
    start_urls = ['http://nr.gd.gov.cn/gkmlpt/index#3100']
    # start_urls = ['http://nr.gd.gov.cn/gkmlpt/index']
    def __init__(self, keyword = "", repeat=0):
        super(GdZhengceSpider, self).__init__()
        self.conflict_count = 0
        self.keyword = keyword
        self.repeat = int(repeat)
        # self.split_p_label = re.compile(SPLITPLABEL)
        # self.split_span_label = re.compile(SPLITSPANLABEL)
        # self.remove_html_label = re.compile(REMOVEHTMLLABEL)
        self.page = 1
        self.count = 0
        self.t1 = time.time()

    def parse(self, response):
        item = GdPoliciesItem()
        dirList = response.xpath("//ul[contains( @class ,'hasChild catalogue')]/li/ul/li")
        startUrls = ["http://nr.gd.gov.cn/gkmlpt/index#3101"]
        # startUrls = ["http://nr.gd.gov.cn/gkmlpt/index#3100"]
        driver = webdriver.Chrome(executable_path="D:\\chromedriver_win32\\chromedriver.exe")
        urls = []
        titleList = []
        fabuDateList = []
        chengwenDateList = []
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
            pageNation =  driver.find_elements_by_xpath("//div[@class='pagination']")
            pages =  pageNation[0].text
            # urls = []
            # titleList = []
            # fabuDateList = []
            # chengwenDateList = []

            pList = driver.find_elements_by_xpath("//div[@class='pagination']//a")
            # while nowPage < lastP:
            flag = True
            while flag:
                sleep(3)
                content = driver.find_element_by_class_name("table-content").text
                url = driver.find_element_by_class_name("table-content").text
                contentList = str(content).split("\n")
                floderurls = driver.find_elements_by_xpath("//td[@class = 'first-td']//a")
                sleep(5)
                try:
                    for floderurl in floderurls:
                        result = floderurl.get_attribute("href")
                        titleInfo = floderurl.text
                        urls.append(result)
                        # titleList
                        # yield scrapy.http.Request(url=result, meta={'item': copy.deepcopy(item)},
                        #                           callback=self.parse_detail, errback=self.errback)

                    for i in range(len(contentList)):
                        cont = contentList[i]
                        if i % 2 == 0:
                            titleList.append(cont)
                        else:
                            date1 = cont.split(" ")[0]
                            date2 = cont.split(" ")[1]
                            fabuDateList.append(date1)
                            chengwenDateList.append(date2)
                    try:
                        # elem1=driver.find_element_by_link_text("下一页")
                        next = driver.find_elements_by_xpath("//div[@class='pagination']//a[@class='next']")
                        nextDisable = driver.find_elements_by_xpath("//div[@class='pagination']//a[@class='next disabled']")
                        if len(next)>0:
                            new = next[0].click()
                        else:
                            flag = False
                    except Exception as e:
                        print(driver.page_source[0])
                except Exception as e:
                    print(e)


        print('After search================')
        print("即将爬取" + str(len(urls)) + "条数据...")
        # 关闭所有窗口
        # driver.quit()
        for i in range(len(urls)):
            url0 = urls[i]
            item['url'] = url0
            yield scrapy.http.Request(url = url0, meta={'item': copy.deepcopy(item)}, callback=self.parse_detail,errback=self.errback)


    def errback(self, failure):
        self.logger.error(repr(failure))

    def parse_detail(self, response):
        item = response.meta['item']
        contentList = response.xpath("//div[contains( @class ,'classify')]/table/tr/td")
        details = response.xpath("//div[contains( @class ,'classify')]/table/tr/td/text()").extract()
        # detailList = response.xpath("//div[contains( @class ,'classify')]/table/tr/td/text()").extract_fist()
        infoList = []
        # contentInfo = response.xpath("//div[contains( @class, 'content')]").extract()
        # contentInfo = response.xpath("//div[contains( @wzades, '信息公开内容正文详情')]").extract()
        contentInfo = response.xpath("//div[@class ='content']").extract()
        for i in range(len(contentList)):
            info = contentList[i]
            if(i%2)==0:
                strList = info.xpath(".//text()").extract()
                if(len(strList)>0):
                    detailss = strList[0]
                    a = info.xpath("/text()").extract()
                else:detailss = ""
            else:
                strList = info.xpath(".//span/text()").extract()
                if(len(strList)>0):
                    detailss = strList[0]
                else:detailss = ""
            if isinstance(detailss,str):
                detail = detailss.replace("\n","").replace("：","").strip()
                if detail:
                    infoList.append(detail)
                else:infoList.append("")
        # for i in range(len(infoList)):
        # text = infoList[i]
        if(len(infoList)>15):
            if isinstance((infoList[1]),str):
                item['index'] = infoList[1]
            if  isinstance((infoList[3]),str):
                item['classification'] = infoList[3]
            if isinstance((infoList[5]), str):
                item['organization'] = infoList[5]
            if isinstance((infoList[7]), str):
                item['createDate'] = infoList[7]
            if isinstance((infoList[9]), str):
                item['title'] = infoList[9]
            if isinstance((infoList[11]), str):
                item['id'] = infoList[11]
            if isinstance((infoList[13]), str):
                item['fabuDate'] = infoList[13]
            if isinstance((infoList[15]), str):
                item['topic'] = infoList[15]
            # if isinstance((infoList[17]), list):
            #     item['abolitionDate'] = infoList[17][0]
            if(len(contentInfo)>0):
                content = Cleaning_data(contentInfo[0])
                content = content.replace(',','，')
                if isinstance(content,str):
                    item['detailInfo'] = content
                elif isinstance(content,list):
                    item['detailInfo'] = " ".join(content)
                else:
                    item['detailInfo'] = ""
                # 如果存在附件，进行附件下载
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
                            # nameList.append(name)
                            nameList.append(fName)

                    item['file_urls'] = ';'.join(file_list)
                    item['files'] = ';'.join(nameList)
                else:
                    item['file_urls'] = ""
                    item['files'] = ""
                            # item["files"] = file
        yield item

