#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/13 14:04
# @File    : getTopic.py

import os
import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import USER_NAME, PASSWORD, URL, DIR


def show_pointer(element: object):
    """
    给传进来的元素增加边框，方便查看当前正在操作的元素
    :param element:
    :return: None
    """
    driver.execute_script(
        "arguments[0].setAttribute('style', arguments[1]);",
        element,
        "border: 2px solid red;"
    )
    time.sleep(1)


def get_topic(order: int, les: object):
    """
    点击小节，判断是否已经完成题目，如果完成获取题目及答案，否则返回False
    :param order: 小节序号
    :param les: 小节按钮
    :return: True 或 False
    """
    show_pointer(les)
    lesson_title = les.text
    driver.execute_script('arguments[0].click();', les)  # 点击
    time.sleep(1)

    # 进入题目页面
    ans_btn = driver.find_element(By.CSS_SELECTOR, '#assignBtnContainer > #assignCheckBtn')
    time.sleep(1)
    if ans_btn.get_attribute('style') != 'display: inline-block;':
        print(f'<<{lesson_title}>> 的题目还未完成，暂时还不能爬取！')
        return False
    show_pointer(ans_btn)
    driver.execute_script("arguments[0].click();", ans_btn)
    time.sleep(1)

    # 获取题目及答案
    time.sleep(3)
    topic_el_list = driver.find_elements(By.CSS_SELECTOR, '#testList .topic')
    topic_txt_list = []
    for tel in topic_el_list:
        topic_txt = []
        topic_txt.append(tel.find_element(By.CSS_SELECTOR, '.topic-info').text
                         .replace('\n', '、')
                         .strip()
                         )  # 题目
        topic_txt.append(tel.find_element(By.CSS_SELECTOR, '.r-answer .r-a-number').text.strip())  # 答案
        ans_ul = tel.find_elements(By.CSS_SELECTOR, 'ul li')  # 所有选项
        for li in ans_ul:  # 解析选项
            topic_txt.append(li.text.replace('\n', ' ').strip())
        pprint(topic_txt)
        topic_txt_list.append(topic_txt)

    if not os.path.exists(DIR):
        os.mkdir(DIR)
    order = str(order + 1)
    order = '0' * (3 - len(order)) + order
    with open(f'{DIR}/{order + "-" + lesson_title}.txt', 'w', encoding='utf-8') as f:
        for t in topic_txt_list:
            f.write('    '.join(t))
            f.write('\n')
    return True


driver = webdriver.Chrome()
driver.get(URL)

# 登陆页面
username_input = driver.find_element(By.CSS_SELECTOR, '#input1')
show_pointer(username_input)
username_input.send_keys(USER_NAME)  # 输入用户名
time.sleep(1)

password_input = driver.find_element(By.CSS_SELECTOR, '#input2')
show_pointer(password_input)
password_input.send_keys(PASSWORD)  # 输入密码
time.sleep(1)

login_btn = driver.find_element(By.CSS_SELECTOR, '#login_bt1')  # 获取登录按钮
show_pointer(login_btn)
driver.execute_script("arguments[0].click();", login_btn)  # 点击登录
time.sleep(1)

# 选择页面
card = driver.find_element(By.CSS_SELECTOR, '#main_content_box > div:nth-child(1) > a')
show_pointer(card)
card.click()  # 点击跳转到主页面
time.sleep(1)

# 主页面
tag = driver.find_element(By.CSS_SELECTOR, '#obj > #btn2 > a')
show_pointer(tag)
driver.execute_script("arguments[0].click();", tag)  # 点击跳转课程页面
time.sleep(1)

# 选择所有小节
lesson_el_list = driver.find_elements(By.CSS_SELECTOR, '.content-left > .firLevel > .secLevel > .secLevelItem')
# 遍历所有课
for el in range(len(lesson_el_list)):
    content_left = driver.find_element(By.CSS_SELECTOR, '.content-left')
    driver.execute_script("arguments[0].scrollTop=arguments[1];", content_left, 45 * el)
    lesson = driver.find_elements(By.CSS_SELECTOR, '.content-left > .firLevel > .secLevel > .secLevelItem')[el]
    print(lesson.text.center(80, '='))
    if get_topic(el, lesson):  # 如果题目未完成，则跳过
        driver.back()  # 返回上一页, 退出答题页
        time.sleep(1)

input()  # 用于阻塞程序，使得爬取完成后不关闭浏览器
