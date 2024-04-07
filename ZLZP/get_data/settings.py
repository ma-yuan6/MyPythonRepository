#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/26 14:59
# @File    : settings.py

from pandas import read_csv

key_words = ['数据分析', 'python', '数据挖掘', '大数据', '算法']

city_code_df = read_csv('city_code.csv')
city_code_dic = dict(city_code_df.itertuples(index=False))

chrom_arg = r'user-data-dir=C:\Users\马\AppData\Local\Google\Chrome\User Data\Default'
# 改为自己的chrome路径
