# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formlistdialogwindow.ui'
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
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_FormListDialogWindow(object):
    def setupUi(self, FormListDialogWindow):
        if not FormListDialogWindow.objectName():
            FormListDialogWindow.setObjectName(u"FormListDialogWindow")
        FormListDialogWindow.resize(350, 350)
        self.verticalLayout = QVBoxLayout(FormListDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_nametable = QLabel(FormListDialogWindow)
        self.label_nametable.setObjectName(u"label_nametable")

        self.verticalLayout.addWidget(self.label_nametable)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.add_button = QPushButton(FormListDialogWindow)
        self.add_button.setObjectName(u"add_button")

        self.buttons_layout.addWidget(self.add_button)

        self.delete_button = QPushButton(FormListDialogWindow)
        self.delete_button.setObjectName(u"delete_button")

        self.buttons_layout.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.buttons_layout)

        self.lw = QListWidget(FormListDialogWindow)
        self.lw.setObjectName(u"lw")

        self.verticalLayout.addWidget(self.lw)

        self.hl_moving = QHBoxLayout()
        self.hl_moving.setObjectName(u"hl_moving")
        self.label_move = QLabel(FormListDialogWindow)
        self.label_move.setObjectName(u"label_move")

        self.hl_moving.addWidget(self.label_move)

        self.btn_up = QPushButton(FormListDialogWindow)
        self.btn_up.setObjectName(u"btn_up")

        self.hl_moving.addWidget(self.btn_up)

        self.btn_down = QPushButton(FormListDialogWindow)
        self.btn_down.setObjectName(u"btn_down")

        self.hl_moving.addWidget(self.btn_down)

        self.hl_moving.setStretch(1, 1)
        self.hl_moving.setStretch(2, 1)

        self.verticalLayout.addLayout(self.hl_moving)

        self.line = QFrame(FormListDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_saveclose = QHBoxLayout()
        self.hl_saveclose.setObjectName(u"hl_saveclose")
        self.btn_save = QPushButton(FormListDialogWindow)
        self.btn_save.setObjectName(u"btn_save")

        self.hl_saveclose.addWidget(self.btn_save)

        self.btn_close = QPushButton(FormListDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.hl_saveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_saveclose)


        self.retranslateUi(FormListDialogWindow)

        QMetaObject.connectSlotsByName(FormListDialogWindow)
    # setupUi

    def retranslateUi(self, FormListDialogWindow):
        FormListDialogWindow.setWindowTitle(QCoreApplication.translate("FormListDialogWindow", u"Dialog", None))
        self.label_nametable.setText(QCoreApplication.translate("FormListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">TextLabel</span></p></body></html>", None))
        self.add_button.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.delete_button.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.label_move.setText(QCoreApplication.translate("FormListDialogWindow", u"\u041f\u0435\u0440\u0435\u043c\u0435\u0441\u0442\u0438\u0442\u044c", None))
        self.btn_up.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0412\u0432\u0435\u0440\u0445", None))
        self.btn_down.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0412\u043d\u0438\u0437", None))
        self.btn_save.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("FormListDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi
