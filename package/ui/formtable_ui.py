# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formtable.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_FormTableWidget(object):
    def setupUi(self, FormTableWidget):
        if not FormTableWidget.objectName():
            FormTableWidget.setObjectName(u"FormTableWidget")
        FormTableWidget.resize(429, 220)
        FormTableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout = QHBoxLayout(FormTableWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(FormTableWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.verticalLayout.addWidget(self.title)

        self.table = QTableWidget(FormTableWidget)
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.add_button = QPushButton(FormTableWidget)
        self.add_button.setObjectName(u"add_button")

        self.buttons_layout.addWidget(self.add_button)

        self.delete_button = QPushButton(FormTableWidget)
        self.delete_button.setObjectName(u"delete_button")

        self.buttons_layout.addWidget(self.delete_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttons_layout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.buttons_layout)

        self.textbrowser = QTextBrowser(FormTableWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textbrowser.sizePolicy().hasHeightForWidth())
        self.textbrowser.setSizePolicy(sizePolicy)
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(FormTableWidget)

        QMetaObject.connectSlotsByName(FormTableWidget)
    # setupUi

    def retranslateUi(self, FormTableWidget):
        FormTableWidget.setWindowTitle(QCoreApplication.translate("FormTableWidget", u"Form", None))
        self.title.setText(QCoreApplication.translate("FormTableWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.add_button.setText(QCoreApplication.translate("FormTableWidget", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443", None))
        self.delete_button.setText(QCoreApplication.translate("FormTableWidget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormTableWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi

