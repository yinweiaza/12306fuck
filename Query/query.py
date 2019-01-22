# coding=utf-8
"""
查询余票功能；
"""

from Query.cdn import Cdn
from Query.RequestUrls import *
from  httpHander.HttpHander import Http_hander          # 用于和12306进行http交互；
import threading
import copy
import random

class Query:
    """
        一个查询；
    """
    def __init__(self, config,http_client, cdn, station_date, from_station, to_station, type="ADULT"):
        """
        查询余票；
        :param config:           配置；
        :param cdn:              CDN对象；
        :param station_date:     出发时间；
        :param from_station:     出发车站；
        :param to_station:       到达车站；
        :param type:             "成人， 小孩"
        """
        self.config = config
        self.http_client = http_client
        self.cdn = cdn
        self.station_date = station_date
        self.from_station = from_station
        self.to_station = to_station
        self.type = type

    def run(self):
        """
        开始查询余票;
        :return:
        """
        t = threading.Thread(target=self.do_query)
        t.setDaemon(True)
        t.start()

    def do_query(self):
        """
        执行查询；
        :return:
        """
        good_ips = self.cdn.get("good_ips", [])
        if good_ips:
            self.http_client.set_cdn_ip(good_ips[random.randint(1, len(good_ips)-1)])       # 随机一个响应快的cdn ip;
        select_url = copy.copy(urls["select_url"])
        select_url["req_url"] = select_url["req_url"].format(self.station_date, self.from_station, self.to_station,"leftTicket/queryZ")
        result = self.http_client.request(select_url)
        print(result)

