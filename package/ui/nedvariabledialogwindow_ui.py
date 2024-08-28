# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedvariabledialogwindow.ui'
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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_NedVariableDialogWindow(object):
    def setupUi(self, NedVariableDialogWindow):
        if not NedVariableDialogWindow.objectName():
            NedVariableDialogWindow.setObjectName(u"NedVariableDialogWindow")
        NedVariableDialogWindow.resize(530, 241)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NedVariableDialogWindow.sizePolicy().hasHeightForWidth())
        NedVariableDialogWindow.setSizePolicy(sizePolicy)
        NedVariableDialogWindow.setBaseSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(NedVariableDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.namevariable = QLabel(NedVariableDialogWindow)
        self.namevariable.setObjectName(u"namevariable")
        self.namevariable.setMinimumSize(QSize(0, 0))
        self.namevariable.setMaximumSize(QSize(16777215, 16))
        self.namevariable.setStyleSheet(u"font-weight: bold;")
        self.namevariable.setTextFormat(Qt.AutoText)
        self.namevariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.namevariable)

        self.lineedit_namevariable = QLineEdit(NedVariableDialogWindow)
        self.lineedit_namevariable.setObjectName(u"lineedit_namevariable")

        self.verticalLayout.addWidget(self.lineedit_namevariable)

        self.titlevariable = QLabel(NedVariableDialogWindow)
        self.titlevariable.setObjectName(u"titlevariable")
        self.titlevariable.setMinimumSize(QSize(0, 0))
        self.titlevariable.setMaximumSize(QSize(16777215, 16))
        self.titlevariable.setStyleSheet(u"font-weight: bold;")
        self.titlevariable.setTextFormat(Qt.AutoText)
        self.titlevariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.titlevariable)

        self.lineedit_titlevariable = QLineEdit(NedVariableDialogWindow)
        self.lineedit_titlevariable.setObjectName(u"lineedit_titlevariable")

        self.verticalLayout.addWidget(self.lineedit_titlevariable)

        self.typevariable = QLabel(NedVariableDialogWindow)
        self.typevariable.setObjectName(u"typevariable")
        self.typevariable.setMinimumSize(QSize(0, 0))
        self.typevariable.setMaximumSize(QSize(16777215, 16))
        self.typevariable.setStyleSheet(u"font-weight: bold;")
        self.typevariable.setTextFormat(Qt.AutoText)
        self.typevariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.typevariable)

        self.combox_typevariable = QComboBox(NedVariableDialogWindow)
        self.combox_typevariable.setObjectName(u"combox_typevariable")

        self.verticalLayout.addWidget(self.combox_typevariable)

        self.hl_placement = QHBoxLayout()
        self.hl_placement.setObjectName(u"hl_placement")
        self.label_placement = QLabel(NedVariableDialogWindow)
        self.label_placement.setObjectName(u"label_placement")

        self.hl_placement.addWidget(self.label_placement)

        self.combox_neighboor = QComboBox(NedVariableDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_placement.addWidget(self.combox_neighboor)

        self.hl_placement.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_placement)

        self.line = QFrame(NedVariableDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.vbl_additional_info = QVBoxLayout()
        self.vbl_additional_info.setSpacing(0)
        self.vbl_additional_info.setObjectName(u"vbl_additional_info")

        self.verticalLayout.addLayout(self.vbl_additional_info)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nesvariable = QPushButton(NedVariableDialogWindow)
        self.btn_nesvariable.setObjectName(u"btn_nesvariable")

        self.hl_addsaveclose.addWidget(self.btn_nesvariable)

        self.btn_close = QPushButton(NedVariableDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)

        self.verticalLayout.setStretch(8, 1)

        self.retranslateUi(NedVariableDialogWindow)

        QMetaObject.connectSlotsByName(NedVariableDialogWindow)
    # setupUi

    def retranslateUi(self, NedVariableDialogWindow):
        NedVariableDialogWindow.setWindowTitle(QCoreApplication.translate("NedVariableDialogWindow", u"\u0420\u0435\u0434\u043a\u0430\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439", None))
        self.namevariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"<html><head/><body><p>\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f</p></body></html>", None))
        self.lineedit_namevariable.setText("")
        self.titlevariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439</p></body></html>", None))
        self.lineedit_titlevariable.setText("")
        self.typevariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"<html><head/><body><p>\u0422\u0438\u043f \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439</p></body></html>", None))
        self.label_placement.setText(QCoreApplication.translate("NedVariableDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435", None))
        self.btn_nesvariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e", None))
        self.btn_close.setText(QCoreApplication.translate("NedVariableDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

