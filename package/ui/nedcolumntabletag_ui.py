# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedcolumntabletag.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_NedColumnTableTag(object):
    def setupUi(self, NedColumnTableTag):
        if not NedColumnTableTag.objectName():
            NedColumnTableTag.setObjectName(u"NedColumnTableTag")
        NedColumnTableTag.resize(400, 148)
        self.verticalLayout = QVBoxLayout(NedColumnTableTag)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.colname = QLabel(NedColumnTableTag)
        self.colname.setObjectName(u"colname")
        self.colname.setMinimumSize(QSize(0, 0))
        self.colname.setMaximumSize(QSize(16777215, 16))
        self.colname.setStyleSheet(u"font-weight: bold;")
        self.colname.setTextFormat(Qt.AutoText)
        self.colname.setScaledContents(False)

        self.verticalLayout.addWidget(self.colname)

        self.lineedit_colname = QLineEdit(NedColumnTableTag)
        self.lineedit_colname.setObjectName(u"lineedit_colname")
        self.lineedit_colname.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_colname)

        self.coltag = QLabel(NedColumnTableTag)
        self.coltag.setObjectName(u"coltag")
        self.coltag.setMinimumSize(QSize(0, 0))
        self.coltag.setMaximumSize(QSize(16777215, 16))
        self.coltag.setStyleSheet(u"font-weight: bold;")
        self.coltag.setTextFormat(Qt.AutoText)
        self.coltag.setScaledContents(False)

        self.verticalLayout.addWidget(self.coltag)

        self.lineedit_coltag = QLineEdit(NedColumnTableTag)
        self.lineedit_coltag.setObjectName(u"lineedit_coltag")
        self.lineedit_coltag.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_coltag)

        self.btn_ned = QPushButton(NedColumnTableTag)
        self.btn_ned.setObjectName(u"btn_ned")

        self.verticalLayout.addWidget(self.btn_ned)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(NedColumnTableTag)

        QMetaObject.connectSlotsByName(NedColumnTableTag)
    # setupUi

    def retranslateUi(self, NedColumnTableTag):
        NedColumnTableTag.setWindowTitle(QCoreApplication.translate("NedColumnTableTag", u"Dialog", None))
        self.colname.setText(QCoreApplication.translate("NedColumnTableTag", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u043e\u043b\u0431\u0446\u0430</p></body></html>", None))
        self.coltag.setText(QCoreApplication.translate("NedColumnTableTag", u"<html><head/><body><p>\u041f\u043e\u0434\u0442\u044d\u0433 </p></body></html>", None))
        self.btn_ned.setText(QCoreApplication.translate("NedColumnTableTag", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u044d\u0433", None))
    # retranslateUi

