from scrapy import cmdline

# f = open("topic.txt",encoding='utf-8')
# f2 = open("keywords.txt",encoding='utf-8')
if __name__ == '__main__':
    command = "scrapy crawl gzZhengce"
    # command = "scrapy crawl gdZhengce"
    # command = "scrapy crawl zhengce"
    # command = "scrapy crawl zrzybZc"
    cmdline.execute(command.split())
