#encoding:utf-8
#调用需要的库
import requests
from bs4 import BeautifulSoup
import csv
import time
import random


def get_content(url):
    # url = "https://s.weibo.com/weibo?q=python&nodup=1"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'SINAGLOBAL=5900907584340.371.1578850135804; UOR=2351.replace.favo.fengmeng.net,weibo.com,www.ffxiv.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhxUuNNVQQQxX1zRenqZdGe5JpX5KMhUgL.Fo-NSh-7S0eXe0M2dJLoI0YLxK-L12BL1KMLxKqL1--L1h2LxKBLBonL1h.LxK-L12qLBoqLxKnL1K.LB-zLxK-L12eL1KqLxKML1-qLBoet; ALF=1680432959; SSOLoginState=1648896960; SCF=AkP41FU3o8dQjEfgAIogTceiVyiJ-GI-Vq4O1f14JDNFdfVsbxNwUfXTWsLQyaAW4cgqX2mRirqpT_t4pdq1L08.; SUB=_2A25PTFuQDeRhGeNJ71cR9y3IyDuIHXVsOMpYrDV8PUNbmtAKLUvGkW9NS9P9rEgfoMMaBlAbv6cLgJKLkg9ke3VJ; _s_tentry=weibo.com; Apache=7893640661834.076.1648896970986; ULV=1648896971036:133:2:3:7893640661834.076.1648896970986:1648809763925',
        'referer': 'https://s.weibo.com/weibo?q=python',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',

    }
    response = requests.get(url,headers=headers)
    html = BeautifulSoup(response.content,'lxml') #用bs包解析当前界面
    conetnt = html.find_all('div',class_="card-wrap") #每条微博都显示在card-wrap模块中
    for ct in conetnt: #for循环打印每条微博内容
       user_info = ct.find_all('a',class_="name") #每个用户的名称在<a>标签里
       if user_info !=[]:
           user_name = user_info[0].text #用户名称
           user_index = "https:"+ user_info[0]['href'] #用户的主页
           unser_from =  str(ct.find('p',class_="from").text).replace(' ','').replace('\n','') #发布时间、设备
           weibo_content = str(ct.find('p',class_="txt").text).replace(' ','').replace('\n','') #微博内容
           data = [weibo_content,user_name,unser_from,user_index] #数据储存
           saveCsv('微博内容', data)
          # print(weibo_content)

#循环50页
def runx():
    n = 0
    for  x in range (1,51):
        print(f"正在抓取第{x}页")
        n += 1
        url = f"https://s.weibo.com/weibo?q=python&nodup=1&page={x}"
        t = random.randint(2,5) #每翻一页休息
        print(f"{t}秒后开始抓取")
        time.sleep(t)


        if n%5 == 0: #翻了五页后休息
            t = random.randint(5,10) #随机抽取5-10
            print(f"{t}秒后继续抓取")
            time.sleep(t) #休息t时间


        get_content(url) #继续运行抓取程序


def saveCsv(filename,content): #新建文件将数据存储到excel表格中
    fp = open(f"{filename}.csv",'a+',encoding='utf-8-sig',newline='')
    csv_fp = csv.writer(fp)
    csv_fp.writerow(content)
    fp.close()
    print(f"成功写入：{content}")


if __name__ == '__main__':
    col = ['微博内容','发布者名称','发布时间及设备','发布者主页'] #表格列名
    saveCsv('微博内容', col)
    runx()

