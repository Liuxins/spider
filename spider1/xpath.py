#coding=utf-8
from lxml import etree

text = ''' <div> <ul> 
        <li class="item-1"><a>first item</a></li> 
        <li class="item-1"><a href="link2.html">second item</a></li> 
        <li class="item-inactive"><a href="link3.html">third item</a></li> 
        <li class="item-1"><a href="link4.html">fourth item</a></li> 
        <li class="item-0"><a href="link5.html">fifth item</a>
        </ul> </div> '''

html = etree.HTML(text) #转化为element对象
# print(html)
# temp = etree.tostring(html).decode()  #把element对象转化为bytes类型
# print(temp)

temp_href = html.xpath("//li[@class='item-1']/a/@href")
print(temp_href)

temp_text = html.xpath("//li[@class='item-1']/a/text()")
print(temp_text)

print("*"*10)
for href in temp_href: #根据索引分组
    temp_dict = dict(
        href = href,
        title = temp_text[temp_href.index(href)]
    )
    # print(temp_dict)

print('6'*30)
temp_herf_text = html.xpath("//li[@class='item-1']/a/@href | //li[@class='item-1']/a/text()")
print(temp_herf_text)

#更好的分组方式
li_list = html.xpath("//li[@class='item-1']")
# print(temp)
for li in li_list:
    temp = {}
    temp["href"] = li.xpath("./a/@href")[0] if len(li.xpath("./a/@href"))>0 else None
    temp["title"] = li.xpath("./a/text()")[0] if len(li.xpath("./a/text()"))>0 else None
    print(temp)


print('6' * 30)
temp_herf_text = html.xpath("//li[@class='item-1']/a/@href | //li[@class='item-1']/a/text()")
print(temp_herf_text)
