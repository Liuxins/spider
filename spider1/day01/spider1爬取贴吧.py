#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Time    : 17-8-12 下午4:28
# @Author  : LiuXin
# @Site    : 
# @File    : spider1爬取贴吧.py
# @Software: PyCharm
import requests


class Tieba(object):


    def __init__(self,tieba_name='汽车'): # 1. 构造待请求的ｕｒｌ
        self.tieba_name = tieba_name
        temp_url = 'https://tieba.baidu.com/f?kw='+self.tieba_name+'&ie=utf-8&pn={}'
        self.url_list=[]    # 因为页面的变化页码也会变　　这是遍历一个范围可以爬取哪些范围
        for i in range(0,21):
            self.url_list.append(temp_url.format(i*50))
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

    #

    def parse_url(self,url):    #发送请求，获取响应
        print('正在获取响应　now parsing',url)
        # 因为请求方式为response = requests.get(url,params = kw,header= header)
        response = requests.get(url,headers = self.headers)
        return response.content.decode()    # 获取字符串

    def save_html(self,html,page_num):    # 保存

        # 定义存储路径
        file_path = self.tieba_name+'_'+str(page_num)+'.html'

        with open(file_path,'w') as  f:
            f.write(html)
            print('save success')

    def run(self):
        # 1. 找到ｕｒｌ规律，构造待请求的ｕｒｌ列表
        for url in self.url_list:
        # 2. 拿到ｕｒｌ，发送请求，获取响应
        # 3. 获取ｈｔｍｌ字符串
            html = self.parse_url(url)
        # 4. 保存
            page_num = self.url_list.index(url) # 获取页码数
            self.save_html(html,page_num)
            print(' crawl %s successful'% self.tieba_name)


def main():
    tieba = Tieba('汽车')
    tieba.run()


if __name__ == "__main__":
    main()