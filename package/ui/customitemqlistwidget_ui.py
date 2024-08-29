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
    QSizePolicy, QWidget)
import resources_rc

class Ui_CustomItemQListWidget(object):
    def setupUi(self, CustomItemQListWidget):
        if not CustomItemQListWidget.objectName():
            CustomItemQListWidget.setObjectName(u"CustomItemQListWidget")
        CustomItemQListWidget.resize(416, 28)
        CustomItemQListWidget.setMinimumSize(QSize(0, 0))
        CustomItemQListWidget.setMaximumSize(QSize(1515, 16777215))
        self.horizontalLayout = QHBoxLayout(CustomItemQListWidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 2, 2, 2)
        self.label_icon = QLabel(CustomItemQListWidget)
        self.label_icon.setObjectName(u"label_icon")
        self.label_icon.setMinimumSize(QSize(24, 0))
        self.label_icon.setMaximumSize(QSize(24, 16777215))
        self.label_icon.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_icon)

        self.label_text = QLabel(CustomItemQListWidget)
        self.label_text.setObjectName(u"label_text")
        self.label_text.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.label_text)

        self.btn_edit = QPushButton(CustomItemQListWidget)
        self.btn_edit.setObjectName(u"btn_edit")
        self.btn_edit.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/white-icons/resources/white-icons/pen.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_edit.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton(CustomItemQListWidget)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setMaximumSize(QSize(16777215, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/white-icons/resources/white-icons/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_delete.setIcon(icon1)

        self.horizontalLayout.addWidget(self.btn_delete)

        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(CustomItemQListWidget)

        QMetaObject.connectSlotsByName(CustomItemQListWidget)
    # setupUi

    def retranslateUi(self, CustomItemQListWidget):
        CustomItemQListWidget.setWindowTitle(QCoreApplication.translate("CustomItemQListWidget", u"Form", None))
        self.label_icon.setText(QCoreApplication.translate("CustomItemQListWidget", u"IC", None))
        self.label_text.setText(QCoreApplication.translate("CustomItemQListWidget", u"224", None))
        self.btn_edit.setText("")
        self.btn_delete.setText("")
    # retranslateUi

