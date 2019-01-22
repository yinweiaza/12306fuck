# coding=utf-8
"""
    CDN查询；
"""
import os
import sys
from exception.exception import ExceptionsEnum
import threading
from Query.RequestUrls import *
import time
from httpHander.HttpHander import Http_hander

class Cdn:
    def __init__(self):
        """
        CDN查询；
        :param cdn_file:
        """
        self.cdn_file = os.path.join(os.path.dirname(__file__), '../data/cdn_ips')
        self.all_ips = []               # 所有的cdn
        self.good_ips = []              # 响应速度快的cdn ip;
        self.time_ips = []              #相应的时间耗损；

    def load(self):
        """
        从 cdn文件中导入ip地址；
        :return:
        """
        if os.path.exists(self.cdn_file):
            try:
                with open(self.cdn_file, 'r') as f:
                    for line in f.readlines():
                        self.all_ips.append(line.strip())
            except IOError:
                print(ExceptionsEnum.CDN_FILE_OPEN_ERROR)
                sys.exit(-1)
        else:
            print(ExceptionsEnum.CDN_FILE_OPEN_ERROR)
            sys.exit(-1)

    def run(self):
        self.load()
        self.start()

    def start(self):
        """
            线程， 持续对cdn进行探索；
        :return:
        """
        t = threading.Thread(target=self.cdn_request, args=(self.all_ips,))
        t.setDaemon(True)           # 设置为后台线程，主线程不用等待子线程；
        t.start()

    def order_good_ip(self, ip, times):
        """
        对检测到的cdn进行排序，按照时间耗损；
        :param ip:
        :param times:
        :return:
        """
        l=len(self.good_ips)
        if l > 10:
            idx = self.time_ips.index(max(self.time_ips))
            if self.time_ips[idx] > times:          #比最大的小，那么就置换；
                self.good_ips[idx] = ip
                self.time_ips[idx] = times
        else:
            self.good_ips.append(ip)
            self.time_ips.append(times)


    def cdn_request(self, all_ips):
        """
        对所有的cdn_ip进行验证;
        :return:
        """
        http_handler = Http_hander()             # 请求子；
        for ip in all_ips:
            ip = ip.replace("\n", "")
            http_handler.set_cdn_ip(ip)
            start_time = time.time()
            url_temp = urls["loginInitCdn"]
            result = http_handler.request(url_temp)           # 请求；
            time_total = int((time.time() - start_time) * 1000)  # 时间耗损；
            print("{0}: {1}ms".format(ip, time_total))
            if result and "message" not in result and time_total<1000:
                self.order_good_ip(ip, time_total)
        print("所有的cdn检测完成")