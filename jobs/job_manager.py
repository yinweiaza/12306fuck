"""
工作管理模块， 每一项工作JOG开启一个线程进行处理；
"""
from data.Config_Info import Config_Info
from Query.cdn import Cdn
from httpHander.HttpHander import Http_hander

class JobManager:
    """
    任务管理器；
    """
    def __init__(self):
        self.config = Config_Info()
        self.httpClient = Http_hander()
        self.jobs = []  # 所有的jobs;
        if self.config.is_cdn():        #如果设置了cdn， 那么久开启cdn查询；
            self.cdn = Cdn()
            self.jobs.append(self.cdn)          #添加一个job
        self.isOver = False

    def is_over(self):
        """
        所有的工作都结束了吗；
        :return:
        """
        return self.isOver

    def start(self):
        """
        开始执行所有的任务
        :return:
        """
        for job in self.jobs:
            job.run()

    def add_job(self, job):
        """
        添加一项工作
        :param job:
        :return:
        """
        self.jobs.append(job)

