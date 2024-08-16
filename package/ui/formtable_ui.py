# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formtable.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_FormTableWidget(object):
    def setupUi(self, FormTableWidget):
        if not FormTableWidget.objectName():
            FormTableWidget.setObjectName(u"FormTableWidget")
        FormTableWidget.resize(429, 202)
        FormTableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormTableWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typetag = QLabel(FormTableWidget)
        self.label_typetag.setObjectName(u"label_typetag")
        self.label_typetag.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typetag)

        self.title = QLabel(FormTableWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.hl.addWidget(self.title)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

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


        self.verticalLayout.addLayout(self.buttons_layout)

        self.textbrowser = QTextBrowser(FormTableWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textbrowser.sizePolicy().hasHeightForWidth())
        self.textbrowser.setSizePolicy(sizePolicy)
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.retranslateUi(FormTableWidget)

        QMetaObject.connectSlotsByName(FormTableWidget)
    # setupUi

    def retranslateUi(self, FormTableWidget):
        FormTableWidget.setWindowTitle(QCoreApplication.translate("FormTableWidget", u"Form", None))
        self.label_typetag.setText(QCoreApplication.translate("FormTableWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormTableWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.add_button.setText(QCoreApplication.translate("FormTableWidget", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
        self.delete_button.setText(QCoreApplication.translate("FormTableWidget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormTableWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi

