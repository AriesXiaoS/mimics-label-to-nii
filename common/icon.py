# coding: utf-8
from enum import Enum

from qfluentwidgets import (
    FluentIconBase, getIconColor, Theme
)

class ICON(FluentIconBase, Enum):

    D3 = '3d'
    D3_3D = '3d3d'
    CURSOR_LINE = 'cursorLine'

    def path(self, theme=Theme.AUTO):
        return f":/icons/{self.value}-{getIconColor(theme)}.svg"


