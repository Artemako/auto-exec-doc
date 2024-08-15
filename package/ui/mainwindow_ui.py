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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QListWidget,
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
        MainWindow.setStyleSheet(u"/*!*************************************\n"
"  VS15 Dark\n"
"****************************************\n"
"  Author: chintsu_kun, holt59, MO2 Team\n"
"  Version: 2.5.0\n"
"  Licence: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)\n"
"  Source: https://github.com/nikolay-borzov/modorganizer-themes\n"
"****************************************\n"
"*/\n"
"/* For some reason applying background-color or border fixes paddings properties */\n"
"QListWidget::item {\n"
"  border-width: 0;\n"
"}\n"
"\n"
"/* Don't override install label on download widget.\n"
"   MO2 assigns color depending on download state */\n"
"#installLabel {\n"
"  color: none;\n"
"}\n"
"\n"
"/* Make `background-color` work for :hover, :focus and :pressed states */\n"
"QToolButton {\n"
"  border: none;\n"
"}\n"
"\n"
"/* Main Window */\n"
"QWidget {\n"
"  background-color: #2d2d30;\n"
"  color: #f1f1f1;\n"
"}\n"
"\n"
"QWidget::disabled {\n"
"  color: #656565;\n"
"}\n"
"\n"
"/* Common */\n"
"/* remove outline */\n"
"* {\n"
""
                        "  outline: 0;\n"
"}\n"
"\n"
"*:disabled,\n"
"QListView::item:disabled,\n"
"*::item:selected:disabled {\n"
"  color: #656565;\n"
"}\n"
"\n"
"/* line heights */\n"
"/* QTreeView#fileTree::item - currently have problem with size column vertical\n"
"   text align */\n"
"#bsaList::item,\n"
"#dataTree::item,\n"
"#modList::item,\n"
"#categoriesTree::item,\n"
"#savegameList::item,\n"
"#tabConflicts QTreeWidget::item {\n"
"  padding: 0.3em 0;\n"
"}\n"
"\n"
"QListView::item,\n"
"QTreeView#espList::item {\n"
"  padding: 0.3em 0;\n"
"}\n"
"\n"
"/* to enable border color */\n"
"QTreeView,\n"
"QListView,\n"
"QTextEdit,\n"
"QWebView,\n"
"QTableView {\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QAbstractItemView {\n"
"  color: #dcdcdc;\n"
"  background-color: #1e1e1e;\n"
"  alternate-background-color: #262626;\n"
"  border-color: #3f3f46;\n"
"}\n"
"\n"
"QAbstractItemView::item:selected,\n"
"QAbstractItemView::item:selected:hover,\n"
"QAbstractItemView::item:alternate:selected,\n"
"QAbstractItemView::ite"
                        "m:alternate:selected:hover {\n"
"  color: #f1f1f1;\n"
"  background-color: #3399ff;\n"
"}\n"
"\n"
"QAbstractItemView[filtered=true] {\n"
"  border: 2px solid #f00 !important;\n"
"}\n"
"\n"
"QAbstractItemView,\n"
"QListView,\n"
"QTreeView {\n"
"  show-decoration-selected: 1;\n"
"}\n"
"\n"
"QAbstractItemView::item:hover,\n"
"QAbstractItemView::item:alternate:hover,\n"
"QAbstractItemView::item:disabled:hover,\n"
"QAbstractItemView::item:alternate:disabled:hover QListView::item:hover,\n"
"QTreeView::branch:hover,\n"
"QTreeWidget::item:hover {\n"
"  background-color: rgba(51, 153, 255, 0.3);\n"
"}\n"
"\n"
"QAbstractItemView::item:selected:disabled,\n"
"QAbstractItemView::item:alternate:selected:disabled,\n"
"QListView::item:selected:disabled,\n"
"QTreeView::branch:selected:disabled,\n"
"QTreeWidget::item:selected:disabled {\n"
"  background-color: rgba(51, 153, 255, 0.3);\n"
"}\n"
"\n"
"QTreeView::branch:selected,\n"
"#bsaList::branch:selected {\n"
"  background-color: #3399ff;\n"
"}\n"
"\n"
"QLabel {\n"
"  backgro"
                        "und-color: transparent;\n"
"}\n"
"\n"
"LinkLabel {\n"
"  qproperty-linkColor: #3399ff;\n"
"}\n"
"\n"
"/* Left Pane & File Trees #QTreeView, #QListView*/\n"
"QTreeView::branch:closed:has-children {\n"
"  image: url(:/png/resources/png/branch-closed.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children {\n"
"  image: url(:/png/resources/png/branch-open.png);\n"
"}\n"
"\n"
"QListView::item {\n"
"  color: #f1f1f1;\n"
"}\n"
"\n"
"/* Text areas and text fields #QTextEdit, #QLineEdit, #QWebView */\n"
"QTextEdit,\n"
"QWebView,\n"
"QLineEdit,\n"
"QAbstractSpinBox,\n"
"QAbstractSpinBox::up-button,\n"
"QAbstractSpinBox::down-button,\n"
"QComboBox {\n"
"  background-color: #333337;\n"
"  border-color: #3f3f46;\n"
"}\n"
"\n"
"QLineEdit:hover,\n"
"QAbstractSpinBox:hover,\n"
"QTextEdit:hover,\n"
"QComboBox:hover,\n"
"QComboBox:editable:hover {\n"
"  border-color: #007acc;\n"
"}\n"
"\n"
"QLineEdit:focus,\n"
"QAbstractSpinBox::focus,\n"
"QTextEdit:focus,\n"
"QComboBox:focus,\n"
"QComboBox:editable:focus,\n"
"QComboBox:on {\n"
""
                        "  background-color: #3f3f46;\n"
"  border-color: #3399ff;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"  border-bottom-color: #3f3f46;\n"
"}\n"
"\n"
"QLineEdit,\n"
"QAbstractSpinBox {\n"
"  min-height: 15px;\n"
"  padding: 2px;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"  margin-top: 0;\n"
"}\n"
"\n"
"/* clear button */\n"
"QLineEdit QToolButton,\n"
"QLineEdit QToolButton:hover {\n"
"  background: none;\n"
"  margin-top: 1px;\n"
"}\n"
"\n"
"QLineEdit#espFilterEdit QToolButton {\n"
"  margin-top: -2px;\n"
"  margin-bottom: 1px;\n"
"}\n"
"\n"
"/* Drop-downs #QComboBox*/\n"
"QComboBox {\n"
"  min-height: 20px;\n"
"  padding-left: 5px;\n"
"  margin: 3px 0 1px 0;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"  padding-left: 3px;\n"
"  /* to enable hover styles */\n"
"  background-color: transparent;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"  width: 20px;\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: top right;\n"
"  border: n"
                        "one;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"  image: url(:/png/resources/png/combobox-down.png);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"  background-color: #1b1b1c;\n"
"  selection-background-color: #3f3f46;\n"
"  border-color: #3399ff;\n"
"  border-style: solid;\n"
"  border-width: 0 1px 1px 1px;\n"
"}\n"
"\n"
"/* Doesn't work http://stackoverflow.com/questions/13308341/qcombobox-abstractitemviewitem */\n"
"/* QComboBox QAbstractItemView:item {\n"
"  padding: 10px;\n"
"  margin: 10px;\n"
"} */\n"
"/* Toolbar */\n"
"QToolBar {\n"
"  border: none;\n"
"}\n"
"\n"
"QToolBar::separator {\n"
"  border-left-color: #222222;\n"
"  border-right-color: #46464a;\n"
"  border-width: 0 1px 0 1px;\n"
"  border-style: solid;\n"
"  width: 0;\n"
"}\n"
"\n"
"QToolButton {\n"
"  padding: 4px;\n"
"}\n"
"\n"
"QToolButton:hover, QToolButton:focus {\n"
"  background-color: #3e3e40;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"  background-color: #3399ff;\n"
"}\n"
"\n"
"QToolButton::menu-indicator {\n"
"  image: url(:/png/re"
                        "sources/png/combobox-down.png);\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: center right;\n"
"  padding-top: 10%;\n"
"  padding-right: 5%;\n"
"}\n"
"\n"
"/* Group Boxes #QGroupBox */\n"
"QGroupBox {\n"
"  border-color: #3f3f46;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"  padding: 1em 0.3em 0.3em 0.3em;\n"
"  margin-top: 0.65em;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"  subcontrol-origin: margin;\n"
"  subcontrol-position: top left;\n"
"  padding: 2px;\n"
"  left: 10px;\n"
"}\n"
"\n"
"/* LCD Count */\n"
"QLCDNumber {\n"
"  border-color: #3f3f46;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"/* Buttons #QPushButton */\n"
"QPushButton {\n"
"  background-color: #333337;\n"
"  border-color: #3f3f46;\n"
"  min-height: 18px;\n"
"  padding: 2px 5px;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QPushButton:hover,\n"
"QPushButton:checked,\n"
"QPushButton:focus,\n"
"QAbstractSpinBox::up-button:hover,\n"
"QAbstractSpinBox::down-button:hover {\n"
"  ba"
                        "ckground-color: #007acc;\n"
"}\n"
"\n"
"QPushButton:pressed,\n"
"QPushButton:checked:hover,\n"
"QAbstractSpinBox::up-button:pressed,\n"
"QAbstractSpinBox::down-button:pressed {\n"
"  background-color: #1c97ea;\n"
"}\n"
"\n"
"QPushButton:disabled,\n"
"QAbstractSpinBox::up-button:disabled,\n"
"QAbstractSpinBox::down-button:disabled {\n"
"  background-color: #333337;\n"
"  border-color: #3f3f46;\n"
"}\n"
"\n"
"QPushButton::menu-indicator {\n"
"  image: url(:/png/resources/png/combobox-down.png);\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: center right;\n"
"  padding-right: 5%;\n"
"}\n"
"\n"
"/* Dialog buttons */\n"
"QSlider::handle:horizontal,\n"
"QSlider::handle:vertical {\n"
"  color: #000000;\n"
"  background-color: #dddddd;\n"
"  border-color: #707070;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover,\n"
"QSlider::handle:vertical:hover,\n"
"QSlider::handle:horizontal:pressed,\n"
"QSlider::handle:horizontal:focus:pressed,\n"
"QSlider::handle:v"
                        "ertical:pressed,\n"
"QSlider::handle:vertical:focus:pressed {\n"
"  background-color: #BEE6FD;\n"
"  border-color: #3c7fb1;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:focus,\n"
"QSlider::handle:vertical:focus {\n"
"  background-color: #dddddd;\n"
"  border-color: #3399ff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal:disabled,\n"
"QSlider::handle:vertical:disabled {\n"
"  background-color: #333337;\n"
"  border-color: #3f3f46;\n"
"}\n"
"\n"
"\n"
"/* Check boxes and Radio buttons common #QCheckBox, #QRadioButton */\n"
"QGroupBox::indicator,\n"
"QTreeView::indicator,\n"
"QCheckBox::indicator,\n"
"QRadioButton::indicator {\n"
"  background-color: #2d2d30;\n"
"  border-color: #3f3f46;\n"
"  width: 13px;\n"
"  height: 13px;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QGroupBox::indicator:hover,\n"
"QTreeView::indicator:hover,\n"
"QCheckBox::indicator:hover,\n"
"QRadioButton::indicator:hover {\n"
"  background-color: #3f3f46;\n"
"  border-color: #007acc;\n"
"}\n"
"\n"
"QGroupBox::indicator:che"
                        "cked,\n"
"QTreeView::indicator:checked,\n"
"QCheckBox::indicator:checked {\n"
"  image: url(:/png/resources/png/checkbox-check.png);\n"
"}\n"
"\n"
"QGroupBox::indicator:disabled,\n"
"QTreeView::indicator:checked:disabled,\n"
"QCheckBox::indicator:checked:disabled {\n"
"  image: url(:/png/resources/png/checkbox-check-disabled.png);\n"
"}\n"
"\n"
"/* Check boxes special */\n"
"QTreeView#modList::indicator {\n"
"  width: 15px;\n"
"  height: 15px;\n"
"}\n"
"\n"
"/* Radio buttons #QRadioButton */\n"
"QRadioButton::indicator {\n"
"  border-radius: 7px;\n"
"}\n"
"\n"
"QRadioButton::indicator::checked {\n"
"  background-color: #B9B9BA;\n"
"  border-width: 2px;\n"
"  width: 11px;\n"
"  height: 11px;\n"
"}\n"
"\n"
"QRadioButton::indicator::checked:hover {\n"
"  border-color: #3f3f46;\n"
"}\n"
"\n"
"/* Spinners #QSpinBox, #QDoubleSpinBox */\n"
"QAbstractSpinBox {\n"
"  margin: 1px;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-button,\n"
"QAbstractSpinBox::down-button {\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"  sub"
                        "control-origin: padding;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-button {\n"
"  subcontrol-position: top right;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-arrow {\n"
"  image: url(:/png/resources/png/spinner-up.png);\n"
"}\n"
"\n"
"QAbstractSpinBox::down-button {\n"
"  subcontrol-position: bottom right;\n"
"}\n"
"\n"
"QAbstractSpinBox::down-arrow {\n"
"  image: url(:/png/resources/png/spinner-down.png);\n"
"}\n"
"\n"
"/* Sliders #QSlider */\n"
"QSlider::groove:horizontal {\n"
"  background-color: #3f3f46;\n"
"  border: none;\n"
"  height: 8px;\n"
"  margin: 2px 0;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"  width: 0.5em;\n"
"  height: 2em;\n"
"  margin: -7px 0;\n"
"  subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Scroll Bars #QAbstractScrollArea, #QScrollBar*/\n"
"/* assigning background still leaves not filled area*/\n"
"QAbstractScrollArea::corner {\n"
"  background-color: transparent;\n"
"}\n"
"\n"
"/* Horizontal */\n"
"QScrollBar:horizontal {\n"
"  height: 18px;\n"
"  border: none;\n"
"  margin: 0 23px 0 23px;\n"
""
                        "}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"  min-width: 32px;\n"
"  margin: 4px 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"  width: 23px;\n"
"  subcontrol-position: right;\n"
"  subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"  width: 23px;\n"
"  subcontrol-position: left;\n"
"  subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Vertical */\n"
"QScrollBar:vertical {\n"
"  width: 20px;\n"
"  border: none;\n"
"  margin: 23px 0 23px 0;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"  min-height: 32px;\n"
"  margin: 2px 4px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"  height: 23px;\n"
"  subcontrol-position: bottom;\n"
"  subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"  height: 23px;\n"
"  subcontrol-position: top;\n"
"  subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Combined */\n"
"QScrollBar {\n"
"  background-color: #3e3e42;\n"
"  border: none;\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
"  background-color: #686868;\n"
"}\n"
"\n"
""
                        "QScrollBar::add-line,\n"
"QScrollBar::sub-line {\n"
"  background-color: #3e3e42;\n"
"  border: none;\n"
"}\n"
"\n"
"/* QScrollBar::add-line:horizontal:hover,\n"
"QScrollBar::sub-line:horizontal:hover,\n"
"QScrollBar::add-line:vertical:hover,\n"
"QScrollBar::sub-line:vertical:hover,\n"
"QScrollBar::add-line:horizontal:pressed,\n"
"QScrollBar::sub-line:horizontal:pressed,\n"
"QScrollBar::add-line:vertical:pressed,\n"
"QScrollBar::sub-line:vertical:pressed { } */\n"
"QScrollBar::handle:hover {\n"
"  background: #9e9e9e;\n"
"}\n"
"\n"
"QScrollBar::handle:pressed {\n"
"  background: #efebef;\n"
"}\n"
"\n"
"QScrollBar::handle:disabled {\n"
"  background: #555558;\n"
"}\n"
"\n"
"QScrollBar::add-page,\n"
"QScrollBar::sub-page {\n"
"  background: transparent;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical {\n"
"  image: url(:/png/resources/png/scrollbar-up.png);\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical:hover {\n"
"  image: url(:/png/resources/png/scrollbar-up-hover.png);\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical:"
                        "disabled {\n"
"  image: url(:/png/resources/png/scrollbar-up-disabled.png);\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal {\n"
"  image: url(:/png/resources/png/scrollbar-right.png);\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal:hover {\n"
"  image: url(:/png/resources/png/scrollbar-right-hover.png);\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal:disabled {\n"
"  image: url(:/png/resources/png/scrollbar-right-disabled.png);\n"
"}\n"
"\n"
"QScrollBar::down-arrow:vertical {\n"
"  image: url(:/png/resources/png/scrollbar-down.png);\n"
"}\n"
"\n"
"QScrollBar::down-arrow:vertical:hover {\n"
"  image: url(:/png/resources/png/scrollbar-down-hover.png);\n"
"}\n"
"\n"
"QScrollBar::down-arrow:vertical:disabled {\n"
"  image: url(:/png/resources/png/scrollbar-down-disabled.png);\n"
"}\n"
"\n"
"QScrollBar::left-arrow:horizontal {\n"
"  image: url(:/png/resources/png/scrollbar-left.png);\n"
"}\n"
"\n"
"QScrollBar::left-arrow:horizontal:hover {\n"
"  image: url(:/png/resources/png/scrollbar-left-hover.png);\n"
"}"
                        "\n"
"\n"
"QScrollBar::left-arrow:horizontal:disabled {\n"
"  image: url(:/png/resources/png/scrollbar-left-disabled.png);\n"
"}\n"
"\n"
"/* Header Rows and Tables (Configure Mod Categories) #QTableView, #QHeaderView */\n"
"QTableView {\n"
"  gridline-color: #3f3f46;\n"
"  selection-background-color: #3399ff;\n"
"  selection-color: #f1f1f1;\n"
"}\n"
"\n"
"QTableView QTableCornerButton::section {\n"
"  background: #252526;\n"
"  border-color: #3f3f46;\n"
"  border-style: solid;\n"
"  border-width: 0 1px 1px 0;\n"
"}\n"
"\n"
"QHeaderView {\n"
"  border: none;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"  background: #252526;\n"
"  border-color: #3f3f46;\n"
"  padding: 3px 5px;\n"
"  border-style: solid;\n"
"  border-width: 0 1px 1px 0;\n"
"}\n"
"\n"
"QHeaderView::section:hover {\n"
"  background: #3e3e40;\n"
"  color: #f6f6f6;\n"
"}\n"
"\n"
"QHeaderView::section:last {\n"
"  border-right: 0;\n"
"}\n"
"\n"
"QHeaderView::up-arrow {\n"
"  image: url(:/png/resources/png/sort-asc.png);\n"
"  margin-bottom: -37px;\n"
"}\n"
""
                        "\n"
"DownloadListView QHeaderView::up-arrow {\n"
"  margin-bottom: -47px;\n"
"}\n"
"\n"
"QHeaderView::down-arrow {\n"
"  image: url(:/png/resources/png/sort-desc.png);\n"
"  margin-bottom: 0;\n"
"}\n"
"\n"
"/* Context menus, toolbar drop-downs #QMenu  */\n"
"QMenu {\n"
"  background-color: #1a1a1c;\n"
"  border-color: #333337;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"  padding: 2px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"  background: transparent;\n"
"  padding: 4px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected,\n"
"QMenuBar::item:selected {\n"
"  background-color: #333334;\n"
"}\n"
"\n"
"QMenu::item:disabled {\n"
"  background-color: transparent;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"  background-color: #333337;\n"
"  height: 1px;\n"
"  margin: 1px 0;\n"
"}\n"
"\n"
"QMenu::icon {\n"
"  margin: 1px;\n"
"}\n"
"\n"
"QMenu::right-arrow {\n"
"  image: url(:/png/resources/png/sub-menu-arrow.png);\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: center right;\n"
"  padding-right: 0.5em;\n"
"}\n"
"\n"
""
                        "QMenu QPushButton {\n"
"  background-color: transparent;\n"
"  border-color: #3f3f46;\n"
"  margin: 1px 0 1px 0;\n"
"}\n"
"\n"
"QMenu QCheckBox,\n"
"QMenu QRadioButton {\n"
"  background-color: transparent;\n"
"  padding: 5px 2px;\n"
"}\n"
"\n"
"/* Tool tips #QToolTip, #SaveGameInfoWidget */\n"
"QToolTip,\n"
"SaveGameInfoWidget {\n"
"  background-color: #424245;\n"
"  border-color: #4d4d50;\n"
"  color: #f1f1f1;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"  padding: 2px;\n"
"}\n"
"\n"
"QStatusBar::item {\n"
"  border: None;\n"
"}\n"
"\n"
"/* Progress Bars (Downloads) #QProgressBar */\n"
"QProgressBar {\n"
"  background-color: #e6e6e6;\n"
"  color: #000;\n"
"  border-color: #bcbcbc;\n"
"  text-align: center;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"  margin: 0px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"  background: #06b025;\n"
"}\n"
"\n"
"DownloadListView[downloadView=standard]::item {\n"
"  padding: 16px;\n"
"}\n"
"\n"
"DownloadListView[downloadView=compact]::item {\n"
"  padding: "
                        "4px;\n"
"}\n"
"\n"
"/* Right Pane and Tab Bars #QTabWidget, #QTabBar */\n"
"QTabWidget::pane {\n"
"  border-color: #3f3f46;\n"
"  border-top-color: #007acc;\n"
"  top: 0;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QTabWidget::pane:disabled {\n"
"  border-top-color: #3f3f46;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"  background-color: transparent;\n"
"  padding: 4px 1em;\n"
"  border: none;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"  background-color: #1c97ea;\n"
"}\n"
"\n"
"QTabBar::tab:selected,\n"
"QTabBar::tab:selected:hover {\n"
"  background-color: #007acc;\n"
"}\n"
"\n"
"QTabBar::tab:disabled {\n"
"  background-color: transparent;\n"
"  color: #656565;\n"
"}\n"
"\n"
"QTabBar::tab:selected:disabled {\n"
"  background-color: #3f3f46;\n"
"}\n"
"\n"
"/* Scrollers */\n"
"QTabBar QToolButton {\n"
"  background-color: #333337;\n"
"  border-color: #3f3f46;\n"
"  padding: 1px;\n"
"  margin: 0;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QTabBar QToolButton:hover {\n"
"  borde"
                        "r-color: #007acc;\n"
"  border-width: 1px;\n"
"  border-style: solid;\n"
"}\n"
"\n"
"QTabBar QToolButton:disabled,\n"
"QTabBar QToolButton:pressed:hover {\n"
"  background-color: #333337;\n"
"}\n"
"\n"
"QTabBar::scroller {\n"
"  width: 23px;\n"
"  background-color: red;\n"
"}\n"
"\n"
"QTabBar QToolButton::right-arrow {\n"
"  image: url(:/png/resources/png/scrollbar-right.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::right-arrow:hover {\n"
"  image: url(:/png/resources/png/scrollbar-right-hover.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::left-arrow {\n"
"  image: url(:/png/resources/png/scrollbar-left.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::left-arrow:hover {\n"
"  image: url(:/png/resources/png/scrollbar-left-hover.png);\n"
"}\n"
"\n"
"/* Special styles */\n"
"QWidget#tabImages QPushButton {\n"
"  background-color: transparent;\n"
"  margin: 0 0.3em;\n"
"  padding: 0;\n"
"}\n"
"\n"
"/* like dialog QPushButton*/\n"
"QWidget#tabESPs QToolButton {\n"
"  color: #000000;\n"
"  background-color: #dddddd;\n"
"  border-co"
                        "lor: #707070;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"}\n"
