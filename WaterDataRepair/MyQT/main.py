import sys
import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import qrcode
from UI import LoginUI
from MyQT.app import APPWindow


class LoginWindow(QMainWindow, LoginUI):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明
        self.ui.btn_qq.clicked.connect(self.pbt_qqorwx_clicked)
        self.ui.btn_wx.clicked.connect(self.pbt_qqorwx_clicked)
        self.ui.btn_login.clicked.connect(self.btn_login_clicked)

    def btn_login_clicked(self):
        username = self.ui.led_username.text().strip()
        password = self.ui.led_password.text().strip()
        if username == 'admin' and password == '123':
            app = APPWindow()  # 创建主窗口
            app.show()  # 显示主窗口
            self.close()  # 关闭登录窗口

    def pbt_qqorwx_clicked(self):
        str = ""
        for i in range(8):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        img = qrcode.make(str)
        img.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.flag = True
            self.position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.flag:
            self.move(mouse_event.globalPos() - self.position)
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.flag = False


if __name__ == "__main__":
    # 设置高DPI缩放因子的四舍五入策略为PassThrough，即将缩放因子的计算结果直接传递给底层窗口系统，不做四舍五入处理。
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # 启用高DPI缩放，使得QApplication能够根据系统的DPI设置自动调整界面元素的大小。
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # 启用高DPI pixmap，使得QApplication在使用图像时能够根据系统的DPI设置自动选择合适的图像版本，以保证在高DPI屏幕上显示清晰。
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    # 目的是为了使Qt应用程序能够正确地在高DPI屏幕上显示，确保界面元素的大小和图像的清晰度与屏幕DPI相适应。
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
