#!/usr/bin/env python
# coding: utf-8
# @Author  : MJX
# @Time    : 2023/12/17 12:21
# @File    : main.py

import sys
from io import StringIO
from pprint import pprint
from fuzzywuzzy.fuzz import ratio
from pandas import read_excel
from PySide6 import QtCore, QtWidgets, QtGui

TOPICS_DF = read_excel('all.xlsx')
TOPICS_DF['题目'] = TOPICS_DF['题目'].apply(lambda x: x[5:])

MyAreaStyle = '''
    QScrollArea {
        background-color: rgba(54, 62, 68, 0.8);
        border: 0px;
        border-radius: 0px;
    }
'''


def get_ans(topic: str):
    all_ans = []
    for t in TOPICS_DF.itertuples():
        rat = ratio(topic, t[2])
        if rat > 80:  # 只要匹配度大于80就输出
            ans_io = StringIO()
            pprint(list(t), stream=ans_io)
            str_ans = ans_io.getvalue()
            all_ans.append(str_ans)
    return all_ans


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('答案查询')
        # 输入框
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText('在此输入题目')
        self.input.returnPressed.connect(self.magic)
        self.input.setFont(QtGui.QFont('Microsoft YaHei', 11))
        self.input.setTextMargins(10, 0, 0, 0)
        self.input.setFixedHeight(40)

        # 按钮
        self.button = QtWidgets.QPushButton('点击查询答案')
        self.button.setFont(QtGui.QFont('Microsoft YaHei', 12))
        self.button.setFixedHeight(50)

        # 输出框
        self.text = QtWidgets.QLabel('还未输入题目', alignment=QtCore.Qt.AlignCenter)
        self.text.setFont(QtGui.QFont('Microsoft YaHei', 18))
        self.text.adjustSize()

        # 滚动条
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.text)
        self.scroll.setWidgetResizable(True)
        # self.scroll.setStyleSheet(MyAreaStyle)

        # 布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 30, 10, 30)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
        self.setStyleSheet(MyAreaStyle)

    @QtCore.Slot()
    def magic(self):
        if self.input.text():
            ans = get_ans(self.input.text())
            if not ans:
                self.text.setText('题库中不存在该题目')
                return
            txt = ''
            for idx, a in enumerate(ans):
                txt += f'相似题目{idx + 1}'.center(60, '=') + '\n'
                txt += a
                txt += '\n'
            self.text.setText(txt)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
