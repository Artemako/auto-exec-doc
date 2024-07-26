import sys
from PySide6.QtWidgets import QApplication

import package.components.mainwindow as mainwindow

# Импорт всех miodules
import package.modules.converter as converter
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.filefoldermanager as filefoldermanager
import package.modules.log as log
import package.modules.project as project
import package.modules.projectdatabase as projectdatabase
import package.modules.sectionsinfo as sectionsinfo
import package.modules.settingsdatabase as settingsdatabase

# Импорт всех controllers
import package.controllers.pagestemplate as pagestemplate
import package.controllers.pdfview as pdfview
import package.controllers.scrollareainput as scrollareainput
import package.controllers.statusbar as statusbar
import package.controllers.structureexecdoc as structureexecdoc

# Импорт всех components
import package.components.dialogwindows as dialogwindows

class ObjectsManager:
    """
    Мененджер объектов.
    """
    def __init__(self):
        # modules
        self.obj_c = None
        self.obj_dpm = None
        self.obj_ffm = None
        self.obj_l = None
        self.obj_p = None
        self.obj_pd = None
        self.obj_si = None
        self.obj_sd = None
        # controllers
        self.obj_pt = None
        self.obj_pv = None
        self.obj_sai = None
        self.obj_sb = None
        self.obj_sed = None
        # components (windows)
        self.obj_dw = None
        self.obj_mw = None
        self.obj_nedtdw = None
        self.obj_tldw = None
        self.obj_tcdw = None
        self.obj_csdw = None

    def initialize_all(self):
        """
        Инициализация всех объектов, кроме MainWindow.
        """
        self.initialize_modules()
        self.initialize_controllers()
        self.initialize_components()
        
    def initialize_modules(self):
        self.obj_c = converter.Converter(self)
        self.obj_dpm = dirpathsmanager.DirPathManager(self)
        self.obj_ffm = filefoldermanager.FileFolderManager(self)
        self.obj_l = log.Log(self)
        self.obj_p = project.Project(self)
        self.obj_pd = projectdatabase.ProjectDatabase(self)
        self.obj_si = sectionsinfo.SectionsInfo(self)
        self.obj_sd = settingsdatabase.SettingsDatabase(self)

    def initialize_controllers(self):
        self.obj_pt = pagestemplate.PagesTemplate(self)
        self.obj_pv = pdfview.PdfView(self)
        self.obj_sai = scrollareainput.ScroolAreaInput(self)
        self.obj_sb = statusbar.StatusBar(self)
        self.obj_sed = structureexecdoc.StructureExecDoc(self)

    def initialize_components(self):
        self.obj_dw = dialogwindows.DialogWindows(self)

class App:
    def __init__(self, current_directory):
        self.current_directory = current_directory
        self.check_before_run()
        self.start_app()

    def check_before_run(self):
        """
        Проверить и наcтроить до запуска.
        """
        # настройка хранилища экземпляров модулей
        self.obs_manager = ObjectsManager()
        self.obs_manager.initialize_all()
        
        # настройка путей
        self.obs_manager.obj_dpm.setting_paths(
            self.current_directory
        )
        # настроить loggerpy
        self.obs_manager.obj_l.setting_logger()
        self.obs_manager.obj_l.debug_logger(f"self.current_directory = {self.current_directory}")
        # Проверка наличия папок.
        self.obs_manager.obj_ffm.create_and_setting_files_and_folders()
        # настроить БД
        self.obs_manager.obj_sd.create_and_setting_db_settings()
        # настроить concerter
        self.obs_manager.obj_c.setting_converter()

    def start_app(self):
        """
        Запуск фронта.
        """
        print(
            "self.obs_manager.obj_dpm.get_templates_main_dirpath() =",
            self.obs_manager.obj_dpm.get_templates_main_dirpath(),
        )
        self.app = QApplication(sys.argv)
        # создание окна
        self.window = mainwindow.MainWindow(self.obs_manager)
        # подключение MainWindow к obs_manager
        self.obs_manager.obj_mw = self.window
        self.window.show()
        # sys.exit(self.app.exec())
        self.app.exec_()

    
