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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, HorizontalSeparator, IconWidget, IndeterminateProgressRing,
    ProgressBar, ProgressRing)

class Ui_itemWidget(object):
    def setupUi(self, itemWidget):
        if not itemWidget.objectName():
            itemWidget.setObjectName(u"itemWidget")
        itemWidget.resize(266, 60)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(itemWidget.sizePolicy().hasHeightForWidth())
        itemWidget.setSizePolicy(sizePolicy)
        itemWidget.setMinimumSize(QSize(150, 36))
        itemWidget.setMaximumSize(QSize(1065, 16777215))
        self.verticalLayout = QVBoxLayout(itemWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(itemWidget)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.widget.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.niiStateIcon = IconWidget(self.widget)
        self.niiStateIcon.setObjectName(u"niiStateIcon")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.niiStateIcon.sizePolicy().hasHeightForWidth())
        self.niiStateIcon.setSizePolicy(sizePolicy2)
        self.niiStateIcon.setMinimumSize(QSize(20, 20))
        self.niiStateIcon.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.niiStateIcon)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QSize(5, 0))
        self.widget_2.setMaximumSize(QSize(5, 16777215))

        self.horizontalLayout.addWidget(self.widget_2)

        self.nameLabel = BodyLabel(self.widget)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setWordWrap(True)

        self.horizontalLayout.addWidget(self.nameLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.loadingRing = IndeterminateProgressRing(self.widget)
        self.loadingRing.setObjectName(u"loadingRing")
        self.loadingRing.setMinimumSize(QSize(26, 26))
        self.loadingRing.setMaximumSize(QSize(26, 26))
        self.loadingRing.setStrokeWidth(3)

        self.horizontalLayout.addWidget(self.loadingRing)

        self.loadedRing = ProgressRing(self.widget)
        self.loadedRing.setObjectName(u"loadedRing")
        self.loadedRing.setMinimumSize(QSize(26, 26))
        self.loadedRing.setMaximumSize(QSize(26, 26))
        self.loadedRing.setValue(100)
        self.loadedRing.setStrokeWidth(3)

        self.horizontalLayout.addWidget(self.loadedRing)


        self.verticalLayout.addWidget(self.widget, 0, Qt.AlignVCenter)

        self.HorizontalSeparator = HorizontalSeparator(itemWidget)
        self.HorizontalSeparator.setObjectName(u"HorizontalSeparator")

        self.verticalLayout.addWidget(self.HorizontalSeparator)


        self.retranslateUi(itemWidget)

        QMetaObject.connectSlotsByName(itemWidget)
    # setupUi

    def retranslateUi(self, itemWidget):
        itemWidget.setWindowTitle(QCoreApplication.translate("itemWidget", u"file item", None))
        self.nameLabel.setText(QCoreApplication.translate("itemWidget", u"name", None))
    # retranslateUi

