from PySide6.QtWidgets import QMainWindow, QStatusBar

import package.ui.mainwindow_ui as mainwindow_ui
import package.modules.project as project
import package.modules.log as log

import package.controllers.structureexecdoc as structureexecdoc
import package.controllers.pagestemplate as pagestemplate
import package.controllers.scrollareainput as scrollareainput


class MainWindow(QMainWindow):
    _statusbar = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # настройка MainWindow
        self.connect_statusbar()
        structureexecdoc.StructureExecdoc.connect_structureexecdoc(
            self.ui.treewidget_structure_execdoc
        )
        pagestemplate.PagesTemplate.connect_pagestemplate(
            self.ui.listwidget_pages_template
        )
        scrollareainput.ScroolAreaInput.connect_pagestemplate(
            self.ui.scrollarea_input, self.ui.scrollarea_input_contents
        )
        self.connecting_actions()

    def connect_statusbar(self):
        """
        Подключить статусбар.
        """
        log.Log.debug_logger("IN connect_statusbar()")
        MainWindow.set_statusbar(self.ui.status_bar)
        MainWindow.set_message_for_statusbar("Проект не открыт")

    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        log.Log.debug_logger("IN connecting_actions()")
        self.ui.action_new.triggered.connect(lambda: project.Project.new_project())
        self.ui.action_open.triggered.connect(lambda: project.Project.open_project())
        # TODO
        # self.ui.action_save.triggered.connect()
        # self.ui.action_saveas.triggered.connect()
        self.ui.action_zoomin.triggered.connect(lambda: self.ui.pdfwidget.zoom_in())
        self.ui.action_zoomout.triggered.connect(lambda: self.ui.pdfwidget.zoom_out())
        self.ui.action_zoomfitpage.triggered.connect(
            lambda: self.ui.pdfwidget.set_zoom_to_fit_view()
            if self.ui.action_zoomfitpage.isChecked()
            else self.ui.pdfwidget.set_zoom_custom()
        )

    @staticmethod
    def set_statusbar(statusbar):
        MainWindow._statusbar = statusbar
        log.Log.debug_logger("set_statusbar(statusbar)")

    @staticmethod
    def get_statusbar() -> QStatusBar:
        log.Log.debug_logger("get_statusbar() -> MainWindow._statusbar")
        return MainWindow._statusbar

    @staticmethod
    def set_message_for_statusbar(message: str):
        """
        Поставить сообщение в статусбар.
        """
        MainWindow.get_statusbar().showMessage(message)
        log.Log.debug_logger(f"set_message_for_statusbar({message})")
