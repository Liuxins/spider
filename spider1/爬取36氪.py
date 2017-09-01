#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/16 16:07
# @Author  : LiuXin
# @Site    : 
# @File    : 爬取36氪.py
# @Software: PyCharm
# @version: 1.0
import json

import requests,re
from retrying import retry


class Kr():
    def __init__(self):
        self.start_url= 'http://36kr.com/api/info-flow/main_site/posts?'

        self.temp_url='http://36kr.com/api/info-flow/main_site/posts?column_id=&b_id={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

    '''发送请求获取响应'''

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        response = requests.get(url, headers=self.headers, timeout=5, verify=False)
        assert response.status_code == 200  # 设置断言，接收到到后返回
        print('发起访问成功', url)
        return response.content.decode()

    def parse_url(self, url):
        try:
            html_str = self._parse_url(url)
        except Exception as e:
            print(e)
            html_str = None
        print('获取响应成功', url)
        return html_str

    def get_content_list(self,html):
        print(type(html))
        content_dict = json.loads(html)
        # print(content_dict)
        temp_data = content_dict['data']['items']
        # print(temp_data)
        content_list = [[i['title'],i['updated_at'],i['cover'],i['id']] for i in temp_data]
        for i in content_list:
            title = i[0]
            image_url = i[2]
            id = i[3]
            updated_at = i[1]
        return content_list,id
        print(content_list)

    def save_content(self,content_list):
        with open('36Kr所有新闻热点标题与链接集合.txt','a+', encoding="utf8") as f:  # 一次打开 避免多次打开引起程序缓慢
            # 因为数据多条所以遍历写入
            for content in content_list:
                f.write(content[2])
                f.write('\n')
                f.write(content[1])
                f.write('\n')
                print(content[0])
                f.write(content[0])

                f.write('\n')
                str1 = str(content[3])
                f.write(str1)
                # f.write(content[3])
                f.write('\n')
                print(content[3],content[2],'已成功爬取，保存成功')


    def run(self):
        # 1 匹配url
        id = True
        next_url = self.start_url
        while id:
            # 2.发送请求获取响应
            html = self.parse_url(next_url)
            # 3.数据筛选
            content_list,url_id=self.get_content_list(html)
            id = url_id
            # 4.保存数据
            self.save_content(content_list)
            # 5.获取下一个url持续循环234操作
            next_url = self.temp_url.format(url_id)

def main():
    kr = Kr()
    kr.run()

if __name__ == "__main__":
    main()