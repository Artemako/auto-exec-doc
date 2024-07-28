# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nodeseditordialogwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QHeaderView, QPushButton, QSizePolicy, QSpacerItem,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_NodesEditorDialogWindow(object):
    def setupUi(self, NodesEditorDialogWindow):
        if not NodesEditorDialogWindow.objectName():
            NodesEditorDialogWindow.setObjectName(u"NodesEditorDialogWindow")
        NodesEditorDialogWindow.resize(573, 500)
        self.verticalLayout_2 = QVBoxLayout(NodesEditorDialogWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.hl_main = QHBoxLayout()
        self.hl_main.setObjectName(u"hl_main")
        self.tw_nodes = QTreeWidget(NodesEditorDialogWindow)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_nodes.setHeaderItem(__qtreewidgetitem)
        self.tw_nodes.setObjectName(u"tw_nodes")

        self.hl_main.addWidget(self.tw_nodes)

        self.vl_buttons = QVBoxLayout()
        self.vl_buttons.setObjectName(u"vl_buttons")
        self.btn_add_form = QPushButton(NodesEditorDialogWindow)
        self.btn_add_form.setObjectName(u"btn_add_form")

        self.vl_buttons.addWidget(self.btn_add_form)

        self.btn_add_group = QPushButton(NodesEditorDialogWindow)
        self.btn_add_group.setObjectName(u"btn_add_group")

        self.vl_buttons.addWidget(self.btn_add_group)

        self.hl_movebtns = QHBoxLayout()
        self.hl_movebtns.setObjectName(u"hl_movebtns")
        self.btn_up = QPushButton(NodesEditorDialogWindow)
        self.btn_up.setObjectName(u"btn_up")

        self.hl_movebtns.addWidget(self.btn_up)

        self.btn_down = QPushButton(NodesEditorDialogWindow)
        self.btn_down.setObjectName(u"btn_down")

        self.hl_movebtns.addWidget(self.btn_down)


        self.vl_buttons.addLayout(self.hl_movebtns)

        self.btn_change_name = QPushButton(NodesEditorDialogWindow)
        self.btn_change_name.setObjectName(u"btn_change_name")

        self.vl_buttons.addWidget(self.btn_change_name)

        self.btn_delete_item = QPushButton(NodesEditorDialogWindow)
        self.btn_delete_item.setObjectName(u"btn_delete_item")

        self.vl_buttons.addWidget(self.btn_delete_item)

        self.vert_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vl_buttons.addItem(self.vert_spacer)


        self.hl_main.addLayout(self.vl_buttons)


        self.verticalLayout_2.addLayout(self.hl_main)

        self.line = QFrame(NodesEditorDialogWindow)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.hl_saveclose = QHBoxLayout()
        self.hl_saveclose.setObjectName(u"hl_saveclose")
        self.btn_save = QPushButton(NodesEditorDialogWindow)
        self.btn_save.setObjectName(u"btn_save")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_save.setIcon(icon)

        self.hl_saveclose.addWidget(self.btn_save)

        self.btn_close = QPushButton(NodesEditorDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon1)

        self.hl_saveclose.addWidget(self.btn_close)


        self.verticalLayout_2.addLayout(self.hl_saveclose)


        self.retranslateUi(NodesEditorDialogWindow)

        QMetaObject.connectSlotsByName(NodesEditorDialogWindow)
    # setupUi

    def retranslateUi(self, NodesEditorDialogWindow):
        NodesEditorDialogWindow.setWindowTitle(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u043e\u0441\u0442\u0430\u0432\u0430 \u0418\u0414", None))
        self.btn_add_form.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0444\u043e\u0440\u043c\u0443", None))
        self.btn_add_group.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0433\u0440\u0443\u043f\u043f\u0443", None))
        self.btn_up.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0412\u0432\u0435\u0440\u0445", None))
        self.btn_down.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0412\u043d\u0438\u0437", None))
        self.btn_change_name.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.btn_delete_item.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None))
        self.btn_save.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

