

# encoding:utf-8
import csv
import pandas as pd
# 对爬取后的csv文件进行处理


# 读取csv文件
in_file = csv.reader(open('F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/zhengce3.csv', encoding='utf-8'))
print(in_file)
filename = 'F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/zhengce1.csv'
# 添加newline可以避免一行之后的空格,这样需要在python3环境下运行
out = open('F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/zhengCePro.csv', 'w', newline='', encoding='utf-8')
out2 = open('F:/爬虫相关/zrzyPolicies/zrzyPolicies/spiders/files/zhengCeProOut.csv', 'w', newline='', encoding='utf-8')


def zrzyPro(csv_file,out1,out2):
    csv_write = csv.writer(out1, dialect='excel')
    csv_write2 = csv.writer(out2, dialect='excel')
    csv_write.writerow(
        ["classification", "title", "url", "index", "topic", "id", "organization", "createDate", "tiCai", "impDate",
         "abolitionDate", "detailInfo"])
    for item in csv_file:
        listnew = []
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
                elif "url" in data:
                    listnew.append(info + ":" + infos[2].replace('"', ""))
                # if "detailInfo" in data:
                # clean_sentence(infos[1])
        csv_write.writerow(listnew)
        # print item
        data = item


def gdDataPro(csv_file,out1,out2):
    csv_write = csv.writer(out1, dialect='excel')
    csv_write2 = csv.writer(out2, dialect='excel')
    csv_write.writerow(
        ["classification", "title", "url", "index", "topic", "id", "organization", "createDate", "fabuDate","detailInfo"])
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


def gzDataPro(csv_file,out1,out2):
    csv_write = csv.writer(out1, dialect='excel')
    csv_write2 = csv.writer(out2, dialect='excel')
    csv_write.writerow(
        ["classification", "title", "url", "index", "topic", "id", "organization", "createDate", "tiCai", "impDate",
         "abolitionDate", "detailInfo"])
    for item in csv_file:
        listnew = []
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
                elif "url" in data:
                    listnew.append(info + ":" + infos[2].replace('"', ""))
                # if "detailInfo" in data:
                # clean_sentence(infos[1])
        csv_write.writerow(listnew)


if __name__ == '__main__':
    print("待处理数据分类：")
    fClass = input()
    if fClass == "zrzy":
        zrzyPro(in_file,out,out2)
    elif fClass == "gd":
        gdDataPro(in_file,out,out2)
    elif fClass == "gz":
        gzDataPro(in_file,out,out2)





# csv_write.writerow(item)
# df = pd.read_csv(filename, index_col=0)
# content_list = df.tolist()
# for content in content_list:
#     a = content

