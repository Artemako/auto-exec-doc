# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'customitemqlistwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)
import resources_rc

class Ui_CustomItemQListWidget(object):
    def setupUi(self, CustomItemQListWidget):
        if not CustomItemQListWidget.objectName():
            CustomItemQListWidget.setObjectName(u"CustomItemQListWidget")
        CustomItemQListWidget.resize(211, 30)
        self.horizontalLayout = QHBoxLayout(CustomItemQListWidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.label_text = QLabel(CustomItemQListWidget)
        self.label_text.setObjectName(u"label_text")

        self.horizontalLayout.addWidget(self.label_text)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_edit = QPushButton(CustomItemQListWidget)
        self.btn_edit.setObjectName(u"btn_edit")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/pen.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_edit.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton(CustomItemQListWidget)
        self.btn_delete.setObjectName(u"btn_delete")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_delete.setIcon(icon1)

        self.horizontalLayout.addWidget(self.btn_delete)


        self.retranslateUi(CustomItemQListWidget)

        QMetaObject.connectSlotsByName(CustomItemQListWidget)
    # setupUi

    def retranslateUi(self, CustomItemQListWidget):
        CustomItemQListWidget.setWindowTitle(QCoreApplication.translate("CustomItemQListWidget", u"Form", None))
        self.label_text.setText(QCoreApplication.translate("CustomItemQListWidget", u"TextLabel", None))
        self.btn_edit.setText("")
        self.btn_delete.setText("")
    # retranslateUi

