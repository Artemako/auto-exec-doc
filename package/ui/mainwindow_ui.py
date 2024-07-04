# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QScrollArea,
    QSizePolicy, QSplitter, QStatusBar, QToolBar,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1000, 581)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        icon = QIcon()
        iconThemeName = u"document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u":/icons/icons/add-file.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.action_new.setIcon(icon)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_open.setIcon(icon1)
        self.action_saveas = QAction(MainWindow)
        self.action_saveas.setObjectName(u"action_saveas")
        self.action_saveas.setEnabled(False)
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save.setEnabled(True)
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_save.setIcon(icon2)
        self.action_zoomin = QAction(MainWindow)
        self.action_zoomin.setObjectName(u"action_zoomin")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/zoom-in.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomin.setIcon(icon3)
        self.action_zoomin.setMenuRole(QAction.TextHeuristicRole)
        self.action_zoomout = QAction(MainWindow)
        self.action_zoomout.setObjectName(u"action_zoomout")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/zoom-out.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomout.setIcon(icon4)
        self.action_zoomout.setMenuRole(QAction.TextHeuristicRole)
        self.action_edit_tags = QAction(MainWindow)
        self.action_edit_tags.setObjectName(u"action_edit_tags")
        self.action_edit_tags.setEnabled(False)
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_tags.setIcon(icon5)
        self.action_zoomfitpage = QAction(MainWindow)
        self.action_zoomfitpage.setObjectName(u"action_zoomfitpage")
        self.action_zoomfitpage.setCheckable(True)
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/zoom-fit-width.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomfitpage.setIcon(icon6)
        self.action_zoomfitpage.setMenuRole(QAction.NoRole)
        self.action_export_to_pdf = QAction(MainWindow)
        self.action_export_to_pdf.setObjectName(u"action_export_to_pdf")
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/export.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_export_to_pdf.setIcon(icon7)
        self.action_edit_templates = QAction(MainWindow)
        self.action_edit_templates.setObjectName(u"action_edit_templates")
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/template.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_templates.setIcon(icon8)
        self.action_edit_templates.setMenuRole(QAction.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.centralwidget_splitter = QSplitter(self.centralwidget)
        self.centralwidget_splitter.setObjectName(u"centralwidget_splitter")
        self.centralwidget_splitter.setOrientation(Qt.Horizontal)
        self.gb_left = QGroupBox(self.centralwidget_splitter)
        self.gb_left.setObjectName(u"gb_left")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gb_left.sizePolicy().hasHeightForWidth())
        self.gb_left.setSizePolicy(sizePolicy1)
        self.gb_left.setMinimumSize(QSize(250, 0))
        self.verticalLayout_8 = QVBoxLayout(self.gb_left)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gb_left_splitter = QSplitter(self.gb_left)
        self.gb_left_splitter.setObjectName(u"gb_left_splitter")
        self.gb_left_splitter.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget = QWidget(self.gb_left_splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vbl_templates = QVBoxLayout(self.verticalLayoutWidget)
        self.vbl_templates.setObjectName(u"vbl_templates")
        self.vbl_templates.setContentsMargins(0, 0, 0, 0)
        self.title_structure_execdoc = QLabel(self.verticalLayoutWidget)
        self.title_structure_execdoc.setObjectName(u"title_structure_execdoc")

        self.vbl_templates.addWidget(self.title_structure_execdoc)

        self.treewidget_structure_execdoc = QTreeWidget(self.verticalLayoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"\u041f\u0440\u043e\u0435\u043a\u0442 \u043d\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d");
        self.treewidget_structure_execdoc.setHeaderItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treewidget_structure_execdoc)
        __qtreewidgetitem1.setCheckState(0, Qt.Checked);
        __qtreewidgetitem2 = QTreeWidgetItem(self.treewidget_structure_execdoc)
        __qtreewidgetitem2.setCheckState(0, Qt.Checked);
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3.setCheckState(0, Qt.Checked);
        self.treewidget_structure_execdoc.setObjectName(u"treewidget_structure_execdoc")
        self.treewidget_structure_execdoc.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.vbl_templates.addWidget(self.treewidget_structure_execdoc)

        self.gb_left_splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.gb_left_splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.vbl_pages = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vbl_pages.setObjectName(u"vbl_pages")
        self.vbl_pages.setContentsMargins(0, 0, 0, 0)
        self.title_pages_template = QLabel(self.verticalLayoutWidget_2)
        self.title_pages_template.setObjectName(u"title_pages_template")

        self.vbl_pages.addWidget(self.title_pages_template)

        self.listwidget_pages_template = QListWidget(self.verticalLayoutWidget_2)
        __qlistwidgetitem = QListWidgetItem(self.listwidget_pages_template)
        __qlistwidgetitem.setCheckState(Qt.Checked);
        __qlistwidgetitem1 = QListWidgetItem(self.listwidget_pages_template)
        __qlistwidgetitem1.setCheckState(Qt.Checked);
        self.listwidget_pages_template.setObjectName(u"listwidget_pages_template")

        self.vbl_pages.addWidget(self.listwidget_pages_template)

        self.gb_left_splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_8.addWidget(self.gb_left_splitter)

        self.centralwidget_splitter.addWidget(self.gb_left)
        self.gb_center = QGroupBox(self.centralwidget_splitter)
        self.gb_center.setObjectName(u"gb_center")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gb_center.sizePolicy().hasHeightForWidth())
        self.gb_center.setSizePolicy(sizePolicy2)
        self.gb_center.setMinimumSize(QSize(350, 0))
        self.horizontalLayout = QHBoxLayout(self.gb_center)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_pdf_view = QPdfView(self.gb_center)
        self.widget_pdf_view.setObjectName(u"widget_pdf_view")
        self.widget_pdf_view.setStyleSheet(u"background-color: rgb(255, 170, 0);")

        self.horizontalLayout.addWidget(self.widget_pdf_view)

        self.centralwidget_splitter.addWidget(self.gb_center)
        self.gb_right = QGroupBox(self.centralwidget_splitter)
        self.gb_right.setObjectName(u"gb_right")
        sizePolicy2.setHeightForWidth(self.gb_right.sizePolicy().hasHeightForWidth())
        self.gb_right.setSizePolicy(sizePolicy2)
        self.gb_right.setMinimumSize(QSize(300, 0))
        self.gb_right.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.gb_right.setFlat(False)
        self.verticalLayout_4 = QVBoxLayout(self.gb_right)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollarea_inputforms = QScrollArea(self.gb_right)
        self.scrollarea_inputforms.setObjectName(u"scrollarea_inputforms")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollarea_inputforms.sizePolicy().hasHeightForWidth())
        self.scrollarea_inputforms.setSizePolicy(sizePolicy3)
        self.scrollarea_inputforms.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollarea_inputforms.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea_inputforms.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollarea_inputforms.setWidgetResizable(True)
        self.scrollarea_inputforms.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollarea_inputforms_layout = QWidget()
        self.scrollarea_inputforms_layout.setObjectName(u"scrollarea_inputforms_layout")
        self.scrollarea_inputforms_layout.setGeometry(QRect(0, 0, 305, 448))
        self.scrollarea_inputforms_layout.setMouseTracking(False)
        self.verticalLayout_5 = QVBoxLayout(self.scrollarea_inputforms_layout)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.scrollarea_inputforms.setWidget(self.scrollarea_inputforms_layout)

        self.verticalLayout_4.addWidget(self.scrollarea_inputforms)

        self.centralwidget_splitter.addWidget(self.gb_right)

        self.verticalLayout_6.addWidget(self.centralwidget_splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1000, 22))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_help = QMenu(self.menu_bar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_tools = QMenu(self.menu_bar)
        self.menu_tools.setObjectName(u"menu_tools")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.tb_main = QToolBar(MainWindow)
        self.tb_main.setObjectName(u"tb_main")
        self.tb_main.setEnabled(True)
        self.tb_main.setAllowedAreas(Qt.TopToolBarArea)
        self.tb_main.setOrientation(Qt.Horizontal)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.tb_main)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_tools.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addAction(self.action_export_to_pdf)
        self.menu_tools.addAction(self.action_edit_tags)
        self.tb_main.addAction(self.action_new)
        self.tb_main.addAction(self.action_open)
        self.tb_main.addAction(self.action_save)
        self.tb_main.addAction(self.action_export_to_pdf)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_edit_tags)
        self.tb_main.addAction(self.action_edit_templates)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_zoomin)
        self.tb_main.addAction(self.action_zoomout)
        self.tb_main.addAction(self.action_zoomfitpage)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0430\u0446\u0438\u044f \u0418\u0414", None))
        self.action_new.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439", None))
