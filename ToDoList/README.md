# 简介

用于打卡算法的一个简单小网页，基于遗忘曲线反复复习。此项目可以简单了解 **Falsk 运行流程**  和 **前后端不分离开发方式** 。

# 技术

- Jquery
- Flask
- pymysql
- 正则表达式

# 运行

1. `conf/app_config.py` 下配置 MYSQL 和 MarkDown 文件位置
2.  运行 `sql/build_database.sql` 创建数据库、表
3.  运行 `update_script.py` 
4. 运行 `app.py`