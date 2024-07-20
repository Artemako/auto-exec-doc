
from PySide6.QtWidgets import QStatusBar, QLabel, QPushButton

import package.components.convertersettingsdialogwindow as convertersettingsdialogwindow

class StatusBar:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__statusbar = None

    def connect_statusbar(self, statusbar):
        """
        Подключить статусбар.
        """
        self.__obs_manager.obj_l.debug_logger("IN connect_statusbar(statusbar)")
        self.__statusbar = statusbar
        self.config_statusbar()
        self.set_message_for_statusbar("Проект не открыт")
        self.update_name_app_converter()
        self.connecting_actions()

    def config_statusbar(self):
        # статус работоспосбности конвертера
        status_converter = QLabel("Статус конвертера: ...")
        setattr(self.__statusbar, "status_converter", status_converter)
        self.__statusbar.addPermanentWidget(status_converter)   
        # выбранный конвертер
        name_app_converter = QLabel("NONE")
        setattr(self.__statusbar, "name_app_converter", name_app_converter)
        self.__statusbar.addPermanentWidget(name_app_converter) 
        # кнопка настройки конвертера
        btn_setting_converter = QPushButton("Настройка конвертера")    
        setattr(self.__statusbar, "btn_setting_converter", btn_setting_converter)
        self.__statusbar.addPermanentWidget(btn_setting_converter) 
        # TODO добавить активности для настройки конвертера    

    def set_message_for_statusbar(self, message: str):
        """
        Поставить сообщение в статусбар.
        """
        self.__statusbar.showMessage(message)
        self.__obs_manager.obj_l.debug_logger(f"set_message_for_statusbar(message):\nmessage = {message}")


    def update_name_app_converter(self):
        app_converter = self.__obs_manager.obj_sd.get_app_converter()
        print(f"app_converter = {app_converter}")
        name_app_converter = "None"
        if app_converter == "MSWORD":
            name_app_converter = "MS Word"
        # elif app_converter == "OPENOFFICE":
        #     name_app_converter = "OpenOffice"
        elif app_converter == "LIBREOFFICE":
            name_app_converter = "LibreOffice"
        print(f"name_app_converter = {name_app_converter}")
        self.__statusbar.name_app_converter.setText(name_app_converter)
        self.__obs_manager.obj_l.debug_logger("update_name_app_converter()")

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger("IN connecting_actions()")
        self.__statusbar.btn_setting_converter.clicked.connect(self.show_converter_settings)
        
    def show_converter_settings(self):
        self.__obs_manager.obj_l.debug_logger("IN show_converter_settings()")
        self.__obs_manager.obj_csdw = convertersettingsdialogwindow.ConverterSettingsDialogWindow(self.__obs_manager)
        self.__obs_manager.obj_csdw.exec()


# obj_sb = StatusBar()
