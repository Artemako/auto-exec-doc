import package.modules.log as log

from PySide6.QtWidgets import QStatusBar

class StatusBar:
    __statusbar = None

    def connect_statusbar(statusbar):
        """
        Подключить статусбар.
        """
        log.Log.debug_logger("IN connect_statusbar(statusbar)")
        StatusBar.__statusbar = statusbar
        StatusBar.set_message_for_statusbar("Проект не открыт")


    @staticmethod
    def set_message_for_statusbar(message: str):
        """
        Поставить сообщение в статусбар.
        """
        StatusBar.__statusbar.showMessage(message)
        log.Log.debug_logger(f"set_message_for_statusbar({message})")