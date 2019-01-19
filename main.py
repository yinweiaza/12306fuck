# coding = utf-8

from Query.cdn import Cdn


def main():
    """
    主程序
    :return:
    """
    Cdn().run()         # 开启多线程进行cdn查询；


def test():
    """
    测试入口；
    :return:
    """
    pass


if __name__ == '__main__':
    main()

