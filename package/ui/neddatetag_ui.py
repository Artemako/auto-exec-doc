# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neddatetag.ui'
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

class Ui_NedDateTag(object):
    def setupUi(self, NedDateTag):
        if not NedDateTag.objectName():
            NedDateTag.setObjectName(u"NedDateTag")
        NedDateTag.resize(400, 68)
        self.verticalLayout = QVBoxLayout(NedDateTag)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formatdate = QLabel(NedDateTag)
        self.formatdate.setObjectName(u"formatdate")
        self.formatdate.setMinimumSize(QSize(0, 0))
        self.formatdate.setMaximumSize(QSize(16777215, 16))
        self.formatdate.setStyleSheet(u"font-weight: bold;")
        self.formatdate.setTextFormat(Qt.AutoText)
        self.formatdate.setScaledContents(False)

        self.verticalLayout.addWidget(self.formatdate)

        self.lineedit_format = QLineEdit(NedDateTag)
        self.lineedit_format.setObjectName(u"lineedit_format")
        self.lineedit_format.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_format)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(NedDateTag)

        QMetaObject.connectSlotsByName(NedDateTag)
    # setupUi

    def retranslateUi(self, NedDateTag):
        NedDateTag.setWindowTitle(QCoreApplication.translate("NedDateTag", u"Form", None))
        self.formatdate.setText(QCoreApplication.translate("NedDateTag", u"<html><head/><body><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0434\u0430\u0442\u044b</p></body></html>", None))
    # retranslateUi

