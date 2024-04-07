#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/11/9 10:04
# @File    : UpdateScript.py
"""
读取并解析Markdow文件，更新数据库。
"""

import re
import pymysql
from conf.app_config import MYSQL
from conf.app_config import FILE_DIR

dbconnect = pymysql.connect(**MYSQL, port=3306, charset='utf8')
dbcursor = dbconnect.cursor()
dbcursor.execute('SELECT COUNT(*) FROM topic')
last_index = dbcursor.fetchall()

with open(FILE_DIR, 'r', encoding='utf-8') as f:
    lines = f.readlines()
all_topics = []
for line in lines:
    # 匹配出大括号和小括号中的值
    topic = re.findall('\[(.*?)\]\((.*?)\)', line, re.M | re.S)
    if topic:
        all_topics.append(topic[0])
now_index = len(all_topics)
print(f'目前的共 {now_index} 个题目')
print(f'数据库中的共存储 {last_index[0][0]} 个题目')
if now_index > last_index[0][0]:
    for i in range(last_index[0][0] + 1, now_index + 1):
        id = i
        title, link, = all_topics[i - 1]
        sql = f"INSERT INTO topic (id, title, link, start_time)\
                    VALUES ({id}, '{title}', '{link}', CURRENT_TIMESTAMP)"
        dbcursor.execute(sql)
# 关闭连接
print('更新完毕')
print(f'共更新 {now_index - last_index[0][0]} 个题目')
dbconnect.commit()
dbcursor.close()
dbconnect.close()
