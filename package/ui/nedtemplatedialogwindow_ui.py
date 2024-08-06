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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_NedTemplateDialogWindow(object):
    def setupUi(self, NedTemplateDialogWindow):
        if not NedTemplateDialogWindow.objectName():
            NedTemplateDialogWindow.setObjectName(u"NedTemplateDialogWindow")
        NedTemplateDialogWindow.resize(425, 100)
        self.verticalLayout = QVBoxLayout(NedTemplateDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
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

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nestag = QPushButton(NedTemplateDialogWindow)
        self.btn_nestag.setObjectName(u"btn_nestag")

        self.hl_addsaveclose.addWidget(self.btn_nestag)

        self.btn_close = QPushButton(NedTemplateDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(NedTemplateDialogWindow)

        QMetaObject.connectSlotsByName(NedTemplateDialogWindow)
    # setupUi

    def retranslateUi(self, NedTemplateDialogWindow):
        NedTemplateDialogWindow.setWindowTitle(QCoreApplication.translate("NedTemplateDialogWindow", u"Dialog", None))
        self.label_nametemplate.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ...</p></body></html>", None))
        self.lineedit_nametemplate.setText("")
        self.btn_nestag.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

