# 简介

PyQT构建的两个美观的登陆界面。

# 技术点

- PyQT
- QSS
- QT程序 **DPI相适应**
- QT自定义窗体
- QTdesigner的使用

# 文件说明

- `static` ：静态资源主要是图标和背景
- `login1.ui` ：登陆界面1
- `login2.ui` ：登陆界面2
- `main.py` ：运行入口
- `login.py` ：由ui文件生成的Python代码

# 运行方式

~~~shell
pyuic5 -o login.py <ui文件>  # 生成Python文件
# login.py名字可自定义, 但是需要修改main.py中的引方式
python main.py  # 运行
~~~