# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedtagdialogwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_NedTagDialogWindow(object):
    def setupUi(self, NedTagDialogWindow):
        if not NedTagDialogWindow.objectName():
            NedTagDialogWindow.setObjectName(u"NedTagDialogWindow")
        NedTagDialogWindow.resize(530, 217)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NedTagDialogWindow.sizePolicy().hasHeightForWidth())
        NedTagDialogWindow.setSizePolicy(sizePolicy)
        NedTagDialogWindow.setBaseSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(NedTagDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nametag = QLabel(NedTagDialogWindow)
        self.nametag.setObjectName(u"nametag")
        self.nametag.setMinimumSize(QSize(0, 0))
        self.nametag.setMaximumSize(QSize(16777215, 16))
        self.nametag.setStyleSheet(u"font-weight: bold;")
        self.nametag.setTextFormat(Qt.AutoText)
        self.nametag.setScaledContents(False)

        self.verticalLayout.addWidget(self.nametag)

        self.lineedit_nametag = QLineEdit(NedTagDialogWindow)
        self.lineedit_nametag.setObjectName(u"lineedit_nametag")

        self.verticalLayout.addWidget(self.lineedit_nametag)

        self.titletag = QLabel(NedTagDialogWindow)
        self.titletag.setObjectName(u"titletag")
        self.titletag.setMinimumSize(QSize(0, 0))
        self.titletag.setMaximumSize(QSize(16777215, 16))
        self.titletag.setStyleSheet(u"font-weight: bold;")
        self.titletag.setTextFormat(Qt.AutoText)
        self.titletag.setScaledContents(False)

        self.verticalLayout.addWidget(self.titletag)

        self.lineedit_titletag = QLineEdit(NedTagDialogWindow)
        self.lineedit_titletag.setObjectName(u"lineedit_titletag")

        self.verticalLayout.addWidget(self.lineedit_titletag)

        self.typetag = QLabel(NedTagDialogWindow)
        self.typetag.setObjectName(u"typetag")
        self.typetag.setMinimumSize(QSize(0, 0))
        self.typetag.setMaximumSize(QSize(16777215, 16))
        self.typetag.setStyleSheet(u"font-weight: bold;")
        self.typetag.setTextFormat(Qt.AutoText)
        self.typetag.setScaledContents(False)

        self.verticalLayout.addWidget(self.typetag)

        self.combox_typetag = QComboBox(NedTagDialogWindow)
        self.combox_typetag.setObjectName(u"combox_typetag")

        self.verticalLayout.addWidget(self.combox_typetag)

        self.line = QFrame(NedTagDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.vbl_additional_info = QVBoxLayout()
        self.vbl_additional_info.setSpacing(0)
        self.vbl_additional_info.setObjectName(u"vbl_additional_info")

        self.verticalLayout.addLayout(self.vbl_additional_info)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nestag = QPushButton(NedTagDialogWindow)
        self.btn_nestag.setObjectName(u"btn_nestag")

        self.hl_addsaveclose.addWidget(self.btn_nestag)

        self.btn_close = QPushButton(NedTagDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedTagDialogWindow)

        QMetaObject.connectSlotsByName(NedTagDialogWindow)
    # setupUi

    def retranslateUi(self, NedTagDialogWindow):
        NedTagDialogWindow.setWindowTitle(QCoreApplication.translate("NedTagDialogWindow", u"Dialog", None))
        self.nametag.setText(QCoreApplication.translate("NedTagDialogWindow", u"<html><head/><body><p>\u0422\u0435\u0433</p></body></html>", None))
        self.lineedit_nametag.setText("")
        self.titletag.setText(QCoreApplication.translate("NedTagDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u044d\u0433\u0430</p></body></html>", None))
        self.lineedit_titletag.setText("")
        self.typetag.setText(QCoreApplication.translate("NedTagDialogWindow", u"<html><head/><body><p>\u0422\u0438\u043f \u0442\u044d\u0433\u0430</p></body></html>", None))
        self.btn_nestag.setText(QCoreApplication.translate("NedTagDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u044d\u0433", None))
        self.btn_close.setText(QCoreApplication.translate("NedTagDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

