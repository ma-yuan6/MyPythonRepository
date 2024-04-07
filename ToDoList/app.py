#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/11/4 18:04
# @File    : App.py


from flask import Flask, render_template, request, g
import pymysql

app = Flask(__name__)
app.config.from_pyfile('./conf/app_config.py')


@app.before_request
def before_request():
    # 请求前创建数据连接
    dbconnect = pymysql.connect(**app.config['MYSQL'], port=3306, charset='utf8')
    dbcursor = dbconnect.cursor()
    g.dbconnect = dbconnect  # 将连接对象存储在全局变量，便于后续关闭
    g.dbcursor = dbcursor


@app.after_request
def after_request(response):
    # 请求后关闭数据连接
    g.dbcursor.close()
    g.dbconnect.close()
    return response


def get_all_data():
    # 获取所有数据
    g.dbcursor.execute(
        'SELECT id, title, link, start_time, day_1, \
        day_2, day_4, day_7, day_15, day_30, day_90, day_180 FROM topic')
    data = g.dbcursor.fetchall()  # 获取所有数据, 用于生成表格
    return data


# 用于修改记录
def updta_data(id: str, time: str):
    id = int(id) + 1  # id从 1 开始
    time = int(time)  # 需要用于索引取值
    time_map = ['1', '2', '4', '7', '15', '30', '90', '180']
    sql_update = f"UPDATE topic SET day_{time_map[time]} = 1 - day_{time_map[time]}, \
                time_{time_map[time]} = CURRENT_TIMESTAMP  WHERE id = {id}"
    sql_insert = f"INSERT INTO modified_records VALUES ({id}, CURRENT_TIMESTAMP, '{time_map[time]}')"
    g.dbcursor.execute(sql_update)
    g.dbcursor.execute(sql_insert)
    g.dbconnect.commit()


# 用于表浏览
@app.route('/')
def index():
    all_topics = get_all_data()
    return render_template('table.html', all_topics=all_topics, enumerate=enumerate)


# 用于处理表格更改接口
@app.route('/updata', methods=['GET', 'POST'])
def updata():
    form = request.form
    id = form.get('id')
    time = form.get('time')
    updta_data(id, time)
    return [id, time]


if __name__ == '__main__':
    app.run(**app.config['APP'], debug=False)
