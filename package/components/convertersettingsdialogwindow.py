from PySide6.QtWidgets import (
    QDialog
)

from functools import partial

import package.ui.convertersettingsdialogwindow_ui as convertersettingsdialogwindow_ui

class ConverterSettingsDialogWindow(QDialog):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("ConverterSettingsDialogWindow __init__(obs_manager)")
        super(ConverterSettingsDialogWindow, self).__init__()
        self.ui = convertersettingsdialogwindow_ui.Ui_ConverterSettingsDialogWindow()
        self.ui.setupUi(self)
        # конфигурация
        self.config()
        # подключаем деействия
        self.connecting_actions()


    def config(self):
        self.__obs_manager.obj_l.debug_logger("ConverterSettingsDialogWindow config()")
        # постоянный размер
        self.setFixedSize(self.sizeHint())
        app_converter = self.__obs_manager.obj_sd.get_app_converter()
        if app_converter == "MSWORD":
            self.ui.radbtn_msword.setChecked(True)
        # elif app_converter == "OPENOFFICE":
        #     self.ui.radbtn_openoffice.setChecked(True)
        elif app_converter == "LIBREOFFICE":
            self.ui.radbtn_libreoffice.setChecked(True)

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger("ConverterSettingsDialogWindow connecting_actions()")
        self.ui.btn_close.clicked.connect(self.close_window)
        self.ui.btn_save.clicked.connect(self.save_converter)

    def get_active_radiobutton(self) -> str:
        result = None
        if self.ui.radbtn_msword.isChecked():
            result = "MSWORD"
        # elif self.ui.radbtn_openoffice.isChecked():
        #     result = "OPENOFFICE"
        elif self.ui.radbtn_libreoffice.isChecked():
            result = "LIBREOFFICE"
        self.__obs_manager.obj_l.debug_logger(f"ConverterSettingsDialogWindow get_active_radiobutton() -> str:\nresult = {result}")
        return result


    def save_converter(self):
        self.__obs_manager.obj_l.debug_logger("ConverterSettingsDialogWindow save()")
        result = self.get_active_radiobutton()
        if result:
            self.__obs_manager.obj_sd.set_app_converter(result)
            self.__obs_manager.obj_sb.set_message(f"{self.windowTitle()}: сохранение прошло успешно!")
        else:
            self.__obs_manager.obj_dw.error_message("Не выбран конвертер.")
        self.__obs_manager.obj_sb.update_name_app_converter()
        

    def close_window(self):
        self.__obs_manager.obj_l.debug_logger("ConverterSettingsDialogWindow close_window()")
        self.close()
