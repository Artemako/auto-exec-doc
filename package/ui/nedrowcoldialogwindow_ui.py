# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedrowcoldialogwindow.ui'
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
import resources_rc

class Ui_NedRowcolDialogWindow(object):
    def setupUi(self, NedRowcolDialogWindow):
        if not NedRowcolDialogWindow.objectName():
            NedRowcolDialogWindow.setObjectName(u"NedRowcolDialogWindow")
        NedRowcolDialogWindow.resize(530, 183)
        NedRowcolDialogWindow.setMaximumSize(QSize(16777215, 183))
        self.verticalLayout = QVBoxLayout(NedRowcolDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.label_attr = QLabel(NedRowcolDialogWindow)
        self.label_attr.setObjectName(u"label_attr")

        self.verticalLayout.addWidget(self.label_attr)

        self.lineedit_attr = QLineEdit(NedRowcolDialogWindow)
        self.lineedit_attr.setObjectName(u"lineedit_attr")

        self.verticalLayout.addWidget(self.lineedit_attr)

        self.label_rowcol = QLabel(NedRowcolDialogWindow)
        self.label_rowcol.setObjectName(u"label_rowcol")
        self.label_rowcol.setMinimumSize(QSize(0, 0))
        self.label_rowcol.setMaximumSize(QSize(16777215, 16))
        self.label_rowcol.setStyleSheet(u"font-weight: bold;")
        self.label_rowcol.setTextFormat(Qt.AutoText)
        self.label_rowcol.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_rowcol)

        self.lineedit_rowcoltitle = QLineEdit(NedRowcolDialogWindow)
        self.lineedit_rowcoltitle.setObjectName(u"lineedit_rowcoltitle")

        self.verticalLayout.addWidget(self.lineedit_rowcoltitle)

        self.hl_placement = QHBoxLayout()
        self.hl_placement.setObjectName(u"hl_placement")
        self.label_placement = QLabel(NedRowcolDialogWindow)
        self.label_placement.setObjectName(u"label_placement")

        self.hl_placement.addWidget(self.label_placement)

        self.combox_neighboor = QComboBox(NedRowcolDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_placement.addWidget(self.combox_neighboor)

        self.hl_placement.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_placement)

        self.line = QFrame(NedRowcolDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nestag = QPushButton(NedRowcolDialogWindow)
        self.btn_nestag.setObjectName(u"btn_nestag")

        self.hl_addsaveclose.addWidget(self.btn_nestag)

        self.btn_close = QPushButton(NedRowcolDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedRowcolDialogWindow)

        QMetaObject.connectSlotsByName(NedRowcolDialogWindow)
    # setupUi

    def retranslateUi(self, NedRowcolDialogWindow):
        NedRowcolDialogWindow.setWindowTitle(QCoreApplication.translate("NedRowcolDialogWindow", u"Dialog", None))
        self.label_attr.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0410\u0442\u0440\u0438\u0431\u0443\u0442 \u0442\u044d\u0433\u0430</span></p></body></html>", None))
        self.label_rowcol.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ...</p></body></html>", None))
        self.lineedit_rowcoltitle.setText("")
        self.label_placement.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435 ", None))
        self.btn_nestag.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

