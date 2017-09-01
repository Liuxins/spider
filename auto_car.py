#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/14 23:49
# @Author  : LiuXin
# @Site    : 
# @File    : auto_car.py
# @Software: PyCharm
# @version: 1.0
import requests


class SpiderCar(object):
    def __init__(self,name):
        self.html_name = name
        temp_url = 'http://car.autohome.com.cn/photo/series/25184/1/3314{}.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'DNT': '1',
        }
        self.url_list = []
        for i in range(200,1000):
            self.url_list.append(temp_url.format(i))
        print(self.url_list)


    def parse_url(self,url):
        print('正在获取响应，爬取网页%s' % url)
        response = requests.get(url, headers=self.headers)
        print(response.encoding)    # 查看返回的是什么编码
        return response.content

    def save(self,html,page_num):
        # 保存之前先定义文件路径以及存储的文件名
        file_path = self.html_name + '_' + str(page_num) + '.html'
        # file_path = self.html_name + '_' + str(page_num) + '.html'

        with open(file_path, 'wb') as f:
            f.write(html)


    def run(self):
        # 1.init 是设置默认的参数
        # 2. parse 开始爬取网页
        for url in self.url_list:
            html = self.parse_url(url)
            page_num = self.url_list.index(url)  # 获取页码数
            if html:
                self.save(html,page_num)
                print('爬取成功')


def main():
    spider = SpiderCar('汽车之家君越')
    spider.run()


if __name__ == "__main__":
    main()