# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formdate.ui'
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QHBoxLayout, QLabel,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_FormDateWidget(object):
    def setupUi(self, FormDateWidget):
        if not FormDateWidget.objectName():
            FormDateWidget.setObjectName(u"FormDateWidget")
        FormDateWidget.resize(439, 121)
        self.verticalLayout = QVBoxLayout(FormDateWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormDateWidget)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setScaledContents(False)
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormDateWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.hl.addWidget(self.title)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.dateedit = QDateEdit(FormDateWidget)
        self.dateedit.setObjectName(u"dateedit")
        self.dateedit.setTimeSpec(Qt.UTC)

        self.verticalLayout.addWidget(self.dateedit)

        self.textbrowser = QTextBrowser(FormDateWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.retranslateUi(FormDateWidget)

        QMetaObject.connectSlotsByName(FormDateWidget)
    # setupUi

    def retranslateUi(self, FormDateWidget):
        FormDateWidget.setWindowTitle(QCoreApplication.translate("FormDateWidget", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormDateWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormDateWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormDateWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi

