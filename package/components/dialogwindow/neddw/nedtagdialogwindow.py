from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer

import re

import package.ui.nedtagdialogwindow_ui as nedtagdialogwindow_ui

import package.components.widgets.nedtags.neddatetag as neddatetag
import package.components.widgets.nedtags.nedtabletag as nedtabletag



class NedTagDialogWindow(QDialog):
    def __init__(self, osbm, type_window, tag=None):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"NedTagDialogWindow(osbm, type_window):\ntype_window = {type_window}\ntag = {tag}"
        )
        self.__type_window = type_window
        self.__tag = tag
        super(NedTagDialogWindow, self).__init__()
        self.ui = nedtagdialogwindow_ui.Ui_NedTagDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        # одноразовые действия
        self.__additional_widget = None
        self.__data = None
        self.__icons = self.__osbm.obj_icons.get_icons()
        #
        self.config_combobox()
        self.config_by_type_window()
        self.config_maindata()
        # многоразовые действия
        self.update_additional_info()
        # подключаем действия
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedTagDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow connecting_actions()")
        self.ui.combox_typetag.currentIndexChanged.connect(
            self.on_combox_typetag_changed
        )
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_nestag.clicked.connect(self.btn_nestag_clicked)
        self.ui.btn_nestag.setShortcut("Ctrl+S")

    def get_is_valid_jinja_tag(self, name_tag):
        pattern = r'^[\w.-]+$'  # эквивалентно [a-zA-Z0-9_.-]
        result = bool(re.match(pattern, name_tag))
        self.__osbm.obj_logg.debug_logger(
            f"NedTagDialogWindow get_is_valid_jinja_tag(name_tag):\name_tag = {name_tag}\n result = {result}"
        )
        return result

    def btn_nestag_clicked(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow btn_nestag_clicked()")
        le_nametag = self.ui.lineedit_nametag.text()
        le_titletag = self.ui.lineedit_titletag.text()
        # проверка на пустоту (уникальность присутствует)
        is_valid_jinja_tag = self.get_is_valid_jinja_tag(le_nametag)
        if len(le_nametag) > 0 and len(le_titletag) > 0 and is_valid_jinja_tag:
            if self.__type_window == "create":
                self.add_new_tag()
            elif self.__type_window == "edit":
                self.save_edit_tag()
        elif le_nametag == "" and le_titletag == "" and is_valid_jinja_tag:
            self.__osbm.obj_dw.warning_message("Заполните все поля")
        elif le_nametag == "":
            self.__osbm.obj_dw.warning_message("Заполните поле тега")
        elif le_titletag == "":
            self.__osbm.obj_dw.warning_message("Заполните поле названия тега")
        elif not is_valid_jinja_tag:
            self.__osbm.obj_dw.warning_message("Уберите пробелы из имени тега.")
        else:
            self.__osbm.obj_dw.warning_message("Поле тега содержит недопустимые символы.")

    def add_new_tag(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow add_new_tag()")
        # получит data в зависимости от типа тега
        index = self.ui.combox_typetag.currentIndex()
        if index == 0:
            self.__data = {}
        else:
            self.__data = self.__additional_widget.get_save_data()
        # проверка на уникальность
        le_nametag = self.ui.lineedit_nametag.text()
        name_tag = self.__osbm.obj_prodb.get_tag_by_name(le_nametag)
        if name_tag:
            self.__osbm.obj_dw.warning_message(
                "Тег с таким именем уже существует."
            )
        else:
            self.accept()

    def save_edit_tag(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow save_edit_tag()")
        # текущий индекс
        index = self.ui.combox_typetag.currentIndex()
        if index == 0:
            self.__data = {}
        else:
            self.__data = self.__additional_widget.get_save_data()
        # проверка на уникальность
        le_nametag = self.ui.lineedit_nametag.text()
        old_name_tag = self.__tag.get("name_tag")
        name_tag = self.__osbm.obj_prodb.get_tag_by_name(le_nametag)        
        if le_nametag == old_name_tag:
            # ↑ если имя тега не изменилось
            self.accept()
        elif name_tag:
            self.__osbm.obj_dw.warning_message(
                "Другой тег с таким именем уже существует."
            )
        else:
            self.accept()
            

    def on_combox_typetag_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"NedTagDialogWindow on_combox_typetag_changed(index):\nindex = {index}"
        )
        self.update_additional_info(index)

    def config_combobox(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow config_combobox()")
        self.ui.combox_typetag.blockSignals(True)
        self.ui.combox_typetag.clear()
        tag_types = self.__osbm.obj_com.tag_types.get_tag_types()
        for tag in tag_types:
            self.ui.combox_typetag.addItem(tag.icon, tag.name_type_tag)
        self.ui.combox_typetag.blockSignals(False)

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTagDialogWindow config_by_type_window()"
        )
        if self.__type_window == "create":
            self.ui.btn_nestag.setText("Добавить тэг")

        elif self.__type_window == "edit":
            self.ui.btn_nestag.setText("Сохранить тэг")

    def config_maindata(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow fill_maindata()")
        print(f"tag = {self.__tag}")
        if self.__tag:
            self.ui.lineedit_nametag.setText(self.__tag.get("name_tag"))
            self.ui.lineedit_titletag.setText(self.__tag.get("title_tag"))
            index = self.find_index_by_type(self.__tag.get("type_tag"))
            self.ui.combox_typetag.blockSignals(True)
            self.ui.combox_typetag.setCurrentIndex(index)
            self.ui.combox_typetag.blockSignals(False)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def update_additional_info(self, index=None):
        self.__osbm.obj_logg.debug_logger(
            f"NedTagDialogWindow config_additional_info(index):\nindex = {index}"
        )
        if index is None:
            index = self.find_index_by_type(self.__tag.get("type_tag"))
        self.clear_layout(self.ui.vbl_additional_info)
        self.__additional_widget = None
        if index == 1:
            self.__additional_widget = neddatetag.NedDateTag(
                self.__osbm, self.__type_window, self.__tag
            )
            self.ui.vbl_additional_info.addWidget(self.__additional_widget)
        elif index == 2:
            self.__additional_widget = nedtabletag.NedTableTag(
                self.__osbm, self.__type_window, self.__tag
            )
            self.ui.vbl_additional_info.addWidget(self.__additional_widget)
        # TODO Изображение
        # elif index == 3:
        #     new_widget = ...
        QTimer.singleShot(0, self, lambda: self.resize_window())

    def resize_window(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow resize_window()")
        width = self.width()
        min_width = self.minimumWidth()
        # self.adjustSize()
        # self.adjustSize()
        # self.resize(width, self.height())
        self.setMinimumWidth(width)
        self.adjustSize()
        self.setMinimumWidth(min_width)

    def find_index_by_type(self, type_tag):
        self.__osbm.obj_logg.debug_logger(
            f"NedTagDialogWindow find_index_by_type(type_tag):\ntype_tag = {type_tag}"
        )
        tag_types = self.__osbm.obj_com.tag_types.get_tag_types()
        for tag in tag_types:
            if tag.type_tag == type_tag:
                return tag.index
