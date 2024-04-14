class StatusBar:
    _status_bar = None

    def __init__(self):
        pass

    @staticmethod
    def connect_statusbar(ui_status_bar):
        StatusBar._status_bar = ui_status_bar

    # def set_message_statusbar(self, message):
    #     """
    #     Метод установки сообщения в statusbar.
    #     """
    #     self.ui.status_bar.showMessage(message)
