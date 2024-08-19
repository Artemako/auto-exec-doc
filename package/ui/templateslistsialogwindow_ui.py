# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'templateslistsialogwindow.ui'
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
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget)
import resources_rc

class Ui_TemplatesListDialogWindow(object):
    def setupUi(self, TemplatesListDialogWindow):
        if not TemplatesListDialogWindow.objectName():
            TemplatesListDialogWindow.setObjectName(u"TemplatesListDialogWindow")
        TemplatesListDialogWindow.resize(400, 600)
        TemplatesListDialogWindow.setMinimumSize(QSize(300, 0))
        TemplatesListDialogWindow.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_3 = QVBoxLayout(TemplatesListDialogWindow)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_form = QLabel(TemplatesListDialogWindow)
        self.label_form.setObjectName(u"label_form")

        self.verticalLayout_3.addWidget(self.label_form)

        self.combox_forms = QComboBox(TemplatesListDialogWindow)
        self.combox_forms.setObjectName(u"combox_forms")

        self.verticalLayout_3.addWidget(self.combox_forms)

        self.splitter = QSplitter(TemplatesListDialogWindow)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vl_templates = QVBoxLayout(self.verticalLayoutWidget)
        self.vl_templates.setObjectName(u"vl_templates")
        self.vl_templates.setContentsMargins(0, 0, 0, 0)
        self.label_template = QLabel(self.verticalLayoutWidget)
        self.label_template.setObjectName(u"label_template")

        self.vl_templates.addWidget(self.label_template)

        self.lw_templates = QListWidget(self.verticalLayoutWidget)
        self.lw_templates.setObjectName(u"lw_templates")

        self.vl_templates.addWidget(self.lw_templates)

        self.btn_add_template = QPushButton(self.verticalLayoutWidget)
        self.btn_add_template.setObjectName(u"btn_add_template")

        self.vl_templates.addWidget(self.btn_add_template)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.vl_pages = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vl_pages.setObjectName(u"vl_pages")
        self.vl_pages.setContentsMargins(0, 0, 0, 0)
        self.label_pages = QLabel(self.verticalLayoutWidget_2)
        self.label_pages.setObjectName(u"label_pages")

        self.vl_pages.addWidget(self.label_pages)

        self.lw_pages = QListWidget(self.verticalLayoutWidget_2)
        self.lw_pages.setObjectName(u"lw_pages")

        self.vl_pages.addWidget(self.lw_pages)

        self.btn_add_page = QPushButton(self.verticalLayoutWidget_2)
        self.btn_add_page.setObjectName(u"btn_add_page")

        self.vl_pages.addWidget(self.btn_add_page)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_3.addWidget(self.splitter)

        self.line = QFrame(TemplatesListDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.btn_close = QPushButton(TemplatesListDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.verticalLayout_3.addWidget(self.btn_close)


        self.retranslateUi(TemplatesListDialogWindow)

        QMetaObject.connectSlotsByName(TemplatesListDialogWindow)
    # setupUi

    def retranslateUi(self, TemplatesListDialogWindow):
        TemplatesListDialogWindow.setWindowTitle(QCoreApplication.translate("TemplatesListDialogWindow", u"Dialog", None))
        self.label_form.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0424\u043e\u0440\u043c\u0430</span></p></body></html>", None))
        self.label_template.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0428\u0430\u0431\u043b\u043e\u043d\u044b</span></p></body></html>", None))
        self.btn_add_template.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d", None))
        self.label_pages.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b</span></p></body></html>", None))
        self.btn_add_page.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443", None))
        self.btn_close.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

