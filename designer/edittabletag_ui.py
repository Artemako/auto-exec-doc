# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edittabletag.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(512, 251)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.columns = QLabel(Form)
        self.columns.setObjectName(u"columns")
        self.columns.setMinimumSize(QSize(0, 0))
        self.columns.setMaximumSize(QSize(16777215, 16))
        self.columns.setStyleSheet(u"font-weight: bold;")
        self.columns.setTextFormat(Qt.AutoText)
        self.columns.setScaledContents(False)

        self.verticalLayout.addWidget(self.columns)

        self.treeWidget = QTreeWidget(Form)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.columns.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u0421\u0442\u043e\u043b\u0431\u0446\u044b</p></body></html>", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Form", u"\u041d\u043e\u0432\u044b\u0439 \u0441\u0442\u043e\u043b\u0431\u0435\u0446", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u043e\u043b\u0431\u0446\u0430", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"\u041f\u043e\u0440\u044f\u0434", None));
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
    # retranslateUi

