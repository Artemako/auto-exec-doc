import package.modules.log as log

from PySide6.QtWidgets import QStatusBar


class StatusBar:
    def __init__(self) -> None:
        self.__statusbar = None

    def connect_statusbar(self, statusbar):
        """
        Подключить статусбар.
        """
        log.obj_l.debug_logger("IN connect_statusbar(statusbar)")
        self.__statusbar = statusbar
        self.set_message_for_statusbar("Проект не открыт")

    def set_message_for_statusbar(self, message: str):
        """
        Поставить сообщение в статусбар.
        """
        self.__statusbar.showMessage(message)
        log.obj_l.debug_logger(f"set_message_for_statusbar({message})")


obj_sb = StatusBar()
