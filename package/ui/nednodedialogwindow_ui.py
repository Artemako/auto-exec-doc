# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nednodedialogwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_NedNodeDialogWindow(object):
    def setupUi(self, NedNodeDialogWindow):
        if not NedNodeDialogWindow.objectName():
            NedNodeDialogWindow.setObjectName(u"NedNodeDialogWindow")
        NedNodeDialogWindow.resize(530, 130)
        self.verticalLayout = QVBoxLayout(NedNodeDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.namenode = QLabel(NedNodeDialogWindow)
        self.namenode.setObjectName(u"namenode")
        self.namenode.setMinimumSize(QSize(0, 0))
        self.namenode.setMaximumSize(QSize(16777215, 16))
        self.namenode.setStyleSheet(u"font-weight: bold;")
        self.namenode.setTextFormat(Qt.AutoText)
        self.namenode.setScaledContents(False)

        self.verticalLayout.addWidget(self.namenode)

        self.lineedit_namenode = QLineEdit(NedNodeDialogWindow)
        self.lineedit_namenode.setObjectName(u"lineedit_namenode")

        self.verticalLayout.addWidget(self.lineedit_namenode)

        self.hl_placement = QHBoxLayout()
        self.hl_placement.setObjectName(u"hl_placement")
        self.label_placement = QLabel(NedNodeDialogWindow)
        self.label_placement.setObjectName(u"label_placement")

        self.hl_placement.addWidget(self.label_placement)

        self.combox_parent = QComboBox(NedNodeDialogWindow)
        self.combox_parent.setObjectName(u"combox_parent")

        self.hl_placement.addWidget(self.combox_parent)

        self.combox_neighboor = QComboBox(NedNodeDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_placement.addWidget(self.combox_neighboor)

        self.hl_placement.setStretch(1, 1)
        self.hl_placement.setStretch(2, 1)

        self.verticalLayout.addLayout(self.hl_placement)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nestag = QPushButton(NedNodeDialogWindow)
        self.btn_nestag.setObjectName(u"btn_nestag")

        self.hl_addsaveclose.addWidget(self.btn_nestag)

        self.btn_close = QPushButton(NedNodeDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(NedNodeDialogWindow)

        QMetaObject.connectSlotsByName(NedNodeDialogWindow)
    # setupUi

    def retranslateUi(self, NedNodeDialogWindow):
        NedNodeDialogWindow.setWindowTitle(QCoreApplication.translate("NedNodeDialogWindow", u"Dialog", None))
        self.namenode.setText(QCoreApplication.translate("NedNodeDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ...</p></body></html>", None))
        self.lineedit_namenode.setText("")
        self.label_placement.setText(QCoreApplication.translate("NedNodeDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u0432\u043d\u0443\u0442\u0440\u0438 ", None))
        self.btn_nestag.setText(QCoreApplication.translate("NedNodeDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedNodeDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

