# coding = utf-8

from Query.cdn import Cdn
from data.Config_Info import Config_Info
import time

def main():
    """
    主程序
    :return:
    """
    # Cdn().run()         # 开启多线程进行cdn查询；
    print(Config_Info().job_number())
    # TODO: 开启登陆  要开启线程对登陆状态进行检查；
    # TODO: 开启查询  线程     查询有票要自动进行提交
    while True:
        time.sleep(1000)


def test():
    """
    测试入口；
    :return:
    """
    pass


if __name__ == '__main__':
    main()

