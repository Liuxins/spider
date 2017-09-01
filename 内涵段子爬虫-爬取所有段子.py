#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/15 17:45
# @Author  : LiuXin
# @Site    : 
# @File    : 内涵段子爬虫-爬取所有段子.py
# @Software: PyCharm
import requests,re
from retrying import retry


class NeiHan(object):
    def __init__(self): # 一些默认参数等 例如url headers
        self.start_url = 'http://neihanshequ.com/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        self.pattern = re.compile(r'<a target=\"_blank\" class=\"image share_url\" href=\"(.*?)\".*?<p>(.*?)</p>',re.S )    # 返回的是一个列表


    def get_content_list(self,html_str):    # 获取匹配内容
        content_list = self.pattern.findall(html_str)
        return content_list


    @retry(stop_max_attempt_number=4)   # 重复次数
    def _parse_url(self):
        response = requests.get(self.start_url,headers=self.headers,timeout=3)  # 请求url 获取响应
        assert response.status_code == 200  # 启用断言，若获取正常则进行下一步
        return response.content.decode()    # 返回


    def parse_url(self):    # 假设获取会产生异常 ，做出异常处理
        try:
            html_str=self._parse_url()
        except Exception as e:
            print(e)
            html_str =None
        return html_str




    def save_content_list(self,content_list):
        with open('内涵段子1简单网页爬取.txt','a+')as f:
            for content in content_list:
                print(content)
                f.write(content[0])
                f.write("\n")
                f.write(content[1])
                f.write("\n")


    def run(self):  # 运行
        # 1. 匹配url
        # 2. 发送请求，获取响应
        html_str = self.parse_url()
        # 3. 提取数据
        content_list = self.get_content_list(html_str)
        # 4. 保存
        self.save_content_list(content_list)
        # 5. 下一页url 循环爬取

def main():
    neihan = NeiHan()
    neihan.run()

if __name__ == "__main__":
    main()