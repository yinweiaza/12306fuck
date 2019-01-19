
from requests.sessions import Session
from collections import OrderedDict             # 有序字典

class Http_hander:
    def __init__(self):
        self.session = Session()            # 会话
        self.session.headers.update(self.getheader())

    def request(self, url, data=None, **kwargs):
        """
        请求；
        :param url: 请求网址；
        :param data:            post数据；
        :param kwargs:          其他参数
        :return:
        """
        if data:                        # post;
            self.session.headers.update(data)
        else:                           # get
            self.session.get(url)

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
        self.session.headers.update(self.reset_header())