"\n"
"QWidget#tabESPs QToolButton:hover {\n"
"  background-color: #BEE6FD;\n"
"  border-color: #3c7fb1;\n"
"}\n"
"\n"
"QWidget#tabESPs QToolButton:focus {\n"
"  background-color: #dddddd;\n"
"  border-color: #3399ff;\n"
"}\n"
"\n"
"QWidget#tabESPs QToolButton:disabled {\n"
"  background-color: #333337;\n"
"  border-color: #3f3f46;\n"
"}\n"
"\n"
"QTreeWidget#categoriesList {\n"
"  /* min-width: 225px; */\n"
"}\n"
"\n"
"QTreeWidget#categoriesList::item {\n"
"  background-position: center left;\n"
"  background-repeat: no-repeat;\n"
"  padding: 0.35em 10px;\n"
"}\n"
"\n"
"QTreeWidget#categoriesList::item:has-children {\n"
"  background-image: url(:/png/resources/png/branch-closed.png);\n"
"}\n"
"\n"
"QTreeWidget#categoriesList::item:has-children:open {\n"
"  background-image: url(:/png/resources/png/branch-open.png);\n"
"}\n"
"\n"
"QDialog#QueryOverwriteDialog QPushButton {\n"
"  margin-left: 0.5em;\n"
"}\n"
"\n"
"QDialog#PyCfgDialog QPush"
                        "Button:hover {\n"
