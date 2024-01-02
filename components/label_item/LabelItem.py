
import os,sys
from typing import Optional
from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

from .Ui_main import Ui_labelItem
from common import signalBus, NAMES


class LabelItem(QWidget, Ui_labelItem):
    SetLabel = Signal(int)
    Delete = Signal(int)
    Edit = Signal(int)
    Click = Signal(int)
    def __init__(self, index, name,):
        super().__init__()
        self.index = int(index)
        self.name = name
        self.setupUi(self)
        self.BodyLabel.setText(f'{index} {name}')
        self.resetUi()
        self.initSignals()
        self.setMode(NAMES.CURSOR)
    
    def setColor(self, color):
        rgb = [int(color[i]*255) for i in range(3)]
        color_hex = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
        self.colorWidget.setStyleSheet(f'background-color: {color_hex};')

    def resetUi(self):
        self.setFixedHeight(36)
        # self.setStyleSheet('background-color: red;')
        btn_size = QSize(24,24)
        icon_size = QSize(14,14)
        self.colorWidget.setFixedSize(20,20)
        self.setBtn.setIcon(FIF.PIN)
        self.setBtn.setFixedSize(btn_size)
        self.setBtn.setIconSize(icon_size)
        self.deleteBtn.setIcon(FIF.DELETE)
        self.deleteBtn.setFixedSize(btn_size)
        self.deleteBtn.setIconSize(icon_size)
        self.editBtn.setIcon(FIF.EDIT)
        self.editBtn.setFixedSize(btn_size)
        self.editBtn.setIconSize(icon_size)

    def initSignals(self):
        self.setBtn.clicked.connect(lambda : self.SetLabel.emit(self.index))
        self.deleteBtn.clicked.connect(lambda : self.Delete.emit(self.index))
        self.editBtn.clicked.connect(lambda : self.Edit.emit(self.index))

    def setMode(self, mode):
        if mode == NAMES.CURSOR:
            self.setBtn.show()
            self.editBtn.hide()
        else:
            self.setBtn.hide()
            self.editBtn.show()

    def setEditing(self, state):
        if state:
            self.editBtn.setChecked(True)
            self.setStyleSheet('background-color: #a0cfff;')
        else:
            self.editBtn.setChecked(False)
            self.setStyleSheet('background-color: transparent;')

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.Click.emit(self.index)


