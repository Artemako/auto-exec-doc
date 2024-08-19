# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tagslistdialogwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QHeaderView, QLayout, QPushButton, QSizePolicy,
    QSplitter, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_TagsListDialog(object):
    def setupUi(self, TagsListDialog):
        if not TagsListDialog.objectName():
            TagsListDialog.setObjectName(u"TagsListDialog")
        TagsListDialog.setWindowModality(Qt.ApplicationModal)
        TagsListDialog.resize(1282, 720)
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        TagsListDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(TagsListDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabwidget = QTabWidget(TagsListDialog)
        self.tabwidget.setObjectName(u"tabwidget")
        self.tab_project = QWidget()
        self.tab_project.setObjectName(u"tab_project")
        self.verticalLayout_4 = QVBoxLayout(self.tab_project)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_create_tag = QPushButton(self.tab_project)
        self.btn_create_tag.setObjectName(u"btn_create_tag")

        self.verticalLayout_4.addWidget(self.btn_create_tag)

        self.splitter_project = QSplitter(self.tab_project)
        self.splitter_project.setObjectName(u"splitter_project")
        self.splitter_project.setOrientation(Qt.Horizontal)
        self.table_editor_project_tags = QTableWidget(self.splitter_project)
        self.table_editor_project_tags.setObjectName(u"table_editor_project_tags")
        self.splitter_project.addWidget(self.table_editor_project_tags)
        self.table_project_tags = QTableWidget(self.splitter_project)
        self.table_project_tags.setObjectName(u"table_project_tags")
        self.splitter_project.addWidget(self.table_project_tags)

        self.verticalLayout_4.addWidget(self.splitter_project)

        self.verticalLayout_4.setStretch(1, 1)
        self.tabwidget.addTab(self.tab_project, "")
        self.tab_group = QWidget()
        self.tab_group.setObjectName(u"tab_group")
        self.verticalLayout_3 = QVBoxLayout(self.tab_group)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.combox_groups = QComboBox(self.tab_group)
        self.combox_groups.setObjectName(u"combox_groups")

        self.verticalLayout_3.addWidget(self.combox_groups)

        self.splitter_group = QSplitter(self.tab_group)
        self.splitter_group.setObjectName(u"splitter_group")
        self.splitter_group.setMidLineWidth(0)
        self.splitter_group.setOrientation(Qt.Horizontal)
        self.table_editor_group_tags = QTableWidget(self.splitter_group)
        self.table_editor_group_tags.setObjectName(u"table_editor_group_tags")
        self.splitter_group.addWidget(self.table_editor_group_tags)
        self.table_group_tags = QTableWidget(self.splitter_group)
        self.table_group_tags.setObjectName(u"table_group_tags")
        self.splitter_group.addWidget(self.table_group_tags)

        self.verticalLayout_3.addWidget(self.splitter_group)

        self.tabwidget.addTab(self.tab_group, "")
        self.tab_form_template_page = QWidget()
        self.tab_form_template_page.setObjectName(u"tab_form_template_page")
        self.verticalLayout_5 = QVBoxLayout(self.tab_form_template_page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.hl_combox = QHBoxLayout()
        self.hl_combox.setObjectName(u"hl_combox")
        self.hl_combox.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.combox_forms = QComboBox(self.tab_form_template_page)
        self.combox_forms.setObjectName(u"combox_forms")

        self.hl_combox.addWidget(self.combox_forms)

        self.combox_templates = QComboBox(self.tab_form_template_page)
        self.combox_templates.setObjectName(u"combox_templates")

        self.hl_combox.addWidget(self.combox_templates)

        self.combox_pages = QComboBox(self.tab_form_template_page)
        self.combox_pages.setObjectName(u"combox_pages")

        self.hl_combox.addWidget(self.combox_pages)


        self.verticalLayout_5.addLayout(self.hl_combox)

        self.splitter_ftp = QSplitter(self.tab_form_template_page)
        self.splitter_ftp.setObjectName(u"splitter_ftp")
        self.splitter_ftp.setOrientation(Qt.Horizontal)
        self.table_editor_ftp_tags = QTableWidget(self.splitter_ftp)
        self.table_editor_ftp_tags.setObjectName(u"table_editor_ftp_tags")
        self.splitter_ftp.addWidget(self.table_editor_ftp_tags)
        self.table_ftp_tags = QTableWidget(self.splitter_ftp)
        self.table_ftp_tags.setObjectName(u"table_ftp_tags")
        self.splitter_ftp.addWidget(self.table_ftp_tags)

        self.verticalLayout_5.addWidget(self.splitter_ftp)

        self.verticalLayout_5.setStretch(1, 1)
        self.tabwidget.addTab(self.tab_form_template_page, "")

        self.verticalLayout_2.addWidget(self.tabwidget)

        self.hl_buttons = QHBoxLayout()
        self.hl_buttons.setObjectName(u"hl_buttons")
        self.btn_save = QPushButton(TagsListDialog)
        self.btn_save.setObjectName(u"btn_save")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_save.setIcon(icon1)

        self.hl_buttons.addWidget(self.btn_save)

        self.btn_close = QPushButton(TagsListDialog)
        self.btn_close.setObjectName(u"btn_close")
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)

        self.hl_buttons.addWidget(self.btn_close)


        self.verticalLayout_2.addLayout(self.hl_buttons)


        self.retranslateUi(TagsListDialog)

        self.tabwidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TagsListDialog)
    # setupUi

    def retranslateUi(self, TagsListDialog):
        TagsListDialog.setWindowTitle(QCoreApplication.translate("TagsListDialog", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0442\u0435\u0433\u043e\u0432 \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None))
        self.btn_create_tag.setText(QCoreApplication.translate("TagsListDialog", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0442\u044d\u0433", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_project), QCoreApplication.translate("TagsListDialog", u"\u041f\u0440\u043e\u0435\u043a\u0442", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_group), QCoreApplication.translate("TagsListDialog", u"\u0413\u0440\u0443\u043f\u043f\u0430", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_form_template_page), QCoreApplication.translate("TagsListDialog", u"\u0424\u043e\u0440\u043c\u0430/\u0428\u0430\u0431\u043b\u043e\u043d/\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.btn_save.setText(QCoreApplication.translate("TagsListDialog", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("TagsListDialog", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

