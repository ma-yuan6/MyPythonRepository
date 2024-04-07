# 简介

分别数据分析、python、数据挖掘、大数据、算法为关键词，爬取智联招聘浙江各个市的招聘信息并分析。

# 技术点

- Pandas
- selenium
- selenium 如何让读取本地登录信息

# 文件说明

1. `get_data/get_city_code.py` ：获取城市对应的code以拼接请求地址
2. `get_data/get_job_informations.py` ：获取职位信息
3. `get_data/merge_and_processed.py` ：合并数据
4. `get_data/settings.py` ：配置项（需要修改）
5. `get_data/utils.py` ：工具函数
6. `.ipynb` ：结尾的均为数据分析