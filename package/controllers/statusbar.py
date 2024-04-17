import package.modules.log as log

from PySide6.QtWidgets import QStatusBar

class StatusBar:
    _statusbar = None

    def connect_statusbar(status_bar):
        """
        Подключить статусбар.
        """
        log.Log.debug_logger("IN connect_statusbar()")
        StatusBar.set_statusbar(status_bar)
        StatusBar.set_message_for_statusbar("Проект не открыт")

    @staticmethod
    def set_statusbar(statusbar):
        StatusBar._statusbar = statusbar
        log.Log.debug_logger("set_statusbar()")

    @staticmethod
    def get_statusbar() -> QStatusBar:
        log.Log.debug_logger("get_statusbar()")
        return StatusBar._statusbar

    @staticmethod
    def set_message_for_statusbar(message: str):
        """
        Поставить сообщение в статусбар.
        """
        StatusBar.get_statusbar().showMessage(message)
        log.Log.debug_logger(f"set_message_for_statusbar({message})")