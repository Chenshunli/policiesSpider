import scrapy
import copy
import time
import re
from dataFilter import Cleaning_data
from zrzyPolicies.items import ZrzypoliciesItem

# punctuation_str = punctuation
# print("中文标点符合：", punctuation_str)

class ZhengceSpider(scrapy.Spider):
    name = 'zhengce'
    allowed_domains = ['gi.mnr.gov.cn']
    start_urls = ['http://gi.mnr.gov.cn/']

    def __init__(self, keyword = "", repeat=0):
        super(ZhengceSpider, self).__init__()
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
        # dirList = response.xpath("/html/body/div[4]/div/div[3]/div[1]/div/span/a")
        dirList = response.xpath("//div[contains( @class ,'listd')]/span")
        # dirList = response.xpath("//div[contains( @class ,'listd')]/span[contains( @class ,'theme_parent')]")
        contList = response.xpath("//div[contains( @ class, 'listd')]/ul")

        item = ZrzypoliciesItem()
        for i in range(len(dirList)):
            dir = dirList[i]
            dirName =  dir.xpath(".//a/text()").extract_first()
            dir2List = contList[i].xpath(".//li")
            for dir2 in dir2List:
                dir2Name = dir2.xpath(".//a/text()").extract_first()
                contentUrl= dir2.css("a::attr(href)").get()
                # url = dir2.xpath(".//a/@href").extract()
                url = contentUrl.replace('./gkml2018','http://gi.mnr.gov.cn')
                punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
                dirNameStr = re.sub(r"[%s]+" % punc, "", str(dirName).strip())
                dir2NameStr = re.sub(r"[%s]+" % punc, "", str(dir2Name).strip())
                classification = dirNameStr + '_' + dir2NameStr
                item['classification'] = dirNameStr+'_'+dir2NameStr
                # 主题为“人事管理”、“建议留言”，无需爬取！！！
                if "人事管理" in classification or "建议留言" in classification or "领导简介" in classification:
                    continue
                if "部门规章" in classification or "规范性文件" in classification:
                    url = url
                    yield scrapy.http.Request(url=url, meta={'item': copy.deepcopy(item)}, callback=self.parseInfo,
                                              errback=self.errback)
                # item['district'] = dir.css("a::text").get()
                else:
                    yield scrapy.http.Request(url = url, meta={'item': copy.deepcopy(item)}, callback=self.parseInfo,errback=self.errback)

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
                infoList.append(text0)
            else:infoList.append("")
        title = infoList[5][0]
        tiCai = infoList[13][0]
        # 体裁为“决定、公告、通报、公示、批复“
        if '决定' not in tiCai and '公告' not in tiCai and '通报' not in tiCai and '公示' not in tiCai and '批复' not in tiCai:
            if(len(infoList)>8):
                if len(item['title']) < 1 and len(infoList[1]) > 0:
                    item['title'] = infoList[1][0]
                if  isinstance((infoList[3]),list):
                    item['index'] = infoList[3][0]
                if isinstance((infoList[5]), list):
                    item['topic'] = infoList[5][0]
                if isinstance((infoList[7]), list):
                    item['id'] = infoList[7][0]
                if isinstance((infoList[9]), list):
                    item['organization'] = infoList[9][0]
                elif isinstance(infoList[9],str):
                    item['organization'] = infoList[9]
                if isinstance((infoList[11]), list):
                    item['createDate'] = infoList[11][0]
                elif isinstance(infoList[11],str):
                    item['createDate'] = infoList[11]
                if isinstance((infoList[13]), list):
                    item['tiCai'] = infoList[13][0]
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
                    item['detailInfo'] = detailInfo
                yield item

    def clean_sentence(item_temp):
        item_temp = item_temp.replace("<p>\r\n\t<br />", "").replace("<br />\r\n\t", "&&").replace("</p>", "").replace(
            "<p>", "").replace("\r\n\t", "")
        item_temp = item_temp.split('、')
        if len(item_temp) == 2:
            item_temp = item_temp[1]
        else:
            # print(item_temp)
            return ''
        if "<a href=" not in item_temp:
            return item_temp + " &$\n"
        return ''

# class XiezilouSpider(scrapy.Spider):
#     name = 'xiezilou'
#     allowed_domains = ['wuhan.shop.fang.com/']
#     start_urls = ['http://wuhan.shop.fang.com//']
#     base_url = "https://wh.lianjia.com"
#
#     start_urls = [
#         "https://wh.lianjia.com/xiaoqu/jiangan/"
#     ]

