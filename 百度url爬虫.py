import requests
import time
import urllib3
import socket
import queue
from lxml import etree

"""
1.发起请求，获取搜索数据
2.定位携带url的标签并取出
3.遍历网页
4.保存遍历信息
"""
def baidu_get():
    while not q.empty():
        url = q.get()
        req = requests.get(url, headers=headers)
        time.sleep(1)
        baidu = req.text

        code = etree.HTML(baidu)
        codes = code.xpath('//*[@class="c-title t t tts-title"]')
        for codess in codes:
            codesss = codess.xpath('./a')
            for codesss in codesss:
                codesssss = codesss.xpath('@href')
                bd_url = codesssss[0]
                urllib3.disable_warnings()
                try:
                    bd_req = requests.get(bd_url, headers=headers, proxies=proxies,verify=False)
                    #requests.DEFAULT_RETRIES = 3
                    #bd_req.keep_alive = False
                    urls = bd_req.url
                    with open("ip.txt", 'a', encoding='utf-8') as f:
                        f.write(str(urls) + '\n')
                        print(urls)
                        bd_req.close()
                        time.sleep(2)
                except:
                    print('跳过异常！！')


if __name__ == "__main__":
    q = queue.Queue()
    select = input("输入你要爬取的内容：")
    url = 'https://www.baidu.com/s?wd='+ select +'&pn='
    socket.setdefaulttimeout(10)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
    proxies = {"http": None, "https": None}
    page = input("输入你要爬的页数：")
    for i in range(int(page)):
        i = i * 10
        urls = url + str(i)
        q.put(urls)  # 把发送的数据发到函数上

    baidu_get()