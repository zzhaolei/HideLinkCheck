#!/usr/bin/python
# -*- coding:utf-8 -*-
'''需要安装selenium，使用chromedriver，需要先安装chrome浏览器'''

import re
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_domain(domain):
    pro, rest = urllib.splittype(domain)
    domain, rest = urllib.splithost(rest)
    return ".".join(domain.split(".")[1:])


node_list = []
url_list = []
hide_list = []

try:
    options = Options()
    # 使用chrome的无界面模式
    options.add_argument("--headless")
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"')
    driver = webdriver.Chrome(chrome_options=options)
    domain = "https://www.baidu.com/"
    driver.get(domain)

    # 获取所有a标签，返回列表
    all_node = driver.find_elements_by_tag_name("a")

    for a in all_node:
        # 判断所有节点是否有属性href或者src
        url = a.get_attribute("href") or a.get_attribute('src')
        if url is None:
            continue

        # 如果有属性，判断是否是http协议
        http_match = re.search(r"^(http).*", url)

        # 能从node中拿到url
        if http_match:
            node_list.append(a)
            url_list.append(url)

    domain = get_domain(domain)
    # 判断URL链接的域名和传进来的参数是否相同
    i = 0
    while i < len(url_list):
        if domain == get_domain(url_list[i]):
            node_list.pop(i)
            url_list.pop(i)
            # 删除后列表元素会前移一位
            i -= 1
        i += 1

    for i in node_list:
        ''''''
        # 元素是否显示
        if not i.is_displayed():
            hide_list.append(i)
        else:
            value = i.value_of_css_property("font-size")
            # 将除数字外的字符清除，一般是px，将字符串转换为整形
            value = int(re.sub(r"[a-zA-Z]", "", value))
            if value < 2:
                hide_list.append(i)

            # 检测visibility属性 visible:hidden
            value = i.value_of_css_property('visibility')
            if value == "hidden":
                hide_list.append(i)

            # 检测color属性{rgba(255, 255, 255, 1)}白色
            color = i.value_of_css_property('color')
            if color == "rgba(255, 255, 255, 1)":
                hide_list.append(i)

            # 检测opacity属性,透明度0.2以下即认为是暗链
            value = i.value_of_css_property('opacity')
            opacity = float(value)
            if opacity <= 0.2:
                hide_list.append(i)

            # 检测display属性 none,inline
            value = i.value_of_css_property('display')
            if value == 'none':
                hide_list.append(i)

    marquee = driver.find_elements_by_tag_name("marquee")
    for i in marquee:
        if not i.is_displayed():
            hide_list.append(i.find_element_by_tag_name("a"))

    meta = driver.find_elements_by_tag_name("meta")
    for i in meta:
        if i.get_attribute("url"):
            hide_list.append(i)

    iframe = driver.find_elements_by_tag_name("iframe")
    for i in iframe:
        hide_list.append(i)

except Exception as e:
    pass
finally:
    test_list = []
    for i in hide_list:
        if i.get_attribute('href'):
            test_list.append(i.get_attribute("href"))
        elif i.get_attribute("src"):
            test_list.append(i.get_attribute("src"))
        elif i.get_attribute('url'):
            test_list.append(i.get_attribute('url'))
    hide_list = test_list
    driver.quit()

