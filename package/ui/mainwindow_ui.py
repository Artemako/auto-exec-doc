# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLayout,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from package.components.pdfwidget import PdfWidget
import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1000, 769)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName("action_new")
        icon = QIcon()
        iconThemeName = "document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(":/icons/icons/add-file.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.action_new.setIcon(icon)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        icon1 = QIcon()
        icon1.addFile(":/icons/icons/open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_open.setIcon(icon1)
        self.action_saveas = QAction(MainWindow)
        self.action_saveas.setObjectName("action_saveas")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        icon2 = QIcon()
        icon2.addFile(":/icons/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_save.setIcon(icon2)
        self.action_zoomin = QAction(MainWindow)
        self.action_zoomin.setObjectName("action_zoomin")
        icon3 = QIcon()
        icon3.addFile(":/icons/icons/zoom-in.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomin.setIcon(icon3)
        self.action_zoomin.setMenuRole(QAction.TextHeuristicRole)
        self.action_zoomout = QAction(MainWindow)
        self.action_zoomout.setObjectName("action_zoomout")
        icon4 = QIcon()
        icon4.addFile(":/icons/icons/zoom-out.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomout.setIcon(icon4)
        self.action_zoomout.setMenuRole(QAction.TextHeuristicRole)
        self.action_edit_templates = QAction(MainWindow)
        self.action_edit_templates.setObjectName("action_edit_templates")
        icon5 = QIcon()
        icon5.addFile(":/icons/icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_templates.setIcon(icon5)
        self.action_zoomfitpage = QAction(MainWindow)
        self.action_zoomfitpage.setObjectName("action_zoomfitpage")
        icon6 = QIcon()
        icon6.addFile(
            ":/icons/icons/zoom-fit-width.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.action_zoomfitpage.setIcon(icon6)
        self.action_zoomfitpage.setMenuRole(QAction.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gl_main = QGridLayout()
        self.gl_main.setObjectName("gl_main")
        self.gl_main.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gb_center = QGroupBox(self.centralwidget)
        self.gb_center.setObjectName("gb_center")
        self.horizontalLayout = QHBoxLayout(self.gb_center)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pdfwidget = PdfWidget(self.gb_center)
        self.pdfwidget.setObjectName("pdfwidget")
        self.pdfwidget.setStyleSheet("background-color: rgb(255, 170, 0);")

        self.horizontalLayout.addWidget(self.pdfwidget)

        self.gl_main.addWidget(self.gb_center, 0, 1, 1, 1)

        self.gb_left = QGroupBox(self.centralwidget)
        self.gb_left.setObjectName("gb_left")
        self.verticalLayout = QVBoxLayout(self.gb_left)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabwidget = QTabWidget(self.gb_left)
        self.tabwidget.setObjectName("tabwidget")
        self.tab_structure_execdoc = QWidget()
        self.tab_structure_execdoc.setObjectName("tab_structure_execdoc")
        self.verticalLayout_2 = QVBoxLayout(self.tab_structure_execdoc)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treewidget_structure_execdoc = QTreeWidget(self.tab_structure_execdoc)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, "1")
        self.treewidget_structure_execdoc.setHeaderItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treewidget_structure_execdoc)
        __qtreewidgetitem1.setCheckState(0, Qt.Checked)
        __qtreewidgetitem2 = QTreeWidgetItem(self.treewidget_structure_execdoc)
        __qtreewidgetitem2.setCheckState(0, Qt.Checked)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3.setCheckState(0, Qt.Checked)
        self.treewidget_structure_execdoc.setObjectName("treewidget_structure_execdoc")
        self.treewidget_structure_execdoc.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.verticalLayout_2.addWidget(self.treewidget_structure_execdoc)

        self.pushButton_2 = QPushButton(self.tab_structure_execdoc)
        self.pushButton_2.setObjectName("pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.tabwidget.addTab(self.tab_structure_execdoc, "")
        self.tab_pages_template = QWidget()
        self.tab_pages_template.setObjectName("tab_pages_template")
        self.verticalLayout_3 = QVBoxLayout(self.tab_pages_template)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listwidget_pages_template = QListWidget(self.tab_pages_template)
        self.listwidget_pages_template.setObjectName("listwidget_pages_template")

        self.verticalLayout_3.addWidget(self.listwidget_pages_template)

        self.tabwidget.addTab(self.tab_pages_template, "")

        self.verticalLayout.addWidget(self.tabwidget)

        self.gl_main.addWidget(self.gb_left, 0, 0, 1, 1)

        self.gb_right = QGroupBox(self.centralwidget)
        self.gb_right.setObjectName("gb_right")
        self.gb_right.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.gb_right.setFlat(False)

        self.gl_main.addWidget(self.gb_right, 0, 2, 1, 1)

        self.gl_main.setColumnStretch(0, 4)
        self.gl_main.setColumnStretch(1, 7)
        self.gl_main.setColumnStretch(2, 5)

        self.gridLayout.addLayout(self.gl_main, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName("menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1000, 22))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QMenu(self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        self.menu_tools = QMenu(self.menu_bar)
        self.menu_tools.setObjectName("menu_tools")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.tb_main = QToolBar(MainWindow)
        self.tb_main.setObjectName("tb_main")
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
        self.menu_tools.addAction(self.action_edit_templates)
        self.tb_main.addAction(self.action_new)
        self.tb_main.addAction(self.action_open)
        self.tb_main.addAction(self.action_save)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_edit_templates)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_zoomin)
        self.tb_main.addAction(self.action_zoomout)

        self.retranslateUi(MainWindow)

        self.tabwidget.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0430\u0446\u0438\u044f \u0418\u0414",
                None,
            )
        )
        self.action_new.setText(
            QCoreApplication.translate(
                "MainWindow", "\u041d\u043e\u0432\u044b\u0439", None
            )
        )
        self.action_open.setText(
            QCoreApplication.translate(
                "MainWindow", "\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None
            )
        )
        self.action_saveas.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a",
                None,
            )
        )
        self.action_save.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
                None,
            )
        )
        self.action_zoomin.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0423\u0432\u0435\u043b\u0438\u0447\u0438\u0442\u044c",
                None,
            )
        )
        # if QT_CONFIG(shortcut)
        self.action_zoomin.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+-", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_zoomout.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0423\u043c\u0435\u043d\u044c\u0448\u0438\u0442\u044c",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.action_zoomout.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                "\u0423\u043c\u0435\u043d\u044c\u0448\u0438\u0442\u044c",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.action_zoomout.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl++", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_edit_templates.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432",
                None,
            )
        )
        self.action_zoomfitpage.setText(
            QCoreApplication.translate(
                "MainWindow", "\u041f\u043e \u0448\u0438\u0440\u0438\u043d\u0435", None
            )
        )
        self.gb_center.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442",
                None,
            )
        )
        self.gb_left.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430",
                None,
            )
        )

        __sortingEnabled = self.treewidget_structure_execdoc.isSortingEnabled()
        self.treewidget_structure_execdoc.setSortingEnabled(False)
        ___qtreewidgetitem = self.treewidget_structure_execdoc.topLevelItem(0)
        ___qtreewidgetitem.setText(
            0,
            QCoreApplication.translate(
                "MainWindow",
                "\u0422\u0438\u0442\u0443\u043b\u044c\u043d\u044b\u0439 \u043b\u0438\u0441\u0442",
                None,
            ),
        )
        ___qtreewidgetitem1 = self.treewidget_structure_execdoc.topLevelItem(1)
        ___qtreewidgetitem1.setText(
            0,
            QCoreApplication.translate(
                "MainWindow", "\u041f\u0430\u0441\u043f\u043e\u0440\u0442", None
            ),
        )
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(
            0, QCoreApplication.translate("MainWindow", "\u041f\u0422-1", None)
        )
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(
            0, QCoreApplication.translate("MainWindow", "\u041f\u0422-2", None)
        )
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(
            0, QCoreApplication.translate("MainWindow", "\u041f\u0422-3", None)
        )
        self.treewidget_structure_execdoc.setSortingEnabled(__sortingEnabled)

        self.pushButton_2.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041a\u043d\u043e\u043f\u043a\u0430 \u0434\u043b\u044f \u0447\u0435\u0433\u043e-\u0442\u043e",
                None,
            )
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_structure_execdoc),
            QCoreApplication.translate(
                "MainWindow", "\u0421\u043e\u0441\u0442\u0430\u0432 \u0418\u0414", None
            ),
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_pages_template),
            QCoreApplication.translate(
                "MainWindow",
                "\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u0448\u0430\u0431\u043b\u043e\u043d\u0430",
                None,
            ),
        )
        self.gb_right.setTitle(
            QCoreApplication.translate("MainWindow", "\u0412\u0432\u043e\u0434 ", None)
        )
        self.menu_file.setTitle(
            QCoreApplication.translate("MainWindow", "\u0424\u0430\u0439\u043b", None)
        )
        self.menu_help.setTitle(
            QCoreApplication.translate(
                "MainWindow", "\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None
            )
        )
        self.menu_tools.setTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b",
                None,
            )
        )
        self.tb_main.setWindowTitle(
            QCoreApplication.translate("MainWindow", "toolBar", None)
        )

    # retranslateUi
