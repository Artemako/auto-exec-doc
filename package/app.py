import sys


from PySide2.QtWidgets import QApplication


import package.components.mainwindow as mainwindow
import package.modules.settingsdatabase as settingsdatabase
import package.modules.log as log
import package.modules.filefoldermanager as filefoldermanager
import package.modules.dirpathsmanager as dirpathsmanager


class App:
    def __init__(self, current_directory):
        self.current_directory = current_directory
        self.check_before_run()
        self.start_app()

    def check_before_run(self):
        """
        Проверить и наcтроить до запуска.
        """
        # настройка путей 
        dirpathsmanager.DirPathManager.config_paths(self.current_directory)    
        # настроить loggerpy
        log.Log.config_logger()
        log.Log.debug_logger(f"self.current_directory = {self.current_directory}")            
        # Проверка наличия папок.
        filefoldermanager.FileFolderManager.create_and_config_files_and_folders()
        # настроить БД
        settingsdatabase.Database.create_and_config_db_settings()

    def start_app(self):
        """
        Запуск фронта.
        """
        print("dirpathsmanager.DirPathManager.get_templates_main_dirpath() =", dirpathsmanager.DirPathManager.get_templates_main_dirpath())
        self.app = QApplication(sys.argv)
        self.window = mainwindow.MainWindow()
        self.window.show()
        sys.exit(self.app.exec())


    



