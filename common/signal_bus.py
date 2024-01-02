# coding: utf-8
from PySide6.QtCore import QObject, Signal
import numpy as np

class SignalBus(QObject):
    """ Signal bus """
    # 主动设置
    alertInfo = Signal(dict)
    stateTooltip = Signal(dict)

    # 图像
    cursorChanged = Signal()

    #
    keyPressed = Signal(int)


signalBus = SignalBus()