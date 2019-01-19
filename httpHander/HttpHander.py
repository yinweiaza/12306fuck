

import json
import socket
from collections import OrderedDict
from time import sleep
import requests
import urllib3

class Http_hander:
    def __init__(self):
        self.session = requests.Session()            # 会话
        self.session.headers.update(self.getheader())
        self.cdn_ip = None

    def cdn(self):
        return self.cdn_ip

    def set_cdn_ip(self, cdn):
        self.cdn_ip = cdn

    def request(self, urls, data=None, **kwargs):
        """
        请求；
        :param urls: 请求网址；
        :param data:            post数据；
        :param kwargs:          其他参数
        :return:
        """
        allow_redirects = False
        re_try = urls.get("re_try", 0)                                         # 请求次数
        re_time = urls.get("re_time", 0)                                       # 请求停留时间
        s_time = urls.get("s_time", 0)
        is_test_cdn = urls.get("is_test_cdn", False)                               # 是否测试cdn;
        if data:                        # post;
            method = "post"
            self.session.headers.update({"Content-Length": "{0}".format(len(data))})
        else:                           # get
            method = "get"
            self.reset_header()
        self.session.headers.update({"Referer": "{0}".format(urls["Referer"])})
        is_cdn = urls.get("is_cdn", False)                  # 是否使用cdn查询；
        self.session.headers.update({"Host": "{0}".format(urls["Host"])})
        host_ip = urls["Host"]
        if is_test_cdn:
            host_ip = self.cdn()
            allow_redirects = True
        if is_cdn:
            ip_temp = self.cdn()
            if ip_temp:
                host_ip = ip_temp
                allow_redirects=True
        error_data = "重复次数达到了上限"
        url="http://" + host_ip + urls["req_url"]
        for iter in range(re_try):                      # 多次尝试
            try:
                sleep(s_time)
                try:
                    urllib3.disable_warnings()
                except:
                    pass
                result = self.session.request(
                                                method=method,
                                                timeout=2,
                                                url="http://" + host_ip + urls["req_url"],
                                                allow_redirects=allow_redirects,
                                                data=data,
                                                verify=False,
                                                **kwargs
                                            )
                if result.status_code == 200 or result.status_code == 302:
                    if urls.get("not_decode", False):           # 如果没有进行编码（明码）， 那么直接返回内容
                        return result.content
                    if result.content:
                        if urls["is_json"]:
                            return json.load(result.content.decode() if isinstance(result.content, bytes) else
                                             result.content)
                        else:
                            return result.content.decode("utf8", "ignore") if isinstance(result.content, bytes) else \
                                             result.content
                    else:
                        error_data = "内容为空"
                        return error_data
                else:
                    sleep(re_time)
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass
        return error_data

    def getheader(self):
        """
        获取请求标头；
        :return:
        """
        header_dict = OrderedDict()
        header_dict["Accept-Encoding"] = "gzip, deflate"
        header_dict[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) " \
                            "12306-electron/1.0.1 Chrome/59.0.3071.115 Electron/1.8.4 Safari/537.36"
        header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        return header_dict

    def update_header(self, headers):
        """
        融合header；
        :param headers:
        :return:
        """
        self.session.headers.update(headers)

    def reset_header(self):
        """
        恢复默认标头；
        :return:
        """
        self.session.headers.clear()
        self.session.headers.update(self.getheader())
