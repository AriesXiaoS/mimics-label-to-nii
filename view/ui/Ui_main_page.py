# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_page.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CardWidget, DoubleSpinBox, LineEdit,
    PlainTextEdit, PrimaryPushButton, PushButton, ScrollArea,
    SimpleCardWidget, Slider, StrongBodyLabel, ToggleToolButton,
    ToolButton)

class Ui_MainPage(object):
    def setupUi(self, MainPage):
        if not MainPage.objectName():
            MainPage.setObjectName(u"MainPage")
        MainPage.resize(1176, 756)
        self.horizontalLayout = QHBoxLayout(MainPage)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(MainPage)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(200, 0))
        self.widget.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.selectFolderBtn = PushButton(self.widget_4)
        self.selectFolderBtn.setObjectName(u"selectFolderBtn")

        self.horizontalLayout_6.addWidget(self.selectFolderBtn)

        self.questionBtn = ToolButton(self.widget_4)
        self.questionBtn.setObjectName(u"questionBtn")

        self.horizontalLayout_6.addWidget(self.questionBtn)


        self.verticalLayout.addWidget(self.widget_4)

        self.folderPathTextEdit = PlainTextEdit(self.widget)
        self.folderPathTextEdit.setObjectName(u"folderPathTextEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.folderPathTextEdit.sizePolicy().hasHeightForWidth())
        self.folderPathTextEdit.setSizePolicy(sizePolicy1)
        self.folderPathTextEdit.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout.addWidget(self.folderPathTextEdit)

        self.SimpleCardWidget_6 = SimpleCardWidget(self.widget)
        self.SimpleCardWidget_6.setObjectName(u"SimpleCardWidget_6")
        self.verticalLayout_9 = QVBoxLayout(self.SimpleCardWidget_6)
        self.verticalLayout_9.setSpacing(3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.BodyLabel_6 = BodyLabel(self.SimpleCardWidget_6)
        self.BodyLabel_6.setObjectName(u"BodyLabel_6")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.BodyLabel_6.sizePolicy().hasHeightForWidth())
        self.BodyLabel_6.setSizePolicy(sizePolicy2)
        self.BodyLabel_6.setTextFormat(Qt.AutoText)
        self.BodyLabel_6.setProperty("pixelFontSize", 12)

        self.verticalLayout_9.addWidget(self.BodyLabel_6)

        self.dicomNameLineEdit = LineEdit(self.SimpleCardWidget_6)
        self.dicomNameLineEdit.setObjectName(u"dicomNameLineEdit")

        self.verticalLayout_9.addWidget(self.dicomNameLineEdit)

        self.BodyLabel_7 = BodyLabel(self.SimpleCardWidget_6)
        self.BodyLabel_7.setObjectName(u"BodyLabel_7")
        self.BodyLabel_7.setProperty("pixelFontSize", 12)

        self.verticalLayout_9.addWidget(self.BodyLabel_7)

        self.niiNameLineEdit = LineEdit(self.SimpleCardWidget_6)
        self.niiNameLineEdit.setObjectName(u"niiNameLineEdit")

        self.verticalLayout_9.addWidget(self.niiNameLineEdit)


        self.verticalLayout.addWidget(self.SimpleCardWidget_6)

        self.updatePathBtn = PushButton(self.widget)
        self.updatePathBtn.setObjectName(u"updatePathBtn")

        self.verticalLayout.addWidget(self.updatePathBtn)

        self.SimpleCardWidget = SimpleCardWidget(self.widget)
        self.SimpleCardWidget.setObjectName(u"SimpleCardWidget")
        self.verticalLayout_4 = QVBoxLayout(self.SimpleCardWidget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)
        self.ScrollArea = ScrollArea(self.SimpleCardWidget)
        self.ScrollArea.setObjectName(u"ScrollArea")
        self.ScrollArea.setStyleSheet(u"background-color:transparent;\n"
"")
        self.ScrollArea.setFrameShape(QFrame.NoFrame)
        self.ScrollArea.setFrameShadow(QFrame.Plain)
        self.ScrollArea.setLineWidth(0)
        self.ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ScrollArea.setWidgetResizable(True)
        self.filesListContent = QWidget()
        self.filesListContent.setObjectName(u"filesListContent")
        self.filesListContent.setGeometry(QRect(0, 0, 160, 391))
        self.filesListContent.setStyleSheet(u"")
        self.ScrollArea.setWidget(self.filesListContent)

        self.verticalLayout_4.addWidget(self.ScrollArea)


        self.verticalLayout.addWidget(self.SimpleCardWidget)


        self.horizontalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(MainPage)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 9, 0, 9)
        self.viewWidget_br = QWidget(self.widget_2)
        self.viewWidget_br.setObjectName(u"viewWidget_br")

        self.gridLayout.addWidget(self.viewWidget_br, 2, 2, 1, 1)

        self.viewWidget_bl = QWidget(self.widget_2)
        self.viewWidget_bl.setObjectName(u"viewWidget_bl")

        self.gridLayout.addWidget(self.viewWidget_bl, 2, 0, 1, 1)

        self.viewWidget_tl = QWidget(self.widget_2)
        self.viewWidget_tl.setObjectName(u"viewWidget_tl")

        self.gridLayout.addWidget(self.viewWidget_tl, 0, 0, 1, 1)

        self.viewWidget_tr = QWidget(self.widget_2)
        self.viewWidget_tr.setObjectName(u"viewWidget_tr")

        self.gridLayout.addWidget(self.viewWidget_tr, 0, 2, 1, 1)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(MainPage)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(200, 0))
        self.widget_3.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.SimpleCardWidget_4 = SimpleCardWidget(self.widget_3)
        self.SimpleCardWidget_4.setObjectName(u"SimpleCardWidget_4")
        self.verticalLayout_7 = QVBoxLayout(self.SimpleCardWidget_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_8 = QWidget(self.SimpleCardWidget_4)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.cursorBtn = ToggleToolButton(self.widget_8)
        self.cursorBtn.setObjectName(u"cursorBtn")

        self.horizontalLayout_2.addWidget(self.cursorBtn)

        self.penBtn = ToggleToolButton(self.widget_8)
        self.penBtn.setObjectName(u"penBtn")

        self.horizontalLayout_2.addWidget(self.penBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.settingBtn = ToolButton(self.widget_8)
        self.settingBtn.setObjectName(u"settingBtn")

        self.horizontalLayout_2.addWidget(self.settingBtn)


        self.verticalLayout_7.addWidget(self.widget_8)


        self.verticalLayout_2.addWidget(self.SimpleCardWidget_4)

        self.SimpleCardWidget_3 = SimpleCardWidget(self.widget_3)
        self.SimpleCardWidget_3.setObjectName(u"SimpleCardWidget_3")
        self.verticalLayout_6 = QVBoxLayout(self.SimpleCardWidget_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 5)
        self.widget_9 = QWidget(self.SimpleCardWidget_3)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout_3 = QVBoxLayout(self.widget_9)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_10 = QWidget(self.widget_9)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.StrongBodyLabel = StrongBodyLabel(self.widget_10)
        self.StrongBodyLabel.setObjectName(u"StrongBodyLabel")
        sizePolicy2.setHeightForWidth(self.StrongBodyLabel.sizePolicy().hasHeightForWidth())
        self.StrongBodyLabel.setSizePolicy(sizePolicy2)
        self.StrongBodyLabel.setProperty("pixelFontSize", 13)

        self.horizontalLayout_3.addWidget(self.StrongBodyLabel)

        self.penSizeLabel = BodyLabel(self.widget_10)
        self.penSizeLabel.setObjectName(u"penSizeLabel")
        self.penSizeLabel.setMinimumSize(QSize(0, 0))
        self.penSizeLabel.setAlignment(Qt.AlignCenter)
        self.penSizeLabel.setProperty("pixelFontSize", 13)

        self.horizontalLayout_3.addWidget(self.penSizeLabel)


        self.verticalLayout_3.addWidget(self.widget_10)

        self.penSizeSlider = Slider(self.widget_9)
        self.penSizeSlider.setObjectName(u"penSizeSlider")
        sizePolicy1.setHeightForWidth(self.penSizeSlider.sizePolicy().hasHeightForWidth())
        self.penSizeSlider.setSizePolicy(sizePolicy1)
        self.penSizeSlider.setMinimumSize(QSize(0, 24))
        self.penSizeSlider.setMaximum(10)
        self.penSizeSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_3.addWidget(self.penSizeSlider)


        self.verticalLayout_6.addWidget(self.widget_9)


        self.verticalLayout_2.addWidget(self.SimpleCardWidget_3)

        self.SimpleCardWidget_5 = SimpleCardWidget(self.widget_3)
        self.SimpleCardWidget_5.setObjectName(u"SimpleCardWidget_5")
        self.verticalLayout_8 = QVBoxLayout(self.SimpleCardWidget_5)
        self.verticalLayout_8.setSpacing(1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.StrongBodyLabel_2 = StrongBodyLabel(self.SimpleCardWidget_5)
        self.StrongBodyLabel_2.setObjectName(u"StrongBodyLabel_2")
        self.StrongBodyLabel_2.setMinimumSize(QSize(0, 20))
        self.StrongBodyLabel_2.setProperty("pixelFontSize", 13)

        self.verticalLayout_8.addWidget(self.StrongBodyLabel_2)

        self.widget_11 = QWidget(self.SimpleCardWidget_5)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.BodyLabel_2 = BodyLabel(self.widget_11)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")
        self.BodyLabel_2.setProperty("pixelFontSize", 12)

        self.horizontalLayout_4.addWidget(self.BodyLabel_2)

        self.imageValue = BodyLabel(self.widget_11)
        self.imageValue.setObjectName(u"imageValue")
        self.imageValue.setAlignment(Qt.AlignCenter)
        self.imageValue.setProperty("pixelFontSize", 13)

        self.horizontalLayout_4.addWidget(self.imageValue)


        self.verticalLayout_8.addWidget(self.widget_11)

        self.widget_12 = QWidget(self.SimpleCardWidget_5)
        self.widget_12.setObjectName(u"widget_12")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.BodyLabel_3 = BodyLabel(self.widget_12)
        self.BodyLabel_3.setObjectName(u"BodyLabel_3")
        self.BodyLabel_3.setProperty("pixelFontSize", 12)

        self.horizontalLayout_5.addWidget(self.BodyLabel_3)

        self.labelValue = BodyLabel(self.widget_12)
        self.labelValue.setObjectName(u"labelValue")
        self.labelValue.setAlignment(Qt.AlignCenter)
        self.labelValue.setProperty("pixelFontSize", 13)

        self.horizontalLayout_5.addWidget(self.labelValue)


        self.verticalLayout_8.addWidget(self.widget_12)


        self.verticalLayout_2.addWidget(self.SimpleCardWidget_5)

        self.SimpleCardWidget_7 = SimpleCardWidget(self.widget_3)
        self.SimpleCardWidget_7.setObjectName(u"SimpleCardWidget_7")
        self.verticalLayout_10 = QVBoxLayout(self.SimpleCardWidget_7)
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(-1, -1, -1, 9)
        self.StrongBodyLabel_3 = StrongBodyLabel(self.SimpleCardWidget_7)
        self.StrongBodyLabel_3.setObjectName(u"StrongBodyLabel_3")
        self.StrongBodyLabel_3.setProperty("pixelFontSize", 13)

        self.verticalLayout_10.addWidget(self.StrongBodyLabel_3)

        self.labelOpacitySpinBox = DoubleSpinBox(self.SimpleCardWidget_7)
        self.labelOpacitySpinBox.setObjectName(u"labelOpacitySpinBox")
        self.labelOpacitySpinBox.setMinimumSize(QSize(0, 26))
        self.labelOpacitySpinBox.setMaximum(1.000000000000000)
        self.labelOpacitySpinBox.setSingleStep(0.010000000000000)

        self.verticalLayout_10.addWidget(self.labelOpacitySpinBox)


        self.verticalLayout_2.addWidget(self.SimpleCardWidget_7)

        self.SimpleCardWidget_2 = SimpleCardWidget(self.widget_3)
        self.SimpleCardWidget_2.setObjectName(u"SimpleCardWidget_2")
        self.verticalLayout_5 = QVBoxLayout(self.SimpleCardWidget_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.labelScrollArea = ScrollArea(self.SimpleCardWidget_2)
        self.labelScrollArea.setObjectName(u"labelScrollArea")
        self.labelScrollArea.setStyleSheet(u"background-color:transparent;\n"
"")
        self.labelScrollArea.setFrameShape(QFrame.NoFrame)
        self.labelScrollArea.setLineWidth(0)
        self.labelScrollArea.setWidgetResizable(True)
        self.labelListContent = QWidget()
        self.labelListContent.setObjectName(u"labelListContent")
        self.labelListContent.setGeometry(QRect(0, 0, 156, 381))
        self.labelScrollArea.setWidget(self.labelListContent)

        self.verticalLayout_5.addWidget(self.labelScrollArea)


        self.verticalLayout_2.addWidget(self.SimpleCardWidget_2)

        self.confirmSaveBtn = PrimaryPushButton(self.widget_3)
        self.confirmSaveBtn.setObjectName(u"confirmSaveBtn")

        self.verticalLayout_2.addWidget(self.confirmSaveBtn)


        self.horizontalLayout.addWidget(self.widget_3)


        self.retranslateUi(MainPage)

        QMetaObject.connectSlotsByName(MainPage)
    # setupUi

    def retranslateUi(self, MainPage):
        MainPage.setWindowTitle(QCoreApplication.translate("MainPage", u"Form", None))
        self.selectFolderBtn.setText(QCoreApplication.translate("MainPage", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.BodyLabel_6.setText(QCoreApplication.translate("MainPage", u"DICOM\u6807\u6ce8\u6587\u4ef6\u5939\u540d", None))
        self.BodyLabel_7.setText(QCoreApplication.translate("MainPage", u"Nifti\u4fdd\u5b58\u6587\u4ef6\u540d", None))
        self.updatePathBtn.setText(QCoreApplication.translate("MainPage", u"\u66f4\u65b0\u8def\u5f84", None))
        self.StrongBodyLabel.setText(QCoreApplication.translate("MainPage", u"\u7b14\u5237\u5927\u5c0f", None))
        self.penSizeLabel.setText(QCoreApplication.translate("MainPage", u"1", None))
        self.StrongBodyLabel_2.setText(QCoreApplication.translate("MainPage", u"\u5149\u6807\u4f4d\u7f6e", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("MainPage", u"\u56fe\u50cf\u7070\u5ea6\u503c", None))
        self.imageValue.setText(QCoreApplication.translate("MainPage", u"0", None))
        self.BodyLabel_3.setText(QCoreApplication.translate("MainPage", u"\u6807\u6ce8\u503c", None))
        self.labelValue.setText(QCoreApplication.translate("MainPage", u"0", None))
        self.StrongBodyLabel_3.setText(QCoreApplication.translate("MainPage", u"label\u900f\u660e\u5ea6", None))
        self.confirmSaveBtn.setText(QCoreApplication.translate("MainPage", u"\u786e\u8ba4 \u4e0b\u4e00\u4e2a", None))
    # retranslateUi

