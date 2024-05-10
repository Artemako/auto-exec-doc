# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formimage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_FormImageWidget(object):
    def setupUi(self, FormImageWidget):
        if not FormImageWidget.objectName():
            FormImageWidget.setObjectName(u"FormImageWidget")
        FormImageWidget.resize(425, 191)
        FormImageWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormImageWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(FormImageWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.verticalLayout.addWidget(self.title)

        self.select_button = QPushButton(FormImageWidget)
        self.select_button.setObjectName(u"select_button")

        self.verticalLayout.addWidget(self.select_button)

        self.label = QLabel(FormImageWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font-style: italic;")

        self.verticalLayout.addWidget(self.label)

        self.scale_layout = QHBoxLayout()
        self.scale_layout.setObjectName(u"scale_layout")
        self.percent_label = QLabel(FormImageWidget)
        self.percent_label.setObjectName(u"percent_label")
        self.percent_label.setMaximumSize(QSize(60, 16777215))

        self.scale_layout.addWidget(self.percent_label)

        self.percent_spinbox = QDoubleSpinBox(FormImageWidget)
        self.percent_spinbox.setObjectName(u"percent_spinbox")
        self.percent_spinbox.setMaximum(500.000000000000000)
        self.percent_spinbox.setValue(100.000000000000000)

        self.scale_layout.addWidget(self.percent_spinbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.scale_layout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.scale_layout)

        self.textbrowser = QTextBrowser(FormImageWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.retranslateUi(FormImageWidget)

        QMetaObject.connectSlotsByName(FormImageWidget)
    # setupUi

    def retranslateUi(self, FormImageWidget):
        FormImageWidget.setWindowTitle(QCoreApplication.translate("FormImageWidget", u"Form", None))
        self.title.setText(QCoreApplication.translate("FormImageWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.select_button.setText(QCoreApplication.translate("FormImageWidget", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
        self.label.setText(QCoreApplication.translate("FormImageWidget", u"\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b", None))
        self.percent_label.setText(QCoreApplication.translate("FormImageWidget", u"\u041c\u0430\u0441\u0448\u0442\u0430\u0431", None))
        self.percent_spinbox.setSuffix(QCoreApplication.translate("FormImageWidget", u"%", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormImageWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi

