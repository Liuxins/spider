#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Time    : 17-8-12 下午7:36
# @Author  : LiuXin
# @Site    :
# @File    : spider2.py
# @Software: PyCharm
import requests


class SpiderTieba(object):
    def __init__(self, sp_name=None):  # 去想要爬取的网站上寻找相关规律
        self.sp_name = sp_name
        # 模拟浏览器批量访问网站
        # 寻找ｕｒｌ规律
        temp_url = 'https://www.qiushibaike.com/text/page/{}/'

        # 模拟浏览器设置
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # 遍历访问一千次上面两个网站　爬取信息
        self.url_list = []
        for i in range(0,100):
            self.url_list.append(temp_url.format(i))
            print(temp_url)
        print(self.url_list)

    def parse_url(self, url):  # 模拟浏览器访问网站　获取内容　并解析
        print('正在获取响应，爬取网页%s' % url)
        response = requests.get(url=url, headers=self.headers)
        return response.content.decode()

    def save_html(self, html, page_num):
        # 保存之前先定义文件路径以及存储的文件名
        file_path = self.sp_name + '_' + str(page_num) + '.html'
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(html)

    def run(self):

        # 1　寻找ｕｒｌ的规律
        # 2. 匹配ｕｒｌ后的ｈｔｍｌ，发送请求获取相应　采用ｇｅｔ方式
        # 3. 获取爬取道的字符串
        for url in self.url_list:
            html = self.parse_url(url)
            # 4. 保存爬取到的内容到指定文件目录和文明名
            page_num = self.url_list.index(url)  # 获取页码数
            self.save_html(html, page_num)
            print('save successful')

        pass


def main():
    spider = SpiderTieba('糗事百科')
    spider.run()
None

if __name__ == "__main__":
    main()