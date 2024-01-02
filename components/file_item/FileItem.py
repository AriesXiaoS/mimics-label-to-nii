
import os,sys
from typing import Optional
from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

from .Ui_main import Ui_itemWidget

class FileItem(QWidget, Ui_itemWidget):
    Click = Signal(int)
    def __init__(self, index, name, nii_state=False):
        super().__init__()
        self.index = index
        self.name = name
        self.nii_state = nii_state
        self.setupUi(self)
        self.resetUi()
        #
        self.loading = 0
        self.setLoadingState(0)
        #
        self.nameLabel.setText(name)
        self.setNiiState()
    
    def resetUi(self):
        # 总宽 182
        self.niiStateIcon.setFixedSize(18, 18)
        # ring 26
        self.nameLabel.setFixedWidth(100)
        # self.nameLabel.setStyleSheet('background-color: red;')
        self.nameLabel.installEventFilter(ToolTipFilter(self.nameLabel, position=ToolTipPosition.RIGHT))
        self.nameLabel.setToolTip(self.name)


    def setNiiState(self, state=None):
        if state is None:
            state = self.nii_state
        else:
            self.nii_state = state
        ##
        if state:
            self.niiStateIcon.setIcon(FIF.ACCEPT)
        else:
            self.niiStateIcon.setIcon(FIF.QUESTION)

    def setSelected(self, state:bool):
        if state:
            self.setStyleSheet('background-color: #a0cfff;')
        else:
            self.setStyleSheet('background-color: transparent;')

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.Click.emit(self.index)

    def setLoadingState(self, state):
        # state 0 nothing 1:loading 2 loaded
        self.loading = state
        if state==0:
            self.loadingRing.hide()
            self.loadedRing.hide()
        elif state==1:
            self.loadingRing.show()
            self.loadedRing.hide()
        else:
            self.loadingRing.hide()
            self.loadedRing.show()




















