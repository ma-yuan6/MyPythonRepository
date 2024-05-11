# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow
from qfluentwidgets import FluentIcon as FLI  # 图标

from settings import QQ
from UI import TrainWidget, ExploreWidget


class APPWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        # create sub interface
        self.train_terface = TrainWidget('Interface1', self)
        self.export_interface = ExploreWidget('Interface2', self)
        self.export_interface.brother = self.train_terface  # 需要将训练窗口赋值给导出窗口，怎样才能获取他的值
        # self.videoInterface = Widget('Interface3', self)
        # self.libraryInterface = Widget('Interface4', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.train_terface, FLI.HOME, '训练', FLI.HOME_FILL)
        self.addSubInterface(self.export_interface, FLI.APPLICATION, '导出')
        # self.addSubInterface(self.videoInterface, FLI.VIDEO, '视频')

        # self.addSubInterface(self.libraryInterface, FLI.BOOK_SHELF, '库', FLI.LIBRARY_FILL,
        #                      NavigationItemPosition.BOTTOM)
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FLI.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.setCurrentItem(self.train_terface.objectName())

    def initWindow(self):
        self.resize(900, 600)
        self.setWindowIcon(QIcon('static/logo.jpg'))
        self.setWindowTitle('水务数据修复智慧应用平台')

        desktop = QApplication.desktop().availableGeometry()  # 屏幕描述
        w, h = desktop.width(), desktop.height()  # 获取屏幕宽高
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)  # 移动到屏幕中心

    def showMessageBox(self):  # 帮助按钮回调函数
        w = MessageBox(
            '联系作者🥰',
            f'您的满意是我们的首要任务，我会认真对待您的反馈。感谢您的耐心等待，\n如果您有任何进一步的疑虑，我们将随时为您提供支持。\n\nQQ:{QQ}',
            self
        )
        w.yesButton.setText('确定')
        w.cancelButton.setText('取消')

        if w.exec():  # 点击确定跳转邮箱
            QDesktopServices.openUrl(QUrl(f'mailto:{QQ}@qq.com'))


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = APPWindow()
    w.show()
    app.exec_()
