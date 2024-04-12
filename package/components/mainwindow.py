from PySide6.QtWidgets import QMainWindow

import package.ui.mainwindow_ui as mainwindow_ui
import package.modules.project as project


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.connecting_actions()

    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        self.ui.action_new.triggered.connect(lambda: project.Project.new_project())
        self.ui.action_open.triggered.connect(lambda: project.Project.open_project())
        # self.ui.action_save.triggered.connect()
        # self.ui.action_saveas.triggered.connect()
        self.ui.action_zoomin.triggered.connect(lambda: self.ui.pdfwidget.zoom_in())
        self.ui.action_zoomout.triggered.connect(lambda: self.ui.pdfwidget.zoom_out())
