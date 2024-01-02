import os,sys
from typing import Optional
from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

import matplotlib.pyplot as plt

import numpy as np
import vtk
from .Ui_main import Ui_ImageView
from common import myImageData, signalBus, globalVar, NAMES

from .slice_view import SliceView


class ImageView(QWidget, Ui_ImageView):
    changeView = Signal()
    def __init__(self, orientation):
        super().__init__()
        self.setupUi(self)
        self.initSetting()
        self.initView(orientation)
        self.initSignals()
        
        self.orientation = orientation

    def initSetting(self):
        self.resetBtn.setFixedWidth(18)
        self.resetBtn.setFixedHeight(18)
        self.resetBtn.setIcon(FIF.SYNC)
        self.resetBtn.setIconSize(QSize(12, 12))

        self.soloBtn.setFixedWidth(18)
        self.soloBtn.setFixedHeight(18)
        self.soloBtn.setIcon(FIF.ZOOM)
        self.soloBtn.setIconSize(QSize(12, 12))

        self.verticalScrollBar.setFixedWidth(18)
        self.sideWidget.setFixedWidth(18)
        #
        self.verticalScrollBar.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

    def initView(self, orientation):
        self.slice_view = SliceView(orientation = orientation, parent = self.viewWidget)
        self.verticalScrollBar.valueChanged.connect(self.slice_view.setSlice)

    def initSignals(self):
        self.resetBtn.clicked.connect(self.slice_view.resetCamera_)
        self.soloBtn.clicked.connect(self.changeView.emit)
        signalBus.cursorChanged.connect(self.changeScollBar)
    
    def setImageLabel(self, image:myImageData, label:myImageData):
        min_ = image.clips[0]
        max_ = image.clips[1]
        c_level = (min_ + max_) / 2
        c_window = max_ - min_

        self.verticalScrollBar.setMaximum(image.size[self.orientation]-1)

        self.slice_view.setImageLabel(image, label)
        self.slice_view.setColor(c_level, c_window)
        self.slice_view.resetCamera_()
        

    def changeScollBar(self):
        curosr = globalVar.get(NAMES.CURSOR)
        self.verticalScrollBar.setValue(curosr[self.orientation])

    def updateRender(self):
        self.slice_view.updateRender()








