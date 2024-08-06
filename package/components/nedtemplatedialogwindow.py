from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import package.ui.nedtemplatedialogwindow_ui as nedtemplatedialogwindow_ui

import resources_rc

# TODO ПОДУМАТЬ ПРО PDF 

class NedTemplateDialogWindow(QDialog):
    def __init__(self, obs_manager, type_ned, template=None):
        self.__obs_manager = obs_manager
        self.__type_ned = type_ned
        self.__template = template
        self.__obs_manager.obj_l.debug_logger(
            f"NedTemplateDialogWindow __init__(obs_manager, type_ned):\nself.__type_ned = {self.__type_ned}"
        )
        super(NedTemplateDialogWindow, self).__init__()
        self.ui = nedtemplatedialogwindow_ui.Ui_NedTemplateDialogWindow()
        self.ui.setupUi(self)
        #
        self.__data = []
        self.__icons = self.__obs_manager.obj_gf.get_icons()
        # одноразовые действия
        self.config_by_type_window()
        self.connecting_actions()

    def get_data(self):
        self.__obs_manager.obj_l.debug_logger(
            f"NedTemplateDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_by_type_window(self):
        self.__obs_manager.obj_l.debug_logger(
            "NedTemplateDialogWindow config_by_type_window()"
        )
        if self.__type_ned == "create":
            self.ui.label_nametemplate.setText("Название нового шаблона")
            self.ui.btn_nestag.setText("Добавить тэг")
            self.ui.btn_nestag.setIcon(self.__icons.get("qicon_add"))
        elif self.__type_ned == "edit":
            self.ui.label_nametemplate.setText("Название шаблона")
            self.ui.lineedit_nametemplate.setText(self.__template.get("name_template"))
            self.ui.btn_nestag.setText("Сохранить тэг")
            self.ui.btn_nestag.setIcon(self.__icons.get("qicon_save"))

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger(
            "NedTemplateDialogWindow connecting_actions()"
        )
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_nestag.clicked.connect(self.btn_nestag_clicked)

    def btn_nestag_clicked(self):
        self.__obs_manager.obj_l.debug_logger(
            "NedTemplateDialogWindow btn_nestag_clicked()"
        )
        self.__data = self.ui.lineedit_nametemplate.text()
        if len(self.__data) > 0:
            self.accept()
        else:
            self.__obs_manager.obj_dw.warning_message("Заполните поле названия")