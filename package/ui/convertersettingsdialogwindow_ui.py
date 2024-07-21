# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'convertersettingsdialogwindow.ui'
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
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_ConverterSettingsDialogWindow(object):
    def setupUi(self, ConverterSettingsDialogWindow):
        if not ConverterSettingsDialogWindow.objectName():
            ConverterSettingsDialogWindow.setObjectName(u"ConverterSettingsDialogWindow")
        ConverterSettingsDialogWindow.resize(546, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConverterSettingsDialogWindow.sizePolicy().hasHeightForWidth())
        ConverterSettingsDialogWindow.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ConverterSettingsDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_converter = QWidget(ConverterSettingsDialogWindow)
        self.widget_converter.setObjectName(u"widget_converter")
        sizePolicy.setHeightForWidth(self.widget_converter.sizePolicy().hasHeightForWidth())
        self.widget_converter.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget_converter)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.converter = QLabel(self.widget_converter)
        self.converter.setObjectName(u"converter")
        self.converter.setMinimumSize(QSize(0, 0))
        self.converter.setMaximumSize(QSize(16777215, 16))
        self.converter.setStyleSheet(u"font-weight: bold;")
        self.converter.setTextFormat(Qt.AutoText)
        self.converter.setScaledContents(False)

        self.verticalLayout_2.addWidget(self.converter)

        self.radbtn_msword = QRadioButton(self.widget_converter)
        self.radbtn_msword.setObjectName(u"radbtn_msword")

        self.verticalLayout_2.addWidget(self.radbtn_msword)

        self.radbtn_libreoffice = QRadioButton(self.widget_converter)
        self.radbtn_libreoffice.setObjectName(u"radbtn_libreoffice")

        self.verticalLayout_2.addWidget(self.radbtn_libreoffice)


        self.horizontalLayout.addWidget(self.widget_converter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.explanation = QLabel(ConverterSettingsDialogWindow)
        self.explanation.setObjectName(u"explanation")
        self.explanation.setTextFormat(Qt.MarkdownText)
        self.explanation.setScaledContents(False)
        self.explanation.setWordWrap(False)

        self.horizontalLayout.addWidget(self.explanation)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_save = QPushButton(ConverterSettingsDialogWindow)
        self.btn_save.setObjectName(u"btn_save")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_save.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.btn_save)

        self.btn_close = QPushButton(ConverterSettingsDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(ConverterSettingsDialogWindow)

        QMetaObject.connectSlotsByName(ConverterSettingsDialogWindow)
    # setupUi

    def retranslateUi(self, ConverterSettingsDialogWindow):
        ConverterSettingsDialogWindow.setWindowTitle(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0435\u0440\u0430", None))
        self.converter.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"<html><head/><body><p>\u041a\u043e\u043d\u0432\u0435\u0440\u0442\u0435\u0440</p></body></html>", None))
        self.radbtn_msword.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"Microsoft Word", None))
        self.radbtn_libreoffice.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"LibreOffice", None))
        self.explanation.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0443, \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043d\u0443\u044e \u043d\u0430 \u0434\u0430\u043d\u043d\u043e\u043c \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0435:\n"
" - \u0414\u043b\u044f \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430 \u0432 \u0440\u0435\u0436\u0438\u043c\u0435 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0432\u0440\u0435\u043c\u0435\u043d\u0438\n"
" - \u0414\u043b\u044f \u044d\u043a\u0441\u043f\u043e\u0440\u0442\u0430 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430 \u0432 PDF", None))
        self.btn_save.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

