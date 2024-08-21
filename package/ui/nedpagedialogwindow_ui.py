# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedpagedialogwindow.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_NedPageDialogWindow(object):
    def setupUi(self, NedPageDialogWindow):
        if not NedPageDialogWindow.objectName():
            NedPageDialogWindow.setObjectName(u"NedPageDialogWindow")
        NedPageDialogWindow.resize(450, 450)
        self.verticalLayout = QVBoxLayout(NedPageDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.label_namepage = QLabel(NedPageDialogWindow)
        self.label_namepage.setObjectName(u"label_namepage")
        self.label_namepage.setMinimumSize(QSize(0, 0))
        self.label_namepage.setMaximumSize(QSize(16777215, 16))
        self.label_namepage.setStyleSheet(u"font-weight: bold;")
        self.label_namepage.setTextFormat(Qt.AutoText)
        self.label_namepage.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_namepage)

        self.lineedit_namepage = QLineEdit(NedPageDialogWindow)
        self.lineedit_namepage.setObjectName(u"lineedit_namepage")

        self.verticalLayout.addWidget(self.lineedit_namepage)

        self.hl_order = QHBoxLayout()
        self.hl_order.setObjectName(u"hl_order")
        self.label_after = QLabel(NedPageDialogWindow)
        self.label_after.setObjectName(u"label_after")

        self.hl_order.addWidget(self.label_after)

        self.combox_neighboor = QComboBox(NedPageDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_order.addWidget(self.combox_neighboor)

        self.hl_order.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_order)

        self.line_2 = QFrame(NedPageDialogWindow)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_document = QLabel(NedPageDialogWindow)
        self.label_document.setObjectName(u"label_document")
        self.label_document.setMinimumSize(QSize(0, 0))
        self.label_document.setMaximumSize(QSize(16777215, 16))
        self.label_document.setStyleSheet(u"font-weight: bold;")
        self.label_document.setTextFormat(Qt.AutoText)
        self.label_document.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_document)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_select = QPushButton(NedPageDialogWindow)
        self.btn_select.setObjectName(u"btn_select")

        self.horizontalLayout.addWidget(self.btn_select)

        self.btn_open_docx = QPushButton(NedPageDialogWindow)
        self.btn_open_docx.setObjectName(u"btn_open_docx")

        self.horizontalLayout.addWidget(self.btn_open_docx)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_file = QLabel(NedPageDialogWindow)
        self.label_file.setObjectName(u"label_file")
        self.label_file.setStyleSheet(u"font-style: italic;")

        self.verticalLayout.addWidget(self.label_file)

        self.label_variables = QLabel(NedPageDialogWindow)
        self.label_variables.setObjectName(u"label_variables")
        self.label_variables.setMinimumSize(QSize(0, 0))
        self.label_variables.setMaximumSize(QSize(16777215, 16))
        self.label_variables.setStyleSheet(u"font-weight: bold;")
        self.label_variables.setTextFormat(Qt.AutoText)
        self.label_variables.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_variables)

        self.tw_variables = QTableWidget(NedPageDialogWindow)
        self.tw_variables.setObjectName(u"tw_variables")

        self.verticalLayout.addWidget(self.tw_variables)

        self.btn_findvariables = QPushButton(NedPageDialogWindow)
        self.btn_findvariables.setObjectName(u"btn_findvariables")

        self.verticalLayout.addWidget(self.btn_findvariables)

        self.line = QFrame(NedPageDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nedvariable = QPushButton(NedPageDialogWindow)
        self.btn_nedvariable.setObjectName(u"btn_nedvariable")

        self.hl_addsaveclose.addWidget(self.btn_nedvariable)

        self.btn_close = QPushButton(NedPageDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedPageDialogWindow)

        QMetaObject.connectSlotsByName(NedPageDialogWindow)
    # setupUi

    def retranslateUi(self, NedPageDialogWindow):
        NedPageDialogWindow.setWindowTitle(QCoreApplication.translate("NedPageDialogWindow", u"Dialog", None))
        self.label_namepage.setText(QCoreApplication.translate("NedPageDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b</p></body></html>", None))
        self.lineedit_namepage.setText("")
        self.label_after.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435 ", None))
        self.label_document.setText(QCoreApplication.translate("NedPageDialogWindow", u"<html><head/><body><p>\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442 (docx \u0438\u043b\u0438 pdf)</p></body></html>", None))
        self.btn_select.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.btn_open_docx.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0438 docx", None))
        self.label_file.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0424\u0430\u0439\u043b \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d", None))
        self.label_variables.setText(QCoreApplication.translate("NedPageDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0439\u0434\u0435\u043d\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435 (\u0434\u043b\u044f docx)</p></body></html>", None))
        self.btn_findvariables.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u041f\u043e\u0438\u0441\u043a \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445 \u0432 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u043c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0435", None))
        self.btn_nedvariable.setText(QCoreApplication.translate("NedPageDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

