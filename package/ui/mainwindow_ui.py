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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGroupBox, QHeaderView, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QScrollArea, QSizePolicy, QSplitter, QStatusBar,
    QToolBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1366, 768)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setStyleSheet(u"")
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        icon = QIcon()
        iconThemeName = u"document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u":/white-icons/resources/white-icons/add-file.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.action_new.setIcon(icon)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        icon1 = QIcon()
        icon1.addFile(u":/white-icons/resources/white-icons/open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_open.setIcon(icon1)
        self.action_saveas = QAction(MainWindow)
        self.action_saveas.setObjectName(u"action_saveas")
        self.action_saveas.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u":/white-icons/resources/white-icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_saveas.setIcon(icon2)
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save.setEnabled(False)
        self.action_save.setIcon(icon2)
        self.action_zoomin = QAction(MainWindow)
        self.action_zoomin.setObjectName(u"action_zoomin")
        self.action_zoomin.setEnabled(False)
        icon3 = QIcon()
        icon3.addFile(u":/white-icons/resources/white-icons/zoom-in.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomin.setIcon(icon3)
        self.action_zoomin.setMenuRole(QAction.TextHeuristicRole)
        self.action_zoomout = QAction(MainWindow)
        self.action_zoomout.setObjectName(u"action_zoomout")
        self.action_zoomout.setEnabled(False)
        icon4 = QIcon()
        icon4.addFile(u":/white-icons/resources/white-icons/zoom-out.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomout.setIcon(icon4)
        self.action_zoomout.setMenuRole(QAction.TextHeuristicRole)
        self.action_edit_variables = QAction(MainWindow)
        self.action_edit_variables.setObjectName(u"action_edit_variables")
        self.action_edit_variables.setEnabled(False)
        icon5 = QIcon()
        icon5.addFile(u":/white-icons/resources/white-icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_variables.setIcon(icon5)
        self.action_zoomfitpage = QAction(MainWindow)
        self.action_zoomfitpage.setObjectName(u"action_zoomfitpage")
        self.action_zoomfitpage.setCheckable(True)
        self.action_zoomfitpage.setEnabled(False)
        icon6 = QIcon()
        icon6.addFile(u":/white-icons/resources/white-icons/zoom-fit-width.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomfitpage.setIcon(icon6)
        self.action_zoomfitpage.setMenuRole(QAction.TextHeuristicRole)
        self.action_export_to_pdf = QAction(MainWindow)
        self.action_export_to_pdf.setObjectName(u"action_export_to_pdf")
        self.action_export_to_pdf.setEnabled(False)
        icon7 = QIcon()
        icon7.addFile(u":/white-icons/resources/white-icons/export.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_export_to_pdf.setIcon(icon7)
        self.action_edit_templates = QAction(MainWindow)
        self.action_edit_templates.setObjectName(u"action_edit_templates")
        self.action_edit_templates.setEnabled(False)
        icon8 = QIcon()
        icon8.addFile(u":/white-icons/resources/white-icons/template.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_templates.setIcon(icon8)
        self.action_edit_templates.setMenuRole(QAction.TextHeuristicRole)
        self.action_edit_composition = QAction(MainWindow)
        self.action_edit_composition.setObjectName(u"action_edit_composition")
        self.action_edit_composition.setEnabled(False)
        icon9 = QIcon()
        icon9.addFile(u":/white-icons/resources/white-icons/items-tree.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_composition.setIcon(icon9)
        self.action_edit_composition.setMenuRole(QAction.TextHeuristicRole)
        self.action_clear_trash = QAction(MainWindow)
        self.action_clear_trash.setObjectName(u"action_clear_trash")
        icon10 = QIcon()
        icon10.addFile(u":/white-icons/resources/white-icons/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_clear_trash.setIcon(icon10)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(4, 0, 4, 0)
        self.centralwidget_splitter = QSplitter(self.centralwidget)
        self.centralwidget_splitter.setObjectName(u"centralwidget_splitter")
        self.centralwidget_splitter.setOrientation(Qt.Horizontal)
        self.gb_left = QGroupBox(self.centralwidget_splitter)
        self.gb_left.setObjectName(u"gb_left")
        self.verticalLayout_8 = QVBoxLayout(self.gb_left)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(4, 4, 4, 4)
        self.gb_left_splitter = QSplitter(self.gb_left)
        self.gb_left_splitter.setObjectName(u"gb_left_splitter")
        self.gb_left_splitter.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget = QWidget(self.gb_left_splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vbl_templates = QVBoxLayout(self.verticalLayoutWidget)
        self.vbl_templates.setObjectName(u"vbl_templates")
        self.vbl_templates.setContentsMargins(0, 0, 0, 0)
        self.label_structure_execdoc = QLabel(self.verticalLayoutWidget)
        self.label_structure_execdoc.setObjectName(u"label_structure_execdoc")
        self.label_structure_execdoc.setEnabled(True)

        self.vbl_templates.addWidget(self.label_structure_execdoc)

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
        self.label_current_template = QLabel(self.verticalLayoutWidget_2)
        self.label_current_template.setObjectName(u"label_current_template")

        self.vbl_pages.addWidget(self.label_current_template)

        self.combox_templates = QComboBox(self.verticalLayoutWidget_2)
        self.combox_templates.setObjectName(u"combox_templates")

        self.vbl_pages.addWidget(self.combox_templates)

        self.label_pages_template = QLabel(self.verticalLayoutWidget_2)
        self.label_pages_template.setObjectName(u"label_pages_template")

        self.vbl_pages.addWidget(self.label_pages_template)

        self.lw_pages_template = QListWidget(self.verticalLayoutWidget_2)
        __qlistwidgetitem = QListWidgetItem(self.lw_pages_template)
        __qlistwidgetitem.setCheckState(Qt.Checked);
        __qlistwidgetitem1 = QListWidgetItem(self.lw_pages_template)
        __qlistwidgetitem1.setCheckState(Qt.Checked);
        self.lw_pages_template.setObjectName(u"lw_pages_template")

        self.vbl_pages.addWidget(self.lw_pages_template)

        self.gb_left_splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_8.addWidget(self.gb_left_splitter)

        self.centralwidget_splitter.addWidget(self.gb_left)
        self.gb_center = QGroupBox(self.centralwidget_splitter)
        self.gb_center.setObjectName(u"gb_center")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gb_center.sizePolicy().hasHeightForWidth())
        self.gb_center.setSizePolicy(sizePolicy1)
        self.gb_center.setMinimumSize(QSize(350, 0))
        self.gb_center.setFlat(False)
        self.gb_center.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.gb_center)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.label_realview = QLabel(self.gb_center)
        self.label_realview.setObjectName(u"label_realview")

        self.verticalLayout.addWidget(self.label_realview)

        self.widget_pdf_view = QPdfView(self.gb_center)
        self.widget_pdf_view.setObjectName(u"widget_pdf_view")
        self.widget_pdf_view.setMaximumSize(QSize(16777215, 16777215))
        self.widget_pdf_view.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.widget_pdf_view)

        self.verticalLayout.setStretch(1, 1)
        self.centralwidget_splitter.addWidget(self.gb_center)
        self.gb_right = QGroupBox(self.centralwidget_splitter)
        self.gb_right.setObjectName(u"gb_right")
        sizePolicy1.setHeightForWidth(self.gb_right.sizePolicy().hasHeightForWidth())
        self.gb_right.setSizePolicy(sizePolicy1)
        self.gb_right.setMinimumSize(QSize(400, 0))
        self.verticalLayout_4 = QVBoxLayout(self.gb_right)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.label_variables = QLabel(self.gb_right)
        self.label_variables.setObjectName(u"label_variables")

        self.verticalLayout_4.addWidget(self.label_variables)

        self.scrollarea_inputforms = QScrollArea(self.gb_right)
        self.scrollarea_inputforms.setObjectName(u"scrollarea_inputforms")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollarea_inputforms.sizePolicy().hasHeightForWidth())
        self.scrollarea_inputforms.setSizePolicy(sizePolicy2)
        self.scrollarea_inputforms.setFrameShape(QFrame.StyledPanel)
        self.scrollarea_inputforms.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollarea_inputforms.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea_inputforms.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollarea_inputforms.setWidgetResizable(True)
        self.scrollarea_inputforms.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollarea_inputforms_layout = QWidget()
        self.scrollarea_inputforms_layout.setObjectName(u"scrollarea_inputforms_layout")
        self.scrollarea_inputforms_layout.setGeometry(QRect(0, 0, 389, 607))
        self.scrollarea_inputforms_layout.setMouseTracking(True)
        self.verticalLayout_5 = QVBoxLayout(self.scrollarea_inputforms_layout)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.scrollarea_inputforms.setWidget(self.scrollarea_inputforms_layout)

        self.verticalLayout_4.addWidget(self.scrollarea_inputforms)

        self.label_default = QLabel(self.gb_right)
        self.label_default.setObjectName(u"label_default")

        self.verticalLayout_4.addWidget(self.label_default)

        self.combox_default = QComboBox(self.gb_right)
        self.combox_default.setObjectName(u"combox_default")

        self.verticalLayout_4.addWidget(self.combox_default)

        self.verticalLayout_4.setStretch(1, 1)
        self.centralwidget_splitter.addWidget(self.gb_right)

        self.verticalLayout_6.addWidget(self.centralwidget_splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1366, 22))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_recent_projects = QMenu(self.menu_file)
        self.menu_recent_projects.setObjectName(u"menu_recent_projects")
        self.menu_editors = QMenu(self.menu_bar)
        self.menu_editors.setObjectName(u"menu_editors")
        self.menu_scale = QMenu(self.menu_bar)
        self.menu_scale.setObjectName(u"menu_scale")
        self.menu = QMenu(self.menu_bar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menu_bar)
        self.tb_main = QToolBar(MainWindow)
        self.tb_main.setObjectName(u"tb_main")
        self.tb_main.setEnabled(True)
        self.tb_main.setMovable(True)
        self.tb_main.setAllowedAreas(Qt.AllToolBarAreas)
        self.tb_main.setOrientation(Qt.Horizontal)
        self.tb_main.setIconSize(QSize(32, 24))
        self.tb_main.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_main.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.tb_main)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        self.status_bar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_editors.menuAction())
        self.menu_bar.addAction(self.menu_scale.menuAction())
        self.menu_bar.addAction(self.menu.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.menu_recent_projects.menuAction())
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_export_to_pdf)
        self.menu_editors.addAction(self.action_edit_composition)
        self.menu_editors.addAction(self.action_edit_templates)
        self.menu_editors.addAction(self.action_edit_variables)
        self.menu_scale.addAction(self.action_zoomin)
        self.menu_scale.addAction(self.action_zoomout)
        self.menu_scale.addAction(self.action_zoomfitpage)
        self.menu.addAction(self.action_clear_trash)
        self.tb_main.addAction(self.action_new)
        self.tb_main.addAction(self.action_open)
        self.tb_main.addAction(self.action_save)
        self.tb_main.addAction(self.action_export_to_pdf)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_edit_composition)
        self.tb_main.addAction(self.action_edit_templates)
        self.tb_main.addAction(self.action_edit_variables)
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
#if QT_CONFIG(shortcut)
        self.action_saveas.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
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
        self.action_edit_variables.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
        self.action_edit_variables.setIconText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
#if QT_CONFIG(tooltip)
        self.action_edit_variables.setToolTip(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
#endif // QT_CONFIG(tooltip)
        self.action_zoomfitpage.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e \u0448\u0438\u0440\u0438\u043d\u0435", None))
        self.action_export_to_pdf.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 PDF", None))
        self.action_edit_templates.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432", None))
        self.action_edit_composition.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u043e\u0441\u0442\u0430\u0432\u0430 \u0418\u0414", None))
        self.action_clear_trash.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u043a\u0430 \u043e\u0442 \u043c\u0443\u0441\u043e\u0440\u0430", None))
        self.label_structure_execdoc.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430</span></p></body></html>", None))

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

        self.label_current_template.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0448\u0430\u0431\u043b\u043e\u043d</span></p></body></html>", None))
        self.label_pages_template.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u0442\u0435\u043a\u0443\u0449\u0435\u0433\u043e \u0448\u0430\u0431\u043b\u043e\u043d\u0430</span></p></body></html>", None))

        __sortingEnabled1 = self.lw_pages_template.isSortingEnabled()
        self.lw_pages_template.setSortingEnabled(False)
        ___qlistwidgetitem = self.lw_pages_template.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 1", None));
        ___qlistwidgetitem1 = self.lw_pages_template.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 2", None));
        self.lw_pages_template.setSortingEnabled(__sortingEnabled1)

        self.label_realview.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0432 \u0440\u0435\u0436\u0438\u043c\u0435 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0432\u0440\u0435\u043c\u0435\u043d\u0438</span></p></body></html>", None))
        self.label_variables.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0424\u043e\u0440\u043c\u0430 \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f</span></p></body></html>", None))
        self.label_default.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e</span></p></body></html>", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_recent_projects.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u0434\u0430\u0432\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u044b", None))
        self.menu_editors.setTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u044b", None))
        self.menu_scale.setTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0441\u0448\u0442\u0430\u0431", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0447\u0435\u0435", None))
        self.tb_main.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u0432", None))
    # retranslateUi

