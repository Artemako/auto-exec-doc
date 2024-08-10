# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedtabletag.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_NedTableTag(object):
    def setupUi(self, NedTableTag):
        if not NedTableTag.objectName():
            NedTableTag.setObjectName(u"NedTableTag")
        NedTableTag.resize(512, 254)
        self.verticalLayout = QVBoxLayout(NedTableTag)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_typetable = QLabel(NedTableTag)
        self.label_typetable.setObjectName(u"label_typetable")

        self.verticalLayout.addWidget(self.label_typetable)

        self.combox_typetable = QComboBox(NedTableTag)
        self.combox_typetable.setObjectName(u"combox_typetable")

        self.verticalLayout.addWidget(self.combox_typetable)

        self.label_rowcol = QLabel(NedTableTag)
        self.label_rowcol.setObjectName(u"label_rowcol")
        self.label_rowcol.setMinimumSize(QSize(0, 0))
        self.label_rowcol.setMaximumSize(QSize(16777215, 16))
        self.label_rowcol.setStyleSheet(u"font-weight: bold;")
        self.label_rowcol.setTextFormat(Qt.AutoText)
        self.label_rowcol.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_rowcol)

        self.tw_attrs = QTableWidget(NedTableTag)
        self.tw_attrs.setObjectName(u"tw_attrs")

        self.verticalLayout.addWidget(self.tw_attrs)

        self.btn_addrowcol = QPushButton(NedTableTag)
        self.btn_addrowcol.setObjectName(u"btn_addrowcol")

        self.verticalLayout.addWidget(self.btn_addrowcol)

        self.line = QFrame(NedTableTag)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(NedTableTag)

        QMetaObject.connectSlotsByName(NedTableTag)
    # setupUi

    def retranslateUi(self, NedTableTag):
        NedTableTag.setWindowTitle(QCoreApplication.translate("NedTableTag", u"Form", None))
        self.label_typetable.setText(QCoreApplication.translate("NedTableTag", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0438\u043f \u0442\u0430\u0431\u043b\u0438\u0446\u044b</span></p></body></html>", None))
        self.label_rowcol.setText(QCoreApplication.translate("NedTableTag", u"<html><head/><body><p>\u0421\u0442\u0440\u043e\u043a\u0438/\u0441\u0442\u043e\u043b\u0431\u0446\u044b</p></body></html>", None))
        self.btn_addrowcol.setText(QCoreApplication.translate("NedTableTag", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
    # retranslateUi

