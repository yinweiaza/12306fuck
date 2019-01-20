# -*- coding: utf8 -*-
import os
import io
import yaml


class Config_Info:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__) + '/../config.yaml')
        self.content = {}
        self.bloaded = self.load()

    def load(self):
        """
        载入所有的配置
        :return:
        """
        if os.path.exists(self.config_path):
            try:
                f = io.open(self.config_path, 'r',encoding = "utf-8")
                self.content = yaml.load(f)
                f.close()
                if self.content:
                    return True
            except IOError:
                return False
        return False

    def get_all_accounts(self):
        """
        获取所有的账号
        :return:
        """
        return self.content.get("12306accouts", [])

    def account_numbers(self):
        """
        账号数
        :return:
        """
        return len(self.get_all_accounts())

    def job_number(self):
        """
        任务数
        """
        jobs = self.content.get("jobs", [])
        return len(jobs)

    def is_cdn(self):
        """
        是否使用cdn查询功能；
        :return:
        """
        return self.content.get("enable_cdn", 1)                    # 默认是开启cdn查询功能的