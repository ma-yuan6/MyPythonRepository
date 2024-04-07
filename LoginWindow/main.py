import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
from login import Ui_login
import qrcode


class loginWindow(QMainWindow, Ui_login):
    def __init__(self):
        super(loginWindow, self).__init__()
        self.ui = Ui_login()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 透明
        self.ui.btn_qq.clicked.connect(self.pbt_qqorwx_clicked)
        self.ui.btn_wx.clicked.connect(self.pbt_qqorwx_clicked)
        self.ui.btn_login.clicked.connect(self.btn_login_clicked)

    def btn_login_clicked(self):
        id1 = self.ui.led_username.text().strip()
        password = self.ui.led_password.text().strip()
        if id1 == 'ma' and password == '123':
            print('登录')

    def pbt_qqorwx_clicked(self):
        str = ""
        for i in range(8):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        img = qrcode.make(str)
        img.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    window = loginWindow()
    window.show()
    sys.exit(app.exec())
