# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesh.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import (CardWidget, SimpleCardWidget, ToolButton)

class Ui_meshView(object):
    def setupUi(self, meshView):
        if not meshView.objectName():
            meshView.setObjectName(u"meshView")
        meshView.resize(479, 358)
        self.horizontalLayout = QHBoxLayout(meshView)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.SimpleCardWidget = SimpleCardWidget(meshView)
        self.SimpleCardWidget.setObjectName(u"SimpleCardWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.SimpleCardWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 6, 6, 6)
        self.viewWidget = QWidget(self.SimpleCardWidget)
        self.viewWidget.setObjectName(u"viewWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewWidget.sizePolicy().hasHeightForWidth())
        self.viewWidget.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.viewWidget)

        self.sideWidget = QWidget(self.SimpleCardWidget)
        self.sideWidget.setObjectName(u"sideWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sideWidget.sizePolicy().hasHeightForWidth())
        self.sideWidget.setSizePolicy(sizePolicy1)
        self.sideWidget.setMinimumSize(QSize(18, 0))
        self.verticalLayout = QVBoxLayout(self.sideWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.resetBtn = ToolButton(self.sideWidget)
        self.resetBtn.setObjectName(u"resetBtn")
        self.resetBtn.setMinimumSize(QSize(18, 18))
        self.resetBtn.setMaximumSize(QSize(18, 18))

        self.verticalLayout.addWidget(self.resetBtn)

        self.soloBtn = ToolButton(self.sideWidget)
        self.soloBtn.setObjectName(u"soloBtn")
        self.soloBtn.setMinimumSize(QSize(18, 18))
        self.soloBtn.setMaximumSize(QSize(18, 18))

        self.verticalLayout.addWidget(self.soloBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.updateBtn = ToolButton(self.sideWidget)
        self.updateBtn.setObjectName(u"updateBtn")
        self.updateBtn.setMinimumSize(QSize(18, 18))
        self.updateBtn.setMaximumSize(QSize(18, 18))

        self.verticalLayout.addWidget(self.updateBtn)


        self.horizontalLayout_2.addWidget(self.sideWidget)


        self.horizontalLayout.addWidget(self.SimpleCardWidget)


        self.retranslateUi(meshView)

        QMetaObject.connectSlotsByName(meshView)
    # setupUi

    def retranslateUi(self, meshView):
        meshView.setWindowTitle(QCoreApplication.translate("meshView", u"Form", None))
    # retranslateUi

