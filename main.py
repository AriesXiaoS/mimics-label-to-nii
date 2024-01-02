

import os,sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

from resource import resource_rc # 必须导入
from view.MainPage import MainPage

from common.config import cfg, APP_NAME, APP_VERSION
from common import signalBus, globalVar

from vtk import vtkOutputWindow
vtkOutputWindow.SetGlobalWarningDisplay(0)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        setThemeColor('#409EFF')
        self.stateTooltip = None
        self.initWindow()
        self.initUi()

        self.initSignals()
        ##
        self.splashScreen.finish()

    def initUi(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.main_page = MainPage()
        self.main_layout.addWidget(self.main_page)

    def initWindow(self):
        self.resize(1280, 720)
        self.setMinimumSize(960,540)
        self.setWindowIcon(QIcon(":/icons/tec.svg"))
        self.setWindowTitle(f'{APP_NAME} - v{APP_VERSION}')
        ## 加载页面 vtk加载需要一点时间
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def initSignals(self):
        signalBus.alertInfo.connect(self.alertInfoBar)
        signalBus.stateTooltip.connect(self.setStateTooltip)


    def alertInfoBar(self, msg:dict):      
        title = msg.get('title', '错误')
        content = msg.get('content', '')
        duration = msg.get('duration', 3000)
        position = msg.get('position', InfoBarPosition.TOP_RIGHT)
        alert_type = msg.get('type', 'error')

        if alert_type == 'error':
            func = InfoBar.error
        elif alert_type == 'warning':
            func = InfoBar.warning
        elif alert_type == 'success':
            func = InfoBar.success
        else:
            func = InfoBar.info

        func(
            title= title,
            content=content,
            orient=Qt.Vertical,
            isClosable=True,
            position=position,
            duration=duration,
            parent=self.window()
        )
    
    def setStateTooltip(self, msg:dict):
        title = msg.get('title', '状态')
        content = msg.get('content', '完成')
        show = msg.get('show', True)

        if show:
            self.stateTooltip = StateToolTip(title, content, self)
            self.stateTooltip.move(15, 15)
            self.stateTooltip.show()
        else:
            if self.stateTooltip:
                self.stateTooltip.setContent(content)
                self.stateTooltip.setState(True)
                self.stateTooltip = None




if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()



































