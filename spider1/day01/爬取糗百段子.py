#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/15 15:16
# @Author  : LiuXin
# @Site    : 
# @File    : 爬取糗百段子.py
# @Software: PyCharm
import requests,re
from retrying import retry









class Spider(object):
    def __init__(self):
        self.start_url = 'http://36kr.com/'
        self.headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}

    def run(self):
        # 1.获取初始url，设置headers等信息
        # 2. 发送请求，获取响应
        # 3. 提取帖子标题，url地址 下一页的url
        # 4. 发送关于帖子的url请求，获取响应
        # 5. 提取图片地址，item，文字地址等
        # 5.1 保存
        # 6. 发送下一页的url请求，循环
        pass
def main():
    spider = Spider()
    spider.run()


if __name__ == "__main__":
    main()