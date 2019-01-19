# coding=utf-8
"""
查询余票功能；
"""

from Query.cdn import Cdn
from Query.RequestUrls import UrlConfig

class Query:
    def __init__(self):
        self.cdn = Cdn()
        self.urlsIns = UrlConfig()

