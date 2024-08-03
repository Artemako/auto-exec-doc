# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pageslistsialogwindow.ui'
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
    QLabel, QListView, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_PagesListDialogWindow(object):
    def setupUi(self, PagesListDialogWindow):
        if not PagesListDialogWindow.objectName():
            PagesListDialogWindow.setObjectName(u"PagesListDialogWindow")
        PagesListDialogWindow.resize(400, 400)
        PagesListDialogWindow.setMaximumSize(QSize(16777215, 720))
        self.verticalLayout = QVBoxLayout(PagesListDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_form = QLabel(PagesListDialogWindow)
        self.label_form.setObjectName(u"label_form")

        self.verticalLayout.addWidget(self.label_form)

        self.combox_forms = QComboBox(PagesListDialogWindow)
        self.combox_forms.setObjectName(u"combox_forms")

        self.verticalLayout.addWidget(self.combox_forms)

        self.label_template = QLabel(PagesListDialogWindow)
        self.label_template.setObjectName(u"label_template")

        self.verticalLayout.addWidget(self.label_template)

        self.lw_templates = QListWidget(PagesListDialogWindow)
        self.lw_templates.setObjectName(u"lw_templates")

        self.verticalLayout.addWidget(self.lw_templates)

        self.btn_add_template = QPushButton(PagesListDialogWindow)
        self.btn_add_template.setObjectName(u"btn_add_template")

        self.verticalLayout.addWidget(self.btn_add_template)

        self.label_pages = QLabel(PagesListDialogWindow)
        self.label_pages.setObjectName(u"label_pages")

        self.verticalLayout.addWidget(self.label_pages)

        self.listView = QListView(PagesListDialogWindow)
        self.listView.setObjectName(u"listView")

        self.verticalLayout.addWidget(self.listView)

        self.btn_add_page = QPushButton(PagesListDialogWindow)
        self.btn_add_page.setObjectName(u"btn_add_page")

        self.verticalLayout.addWidget(self.btn_add_page)

        self.line = QFrame(PagesListDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.btn_close = QPushButton(PagesListDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.verticalLayout.addWidget(self.btn_close)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(6, 1)

        self.retranslateUi(PagesListDialogWindow)

        QMetaObject.connectSlotsByName(PagesListDialogWindow)
    # setupUi

    def retranslateUi(self, PagesListDialogWindow):
        PagesListDialogWindow.setWindowTitle(QCoreApplication.translate("PagesListDialogWindow", u"Dialog", None))
        self.label_form.setText(QCoreApplication.translate("PagesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0424\u043e\u0440\u043c\u0430</span></p></body></html>", None))
        self.label_template.setText(QCoreApplication.translate("PagesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0428\u0430\u0431\u043b\u043e\u043d\u044b</span></p></body></html>", None))
        self.btn_add_template.setText(QCoreApplication.translate("PagesListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d", None))
        self.label_pages.setText(QCoreApplication.translate("PagesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b</span></p></body></html>", None))
        self.btn_add_page.setText(QCoreApplication.translate("PagesListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443", None))
        self.btn_close.setText(QCoreApplication.translate("PagesListDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

