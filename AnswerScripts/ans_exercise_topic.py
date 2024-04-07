# !/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/13 14:04
# @File    : ansTopic.py

import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from fuzzywuzzy.fuzz import ratio
from settings import USER_NAME, PASSWORD, URL, DIR

TOPICS_DF = pd.read_excel(f'{DIR}/{DIR}_all.xlsx')


def get_ans(topic: str):
    """
    根据传来的题目，从题库中找到对应的答案
    :param topic: 题目
    :return: ans：对应选项的下标, 从0开始，元组类型
    """
    ans = None
    for t in TOPICS_DF.itertuples():
        max_rat = 0
        rat = ratio(topic, t[2])
        if rat > 80 and rat > max_rat:  # 只要匹配度大于80就打印
            max_rat = rat
            pprint(topic)
            ans = t[3]  # 注意第一个元素是 index
            print('答案->', ans)
            pprint(list(t))
            print()
            ans = tuple(map(lambda x: {'A': 0, 'B': 1, 'C': 2, 'D': 3}[x], ans))
    return ans  # 返回最符合题目的答案
    # return None


def answer(topic_card):
    anwer_btn = topic_card.find_element(By.CSS_SELECTOR, '.taskContent #assignAnswerBtn')
    # if anwer_btn.get_attribute('style') != 'display: inline-block;':
    #     return False
    show_pointer(anwer_btn)
    driver.execute_script("arguments[0].click();", anwer_btn)  # 点击进入答题界面
    time.sleep(1)
    test_el_list = driver.find_elements(By.CSS_SELECTOR, '#testList .topic')  # 找到所有题目
    for tes in test_el_list:
        tes_str = (tes.find_element(By.CSS_SELECTOR, '.topic-info').text
                   .replace('\n', '、')
                   .strip().replace(' ', '')
                   )
        ans = get_ans(tes_str)  # 获取答案
        if not ans:
            continue


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
    topic_card = driver.find_elements(By.CSS_SELECTOR, '.firLevel .secLevel .secLevelItem')[i]  # 获取每个题目的卡片
    topic_title = topic_card.find_element(By.CSS_SELECTOR, '#assignArticleTitle').text  # 获取题目标题
    print(topic_title.center(70, '='))
    show_pointer(topic_card)
    answer(topic_card)  # 答每个卡片对应的题
    time.sleep(1)
    driver.back()
    time.sleep(1)

input()
