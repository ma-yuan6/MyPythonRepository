#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/26 16:08
# @File    : merge.py

import re
from pathlib import Path
import pandas as pd
from utils import handel_city_name


def handel_salary_inner(salary_str):
    """
        300-400/天
        400-500/周
        6千-7.2千
        6千-1.2万
        1万-1.2万
    :return:
    """
    salary_li = re.findall('(\d+\.?\d*)-(\d+\.?\d*)/(.)', salary_str)  # 天、周
    if salary_li:
        if salary_li[0][2] == '天':
            min_salary = float(salary_li[0][0]) * 21.75
            max_salary = float(salary_li[0][1]) * 21.75
            return min_salary, max_salary
        elif salary_li[0][2] == '周':
            min_salary = float(salary_li[0][0]) / 5 * 21.75
            max_salary = float(salary_li[0][1]) / 5 * 21.75
            return min_salary, max_salary
    salary_li = re.findall('(\d+\.?\d*)千-(\d+\.?\d*)千', salary_str)  # 千/千
    if salary_li:
        min_salary = float(salary_li[0][0]) * 1000
        max_salary = float(salary_li[0][1]) * 1000
        return min_salary, max_salary
    salary_li = re.findall('(\d+\.?\d*)千-(\d+\.?\d*)万', salary_str)  # 千/万
    if salary_li:
        min_salary = float(salary_li[0][0]) * 1000
        max_salary = float(salary_li[0][1]) * 10000
        return min_salary, max_salary
    salary_li = re.findall('(\d+\.?\d*)万-(\d+\.?\d*)万', salary_str)  # 万/万
    if salary_li:
        min_salary = float(salary_li[0][0]) * 10000
        max_salary = float(salary_li[0][1]) * 10000
        if max_salary > 10 * 10000:  # 年薪变月薪
            max_salary = max_salary / 12
            min_salary = min_salary / 12
        return min_salary, max_salary


def handel_salary(salary_str):
    salary_str = salary_str.replace('元', '')
    salary_str = salary_str.replace('/月', '')
    if salary_str == '面议':
        return None, None
    if '-' in salary_str:
        if salary_str.endswith('薪'):
            salary_with_xing = salary_str.split(' · ')
            times = float(salary_with_xing[1].strip('薪'))
            min_salary, max_salary = handel_salary_inner(salary_with_xing[0])
            min_salary = min_salary / 12 * times
            max_salary = max_salary / 12 * times
            return min_salary, max_salary
        else:
            min_salary, max_salary = handel_salary_inner(salary_str)
            return min_salary, max_salary
    else:
        min_salary, unit = salary_str.split('/')
        if unit == '天':
            min_salary = float(min_salary) * 21.75
        if unit == '时':
            min_salary = float(min_salary) * 8 * 21.75
        max_salary = min_salary
        return min_salary, max_salary


file_list = Path('../data').iterdir()

# 合并所有数据
all_df = pd.DataFrame()
for file in file_list:
    if file.suffix == '.csv':
        df = pd.read_csv(file)
        df['市'] = file.name.split('-')[0]  # 市
        df['关键字'] = file.name.split('-')[1]
        df['工作地点'] = df['工作地点'].apply(lambda x: handel_city_name(x)[1])  # 县
    else:
        continue
    if all_df.empty:
        all_df = df
    else:
        all_df = pd.concat([all_df, df], axis=0)
all_df['经验要求'] = all_df['经验要求'].str.replace('无经验', '经验不限')  # 将无经验替换为经验不限

# 处理工资
all_df['最低工资'] = all_df['薪水'].apply(lambda x: handel_salary(x)[0])
all_df['最高工资'] = all_df['薪水'].apply(lambda x: handel_salary(x)[1])
all_df['最低工资'].fillna(all_df['最低工资'].mean(), inplace=True)
all_df['最高工资'].fillna(all_df['最高工资'].mean(), inplace=True)
print(all_df['最低工资'].mean())
print(all_df['最高工资'].mean())

all_df.to_csv('../data/all_data.csv', index=False, encoding='gbk')

# 去重
all_df['职位标识'] = all_df[['职位名称', '公司名称']].apply(lambda x: '-'.join(x.dropna().astype(str)), axis=1)
unique_df = all_df.groupby('职位标识').first()
unique_df.reset_index(inplace=True)
del unique_df['关键字']
del unique_df['职位标识']
unique_df.to_csv('..data/unique_data.csv', index=False, encoding='gbk')