"  background-color: #BEE6FD;\n"
"}\n"
"\n"
"QLineEdit#modFilterEdit {\n"
"  margin-top: 2px;\n"
"}\n"
"\n"
"/* highlight unchecked BSAs */\n"
"QWidget#bsaTab QTreeWidget::indicator:unchecked {\n"
"  background-color: #3399ff;\n"
"}\n"
"\n"
"/* increase version text field */\n"
"QLineEdit#versionEdit {\n"
"  max-width: 100px;\n"
"}\n"
"\n"
"/* Dialogs width changes */\n"
"/* increase width to prevent buttons cutting */\n"
"QDialog#QueryOverwriteDialog {\n"
"  min-width: 565px;\n"
"}\n"
"\n"
"QDialog#ModInfoDialog {\n"
"  min-width: 850px;\n"
"}\n"
"\n"
"QLineEdit[valid-filter=false] {\n"
"  background-color: #661111 !important;\n"
"}")
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
        self.action_edit_tags = QAction(MainWindow)
        self.action_edit_tags.setObjectName(u"action_edit_tags")
        self.action_edit_tags.setEnabled(False)
        icon5 = QIcon()
        icon5.addFile(u":/white-icons/resources/white-icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_tags.setIcon(icon5)
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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.centralwidget_splitter = QSplitter(self.centralwidget)
        self.centralwidget_splitter.setObjectName(u"centralwidget_splitter")
        self.centralwidget_splitter.setOrientation(Qt.Horizontal)
        self.gb_left = QGroupBox(self.centralwidget_splitter)
        self.gb_left.setObjectName(u"gb_left")
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
        self.title_structure_execdoc.setEnabled(True)

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
        self.horizontalLayout = QHBoxLayout(self.gb_center)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_pdf_view = QPdfView(self.gb_center)
        self.widget_pdf_view.setObjectName(u"widget_pdf_view")
        self.widget_pdf_view.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.widget_pdf_view)

        self.centralwidget_splitter.addWidget(self.gb_center)
        self.gb_right = QGroupBox(self.centralwidget_splitter)
        self.gb_right.setObjectName(u"gb_right")
        sizePolicy1.setHeightForWidth(self.gb_right.sizePolicy().hasHeightForWidth())
        self.gb_right.setSizePolicy(sizePolicy1)
        self.gb_right.setMinimumSize(QSize(300, 0))
        self.gb_right.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.gb_right.setFlat(False)
        self.verticalLayout_4 = QVBoxLayout(self.gb_right)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollarea_inputforms = QScrollArea(self.gb_right)
        self.scrollarea_inputforms.setObjectName(u"scrollarea_inputforms")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollarea_inputforms.sizePolicy().hasHeightForWidth())
        self.scrollarea_inputforms.setSizePolicy(sizePolicy2)
        self.scrollarea_inputforms.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollarea_inputforms.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea_inputforms.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollarea_inputforms.setWidgetResizable(True)
        self.scrollarea_inputforms.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollarea_inputforms_layout = QWidget()
        self.scrollarea_inputforms_layout.setObjectName(u"scrollarea_inputforms_layout")
        self.scrollarea_inputforms_layout.setGeometry(QRect(0, 0, 248, 625))
        self.scrollarea_inputforms_layout.setMouseTracking(True)
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
        self.menu_bar.setGeometry(QRect(0, 0, 1366, 22))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_recent_projects = QMenu(self.menu_file)
        self.menu_recent_projects.setObjectName(u"menu_recent_projects")
        self.menu_help = QMenu(self.menu_bar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_tools = QMenu(self.menu_bar)
        self.menu_tools.setObjectName(u"menu_tools")
        MainWindow.setMenuBar(self.menu_bar)
        self.tb_main = QToolBar(MainWindow)
        self.tb_main.setObjectName(u"tb_main")
        self.tb_main.setEnabled(True)
        self.tb_main.setAllowedAreas(Qt.TopToolBarArea)
        self.tb_main.setOrientation(Qt.Horizontal)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.tb_main)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        self.status_bar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_tools.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.menu_recent_projects.menuAction())
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_export_to_pdf)
        self.menu_tools.addAction(self.action_edit_tags)
        self.menu_tools.addAction(self.action_edit_templates)
        self.tb_main.addAction(self.action_new)
        self.tb_main.addAction(self.action_open)
        self.tb_main.addAction(self.action_save)
        self.tb_main.addAction(self.action_export_to_pdf)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_edit_tags)
        self.tb_main.addAction(self.action_edit_templates)
        self.tb_main.addAction(self.action_edit_composition)
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
        self.action_edit_tags.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0442\u0435\u0433\u043e\u0432", None))
        self.action_edit_tags.setIconText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0442\u0435\u0433\u043e\u0432", None))
