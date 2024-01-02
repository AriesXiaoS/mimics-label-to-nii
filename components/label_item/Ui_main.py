# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget)

from qfluentwidgets import (BodyLabel, HorizontalSeparator, ToggleToolButton, ToolButton)

class Ui_labelItem(object):
    def setupUi(self, labelItem):
        if not labelItem.objectName():
            labelItem.setObjectName(u"labelItem")
        labelItem.resize(390, 68)
        self.verticalLayout = QVBoxLayout(labelItem)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(labelItem)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.setBtn = ToolButton(self.widget)
        self.setBtn.setObjectName(u"setBtn")

        self.horizontalLayout.addWidget(self.setBtn)

        self.editBtn = ToggleToolButton(self.widget)
        self.editBtn.setObjectName(u"editBtn")

        self.horizontalLayout.addWidget(self.editBtn)

        self.colorWidget = QWidget(self.widget)
        self.colorWidget.setObjectName(u"colorWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorWidget.sizePolicy().hasHeightForWidth())
        self.colorWidget.setSizePolicy(sizePolicy)
        self.colorWidget.setMinimumSize(QSize(20, 20))
        self.colorWidget.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.colorWidget)

        self.BodyLabel = BodyLabel(self.widget)
        self.BodyLabel.setObjectName(u"BodyLabel")
        self.BodyLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.BodyLabel)

        self.deleteBtn = ToolButton(self.widget)
        self.deleteBtn.setObjectName(u"deleteBtn")

        self.horizontalLayout.addWidget(self.deleteBtn)


        self.verticalLayout.addWidget(self.widget, 0, Qt.AlignVCenter)

        self.HorizontalSeparator = HorizontalSeparator(labelItem)
        self.HorizontalSeparator.setObjectName(u"HorizontalSeparator")

        self.verticalLayout.addWidget(self.HorizontalSeparator)


        self.retranslateUi(labelItem)

        QMetaObject.connectSlotsByName(labelItem)
    # setupUi

    def retranslateUi(self, labelItem):
        labelItem.setWindowTitle(QCoreApplication.translate("labelItem", u"label item", None))
        self.BodyLabel.setText(QCoreApplication.translate("labelItem", u"Body label", None))
    # retranslateUi

