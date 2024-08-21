# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neddocxpdfdialogwindow.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_NedDocxPdfDialogWindow(object):
    def setupUi(self, NedDocxPdfDialogWindow):
        if not NedDocxPdfDialogWindow.objectName():
            NedDocxPdfDialogWindow.setObjectName(u"NedDocxPdfDialogWindow")
        NedDocxPdfDialogWindow.resize(450, 450)
        self.verticalLayout = QVBoxLayout(NedDocxPdfDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_typefile = QLabel(NedDocxPdfDialogWindow)
        self.label_typefile.setObjectName(u"label_typefile")

        self.verticalLayout.addWidget(self.label_typefile)

        self.combox_typefile = QComboBox(NedDocxPdfDialogWindow)
        self.combox_typefile.setObjectName(u"combox_typefile")

        self.verticalLayout.addWidget(self.combox_typefile)

        self.label_document = QLabel(NedDocxPdfDialogWindow)
        self.label_document.setObjectName(u"label_document")
        self.label_document.setMinimumSize(QSize(0, 0))
        self.label_document.setMaximumSize(QSize(16777215, 16))
        self.label_document.setStyleSheet(u"font-weight: bold;")
        self.label_document.setTextFormat(Qt.AutoText)
        self.label_document.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_document)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_select = QPushButton(NedDocxPdfDialogWindow)
        self.btn_select.setObjectName(u"btn_select")

        self.horizontalLayout.addWidget(self.btn_select)

        self.btn_open_docx = QPushButton(NedDocxPdfDialogWindow)
        self.btn_open_docx.setObjectName(u"btn_open_docx")

        self.horizontalLayout.addWidget(self.btn_open_docx)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_file = QLabel(NedDocxPdfDialogWindow)
        self.label_file.setObjectName(u"label_file")
        self.label_file.setStyleSheet(u"font-style: italic;")

        self.verticalLayout.addWidget(self.label_file)

        self.label_variables = QLabel(NedDocxPdfDialogWindow)
        self.label_variables.setObjectName(u"label_variables")
        self.label_variables.setMinimumSize(QSize(0, 0))
        self.label_variables.setMaximumSize(QSize(16777215, 16))
        self.label_variables.setStyleSheet(u"font-weight: bold;")
        self.label_variables.setTextFormat(Qt.AutoText)
        self.label_variables.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_variables)

        self.tw_variables = QTableWidget(NedDocxPdfDialogWindow)
        self.tw_variables.setObjectName(u"tw_variables")

        self.verticalLayout.addWidget(self.tw_variables)

        self.btn_findvariables = QPushButton(NedDocxPdfDialogWindow)
        self.btn_findvariables.setObjectName(u"btn_findvariables")

        self.verticalLayout.addWidget(self.btn_findvariables)

        self.line = QFrame(NedDocxPdfDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nedvariable = QPushButton(NedDocxPdfDialogWindow)
        self.btn_nedvariable.setObjectName(u"btn_nedvariable")

        self.hl_addsaveclose.addWidget(self.btn_nedvariable)

        self.btn_close = QPushButton(NedDocxPdfDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedDocxPdfDialogWindow)

        QMetaObject.connectSlotsByName(NedDocxPdfDialogWindow)
    # setupUi

    def retranslateUi(self, NedDocxPdfDialogWindow):
        NedDocxPdfDialogWindow.setWindowTitle(QCoreApplication.translate("NedDocxPdfDialogWindow", u"Dialog", None))
        self.label_typefile.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0438\u043f \u0444\u0430\u0439\u043b\u0430</span></p></body></html>", None))
        self.label_document.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"<html><head/><body><p>\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442</p></body></html>", None))
        self.btn_select.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c docx", None))
        self.btn_open_docx.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0438 docx", None))
        self.label_file.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b", None))
        self.label_variables.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0439\u0434\u0435\u043d\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435</p></body></html>", None))
        self.btn_findvariables.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u041f\u043e\u0438\u0441\u043a \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445 \u0432 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u043c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0435", None))
        self.btn_nedvariable.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

