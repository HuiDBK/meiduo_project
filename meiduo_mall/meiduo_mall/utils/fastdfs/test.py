#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { FastDFS 客户端测试模块 }
# @Date: 2021/10/07 20:47
from fdfs_client.client import get_tracker_conf, Fdfs_client


def main():

    # 加载追踪服务器的配置信息
    tracker_conf = get_tracker_conf('client.conf')

    # 创建FastDFS客户端实例
    client = Fdfs_client(tracker_conf)

    # 调用FastDFS客户端上传文件方法
    ret = client.upload_by_filename('02.jpeg')

    print(ret)


if __name__ == '__main__':
    main()
