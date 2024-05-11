#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2024/4/4 22:53
# @File    : widgets.py

import os
import time
import pandas as pd

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QHBoxLayout, QFileDialog, QWidget, QVBoxLayout
from qfluentwidgets import (SubtitleLabel, PushButton, Flyout, InfoBarIcon, FlyoutAnimationType,
                            LineEdit, CheckBox, StateToolTip)
from qfluentwidgets import FluentIcon as FLI  # 图标
from .canvas import FigureCanvas
from MyQT.arithmetic.gru import prepare_data, train
from MyQT.settings import canvas_style


class ExploreWidget(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)
        # self.brother = TrainWidget()
        self.setup()

    def setup(self):
        """
        初始化UI组件
        :return:
        """
        self.title = SubtitleLabel('导出控制台')
        self.title.resize(200, 50)
        # self.title.setStyleSheet(canvas_style)

        self.select_opthons = QWidget(self)
        self.vbox_layout = QVBoxLayout(self.select_opthons)
        self.picture_check = CheckBox(text='图片')
        self.data_check = CheckBox(text='数据')
        self.description_check = CheckBox(text='数据描述')
        self.picture_check.setChecked(True)
        self.data_check.setChecked(True)
        self.description_check.setChecked(False)
        self.vbox_layout.addWidget(self.picture_check)
        self.vbox_layout.addWidget(self.data_check)
        self.vbox_layout.addWidget(self.description_check)

        self.ouput_button = PushButton(FLI.SAVE.icon(), '导出')
        self.ouput_button.setFixedSize(200, 50)
        self.ouput_button.setCursor(Qt.PointingHandCursor)
        self.ouput_button.clicked.connect(self.export)

        self.vbox_layout = QVBoxLayout(self)
        self.vbox_layout.addWidget(self.title, 0, Qt.AlignCenter)
        self.vbox_layout.addWidget(self.select_opthons, 0, Qt.AlignCenter)
        self.vbox_layout.addWidget(self.ouput_button, 0, Qt.AlignCenter)

    def export(self):
        """
        导出数据
        :return:
        """
        sour_dir = os.path.dirname(self.brother.file_dir)  # 获取导入数据的文件夹
        today_list = time.ctime().split(' ')
        today = '-'.join(today_list[:-2]) + '-' + today_list[-1]  # 只获取到天
        result_dir = sour_dir + '/' + today + '-result'
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)  # 在此文件夹下创建result文件夹
        if self.picture_check.isChecked():
            df = pd.DataFrame({
                '时间': list(self.brother.predata['tick'].values),  # Series格式需要转
                '真实值': list(self.brother.predata['rel']),
                '预测值': list(self.brother.predata['pre'].reshape(-1))  # 二维需要转一维
            })
            df.to_excel(result_dir + '/' + '修复结果.xlsx', index=False)
        if self.data_check.isChecked():
            self.brother.canvas.figs.savefig(result_dir + '/' + '对比图.png')
        if self.description_check.isChecked():
            dic = {}
            dic['均值'] = self.brother.box_ans['means'][0].get_ydata()[0]
            dic['最大值'] = self.brother.box_ans['caps'][1].get_ydata()[0]
            dic['最小值'] = self.brother.box_ans['caps'][0].get_ydata()[0]
            dic['Q1'] = min(self.brother.box_ans['boxes'][0].get_ydata())
            dic['Q3'] = max(self.brother.box_ans['boxes'][0].get_ydata())
            df = pd.DataFrame({'描述': dic.keys(), '值': dic.values()})
            df.to_excel(result_dir + '/' + '数据描述.xlsx', index=False)

            # print(self.brother.box_ans['means'][0].get_ydata()[0], '均值')
            # print(self.brother.box_ans['caps'][1].get_ydata()[0], '最大值')
            # print(self.brother.box_ans['caps'][0].get_ydata()[0], '最小值')
            # print(min(self.brother.box_ans['boxes'][0].get_ydata()), 'Q1')
            # print(max(self.brother.box_ans['boxes'][0].get_ydata()), 'Q3')

            Q1 = min(self.brother.box_ans['boxes'][0].get_ydata())
            Q3 = max(self.brother.box_ans['boxes'][0].get_ydata())
            df = pd.read_csv(self.brother.file_dir)
            df = df[(df.iloc[:, -1] < (Q1 - 1.5 * (Q3 - Q1))) | (df.iloc[:, -1] > (Q3 + 1.5 * (Q3 - Q1)))]
            if df.shape[0]:
                df.to_excel(result_dir + '/' + '异常数据.xlsx', index=False)
            else:
                with open(result_dir + '/' + '异常数据.txt', 'w') as f:
                    f.write('无异常数据!')
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='数据导出成功',
            content=f'文件路径为：{result_dir}',
            target=self.parent(),
            parent=self.parent(),
            isClosable=True,
            aniType=FlyoutAnimationType.FADE_IN
        )


