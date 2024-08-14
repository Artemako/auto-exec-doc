import sys
from PySide6.QtWidgets import QApplication

import package.components.mainwindow as mainwindow

import package.controllers.icons as icons

# Импорт всех miodules
import package.modules.converter as converter
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.filefoldermanager as filefoldermanager
import package.modules.log as log
import package.modules.project as project
import package.modules.projectdatabase as projectdatabase
import package.modules.sectionsinfo as sectionsinfo
import package.modules.settingsdatabase as settingsdatabase
import package.modules.officepackets as officepackets

# Импорт всех controllers
import package.controllers.lwpagestemplate as lwpagestemplate
import package.controllers.pdfview as pdfview
import package.controllers.sainputforms as sainputforms
import package.controllers.statusbar as statusbar
import package.controllers.twstructureexecdoc as twstructureexecdoc
import package.controllers.comboxtemplates as comboxtemplates

# Импорт всех components
import package.components.style as style
import package.components.dialogwindow.dialogwindows as dialogwindows

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
        self.obj_ofp = None
        # controllers
        self.obj_lwpt = None
        self.obj_pv = None
        self.obj_saif = None
        self.obj_sb = None
        self.obj_twsed = None
        self.obj_comboxts = None
        # components (windows)
        self.obj_style = None
        self.obj_dw = None
        self.obj_mw = None
        self.obj_nedtdw = None
        self.obj_nedndw = None
        self.obj_tagsldw = None
        self.obj_nedw = None
        self.obj_csdw = None
        self.obj_templdw = None
        self.obj_nedtempdw = None
        self.obj_nedpagedw = None

    def initialize_all(self):
        """
        Инициализация всех объектов, кроме MainWindow.
        """
        self.initialize_modules()
        self.initialize_controllers()
        self.initialize_components()
        
    def initialize_modules(self):
        self.obj_l = log.Log()
        self.obj_c = converter.Converter()
        self.obj_dpm = dirpathsmanager.DirPathManager()
        self.obj_ffm = filefoldermanager.FileFolderManager()        
        self.obj_p = project.Project()
        self.obj_pd = projectdatabase.ProjectDatabase()
        self.obj_si = sectionsinfo.SectionsInfo()
        self.obj_sd = settingsdatabase.SettingsDatabase()
        self.obj_ofp = officepackets.OfficePackets()

    def initialize_controllers(self):
        self.obj_lwpt = lwpagestemplate.LWPagesTemplate()
        self.obj_pv = pdfview.PdfView()
        self.obj_saif = sainputforms.SAInputForms()
        self.obj_sb = statusbar.StatusBar()
        self.obj_twsed = twstructureexecdoc.TWStructureExecDoc()
        self.obj_icons = icons.Icons()
        self.obj_comboxts = comboxtemplates.ComboxTemplates()

    def initialize_components(self):
        self.obj_style = style.Style()
        self.obj_dw = dialogwindows.DialogWindows()

class App:
    def __init__(self, current_directory):
        self.current_directory = current_directory
        self.check_before_run()
        self.start_app()

    def setting_obs_manager(self):
        self.setting_obs_manager_for_modules()
        self.setting_obs_manager_for_controllers()
        self.setting_obs_manager_for_components()

    def setting_obs_manager_for_modules(self):
        self.obs_manager.obj_c.setting_obs_manager(self.obs_manager)
        self.obs_manager.obj_dpm.setting_obs_manager(self.obs_manager)
        self.obs_manager.obj_ffm.setting_obs_manager(self.obs_manager)
        self.obs_manager.obj_l.setting_obs_manager(self.obs_manager)
        self.obs_manager.obj_p.setting_all_obs_manager(self.obs_manager)
        self.obs_manager.obj_pd.setting_obs_manager(self.obs_manager)
        self.obs_manager.obj_si.setting_obs_manager(self.obs_manager)
        self.obs_manager.obj_sd.setting_obs_manager(self.obs_manager)
        self.obs_manager.obj_ofp.setting_all_obs_manager(self.obs_manager)

    def setting_obs_manager_for_controllers(self):    
        self.obs_manager.obj_lwpt.setting_all_obs_manager(self.obs_manager)
        self.obs_manager.obj_pv.setting_all_obs_manager(self.obs_manager)
        self.obs_manager.obj_saif.setting_all_obs_manager(self.obs_manager)
        self.obs_manager.obj_sb.setting_all_obs_manager(self.obs_manager)
        self.obs_manager.obj_twsed.setting_all_obs_manager(self.obs_manager)
        self.obs_manager.obj_icons.setting_all_obs_manager(self.obs_manager)
        self.obs_manager.obj_comboxts.setting_all_obs_manager(self.obs_manager)

    def setting_obs_manager_for_components(self):
        self.obs_manager.obj_dw.setting_all_obs_manager(self.obs_manager)

    def check_before_run(self):
        """
        Проверить и наcтроить до запуска.
        """
        # настройка хранилища экземпляров модулей
        self.obs_manager = ObjectsManager()
        self.obs_manager.initialize_all()
        self.setting_obs_manager()
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
        # настройка officepackets
        self.obs_manager.obj_ofp.resetting_office_packets()

    def start_app(self):
        """
        Запуск фронта.
        """
        try:
            self.app = QApplication(sys.argv)
            # создание окна
            self.window = mainwindow.MainWindow(self.obs_manager)
            # подключение MainWindow к obs_manager
            self.obs_manager.obj_mw = self.window
            self.window.show()
            # sys.exit(self.app.exec())
            self.app.exec_()
        except Exception as e:
            self.obs_manager.obj_l.error_logger(f"Error: {e}")

    
