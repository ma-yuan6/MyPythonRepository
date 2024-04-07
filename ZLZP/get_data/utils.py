#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/26 14:11
# @File    : module.py

def handel_city_name(city_name):
    """
    处理获取的城市字符串
    :param: 类似 杭州-上城 或 杭州 这样的字符串
    :return: 杭州-上城 -> [杭州, 上城] 杭州 -> [杭州, 无]
    """
    if '-' in city_name:
        return city_name.split('-')
    else:
        return [city_name, city_name]
