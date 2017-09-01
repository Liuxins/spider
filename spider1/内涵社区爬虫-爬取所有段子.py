#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/15 21:06
# @Author  : LiuXin
# @Site    : 
# @File    : 内涵社区爬虫-爬取所有段子.py
# @Software: PyCharm
# @version: 1.0
import json

import requests,re
from retrying import retry








class NeiHan(object):
    def __init__(self): #1 start_url 设定
        self.start_url = 'http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web'  # 根据后续的json加载 试验这个可以成为第一页 也可以返回数据 但与直接输入不同 也可以作为爬取数据用
        self.temp_next_url = 'http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time={}'   # 根据规律来制定url 后续的直接ma_time直接后面生成
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}

    '''发送请求获取响应'''
    @retry(stop_max_attempt_number=3)
    def _parse_url(self,url):
        response = requests.get(url,headers=self.headers,timeout=5,verify=False)
        assert response.status_code==200 # 设置断言，接收到到后返回
        print('发起访问成功',url)
        return response.content.decode()
    def parse_url(self,url):
        try:
            html_str = self._parse_url(url)
        except Exception as e:
            print(e)
            html_str = None
        print('获取响应成功',url)
        return html_str


    '''提取数据和提起下一步的max_time'''
    def get_content_list(self,json_str):
        content_dict = json.loads(json_str) # 得到的数据转化成python识别的字典
        temp_data = content_dict['data']['data']    # 根据json表中的数据将所有段子取出来 当前页面的20条 返回的事业列表
        # 然后遍历列表中的字典 得到url与段子内容字典集合
        content_list = [[i['group']['share_url'],i['group']['text']] for i in temp_data]
        max_time = content_dict['data']['max_time']     # 这是得到max_time 就是下一个url内容后缀
        has_more = content_dict['data']['has_more']     # 这是取得终止的条件等
        return content_list,max_time,has_more

    '''保存数据'''
    def save_content_list(self,content_list):
        with open('内涵段子所有段子集合.txt','a+') as f:  # 一次打开 避免多次打开引起程序缓慢
            # 因为数据多条所以遍历写入
            for content in content_list:
                f.write(content[0])
                f.write('\n')
                f.write(content[1])
                f.write('\n')
                print(content[0],'已成功爬取，保存成功')


    '''初始运行'''
    def run(self):
        has_more = True
        next_url = self.start_url
        while has_more:
            # 1.start_url 设定
            # 2.发送请求，获取响应
            html = self.parse_url(next_url)
            # 3.提取数据与下一步的max_time
            content_list,max_time,has_more=self.get_content_list(html)
            # 4.保存数据
            self.save_content_list(content_list)
            # 5.下一页url，循环直到has_more位Flase终止
            next_url = self.temp_next_url.format(max_time)

def main():
    neihan=NeiHan()
    neihan.run()


if __name__ == "__main__":
    main()