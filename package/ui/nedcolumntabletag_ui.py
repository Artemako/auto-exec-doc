# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedcolumntablevariable.ui'
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

class Ui_NedColumnTableVariable(object):
    def setupUi(self, NedColumnTableVariable):
        if not NedColumnTableVariable.objectName():
            NedColumnTableVariable.setObjectName(u"NedColumnTableVariable")
        NedColumnTableVariable.resize(400, 148)
        self.verticalLayout = QVBoxLayout(NedColumnTableVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.colname = QLabel(NedColumnTableVariable)
        self.colname.setObjectName(u"colname")
        self.colname.setMinimumSize(QSize(0, 0))
        self.colname.setMaximumSize(QSize(16777215, 16))
        self.colname.setStyleSheet(u"font-weight: bold;")
        self.colname.setTextFormat(Qt.AutoText)
        self.colname.setScaledContents(False)

        self.verticalLayout.addWidget(self.colname)

        self.lineedit_colname = QLineEdit(NedColumnTableVariable)
        self.lineedit_colname.setObjectName(u"lineedit_colname")
        self.lineedit_colname.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_colname)

        self.colvariable = QLabel(NedColumnTableVariable)
        self.colvariable.setObjectName(u"colvariable")
        self.colvariable.setMinimumSize(QSize(0, 0))
        self.colvariable.setMaximumSize(QSize(16777215, 16))
        self.colvariable.setStyleSheet(u"font-weight: bold;")
        self.colvariable.setTextFormat(Qt.AutoText)
        self.colvariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.colvariable)

        self.lineedit_colvariable = QLineEdit(NedColumnTableVariable)
        self.lineedit_colvariable.setObjectName(u"lineedit_colvariable")
        self.lineedit_colvariable.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_colvariable)

        self.btn_ned = QPushButton(NedColumnTableVariable)
        self.btn_ned.setObjectName(u"btn_ned")

        self.verticalLayout.addWidget(self.btn_ned)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(NedColumnTableVariable)

        QMetaObject.connectSlotsByName(NedColumnTableVariable)
    # setupUi

    def retranslateUi(self, NedColumnTableVariable):
        NedColumnTableVariable.setWindowTitle(QCoreApplication.translate("NedColumnTableVariable", u"Dialog", None))
        self.colname.setText(QCoreApplication.translate("NedColumnTableVariable", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u043e\u043b\u0431\u0446\u0430</p></body></html>", None))
        self.colvariable.setText(QCoreApplication.translate("NedColumnTableVariable", u"<html><head/><body><p>\u041f\u043e\u0434\u0442\u044d\u0433 </p></body></html>", None))
        self.btn_ned.setText(QCoreApplication.translate("NedColumnTableVariable", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u044d\u0433", None))
    # retranslateUi

