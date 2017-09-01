#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/16 21:29
# @Author  : LiuXin
# @Site    : 
# @File    : 百度贴吧 定名爬取所有内容 包括回复等.py
# @Software: PyCharm
# @version: 1.0
import requests,time,re     # 爬虫请求头
from retrying import retry  # 反复测试
from queue import Queue     # 队列
import threading            # 多线程
from selenium import webdriver  # 这个是浏览器自动测试工具
from lxml import etree  # 导入etree库 将字符串内容北城Element对象  然后利用Element对象用xpath方法
driver = webdriver.PhantomJS()   # 调用隐藏窗口
# driver = webdriver.Firefox()   # 调用显示窗口
# driver.maximize_window() #窗口最大化

class Tieba(object):
    '''1. url设定'''
    def __init__(self,name):
        self.name = name
        self.url = 'https://tieba.baidu.com/mo/q---7E12BBFA82E1A336C8D45C937DB01329:FG=1-sz@320_240,,-2-3-0--2/m?kw={}&lp=7202&referer=tieba.baidu.com&pn=0&'.format(self.name)
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        self.url_queue = Queue() # url 对列表
        self.html_queue = Queue()   # 获取到的html对列表
        self.content_list_queue = Queue()   # 信息对列表
        print(self.url)
    '''发送请求 ，获取响应'''
    @retry(stop_max_attempt_number=3)
    def _parse_url(self,url):
        response = requests.get(url,headers= self.headers,timeout=5,proxies=None)
        assert response.status_code==200
        return etree.HTML(response.content) # 返回element对象 所以不用decode 方面后续用对象操作


    def parse_url(self,url):
        try:
            html = self._parse_url(url)
        except Exception as e:
            html=None
        return html


    def get_content(self,html):
        #                contains只要包含属性的都能取 帖子内容都包含tl
        div_list = html.xpath("//div/ul/li[contains(@class,'tl_shadow')]")  # 首先获取帖子标题及内容 包含class中有tl的

        content_list = []   # 储存所有帖子的列表
        for div in div_list:
            # print(div)
            content = {}    # 存储单个帖子的列表
            content['title'] = div.xpath("./a/div/span/text()")[0] if len(div.xpath("./a/div/span/text()")) > 0 else None
            content['title_href'] = "https://wapp.baidu.com"+ div.xpath("./a/@href")[0]  if len(div.xpath("./a/@href"))  > 0 else None     # 获取帖子链接
            last_answerer= div.xpath("./a/div/div/span[1]/text()")[0].lstrip()  if len(div.xpath("./a/div/div/span[1]/text()"))  > 0 else None  # 去除左边空白字符
            content['last_answerer'] = last_answerer    # 最后回复者
            content['last_answerer_time'] = div.xpath("./a/div/div/span[2]/text()")[0]  if len(div.xpath("./a/div/div/span[2]/text()")) > 0 else None   # 最后回复者的时间
            content_list.append(content)

        return content_list

    def save_title_content(self,content_list):      # 保存封面标题
        self.name =  re.match(r'\S*',self.name).group()
        with open('J:/爬虫/day 04/tieba/tiebainfo/'+self.name+'.txt',"w", encoding="utf8")as f:
            for content in content_list:
                if content['title']:
                    title = content['title']+"   ；   "
                    f.write(title)
                if content['title_href']:
                    title_href = content['title_href']+"   ；   "
                    f.write(title_href)
                if content['last_answerer']:
                    last_answerer = content['last_answerer']+"   ；   "
                    f.write(last_answerer)
                if content['last_answerer_time']:
                    last_answerer_time = content['last_answerer_time']+"   ；   "
                    f.write(last_answerer_time)
                f.write('\n')
                print('标题',content['title'],'抓取成功')

    @retry(stop_max_attempt_number=5)
    def get_img_list(self, html): #获取图片
        img_list = html.xpath("//img[@class='BDE_Image']/@src")
        # 也可以用这种方法找到图片
        img_response_list = []
        temp_img_response_list=[requests.utils.unquote(i).split('src=')[-1] for i in img_list]

        for img in temp_img_response_list:
            img_response = requests.get(img,timeout=5).content
            img_response_list.append(img_response)

        # 第二种办法也可以直接更改尺寸找到图片
        # for img in img_list:
        #     img_url = img.replace(img[43:56],'size=b2000_2000')
        #     img_response = requests.get(img_url)
        #     img_content = img_response.content
        #     img_response_list.append(img_content)     #获取图片 改变图片尺寸

        return img_response_list

    def save_img_content(self,img_list,datail_title):
        i = 1
        datail_title =  re.match(r'\S*',datail_title).group()
        for img in img_list:
            with open('J:/爬虫\day 04/tieba/tiabaimage/'+datail_title+str(i)+'.png',"ab")as f:
                f.write(img)
                print('图片%d保存成功'%i)
                i+=1


    def get_answer_content(self,detail_html):
        content_div = detail_html.xpath("//div[@class='i']")
        next_url = detail_html.xpath("//a[text()='下一页']/@href")
        if len(next_url) > 0:
            next_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/" + next_url[0]
        else:
            next_url = None
        print(next_url)
        # print(content_div)
        answer_content=[]
        for detail in content_div:
            answers = {}
            # xpath  返回的都是列表 故尾部加[0]
            answers['answser'] = detail.xpath("./table/tr/td[1]/span/a//text()")[0]
            answers['answer_time'] = detail.xpath("./table/tr/td[1]/span[@class='b']//text()")[0]
            answers['text'] = detail.xpath("./text()")[0]
            answer_content.append(answers)

        return answer_content,next_url

    def save_answer_info_text(self,answer_content,datail_title):
        answer_title_name = datail_title+'.txt'
        answer_title_name = re.match(r'\S*', answer_title_name).group()
        with open('J:/爬虫\day 04/tieba/tiebainfo/'+answer_title_name,"a+", encoding="utf8")as f:
            for content in answer_content:
                answer = content['answser'] + "   ；   "
                f.write(answer)
                answer_time = content['answer_time'] + "   ；   "
                f.write(answer_time)
                text = content['text'] + "   ；   "
                f.write(text)
                f.write('\n')
            print(answer_title_name,'保存成功')

    def run(self):

        # 处理线程
        # thread_list=[]

        # 1. 定初始url
        # #   1.1 用浏览器自动全部获取先 等加载完后吧
        # driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")      # 使用chrome浏览器
        # # driver = webdriver.Firefox("D:\Program Files\Mozilla Firefox\geckodriver.exe")
        # # driver = webdriver.PhantomJS()  # 这是使用不打开的窗口
        # # driver.maximize_window(self)  # 窗口根据浏览器最大化
        # driver.set_window_size(1200,900)   # 这是设置浏览器的大小的
        # # driver.set_window_size(1200,90)
        # driver.get(self.url)  # 访问url地址及其内容
        # # driver.save_screenshot("./当前窗口截屏.png")  #截屏保存图片的
        # while True:
        #     try:
        #         print(driver.page_source)   # 查看当前网页的源码
        #         print(driver.get_cookie())  # 查看当前登陆的cookie
        #         driver.find_element_by_class_name("j_pager_next pager_btn pager_next").click()      # 找到元素点击加载
        #         print(driver.current_url)       # 打印当前窗口的url
        #     except Exception as e:
        #         break
        # 2. 发送请求，获取响应
        html=self.parse_url(self.url)
        driver.get(self.url)    # 点击打开初始窗口
        print('正在加载所有页面 请稍后')
        time.sleep(1)


        # href = driver.find_element_by_link_text("点击加载下一页>").get_attribute("href")
        # print(href)
        # driver.find_element_by_class_name("j_pager_next pager_btn pager_next").click()  # 找到元素,点击
        while True:
            try:
                el_list = driver.find_elements_by_css_selector('li[class="tl_shadow"] > a')
                print(len(el_list))
                for el in el_list:
                    print(el.get_attribute('href'))
                    self.url_queue.put(el.get_attribute('href'))

                driver.find_element_by_css_selector("#tlist > a").click()  # 找到元素,点击（这是点击加载下一页）
                time.sleep(1)
            except Exception as e:
                driver.quit()
                break
                print('加载所有页面成功')


        # 3. 提取数据
        if html is not None:
            content_list = self.get_content(html)
            # 先保存 标题信息吧
            self.save_title_content(content_list)
            for content in content_list:
                next_url = content['title_href']  # 具体详情页的请求 用这个变量表示
                print(next_url)
                datail_title = content['title']
                while next_url is not None:
                    detail_html = self.parse_url(next_url)    # 获取每个帖子内的内容
                    # 提取图片 回复 回复时间 回复人 下一页等
                    answer_content,next_url = self.get_answer_content(detail_html)
                    # 保存回复消息
                    self.save_answer_info_text(answer_content,datail_title)
                    # 获取图片
                    content["img_list"] = self.get_img_list(detail_html)
                    if content['img_list'] is not None:
                        # 保存图片
                        self.save_img_content(content['img_list'],datail_title)

                        # driver.find_element_by_id("kw").send_keys("传智播客")
                        # driver.find_element_by_id("su").click()  # 找到元素,点击
                    # 5.提取图片


        # 5. 持续循环自动下一步访问
def main():
    name = input('请输入需要爬取的百度贴吧名》》》》》》')

    tieba = Tieba(name)
    tieba.run()


if __name__ == "__main__":
    main()


# j_pager_next pager_btn pager_next