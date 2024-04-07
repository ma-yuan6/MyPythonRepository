# !/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/13 14:04
# @File    : ansTopic.py

import os
import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from settings import USER_NAME, PASSWORD, URL, DIR

TOPICS_DF = pd.read_excel(f'{DIR}/{DIR}_all.xlsx')


def get_topic(order: int, ex_card: object):
    """
    判断练习是否已经完成，如果完成获取题目及答案，否则返回False
    :param order: 练习序号
    :param ex_card: 练习卡
    :return: True 或 False
    """
    order = order + 39
    time.sleep(1)
    ex_title = ex_card.find_element(By.CSS_SELECTOR, '#assignArticleTitle').text  # 获取练习标题
    print(ex_title.center(70, '='))

    # 进入题目页面
    try:
        ans_btn = ex_card.find_element(By.CSS_SELECTOR, '#assignBtnContainer #assignCheckBtn')
    except:
        return False
    show_pointer(ans_btn)
    driver.execute_script("arguments[0].click();", ans_btn)
    time.sleep(1)

    # 获取题目及答案
    time.sleep(3)
    topic_el_list = driver.find_elements(By.CSS_SELECTOR, '#testList .topic')
    topic_txt_list = []
    for tel in topic_el_list:
        test = []
        test.append(tel.find_element(By.CSS_SELECTOR, '.topic-info').text
                    .replace('\n', '、')
                    .strip()
                    )  # 题目
        test.append(tel.find_element(By.CSS_SELECTOR, '.r-answer .r-a-number').text.strip())  # 答案
        ans_ul = tel.find_elements(By.CSS_SELECTOR, 'ul li')  # 所有选项
        for li in ans_ul:  # 解析选项
            test.append(li.text.replace('\n', ' ').strip())
        pprint(test)
        topic_txt_list.append(test)

    if not os.path.exists(DIR):
        os.mkdir(DIR)
    order = str(order + 1)
    order = '0' * (3 - len(order)) + order
    with open(f'{DIR}/{order + "-" + ex_title}.txt', 'w', encoding='utf-8') as f:
        for t in topic_txt_list:
            f.write('    '.join(t))
            f.write('\n')
    return True


def show_pointer(element):
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
tag = driver.find_element(By.CSS_SELECTOR, '#obj > #btn4 > a')
show_pointer(tag)
driver.execute_script("arguments[0].click();", tag)  # 点击跳转课程页面
time.sleep(1)

topic_el_list = driver.find_elements(By.CSS_SELECTOR, '.firLevel .secLevel .secLevelItem')
for i in range(len(topic_el_list)):
    ex_card = driver.find_elements(By.CSS_SELECTOR, '.firLevel .secLevel .secLevelItem')[i]  # 获取每个题目的卡片
    if get_topic(i, ex_card):
        driver.back()
        time.sleep(1)

input()
