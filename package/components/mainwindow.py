from PySide6.QtWidgets import QMainWindow, QStatusBar

import package.ui.mainwindow_ui as mainwindow_ui
import package.modules.project as project


class MainWindow(QMainWindow):
    _statusbar = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect_statusbar()
        self.connecting_actions()

    def connect_statusbar(self):
        """
        Подключить статусбар.
        """
        MainWindow.set_statusbar(self.ui.status_bar)
        MainWindow.set_message_for_statusbar("Проект не открыт")

    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        self.ui.action_new.triggered.connect(lambda: project.Project.new_project())
        self.ui.action_open.triggered.connect(lambda: project.Project.open_project())
        # TODO
        # self.ui.action_save.triggered.connect()
        # self.ui.action_saveas.triggered.connect()
        self.ui.action_zoomin.triggered.connect(lambda: self.ui.pdfwidget.zoom_in())
        self.ui.action_zoomout.triggered.connect(lambda: self.ui.pdfwidget.zoom_out())

    @staticmethod
    def set_statusbar(statusbar):
        MainWindow._statusbar = statusbar

    @staticmethod
    def get_statusbar() -> QStatusBar:
        return MainWindow._statusbar

    @staticmethod
    def set_message_for_statusbar(message: str):
        """
        Поставить сообщение в статусбар.
        """
        MainWindow.get_statusbar().showMessage(message)
