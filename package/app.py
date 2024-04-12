import sys
import os

from PySide6.QtWidgets import QApplication


import package.components.mainwindow as mainwindow
import package.modules.database as database
import package.modules.log as log
import package.modules.filefoldermanager as filefoldermanager


class App:
    def __init__(self):
        self.check_before_run()
        self.start_app()

    def check_before_run(self):
        """
        Проверить и наcтроить до запуска.
        """

        # настроить logging
        # log.Log.create_and_config_logging()

        # Проверка наличия папок.
        filefoldermanager.FileFolderManager.create_and_config_files_and_folders()

        # настроить БД
        database.Database.create_and_config_database()

    def start_app(self):
        """
        Запуск фронта.
        """
        self.app = QApplication(sys.argv)
        self.window = mainwindow.MainWindow()
        self.window.show()
        sys.exit(self.app.exec())
