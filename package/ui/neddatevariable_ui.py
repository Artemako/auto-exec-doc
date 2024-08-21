# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neddatevariable.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_NedDateVariable(object):
    def setupUi(self, NedDateVariable):
        if not NedDateVariable.objectName():
            NedDateVariable.setObjectName(u"NedDateVariable")
        NedDateVariable.resize(400, 53)
        self.verticalLayout = QVBoxLayout(NedDateVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formatdate = QLabel(NedDateVariable)
        self.formatdate.setObjectName(u"formatdate")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formatdate.sizePolicy().hasHeightForWidth())
        self.formatdate.setSizePolicy(sizePolicy)
        self.formatdate.setMinimumSize(QSize(0, 0))
        self.formatdate.setMaximumSize(QSize(16777215, 16))
        self.formatdate.setStyleSheet(u"font-weight: bold;")
        self.formatdate.setTextFormat(Qt.AutoText)
        self.formatdate.setScaledContents(False)

        self.verticalLayout.addWidget(self.formatdate)

        self.lineedit_format = QLineEdit(NedDateVariable)
        self.lineedit_format.setObjectName(u"lineedit_format")
        self.lineedit_format.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_format)

        self.line = QFrame(NedDateVariable)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(NedDateVariable)

        QMetaObject.connectSlotsByName(NedDateVariable)
    # setupUi

    def retranslateUi(self, NedDateVariable):
        NedDateVariable.setWindowTitle(QCoreApplication.translate("NedDateVariable", u"Form", None))
        self.formatdate.setText(QCoreApplication.translate("NedDateVariable", u"<html><head/><body><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0434\u0430\u0442\u044b</p></body></html>", None))
    # retranslateUi

