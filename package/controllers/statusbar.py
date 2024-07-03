
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

    def set_message_for_statusbar(self, message: str):
        """
        Поставить сообщение в статусбар.
        """
        self.__statusbar.showMessage(message)
        self.__obs_manager.obj_l.debug_logger(f"set_message_for_statusbar({message})")


# obj_sb = StatusBar()
