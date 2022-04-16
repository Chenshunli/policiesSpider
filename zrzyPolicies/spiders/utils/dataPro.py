

# encoding:utf-8
import csv
import pandas as pd
# 对爬取后的csv文件进行处理


# 读取csv文件
in_file1 = csv.reader(open('F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/zrzybZc.csv', encoding='utf-8'))
in_file2 = csv.reader(open('F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/gdZhengce.csv', encoding='utf-8'))
in_file3 = csv.reader(open('F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/gzZhengce0408.csv', encoding='utf-8'))
# F:\爬虫相关\zrzyPolicies\zrzyPolicies\spiders
# print(in_file)
# filename = 'F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/zhengce1.csv'
# 添加newline可以避免一行之后的空格,这样需要在python3环境下运行
outpath = 'F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/new/'
# out2 = open('F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/new/zhengCeProOut.csv', 'w', newline='', encoding='utf-8')


def zrzyPro(csv_file,outfile1,outfile2):
    out1 = open(outfile1, 'w', newline='',encoding='utf-8')
    out2 = open(outfile2, 'w', newline='',encoding='utf-8')
    csv_write = csv.writer(out1, dialect='excel')
    csv_write2 = csv.writer(out2, dialect='excel')
    csv_write.writerow(
        ["url","title", "index", "classification", "id", "organization", "createDate", "tiCai", "impDate",
         "abolitionDate", "detailInfo"])
    for item in csv_file:
        listnew = []
        for data in item:
            # if data.find("http"):
            #     infos = data.split(':')
            #     info = infos[1].replace('"', "").replace("?", "")
            infos = data.split(':')
            if len(infos) < 2:
                csv_write2.writerow(infos[0])
            else:
                info = infos[1].replace('"', "").replace("?", "")
                if "topic" in infos[0]:
                    listnew.append(info)
                    continue
                elif "title" in infos[0]:
                    listnew.append(info)
                    continue
                elif "index" in infos[0]:
                    listnew.append(info)
                    continue
                elif "id" in infos[0]:
                    listnew.append(info)
                    continue
                elif "organization" in infos[0]:
                    listnew.append(info)
                    continue
                elif "createDate" in infos[0]:
                    listnew.append(info)
                    continue
                elif "tiCai" in infos[0]:
                    listnew.append(info)
                    continue
                elif "impDate" in infos[0]:
                    listnew.append(info)
                    continue
                elif "abolitionDate" in infos[0]:
                    listnew.append(info)
                    continue
                elif "detailInfo" in infos[0]:
                    listnew.append(info)
                    continue
                # print(infos[0])
                elif "http" in data:
                    try:
                        listnew.append(info + ":" + infos[2].replace('"', ""))
                    except Exception as e:
                        print(infos[2])
                        print(e)
                # if "detailInfo" in data:
                # clean_sentence(infos[1])
        csv_write.writerow(listnew)
        # print item


def gdDataPro(csv_file,outfile1,outfile2):
    out1 = open(outfile1, 'w', newline='', encoding='utf-8')
    out2 = open(outfile2, 'w', newline='', encoding='utf-8')
    csv_write = csv.writer(out1, dialect='excel')
    csv_write2 = csv.writer(out2, dialect='excel')
    csv_write.writerow(
        ["url", "index","classification","organization", "createDate", "title", "id",  "fabuDate", "topic", "detailInfo"])
    for item in csv_file:
        listnew = []
        # download = False
        for data in item:
            infos = data.split(':')
            if len(infos) < 2:
                csv_write2.writerow(infos[0])
            else:
                info = infos[1].replace('"', "").replace("?", "")
                if "classification" in infos[0]:
                    listnew.append(info)
                    continue
                elif "title" in infos[0]:
                    listnew.append(info)
                    continue
                elif "index" in infos[0]:
                    listnew.append(info)
                    continue
                elif "topic" in infos[0]:
                    listnew.append(info)
                    continue
                elif "id" in infos[0]:
                    listnew.append(info)
                    continue
                elif "organization" in infos[0]:
                    listnew.append(info)
                    continue
                elif "createDate" in infos[0]:
                    listnew.append(info)
                    continue
                elif "fabuDate" in infos[0]:
                    listnew.append(info)
                    continue
                elif "detailInfo" in infos[0]:
                    listnew.append(info)
                    # 如果存在附件，进行附件下载
                    # if "附件" in info:
                    #     download = True
                    continue
                # print(infos[0])
                elif "url" in data:
                    listnew.append(info + ":" + infos[2].replace('"', ""))

                # if "detailInfo" in data:
                # clean_sentence(infos[1])
        csv_write.writerow(listnew)


def gzDataPro(csv_file,outfile1,outfile2):
    out1 = open(outfile1, 'w', newline='', encoding='utf-8')
    out2 = open(outfile2, 'w', newline='', encoding='utf-8')
    csv_write = csv.writer(out1, dialect='excel')
    csv_write2 = csv.writer(out2, dialect='excel')
    csv_write.writerow(
        ["url", "index", "title","source","createDate", "detailInfo"])
    for item in csv_file:
        listnew = []
        for data in item:
            infos = data.split(':')
            if len(infos) < 2:
                csv_write2.writerow(infos[0])
            else:
                info = infos[1].replace('"', "").replace("?", "")
                if "source" in infos[0]:
                    listnew.append(info)
                    continue
                elif "title" in infos[0]:
                    listnew.append(info)
                    continue
                elif "index" in infos[0]:
                    listnew.append(info)
                    continue
                elif "createDate" in infos[0]:
                    newData = data.replace('": "','/')
                    info2 = newData.split('/')[1].replace('"', "").replace("?", "")
                    listnew.append(info2)
                    continue
                elif "detailInfo" in infos[0]:
                    listnew.append(info)
                    continue
                # print(infos[0])
                elif "url" in data:
                    listnew.append(info + ":" + infos[2].replace('"', ""))
                # if "detailInfo" in data:
                # clean_sentence(infos[1])
        csv_write.writerow(listnew)


if __name__ == '__main__':
    print("待处理数据分类：")
    fClass = input()
    if fClass == "zrzy":
        out = outpath+"zrzyRes.csv"
        out2 = outpath+"zrzyOut.csv"
        zrzyPro(in_file1,out,out2)
    elif fClass == "gd":
        out = outpath + "gdRes.csv"
        out2 = outpath + "gdOut.csv"
        gdDataPro(in_file2,out,out2)
    elif fClass == "gz":
        out = outpath + "gzRes0408.csv"
        out2 = outpath + "gzOut0408.csv"
        gzDataPro(in_file3,out,out2)





# csv_write.writerow(item)
# df = pd.read_csv(filename, index_col=0)
# content_list = df.tolist()
# for content in content_list:
#     a = content

