
from PySide6.QtWidgets import QStatusBar


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
        self.set_message_for_statusbar("Проект не открыт")
        self.update_name_app_converter()

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
        elif app_converter == "OPENOFFICE":
            name_app_converter = "OpenOffice"
        elif app_converter == "LIBREOFFICE":
            name_app_converter = "LibreOffice"
        print(f"name_app_converter = {name_app_converter}")
        self.__statusbar.name_app_converter.setText(name_app_converter)
        self.__obs_manager.obj_l.debug_logger("update_name_app_converter()")

# obj_sb = StatusBar()
