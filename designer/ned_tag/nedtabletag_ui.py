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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_NedTableTag(object):
    def setupUi(self, NedTableTag):
        if not NedTableTag.objectName():
            NedTableTag.setObjectName(u"NedTableTag")
        NedTableTag.resize(512, 132)
        self.verticalLayout = QVBoxLayout(NedTableTag)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.columns = QLabel(NedTableTag)
        self.columns.setObjectName(u"columns")
        self.columns.setMinimumSize(QSize(0, 0))
        self.columns.setMaximumSize(QSize(16777215, 16))
        self.columns.setStyleSheet(u"font-weight: bold;")
        self.columns.setTextFormat(Qt.AutoText)
        self.columns.setScaledContents(False)

        self.verticalLayout.addWidget(self.columns)

        self.tw_attrs = QTableView(NedTableTag)
        self.tw_attrs.setObjectName(u"tw_attrs")

        self.verticalLayout.addWidget(self.tw_attrs)

        self.btn_addattr = QPushButton(NedTableTag)
        self.btn_addattr.setObjectName(u"btn_addattr")

        self.verticalLayout.addWidget(self.btn_addattr)

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
        self.columns.setText(QCoreApplication.translate("NedTableTag", u"<html><head/><body><p>\u0410\u0442\u0440\u0438\u0431\u0443\u0442\u044b</p></body></html>", None))
        self.btn_addattr.setText(QCoreApplication.translate("NedTableTag", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0430\u0442\u0440\u0438\u0431\u0443\u0442", None))
    # retranslateUi

