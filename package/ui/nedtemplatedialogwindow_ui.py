# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedtemplatedialogwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_NedTemplateDialogWindow(object):
    def setupUi(self, NedTemplateDialogWindow):
        if not NedTemplateDialogWindow.objectName():
            NedTemplateDialogWindow.setObjectName(u"NedTemplateDialogWindow")
        NedTemplateDialogWindow.resize(500, 168)
        self.verticalLayout = QVBoxLayout(NedTemplateDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.label_nametemplate = QLabel(NedTemplateDialogWindow)
        self.label_nametemplate.setObjectName(u"label_nametemplate")
        self.label_nametemplate.setMinimumSize(QSize(0, 0))
        self.label_nametemplate.setMaximumSize(QSize(16777215, 16))
        self.label_nametemplate.setStyleSheet(u"font-weight: bold;")
        self.label_nametemplate.setTextFormat(Qt.AutoText)
        self.label_nametemplate.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_nametemplate)

        self.lineedit_nametemplate = QLineEdit(NedTemplateDialogWindow)
        self.lineedit_nametemplate.setObjectName(u"lineedit_nametemplate")

        self.verticalLayout.addWidget(self.lineedit_nametemplate)

        self.line_2 = QFrame(NedTemplateDialogWindow)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.hl_copytemplate = QHBoxLayout()
        self.hl_copytemplate.setObjectName(u"hl_copytemplate")
        self.label_copyfrom = QLabel(NedTemplateDialogWindow)
        self.label_copyfrom.setObjectName(u"label_copyfrom")

        self.hl_copytemplate.addWidget(self.label_copyfrom)

        self.combox_templates = QComboBox(NedTemplateDialogWindow)
        self.combox_templates.setObjectName(u"combox_templates")

        self.hl_copytemplate.addWidget(self.combox_templates)

        self.hl_copytemplate.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_copytemplate)

        self.checkbox_is_active = QCheckBox(NedTemplateDialogWindow)
        self.checkbox_is_active.setObjectName(u"checkbox_is_active")

        self.verticalLayout.addWidget(self.checkbox_is_active)

        self.line = QFrame(NedTemplateDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nesvariable = QPushButton(NedTemplateDialogWindow)
        self.btn_nesvariable.setObjectName(u"btn_nesvariable")

        self.hl_addsaveclose.addWidget(self.btn_nesvariable)

        self.btn_close = QPushButton(NedTemplateDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedTemplateDialogWindow)

        QMetaObject.connectSlotsByName(NedTemplateDialogWindow)
    # setupUi

    def retranslateUi(self, NedTemplateDialogWindow):
        NedTemplateDialogWindow.setWindowTitle(QCoreApplication.translate("NedTemplateDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u0430", None))
        self.label_nametemplate.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ...</p></body></html>", None))
        self.lineedit_nametemplate.setText("")
        self.label_copyfrom.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u0441 ", None))
        self.checkbox_is_active.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u043c \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u043c \u0444\u043e\u0440\u043c\u044b", None))
        self.btn_nesvariable.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

