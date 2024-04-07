#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/17 21:10
# @File    : mergerAll.py

from pathlib import Path
import shutil
import pandas as pd

df1 = pd.read_excel('platform1/platform1_all.xlsx')
df2 = pd.read_excel('platform2/platform2_all.xlsx')
df3 = pd.read_excel('platform3/platform3_all.xlsx')

df1['来源'] = 1
df2['来源'] = 2
df3['来源'] = 3

dir_list = list(Path(__file__).parent.glob('platform*'))
if not Path(__file__).parent.joinpath('all').exists():
    Path(__file__).parent.joinpath('all').mkdir()

for dir in dir_list:
    file_list = dir.glob('platform*')
    for file in file_list:
        shutil.copy(file, Path(__file__).parent.joinpath('all'))

df_all = pd.concat([df3, df2, df1])
df_all.to_excel('QT/all.xlsx', index=False)
df_all.to_excel('all/all.xlsx', index=False)
