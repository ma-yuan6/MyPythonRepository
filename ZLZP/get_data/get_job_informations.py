#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/26 13:04
# @File    : get_job_informations.py

import time
import random
import os
from pandas import DataFrame
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from settings import chrom_arg, key_words, city_code_dic


def get_job_tag(job_tag_el):
    """
    从标签列表的 el 中获取标签信息并拼接
    :param job_tag_el:
    :return:
    """
    job_tag_item_el = job_tag_el.find_elements(By.CSS_SELECTOR, '.iteminfo__line3__welfare__item')
    job_tag_str_list = []
    for job_tag_item in job_tag_item_el:
        job_tag_str_list.append(job_tag_item.text)
    return '、'.join(job_tag_str_list)


def get_job_info(job_el):
    """
    从 el 对象里获取职位信息
    :param job_el:
    :return:
    """
    job_name_el = job_el.find_element(By.CSS_SELECTOR, '.iteminfo__line1__jobname > span')
    job_name = job_name_el.get_attribute('title')
    salary = job_el.find_element(By.CSS_SELECTOR, '.iteminfo__line2__jobdesc__salary').text
    location = job_el.find_element(By.CSS_SELECTOR, '.iteminfo__line2__jobdesc__demand > li:nth-child(1)').text
    experience = job_el.find_element(By.CSS_SELECTOR, '.iteminfo__line2__jobdesc__demand > li:nth-child(2)').text
    degree = job_el.find_element(By.CSS_SELECTOR, '.iteminfo__line2__jobdesc__demand > li:nth-child(3)').text
    job_tag_el = job_el.find_element(By.CSS_SELECTOR, '.iteminfo__line3__welfare')
    job_tag = get_job_tag(job_tag_el)
    compname = job_el.find_element(By.CSS_SELECTOR, '.iteminfo__line1__compname > span').text
    detail_url_el = job_el.find_element(By.CSS_SELECTOR, 'a')
    detail_url = detail_url_el.get_attribute('href')
    return [job_name, salary, location, experience, degree, job_tag, compname, detail_url]


def get_data_of_page(page_num, key_word, city_code, city_name):
    """
    获取指定页数的职位信息
    :param page_num:
    :return:
    """
    driver.get(f'https://sou.zhaopin.com/?jl={city_code}&kw={key_word}&p={page_num}')
    job_el_list = driver.find_elements(By.CSS_SELECTOR, '.joblist-box__item')
    if not job_el_list:
        return False
    job_info_list = []
    for job_el in job_el_list:
        job_info = get_job_info(job_el)
        job_info_list.append(job_info)

    header = ['职位名称', '薪水', '工作地点', '经验要求', '学历要求', '职位标签', '公司名称', '详情链接']
    DataFrame(job_info_list).to_csv(f'../data/{city_name}-{key_word}-{page_num}.csv', header=header, index=False)
    return True


if __name__ == '__main__':

    option = Options()
    option.add_argument(chrom_arg)
    # 如果这里没有成功需要在这里登录一下, 然后关闭浏览器再次运行程序
    driver = Chrome(options=option)

    if not os.path.exists('../data'):
        os.mkdir('../data')
    # del city_code_dic[653]
    for key_word in key_words:  # 关键词
        for city_code in city_code_dic:  # 城市
            for page_num in range(1, 30):  # 页数
                if page_num < 10:
                    page_num = '0' + str(page_num)
                else:
                    page_num = str(page_num)
                have_job = get_data_of_page(page_num, key_word, city_code, city_code_dic[city_code])
                print(f'{city_code_dic[city_code]}-{key_word}-{page_num}的职位信息获取成功')
                time.sleep(random.randint(1, 3))
                if not have_job:
                    break

    input()
