import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

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
# import package.modules.settingsdatabase as settingsdatabase
import package.modules.settingsmanager as settingsmanager
import package.modules.officepackets as officepackets
import package.modules.imageresizer as imageresizer

import package.common as common
import package.commonwithosbm as commonwithosbm

# Импорт всех controllers
import package.controllers.lwpagestemplate as lwpagestemplate
import package.controllers.pdfview as pdfview
import package.controllers.tabwinputforms as tabwinputforms
import package.controllers.statusbar as statusbar
import package.controllers.twstructureexecdoc as twstructureexecdoc
import package.controllers.comboxtemplates as comboxtemplates

# Импорт всех components
import package.controllers.style as style
import package.components.dialogwindow.dialogwindows as dialogwindows

class ObjectsManager:
    """
    Мененджер объектов.
    """
    def __init__(self):
        # modules
        self.obj_conv = None
        self.obj_dirm = None
        self.obj_film = None
        self.obj_logg = None
        self.obj_proj = None
        self.obj_prodb = None
        self.obj_seci = None
        self.obj_settings = None
        self.obj_offp = None
        self.obj_imgr = None
        # controllers
        self.obj_lwpt = None
        self.obj_pdfv = None
        self.obj_tabwif = None
        self.obj_stab = None
        self.obj_twsed = None
        self.obj_comt = None
        # components (windows)
        self.obj_style = None
        self.obj_dw = None
        self.obj_mw = None
        self.obj_nedtdw = None
        self.obj_nedndw = None
        self.obj_variablesldw = None
        self.obj_nedw = None
        self.obj_convsdw = None
        self.obj_templdw = None
        self.obj_nedtempdw = None
        self.obj_nedpagedw = None
        self.obj_nedrowcoldw = None
        self.obj_formtabledw = None
        self.obj_formlistdw = None
        self.obj_setdw = None
        self.obj_storagedw = None
        
        # общее
        self.obj_com = None
        self.obj_comwith = None

    def initialize_all(self):
        """
        Инициализация всех объектов, кроме MainWindow.
        """
        self.initialize_modules()
        self.initialize_controllers()
        self.initialize_components()
        self.obj_com = common.Common()
        self.obj_comwith = commonwithosbm.CommonWithOsmb()
        
    def initialize_modules(self):
        self.obj_logg = log.Log()
        self.obj_conv = converter.Converter()
        self.obj_dirm = dirpathsmanager.DirPathManager()
        self.obj_film = filefoldermanager.FileFolderManager()        
        self.obj_proj = project.Project()
        self.obj_prodb = projectdatabase.ProjectDatabase()
        self.obj_seci = sectionsinfo.SectionsInfo()
        self.obj_settings = settingsmanager.SettingsManager()
        self.obj_offp = officepackets.OfficePackets()        
        self.obj_imgr = imageresizer.ImageResizer()

    def initialize_controllers(self):
        self.obj_lwpt = lwpagestemplate.LWPagesTemplate()
        self.obj_pdfv = pdfview.PdfView()
        self.obj_tabwif = tabwinputforms.TabWInputForms()
        self.obj_stab = statusbar.StatusBar()
        self.obj_twsed = twstructureexecdoc.TWStructureExecDoc()
        self.obj_icons = icons.Icons()
        self.obj_comt = comboxtemplates.ComboxTemplates()
        self.obj_style = style.StyleController()

    def initialize_components(self):
        self.obj_dw = dialogwindows.DialogWindows()

class App:
    def __init__(self, current_directory):
        self.current_directory = current_directory
        self.check_before_run()
        self.start_app()

    def setting_osbm(self):
        self.setting_osbm_for_modules()
        self.setting_osbm_for_controllers()
        self.setting_osbm_for_components()
        self.osbm.obj_comwith.setting_all_osbm(self.osbm)

    def setting_osbm_for_modules(self):
        self.osbm.obj_conv.setting_osbm(self.osbm)
        self.osbm.obj_dirm.setting_osbm(self.osbm)
        self.osbm.obj_film.setting_osbm(self.osbm)
        self.osbm.obj_logg.setting_osbm(self.osbm)
        self.osbm.obj_proj.setting_all_osbm(self.osbm)
        self.osbm.obj_prodb.setting_osbm(self.osbm)
        self.osbm.obj_seci.setting_osbm(self.osbm)
        self.osbm.obj_settings.setting_osbm(self.osbm)
        self.osbm.obj_offp.setting_all_osbm(self.osbm)
        self.osbm.obj_imgr.setting_osbm(self.osbm)

    def setting_osbm_for_controllers(self):    
        self.osbm.obj_lwpt.setting_all_osbm(self.osbm)
        self.osbm.obj_pdfv.setting_all_osbm(self.osbm)
        self.osbm.obj_tabwif.setting_all_osbm(self.osbm)
        self.osbm.obj_stab.setting_all_osbm(self.osbm)
        self.osbm.obj_twsed.setting_all_osbm(self.osbm)
        self.osbm.obj_icons.setting_all_osbm(self.osbm)
        self.osbm.obj_comt.setting_all_osbm(self.osbm)
        self.osbm.obj_style.setting_all_osbm(self.osbm)

    def setting_osbm_for_components(self):
        self.osbm.obj_dw.setting_all_osbm(self.osbm)

    def check_before_run(self):
        """
        Проверить и наcтроить до запуска.
        """
        # настройка хранилища экземпляров модулей
        self.osbm = ObjectsManager()
        self.osbm.initialize_all()
        self.setting_osbm()
        # настройка путей
        self.osbm.obj_dirm.setting_paths(
            self.current_directory
        )
        # настроить loggerpy
        self.osbm.obj_logg.setting_logger()
        self.osbm.obj_logg.debug_logger(f"self.current_directory = {self.current_directory}")
        # Проверка наличия папок.
        self.osbm.obj_film.create_and_setting_files_and_folders()
        # настроить БД
        self.osbm.obj_settings.initialize_default_settings()
        # настройка officepackets
        self.osbm.obj_offp.resetting_office_packets()

    def start_app(self):
        """
        Запуск фронта.
        """
        try:
            self.app = QApplication(sys.argv)
            # настройка шрифтов
            self.__font_main = QFontDatabase.addApplicationFont(":/fonts/resources/fonts/OpenSans-VariableFont_wdth,wght.ttf")
            self.__font_italic = QFontDatabase.addApplicationFont(":/fonts/resources/fonts/OpenSans-Italic-VariableFont_wdth,wght.ttf")
            # Получаем название шрифта
            try:
                font_families = QFontDatabase.applicationFontFamilies(self.__font_main)
                if font_families:
                    self.__size_font = 10
                    self.__custom_font = QFont(font_families[0], self.__size_font)
                    self.app.setFont(self.__custom_font) 
            except Exception as e:
                self.osbm.obj_logg.error_logger(f"Error: {e}")
            # создание окна
            self.window = mainwindow.MainWindow(self.osbm)
            # подключение MainWindow к osbm
            self.osbm.obj_mw = self.window
            self.window.show()
            # sys.exit(self.app.exec())
            return self.app.exec()
        except Exception as e:
            self.osbm.obj_logg.error_logger(f"Error: {e}")

    
