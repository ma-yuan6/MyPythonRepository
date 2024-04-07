#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/26 11:13
# @File    : get_city_code.py

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from pandas import DataFrame
from utils import handel_city_name

city_item_list = []
driver = Chrome()

# 获取城市编码
for city_code in range(653, 664):
    driver.get(f'https://sou.zhaopin.com/?jl={city_code}&kw=python')
    city_name_selecter = '.iteminfo__line2__jobdesc__demand > li:nth-child(1)'
    city_name_el = driver.find_element(By.CSS_SELECTOR, city_name_selecter)
    city_name = handel_city_name(city_name_el.text)[0]
    print(city_name)
    city_item_list.append((city_code, city_name))

DataFrame(city_item_list).to_csv('city_code.csv', header=['城市编码', '城市名称'], index=False)
