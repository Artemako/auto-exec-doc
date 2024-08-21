# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedimagevariable.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_NedImageVariable(object):
    def setupUi(self, NedImageVariable):
        if not NedImageVariable.objectName():
            NedImageVariable.setObjectName(u"NedImageVariable")
        NedImageVariable.resize(516, 173)
        self.verticalLayout = QVBoxLayout(NedImageVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title_units = QLabel(NedImageVariable)
        self.title_units.setObjectName(u"title_units")

        self.verticalLayout.addWidget(self.title_units)

        self.combox_units = QComboBox(NedImageVariable)
        self.combox_units.setObjectName(u"combox_units")

        self.verticalLayout.addWidget(self.combox_units)

        self.title_sms = QLabel(NedImageVariable)
        self.title_sms.setObjectName(u"title_sms")

        self.verticalLayout.addWidget(self.title_sms)

        self.combox_sms = QComboBox(NedImageVariable)
        self.combox_sms.setObjectName(u"combox_sms")

        self.verticalLayout.addWidget(self.combox_sms)

        self.title_wh = QLabel(NedImageVariable)
        self.title_wh.setObjectName(u"title_wh")

        self.verticalLayout.addWidget(self.title_wh)

        self.hl_width = QHBoxLayout()
        self.hl_width.setObjectName(u"hl_width")
        self.label = QLabel(NedImageVariable)
        self.label.setObjectName(u"label")

        self.hl_width.addWidget(self.label)

        self.dsb_height = QDoubleSpinBox(NedImageVariable)
        self.dsb_height.setObjectName(u"dsb_height")
        self.dsb_height.setMaximum(99999.990000000005239)

        self.hl_width.addWidget(self.dsb_height)

        self.label_2 = QLabel(NedImageVariable)
        self.label_2.setObjectName(u"label_2")

        self.hl_width.addWidget(self.label_2)

        self.dsb_width = QDoubleSpinBox(NedImageVariable)
        self.dsb_width.setObjectName(u"dsb_width")
        self.dsb_width.setMaximum(99999.990000000005239)

        self.hl_width.addWidget(self.dsb_width)

        self.hl_width.setStretch(1, 1)
        self.hl_width.setStretch(3, 1)

        self.verticalLayout.addLayout(self.hl_width)

        self.line = QFrame(NedImageVariable)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(NedImageVariable)

        QMetaObject.connectSlotsByName(NedImageVariable)
    # setupUi

    def retranslateUi(self, NedImageVariable):
        NedImageVariable.setWindowTitle(QCoreApplication.translate("NedImageVariable", u"Form", None))
        self.title_units.setText(QCoreApplication.translate("NedImageVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0415\u0434\u0438\u043d\u0438\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f</span></p></body></html>", None))
        self.title_sms.setText(QCoreApplication.translate("NedImageVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u041c\u0435\u0442\u043e\u0434 \u0440\u0435\u0441\u0430\u0439\u0437\u0430 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f</span></p></body></html>", None))
        self.title_wh.setText(QCoreApplication.translate("NedImageVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0428\u0438\u0440\u0438\u043d\u0430 \u0438 \u0432\u044b\u0441\u043e\u0442\u0430</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("NedImageVariable", u"\u0428:", None))
        self.label_2.setText(QCoreApplication.translate("NedImageVariable", u"\u0412:", None))
    # retranslateUi