class TrainWidget(QWidget):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)  # 窗口名
        self.epochs = 5
        self.file_dir = ''  # 文件路径
        self.data = None  # 存储数据
        self.box_ans = None
        self.predata = {}  # 存储预测数据和预测结果
        self.setup()

    def setup(self):
        """
        初始化UI组件
        :return:
        """
        self.stateTooltip = None
        self.title = SubtitleLabel('模型训练')  # 标题

        # 中间部分
        self.canvas_box = QWidget()
        self.canvas_box.vbox_layout = QVBoxLayout(self.canvas_box)
        self.canvas = FigureCanvas()  # 画布
        self.canvas_box.vbox_layout.addWidget(self.canvas)
        self.canvas_box.setStyleSheet(canvas_style)

        self.line_edit = LineEdit()
        self.line_edit.setPlaceholderText('训练轮数')  # 设置提示文本
        self.file_selecter_btn = PushButton(FLI.FOLDER.icon(), '点击这里选择文件')  # 选择文件按钮
        self.file_selecter_btn.setCursor(Qt.PointingHandCursor)
        self.file_selecter_btn.clicked.connect(self.select_file)  # 注册点击事件

        self.train_btn = PushButton('点击训练')  # 选择文件按钮
        self.train_btn.setCursor(Qt.PointingHandCursor)
        self.train_btn.clicked.connect(self.plot_)  # 注册点击事件

        # 底部区域用来放置两个按钮
        self.bottum_area = QWidget()
        self.bottum_area.setMaximumHeight(50)
        self.bottum_area.hbox_layout = QHBoxLayout(self.bottum_area)
        self.bottum_area.hbox_layout.addWidget(self.line_edit)
        self.bottum_area.hbox_layout.addWidget(self.file_selecter_btn)
        self.bottum_area.hbox_layout.addWidget(self.train_btn)

        self.vbox_layout = QVBoxLayout(self)
        self.vbox_layout.addWidget(self.title, 0, Qt.AlignCenter)
        # self.vbox_layout.addWidget(self.canvas, 0, Qt.AlignCenter)
        self.vbox_layout.addWidget(self.canvas_box, 0, Qt.AlignCenter)
        self.vbox_layout.addWidget(self.bottum_area, 0, Qt.AlignCenter)

    def showFlyout(self):
        if self.file_dir:
            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title='文件选择成功',
                content=f'文件路径为：{self.file_dir}',
                target=self,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.FADE_IN
            )

    def select_file(self):
        """选择文件获取文件地址"""
        self.file_dir = QFileDialog.getOpenFileName(self, 'Open file', 'd:\\', "files (*.csv *.xlsx)")[0]
        self.data = prepare_data(self.file_dir)
        self.box_ans = self.canvas.draw_box(self.data[4])
        self.showFlyout()

    def plot_(self):
        """训练模型, 绘图"""
        if self.line_edit.text():  # 判断是否输入了训练轮数
            self.epochs = int(self.line_edit.text())
        if self.file_dir:  # 判断是否选择文件了
            self.stateTooltip = StateToolTip('正在训练模型', '客官请耐心等待哦~~', self)
            self.stateTooltip.move(1000, 30)
            self.stateTooltip.show()
            tick, rel, pre = train(self.data[:4], self.data[-1], self.epochs)
            self.stateTooltip.setContent('模型训练完成啦 😆')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
            self.predata = {'tick': tick, 'rel': rel, 'pre': pre}
            self.canvas.draw_line(tick, rel, pre)
        else:
            Flyout.create(
                icon=InfoBarIcon.WARNING,
                title='警告',
                content='请先选择文件',
                target=self,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.FADE_IN
            )
