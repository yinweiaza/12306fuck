from  Query.query import Query


class QueryJob:
    def __init__(self):
        self.querys = []

    def addQuery(self, query):
        """
        添加查询任务;
        :return:
        """
        self.querys.append(query)

    def queryNumber(self):
        """
        总共又多少查询任务；
        :return:
        """
        return len(self.querys)

    def run(self):
        """
        执行所有的查询任务
        :return:
        """
        for qy in self.querys:
            qy.run()