#if QT_CONFIG(tooltip)
        self.action_edit_tags.setToolTip(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0442\u0435\u0433\u043e\u0432", None))
#endif // QT_CONFIG(tooltip)
        self.action_zoomfitpage.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e \u0448\u0438\u0440\u0438\u043d\u0435", None))
        self.action_export_to_pdf.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 PDF", None))
        self.action_edit_templates.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432", None))
        self.action_edit_composition.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u043e\u0441\u0442\u0430\u0432\u0430 \u0418\u0414", None))
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

        self.label_current_template.setText(QCoreApplication.translate("MainWindow", u"\u0428\u0430\u0431\u043b\u043e\u043d", None))
        self.label_pages_template.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u0448\u0430\u0431\u043b\u043e\u043d\u0430", None))

        __sortingEnabled1 = self.lw_pages_template.isSortingEnabled()
        self.lw_pages_template.setSortingEnabled(False)
        ___qlistwidgetitem = self.lw_pages_template.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 1", None));
        ___qlistwidgetitem1 = self.lw_pages_template.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 2", None));
        self.lw_pages_template.setSortingEnabled(__sortingEnabled1)

        self.gb_center.setTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0432 \u0440\u0435\u0436\u0438\u043c\u0435 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0432\u0440\u0435\u043c\u0435\u043d\u0438", None))
        self.gb_right.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u043e\u0434 ", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_recent_projects.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u0434\u0430\u0432\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u044b", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.menu_tools.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b", None))
        self.tb_main.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

