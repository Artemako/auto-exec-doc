from PySide6.QtWidgets import (
    QDialog
)
from PySide6.QtCore import Qt

from functools import partial

import package.ui.convertersettingsdialogwindow_ui as convertersettingsdialogwindow_ui

class ConverterSettingsDialogWindow(QDialog):
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow __init__(osbm)")
        super(ConverterSettingsDialogWindow, self).__init__()
        self.ui = convertersettingsdialogwindow_ui.Ui_ConverterSettingsDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        # конфигурация
        self.config()
        # подключаем деействия
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def config(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow config()")
        # постоянный размер
        self.setFixedSize(self.sizeHint())
        app_converter = self.__osbm.obj_setdb.get_app_converter()
        if app_converter == "MSWORD":
            self.ui.radbtn_msword.setChecked(True)
        # elif app_converter == "OPENOFFICE":
        #     self.ui.radbtn_openoffice.setChecked(True)
        elif app_converter == "LIBREOFFICE":
            self.ui.radbtn_libreoffice.setChecked(True)
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow connecting_actions()")
        self.ui.btn_close.clicked.connect(self.close_window)
        self.ui.btn_save.clicked.connect(self.save_converter)
        self.ui.btn_save.setShortcut("Ctrl+S")
        self.ui.btn_close.setShortcut("Ctrl+Q")


    def get_active_radiobutton(self) -> str:
        result = None
        if self.ui.radbtn_msword.isChecked():
            result = "MSWORD"
        # elif self.ui.radbtn_openoffice.isChecked():
        #     result = "OPENOFFICE"
        elif self.ui.radbtn_libreoffice.isChecked():
            result = "LIBREOFFICE"
        self.__osbm.obj_logg.debug_logger(f"ConverterSettingsDialogWindow get_active_radiobutton() -> str:\nresult = {result}")
        return result


    def save_converter(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow save()")
        result = self.get_active_radiobutton()
        if result:
            self.__osbm.obj_setdb.set_app_converter(result)
            self.__osbm.obj_offp.resetting_office_packets()
            self.__osbm.obj_stab.set_message(f"{self.windowTitle()}: сохранение прошло успешно!")
        else:
            self.__osbm.obj_dw.error_message("Не выбран конвертер.")
        self.__osbm.obj_stab.update_name_app_converter()
        

    def close_window(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow close_window()")
        self.close()
