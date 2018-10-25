# -*- coding: utf-8 -*-

import csv
import requests
from requests.exceptions import RequestException
import re
import time

district_id = input("请输入区号：")
spe_id = input("请输入帖子id：")
page = input("请输入总页数：")
file_name = input("保存文件名（名字末尾加上“.csv”）：")

# 写入fieldnames
with open(file_name, 'a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', '发言时间', '发言内容', '楼层号'])


def get_one_page(page_now):
    """
    输入：需要爬取帖子的总页码
    输出：本页的源代码html(str格式)
    """
    url = "http://bbs.jjwxc.net/showmsg.php?board=" + district_id + "&boardpagemsg=1&id=" + spe_id + "&page=" + str(
        page_now)
    try:
        headers = {
            "Cookie" : "__gads=ID=694b97efeb86c8c2:T=1540287492:S=ALNI_MYmL7fQknkgH9acS7bA_Zg2B8IA5Q; U"
                       "M_distinctid=166a65c9be115c-01270474249844-b79193d-144000-166a65c9be634b; CNZZDA"
                       "TA30012213=cnzz_eid%3D976476925-1540385198-http%253A%252F%252Fbbs.jjwxc.net%252F%2"
                       "6ntime%3D1540385198; jjwxcImageCode=d0e497aa8ce44738ecf9443e7e3b959e; jjwxcImageCo"
                       "deTimestamp=2018-10-24+22%3A07%3A51; nicknameAndsign=2%257E%2529%2524launa; token=Mj"
                       "A0Mzc2ODl8YTZjOTYzNzNmZDc2Mzc0NGZhYmI4ZGE5NDEwODUzOTF8fHx8MTA4MDB8MXx8fOasoui%2Fjua"
                       "CqO%2B8jOaZi%2Baxn%2BeUqOaIt3wxfG1vYmlsZQ%3D%3D; JJEVER=%7B%22ispayuser%22%3A%22204"
                       "37689-1%22%2C%22foreverreader%22%3A%2220437689%22%7D; bbsnicknameAndsign=2%257E%2529"
                       "%2524launa; bbstoken=MjA0Mzc2ODlfMF9jMGQ1YjNiMjVkMzRmM2RjY2QzMGMyOGY5ZDk0YmI3OV8xX18%3D",
            "Host" : "bbs.jjwxc.net",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = "gbk"
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 元组组内容：第一项：楼层内容；第二项：楼层号码；第三项：随机id；第四项：发表时间
def parse_one_page(html):
    """
    输入：源代码html;
    输出：findall:返回符合正则表达式的所有元素，形式为：列表中的元组形式[(a,b,c,d)]
    """
    pattern = re.compile("""<td class="read" >.*?id='replybody.*?'>(.*?)</div>.*?№(.*?)</font>.*?<font color=#999999>(.*?)</font>.*?于</font>(.*?)留言""", re.S)
    items = re.findall(pattern, html)
    return items

# 将所得四项内容（随机id、发表时间、楼层内容、楼层号码）的顺序写入文件
def write_to_file(content):
    """
    输入：字典形式
    输出：csv文档
    """
    with open(file_name, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([content[2], content[3], content[0], content[1]])


# 整合函数，做单个页上的内容爬取
def main(page_now):
    html = get_one_page(page_now)
    for item in parse_one_page(html):
        write_to_file(item)


# 执行函数,遍历所有页
if __name__ == '__main__':
    for i in range(int(page)):
        main(page_now=i)
        time.sleep(1)