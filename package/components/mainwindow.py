from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

import package.ui.mainwindow_ui as mainwindow_ui
import package.modules.project as project
import package.modules.log as log

import package.controllers.structureexecdoc as structureexecdoc
import package.controllers.pagestemplate as pagestemplate
import package.controllers.scrollareainput as scrollareainput
import package.controllers.statusbar as statusbar


class MainWindow(QMainWindow):
    _statusbar = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # настройка контроллеров
        self.config_controllers()
        # Подключаем действия
        self.connecting_actions()


    def config_controllers(self):
        """
        Method to configure controllers.
        """
        log.Log.debug_logger("IN config_controllers()")
        # настройка статус бара
        statusbar.StatusBar.connect_statusbar(self.ui.status_bar)
        # настройка structureexecdoc
        structureexecdoc.StructureExecDoc.connect_structureexecdoc(
            self.ui.treewidget_structure_execdoc,
            self.ui.title_structure_execdoc
        )
        # настройка pagestemplate
        pagestemplate.PagesTemplate.connect_pages_template(
            self.ui.listwidget_pages_template
        )
        # настройка inputforms
        scrollareainput.ScroolAreaInput.connect_inputforms(
            self.ui.scrollarea_inputforms, self.ui.scrollarea_inputforms_layout
        )


    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        log.Log.debug_logger("IN connecting_actions()")
        self.ui.action_new.triggered.connect(lambda: project.Project.new_project())
        self.ui.action_open.triggered.connect(lambda: project.Project.open_project())
        # TODO Добавить активности для сохранения
        # self.ui.action_save.triggered.connect()
        # self.ui.action_saveas.triggered.connect()
        self.ui.action_zoomin.triggered.connect(lambda: self.ui.pdfwidget.zoom_in())
        self.ui.action_zoomout.triggered.connect(lambda: self.ui.pdfwidget.zoom_out())
        self.ui.action_zoomfitpage.triggered.connect(
            lambda: self.ui.pdfwidget.set_zoom_to_fit_view()
            if self.ui.action_zoomfitpage.isChecked()
            else self.ui.pdfwidget.set_zoom_custom()
        )
