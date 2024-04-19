# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pdfwidget.ui'
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
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QWidget)

class Ui_PdfWidget(object):
    def setupUi(self, PdfWidget):
        if not PdfWidget.objectName():
            PdfWidget.setObjectName(u"PdfWidget")
        PdfWidget.resize(300, 240)
        self.horizontalLayout = QHBoxLayout(PdfWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pdf_view = QPdfView(PdfWidget)
        self.pdf_view.setObjectName(u"pdf_view")

        self.horizontalLayout.addWidget(self.pdf_view)


        self.retranslateUi(PdfWidget)

        QMetaObject.connectSlotsByName(PdfWidget)
    # setupUi

    def retranslateUi(self, PdfWidget):
        PdfWidget.setWindowTitle(QCoreApplication.translate("PdfWidget", u"Form", None))
    # retranslateUi

