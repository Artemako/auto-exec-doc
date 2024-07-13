# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editdatetag.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 68)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formatdate = QLabel(Form)
        self.formatdate.setObjectName(u"formatdate")
        self.formatdate.setMinimumSize(QSize(0, 0))
        self.formatdate.setMaximumSize(QSize(16777215, 16))
        self.formatdate.setStyleSheet(u"font-weight: bold;")
        self.formatdate.setTextFormat(Qt.AutoText)
        self.formatdate.setScaledContents(False)

        self.verticalLayout.addWidget(self.formatdate)

        self.lineedit_format = QLineEdit(Form)
        self.lineedit_format.setObjectName(u"lineedit_format")
        self.lineedit_format.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_format)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.formatdate.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0434\u0430\u0442\u044b</p></body></html>", None))
    # retranslateUi

