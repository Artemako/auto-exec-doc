# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formlist.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_FormListWidget(object):
    def setupUi(self, FormListWidget):
        if not FormListWidget.objectName():
            FormListWidget.setObjectName(u"FormListWidget")
        FormListWidget.resize(431, 123)
        FormListWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormListWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormListWidget)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormListWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.hl.addWidget(self.title)

        self.label_variable = QLabel(FormListWidget)
        self.label_variable.setObjectName(u"label_variable")

        self.hl.addWidget(self.label_variable)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.btn_edittable = QPushButton(FormListWidget)
        self.btn_edittable.setObjectName(u"btn_edittable")

        self.verticalLayout.addWidget(self.btn_edittable)

        self.textbrowser = QTextBrowser(FormListWidget)
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

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(FormListWidget)

        QMetaObject.connectSlotsByName(FormListWidget)
    # setupUi

    def retranslateUi(self, FormListWidget):
        FormListWidget.setWindowTitle(QCoreApplication.translate("FormListWidget", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormListWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormListWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.label_variable.setText(QCoreApplication.translate("FormListWidget", u"<html><head/><body><p><span style=\" font-style:italic;\">TextLabel</span></p></body></html>", None))
        self.btn_edittable.setText(QCoreApplication.translate("FormListWidget", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormListWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi

