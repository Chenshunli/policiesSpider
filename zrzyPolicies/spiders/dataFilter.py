# -*- coding:utf-8 -*-

import pandas as pd
import re


import jieba


def filter_tags(htmlstr):
    """
    # Python通过正则表达式去除(过滤)HTML标签
    :param htmlstr:
    :return:
    """
    # 先过滤CDATA
    re_cdata = re.compile('//<!\
    CDATA\[[ >]∗ //\
    CDATA\[[ >]∗ //\
    \] > ',re.I) #匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    # style
    re_br = re.compile('<br\s*?/?>')
    # 处理换行
    re_h = re.compile('</?\w+[^>]*>')
    # HTML标签
    re_comment = re.compile('<!--[^>]*-->')
    # HTML注释
    s = re_cdata.sub('', htmlstr)
    # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)
    # 去掉style
    s = re_br.sub('\n', s)
    # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)
    # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s



def replaceCharEntity(htmlstr):
    """
    :param htmlstr:HTML字符串
    :function:过滤HTML中的标签
    """
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string,s)



def Cleaning_data(x):
    m2=str(x).replace('<p>&nbsp; &nbsp; &nbsp; &nbsp;','').replace('</p><p><br></p>','').replace('<br>','').replace('</p>','').replace('<p>','').replace('       ','').replace('[图片]','').strip()
    m3=filter_tags(m2)
    m4=replaceCharEntity(m3)
    print(m4)
    m5 = m4.replace("\n","").replace("\t","")
    print(m5)
    m6 = m5.strip()
    print(m6)
    return m6



if __name__ == '__main__':
    # # 读取数据
    # data = pd.read_csv('C:\\Users\\xiaohu\\Desktop\\香蕉球用户话题\\香蕉球用户话题.csv')
    # # print(data)
    #
    # for each in data.iloc[:,3]:
    #     # print(each)

        # Cleaning_data(each)
    data = '"detailInfo": "<div class=\"xx\" id=\"content\">\n\t\t\t<h3 style=\"margin-bottom:14px;\">国土资源部机关办公用房局部维修改造项目招标公告</h3>\n                          <h6 style=\"text-align:center;font-size:22px;color:#555;margin:16px 0;\"></h6>\n\t\t\t<p>\n </p><div style=\"text-align: center;\"><span style=\"font-size: 12pt;\"> </span><strong style=\"font-size: 12pt; line-height: 1; text-align: center;\">（工程类）</strong></div>\n<table cellpadding=\"0\">\n    <tbody>\n        <tr class=\"firstRow\">\n            <td style=\"BORDER-BOTTOM-COLOR: #000000; PADDING-BOTTOM: 1px; BACKGROUND-COLOR: transparent; BORDER-TOP-COLOR: #000000; PADDING-LEFT: 1px; PADDING-RIGHT: 1px; BORDER-RIGHT-COLOR: #000000; BORDER-LEFT-COLOR: #000000; PADDING-TOP: 1px\" width=\"340\">\n            <p>项目编号：GC-GG3171273B</p>\n            </td>\n            <td style=\"BORDER-BOTTOM-COLOR: #000000; PADDING-BOTTOM: 1px; BACKGROUND-COLOR: transparent; BORDER-TOP-COLOR: #000000; PADDING-LEFT: 1px; PADDING-RIGHT: 1px; BORDER-RIGHT-COLOR: #000000; BORDER-LEFT-COLOR: #000000; PADDING-TOP: 1px\" width=\"310\">\n            <p style=\"TEXT-ALIGN: right\">日期：2018年1月12日</p>\n            </td>\n        </tr>\n    </tbody>\n</table>\n<p><span style=\"FONT-SIZE: 12px\"> </span></p>\n<table cellspacing=\"0\" cellpadding=\"0\">\n    <tbody>\n        <tr style=\"HEIGHT: 34px\" class=\"firstRow\">\n            <td style=\"border-color: black; border-style: inset; padding: 1px; background-color: transparent;\" height=\"34\" rowspan=\"7\" width=\"75\">\n            <p style=\"TEXT-ALIGN: center; MARGIN-TOP: auto; MARGIN-BOTTOM: auto\">招标项目</p>\n            <p style=\"TEXT-ALIGN: center; MARGIN-TOP: auto; MARGIN-BOTTOM: auto\">概  况</p>\n            </td>\n            <td style=\"border-color: black black black rgb(0'
    Cleaning_data(data)