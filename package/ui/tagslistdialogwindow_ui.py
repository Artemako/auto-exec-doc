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
    QHeaderView, QPushButton, QSizePolicy, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_TagsListDialog(object):
    def setupUi(self, TagsListDialog):
        if not TagsListDialog.objectName():
            TagsListDialog.setObjectName(u"TagsListDialog")
        TagsListDialog.resize(825, 566)
        self.verticalLayout_2 = QVBoxLayout(TagsListDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabwidget = QTabWidget(TagsListDialog)
        self.tabwidget.setObjectName(u"tabwidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_8 = QVBoxLayout(self.tab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.table_all_tags = QTableWidget(self.tab)
        self.table_all_tags.setObjectName(u"table_all_tags")

        self.verticalLayout_8.addWidget(self.table_all_tags)

        self.btn_create_tag = QPushButton(self.tab)
        self.btn_create_tag.setObjectName(u"btn_create_tag")

        self.verticalLayout_8.addWidget(self.btn_create_tag)

        self.tabwidget.addTab(self.tab, "")
        self.tab_project = QWidget()
        self.tab_project.setObjectName(u"tab_project")
        self.verticalLayout_4 = QVBoxLayout(self.tab_project)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.table_project_tags = QTableWidget(self.tab_project)
        self.table_project_tags.setObjectName(u"table_project_tags")

        self.verticalLayout_4.addWidget(self.table_project_tags)

        self.btn_add_tag_to_project = QPushButton(self.tab_project)
        self.btn_add_tag_to_project.setObjectName(u"btn_add_tag_to_project")

        self.verticalLayout_4.addWidget(self.btn_add_tag_to_project)

        self.tabwidget.addTab(self.tab_project, "")
        self.tab_group = QWidget()
        self.tab_group.setObjectName(u"tab_group")
        self.verticalLayout_5 = QVBoxLayout(self.tab_group)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.combox_groups = QComboBox(self.tab_group)
        self.combox_groups.setObjectName(u"combox_groups")

        self.verticalLayout_5.addWidget(self.combox_groups)

        self.table_group_tags = QTableWidget(self.tab_group)
        self.table_group_tags.setObjectName(u"table_group_tags")

        self.verticalLayout_5.addWidget(self.table_group_tags)

        self.btn_add_tag_to_group = QPushButton(self.tab_group)
        self.btn_add_tag_to_group.setObjectName(u"btn_add_tag_to_group")

        self.verticalLayout_5.addWidget(self.btn_add_tag_to_group)

        self.tabwidget.addTab(self.tab_group, "")
        self.tab_form_template_page = QWidget()
        self.tab_form_template_page.setObjectName(u"tab_form_template_page")
        self.verticalLayout_6 = QVBoxLayout(self.tab_form_template_page)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.combox_forms = QComboBox(self.tab_form_template_page)
        self.combox_forms.setObjectName(u"combox_forms")

        self.horizontalLayout_2.addWidget(self.combox_forms)

        self.combox_templates = QComboBox(self.tab_form_template_page)
        self.combox_templates.setObjectName(u"combox_templates")

        self.horizontalLayout_2.addWidget(self.combox_templates)

        self.combox_pages = QComboBox(self.tab_form_template_page)
        self.combox_pages.setObjectName(u"combox_pages")

        self.horizontalLayout_2.addWidget(self.combox_pages)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.table_form_template_page_tags = QTableWidget(self.tab_form_template_page)
        self.table_form_template_page_tags.setObjectName(u"table_form_template_page_tags")

        self.verticalLayout_6.addWidget(self.table_form_template_page_tags)

        self.btn_add_tag_to_template_or_page = QPushButton(self.tab_form_template_page)
        self.btn_add_tag_to_template_or_page.setObjectName(u"btn_add_tag_to_template_or_page")

        self.verticalLayout_6.addWidget(self.btn_add_tag_to_template_or_page)

        self.tabwidget.addTab(self.tab_form_template_page, "")

        self.verticalLayout_2.addWidget(self.tabwidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_save = QPushButton(TagsListDialog)
        self.btn_save.setObjectName(u"btn_save")

        self.horizontalLayout.addWidget(self.btn_save)

        self.btn_close = QPushButton(TagsListDialog)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout.addWidget(self.btn_close)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(TagsListDialog)

        self.tabwidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(TagsListDialog)
    # setupUi

    def retranslateUi(self, TagsListDialog):
        TagsListDialog.setWindowTitle(QCoreApplication.translate("TagsListDialog", u"Dialog", None))
        self.btn_create_tag.setText(QCoreApplication.translate("TagsListDialog", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0442\u0435\u0433", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab), QCoreApplication.translate("TagsListDialog", u"\u0412\u0441\u0435 \u0442\u0435\u0433\u0438", None))
        self.btn_add_tag_to_project.setText(QCoreApplication.translate("TagsListDialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u0435\u0433", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_project), QCoreApplication.translate("TagsListDialog", u"\u041f\u0440\u043e\u0435\u043a\u0442", None))
        self.btn_add_tag_to_group.setText(QCoreApplication.translate("TagsListDialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u0435\u0433", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_group), QCoreApplication.translate("TagsListDialog", u"\u0413\u0440\u0443\u043f\u043f\u0430", None))
        self.btn_add_tag_to_template_or_page.setText(QCoreApplication.translate("TagsListDialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u0435\u0433", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_form_template_page), QCoreApplication.translate("TagsListDialog", u"\u0424\u043e\u0440\u043c\u0430/\u0428\u0430\u0431\u043b\u043e\u043d/\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.btn_save.setText(QCoreApplication.translate("TagsListDialog", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("TagsListDialog", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

