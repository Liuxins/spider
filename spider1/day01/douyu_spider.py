from selenium import webdriver
import json
import time
import requests


class DouYuSpider(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS()

        # time.sleep(3)
        # 请求首页
        self.driver.get("https://www.douyu.com/directory/all")

    def get_content(self):
        time.sleep(3)
        self.driver.save_screenshot("斗鱼.png")
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        # print("========")
        # print(li_list)
        content_list = []
        for i in li_list:

            item = {}
            # 获取房间图片
            item["img"] = i.find_element_by_xpath("./a//img").get_attribute("data-original")
            print(item['img'],'===================')
            # 获取标题
            item["title"] = i.find_element_by_xpath("./a").get_attribute("title")
            # 获取标签
            item["tag"] = i.find_element_by_xpath("./a/div/div/span").text
            # 房间名
            item["room_name"] = i.find_element_by_xpath("./a/div/p/span[1]").text
            # 观看人数
            item["num"] = i.find_element_by_xpath("./a/div/p/span[2]").text
            # print("----")
            # print(item)
            content_list.append(item)
        return content_list

    def parse_img(self, url):
        img = requests.get(url)
        print(img.content,'------------------------------------------')
        return img.content

    def save_img(self, content_list, i):
        for con in content_list:
            # print(con)
            index = content_list.index(con)
            img_url = con["img"]
            file_path = "J:/爬虫/day 04/douyuimage/第" + str(i) + "页" + str(index) + ".png"
            with open(file_path, "wb") as f:
                img1 = self.parse_img(img_url)
                f.write(img1)
                print("----")

    def run(self):
        # 2 .获取内容
        content_list = self.get_content()
        # print(content_list)
        # 3. 保存内容
        self.save_img(content_list, 1)
        i = 2
        while self.driver.find_element_by_class_name("shark-pager-next"):
            self.driver.find_element_by_class_name("shark-pager-next").click()
            content_list = self.get_content()
            self.save_img(content_list, i)
            i += 1


if __name__ == '__main__':
    dy = DouYuSpider()
    dy.run()