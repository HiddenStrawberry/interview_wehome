# encoding=utf8
import json
import threading
import traceback
import re
import requests
import time

IP_POOL = []

retry_times = 50  # 请求重试数量
min_ip = 50  # 最小IP数量
DAXIANG_ORDER = ''


def get_ip_daxiang():
    while True:
        time.sleep(0.1)
        if len(IP_POOL) < min_ip:
            for x in range(retry_times):
                try:
                    js = requests.get(
                            'http://vtp.daxiangdaili.com/ip/?tid=' + DAXIANG_ORDER + '&num=' + str(
                                min_ip) + '&delay=3').text
                    for each in js.split('\r\n'):
                        IP_POOL.append(each)

                    break
                except Exception as err:
                    print err


def ip_process():
    threading.Thread(target=get_ip_daxiang).start()


class Connection:
    def __init__(self, error_page=[]):
        global IP_POOL
        self.proxies = {}
        self.count = 0
        self.ip_used = 0
        self.timeout = 10
        self.error_page = error_page
        self.proxy_error = ['bad request','error_crawler_page_top','maximum web proxy', 'squid software', '500 internal privoxy error',
                            'number of open connections reached', 'ccproxy', 'proxy error', 'hhgb4', 'artica-proxy',
                            '403 forbidden', '503 service','antispider']
        self.proxy_error.extend(error_page)
        self.session = requests.session()

    def changeip(self):
        js = IP_POOL[0]
        del IP_POOL[0]
        proxies = {'http': 'http://' + js}

        self.proxies = proxies
        self.ip_used += 1

    def antiSpiderCheck(self, word):
        word = word.lower()
        for each in self.proxy_error:
            if each in word:
                return False
        else:
            return True

    def geturl(self, URL, needproxy=True, headers={}):
        for x in range(10000000):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
                }
                html = self.session.get(URL, headers=headers, proxies=self.proxies, timeout=self.timeout).text
                return html
            except Exception as err:

                if needproxy:
                    self.changeip()
                else:
                    pass

    def posturl(self, URL, data={},needproxy=True,headers={}):
        for x in range(100):
            try:
                html = self.session.post(URL, data=data, headers=headers, proxies=self.proxies,
                                         timeout=self.timeout).text
                if '"success"' in html:
                    return html
                else:
                    raise Exception('Network Error')
            except Exception as err:
                if needproxy:
                    self.changeip()
                else:
                    pass

# c = Connection
