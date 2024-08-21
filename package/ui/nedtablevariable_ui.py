# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedtablevariable.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_NedTableVariable(object):
    def setupUi(self, NedTableVariable):
        if not NedTableVariable.objectName():
            NedTableVariable.setObjectName(u"NedTableVariable")
        NedTableVariable.resize(512, 254)
        self.verticalLayout = QVBoxLayout(NedTableVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_typetable = QLabel(NedTableVariable)
        self.label_typetable.setObjectName(u"label_typetable")

        self.verticalLayout.addWidget(self.label_typetable)

        self.combox_typetable = QComboBox(NedTableVariable)
        self.combox_typetable.setObjectName(u"combox_typetable")

        self.verticalLayout.addWidget(self.combox_typetable)

        self.label_rowcol = QLabel(NedTableVariable)
        self.label_rowcol.setObjectName(u"label_rowcol")
        self.label_rowcol.setMinimumSize(QSize(0, 0))
        self.label_rowcol.setMaximumSize(QSize(16777215, 16))
        self.label_rowcol.setStyleSheet(u"font-weight: bold;")
        self.label_rowcol.setTextFormat(Qt.AutoText)
        self.label_rowcol.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_rowcol)

        self.lw_attrs = QListWidget(NedTableVariable)
        self.lw_attrs.setObjectName(u"lw_attrs")

        self.verticalLayout.addWidget(self.lw_attrs)

        self.btn_addrowcol = QPushButton(NedTableVariable)
        self.btn_addrowcol.setObjectName(u"btn_addrowcol")

        self.verticalLayout.addWidget(self.btn_addrowcol)

        self.line = QFrame(NedTableVariable)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(NedTableVariable)

        QMetaObject.connectSlotsByName(NedTableVariable)
    # setupUi

    def retranslateUi(self, NedTableVariable):
        NedTableVariable.setWindowTitle(QCoreApplication.translate("NedTableVariable", u"Form", None))
        self.label_typetable.setText(QCoreApplication.translate("NedTableVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0438\u043f \u0442\u0430\u0431\u043b\u0438\u0446\u044b</span></p></body></html>", None))
        self.label_rowcol.setText(QCoreApplication.translate("NedTableVariable", u"<html><head/><body><p>\u0421\u0442\u0440\u043e\u043a\u0438/\u0441\u0442\u043e\u043b\u0431\u0446\u044b</p></body></html>", None))
        self.btn_addrowcol.setText(QCoreApplication.translate("NedTableVariable", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
    # retranslateUi

