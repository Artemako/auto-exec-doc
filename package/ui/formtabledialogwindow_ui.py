# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formtabledialogwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_FormTableDialogWindow(object):
    def setupUi(self, FormTableDialogWindow):
        if not FormTableDialogWindow.objectName():
            FormTableDialogWindow.setObjectName(u"FormTableDialogWindow")
        FormTableDialogWindow.resize(600, 400)
        self.verticalLayout = QVBoxLayout(FormTableDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_nametable = QLabel(FormTableDialogWindow)
        self.label_nametable.setObjectName(u"label_nametable")

        self.verticalLayout.addWidget(self.label_nametable)

        self.table = QTableWidget(FormTableDialogWindow)
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.add_button = QPushButton(FormTableDialogWindow)
        self.add_button.setObjectName(u"add_button")

        self.buttons_layout.addWidget(self.add_button)

        self.delete_button = QPushButton(FormTableDialogWindow)
        self.delete_button.setObjectName(u"delete_button")

        self.buttons_layout.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.buttons_layout)

        self.line = QFrame(FormTableDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_saveclose = QHBoxLayout()
        self.hl_saveclose.setObjectName(u"hl_saveclose")
        self.btn_save = QPushButton(FormTableDialogWindow)
        self.btn_save.setObjectName(u"btn_save")

        self.hl_saveclose.addWidget(self.btn_save)

        self.btn_close = QPushButton(FormTableDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.hl_saveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_saveclose)


        self.retranslateUi(FormTableDialogWindow)

        QMetaObject.connectSlotsByName(FormTableDialogWindow)
    # setupUi

    def retranslateUi(self, FormTableDialogWindow):
        FormTableDialogWindow.setWindowTitle(QCoreApplication.translate("FormTableDialogWindow", u"Dialog", None))
        self.label_nametable.setText(QCoreApplication.translate("FormTableDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">TextLabel</span></p></body></html>", None))
        self.add_button.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
        self.delete_button.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
        self.btn_save.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