#if QT_CONFIG(shortcut)
        self.action_new.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.action_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_saveas.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a", None))
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.action_save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_zoomin.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0432\u0435\u043b\u0438\u0447\u0438\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.action_zoomin.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl++", None))
#endif // QT_CONFIG(shortcut)
        self.action_zoomout.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043c\u0435\u043d\u044c\u0448\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.action_zoomout.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u043c\u0435\u043d\u044c\u0448\u0438\u0442\u044c", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_zoomout.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+-", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_tags.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432", None))
#if QT_CONFIG(tooltip)
        self.action_edit_tags.setToolTip(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0442\u0435\u0433\u043e\u0432", None))
#endif // QT_CONFIG(tooltip)
        self.action_zoomfitpage.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e \u0448\u0438\u0440\u0438\u043d\u0435", None))
        self.action_export_to_pdf.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 PDF", None))
        self.action_edit_templates.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432", None))
        self.gb_left.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None))
        self.title_structure_execdoc.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None))

        __sortingEnabled = self.treewidget_structure_execdoc.isSortingEnabled()
        self.treewidget_structure_execdoc.setSortingEnabled(False)
        ___qtreewidgetitem = self.treewidget_structure_execdoc.topLevelItem(0)
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u0422\u0438\u0442\u0443\u043b\u044c\u043d\u044b\u0439 \u043b\u0438\u0441\u0442", None));
        ___qtreewidgetitem1 = self.treewidget_structure_execdoc.topLevelItem(1)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0441\u043f\u043e\u0440\u0442", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0422-1", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0422-2", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0422-3", None));
        self.treewidget_structure_execdoc.setSortingEnabled(__sortingEnabled)

        self.title_pages_template.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0448\u0430\u0431\u043b\u043e\u043d\u0430.", None))

        __sortingEnabled1 = self.listwidget_pages_template.isSortingEnabled()
        self.listwidget_pages_template.setSortingEnabled(False)
        ___qlistwidgetitem = self.listwidget_pages_template.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 1", None));
        ___qlistwidgetitem1 = self.listwidget_pages_template.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 2", None));
        self.listwidget_pages_template.setSortingEnabled(__sortingEnabled1)

        self.gb_center.setTitle(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442", None))
        self.gb_right.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u043e\u0434 ", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.menu_tools.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b", None))
        self.tb_main.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

