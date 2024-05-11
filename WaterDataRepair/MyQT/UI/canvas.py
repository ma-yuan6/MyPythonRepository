#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2024/4/4 22:57
# @File    : canvas.py

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

matplotlib.use('Qt5Agg')
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题


class FigureCanvas(FigureCanvasQTAgg):
    """
    创建一个画布类，并把画布放到FigureCanvasQTAgg
    """

    def __init__(self, width=10, heigh=10, dpi=100):
        self.figs = plt.Figure(figsize=(width, heigh), dpi=dpi)
        super(FigureCanvas, self).__init__(self.figs)  # 在父类种激活self.fig，
        self.axes = None

    def draw_box(self, t):
        """
        用清除画布刷新的方法绘图
        :return:
        """
        self.figs.clf()  # 清理画布，这里是clf()
        self.axes = self.figs.add_subplot(111)  # 添加绘图区
        quartiles = self.axes.boxplot(t, showmeans=True)
        self.figs.suptitle('原始数据箱线图')
        self.figs.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.figs.canvas.flush_events()  # 画布刷新self.figs.canvas
        return quartiles

    def draw_line(self, tick, rel, pre):
        """
        用清除画布刷新的方法绘图
        :return:
        """
        self.figs.clf()  # 清除绘图区
        self.axes = self.figs.add_subplot(111)  # 添加绘图区
        self.axes.plot(tick, rel)
        self.axes.plot(pre)
        self.axes.legend(['真实值', '预测值'])
        # self.axes.set_xticklabels(tick[::20], rotation=45)
        self.axes.set_xticks([i for i in range(0, len(tick), 20)])  # 设置刻度
        self.axes.set_xticklabels(tick[::20], rotation=30, fontsize='small')  # 设置刻度标签
        self.figs.suptitle('GRU 网络预测结果')
        self.figs.canvas.draw()  # 这里注意是画布重绘，self.figs.canvas
        self.figs.canvas.flush_events()  # 画布刷新self.figs.canvas
