#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/14 23:19
# @Author  : LiuXin
# @Site    : 
# @File    : auto_image.py
# @Software: PyCharm
# 爬取汽车之家君越车型的图片
import requests
from retrying import retry




class Spider(object):




    def __init__(self):
        self.url='http://car.autohome.com.cn/photo/series/25184/1/3314{}.html'
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'DNT':1,
        }

    def parse_url(self,url):
        try:
            response = requests.get(url,headers=self.headers)
            return response.content.decode()
        except Exception as e:
            print(e)
    def run(self):
        url_list = []
        for i in range(1,1000):
            url_list.append(self.url.format(i))

        # 开始请求了

        file_path = 'auto_image' + '_' + str(i) + '.html'
        for url in url_list:
            auto = self.parse_url(url)
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(auto)


if __name__ == "__main__":
    spider = Spider()
    spider.run()