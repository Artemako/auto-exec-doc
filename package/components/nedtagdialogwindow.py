from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import package.ui.nedtagdialogwindow_ui as nedtagdialogwindow_ui

import package.components.widgets.nedtags.nedcolumntabletag as nedcolumntabletag
import package.components.widgets.nedtags.neddatetag as neddatetag
import package.components.widgets.nedtags.nedtabletag as nedtabletag

import resources_rc


class TagType:
    def __init__(self, index, name_type_tag, type_tag, icon):
        self.index = index
        self.name_type_tag = name_type_tag
        self.type_tag = type_tag
        self.icon = icon


class NedTagDialogWindow(QDialog):
    def __init__(self, obs_manager, type_window, tag=None):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            f"NedTagDialogWindow(obs_manager, type_window):\ntype_window = {type_window}\ntag = {tag}"
        )
        self.__type_window = type_window
        self.__tag = tag
        super(NedTagDialogWindow, self).__init__()
        self.ui = nedtagdialogwindow_ui.Ui_NedTagDialogWindow()
        self.ui.setupUi(self)
        # одноразовые действия
        self.__icons = self.__obs_manager.obj_gf.get_icons()
        self.config_combobox()
        self.config_by_type_window()
        self.config_maindata()
        # многоразовые действия
        self.update_additional_info()
        # подключаем действия
        self.connecting_actions()

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow connecting_actions()")
        self.ui.combox_typetag.currentIndexChanged.connect(
            self.on_combox_typetag_changed
        )
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_nestag.clicked.connect(self.btn_nestag_clicked)
        
    def btn_nestag_clicked(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow btn_nestag_clicked()")
        if self.__type_window == "create":
            self.add_new_tag()
        elif self.__type_window == "edit":
            self.save_edit_tag()

    def add_new_tag(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow add_new_tag()")
        # TODO add_new_tag (проверить на наличие дупликатов) (при добавлении документа?)
        # self.__tag = старая информация


    def save_edit_tag(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow save_edit_tag()")
        # TODO Save (проверить на наличие дупликатов)
        print(f"tag = {self.__tag}")
        # self.__tag = старая информация

    def on_combox_typetag_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"NedTagDialogWindow on_combox_typetag_changed(index):\nindex = {index}"
        )
        self.update_additional_info(index)

    def config_combobox(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow config_combobox()")
        self.ui.combox_typetag.blockSignals(True)
        self.ui.combox_typetag.clear()
        tag_types = self.get_tag_types()
        for tag in tag_types:
            self.ui.combox_typetag.addItem(tag.icon, tag.name_type_tag)
        self.ui.combox_typetag.blockSignals(False)

    def config_by_type_window(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow config_by_type_window()")
        if self.__type_window == "create":
            self.ui.btn_nestag.setText("Добавить тэг")
            self.ui.btn_nestag.setIcon(self.__icons.get("qicon_add"))

        elif self.__type_window == "edit":
            self.ui.btn_nestag.setText("Сохранить тэг")
            self.ui.btn_nestag.setIcon(self.__icons.get("qicon_save"))

    def config_maindata(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow fill_maindata()")
        print(f"tag = {self.__tag}")
        if self.__tag:
            self.ui.lineedit_nametag.setText(self.__tag.get("name_tag"))
            self.ui.lineedit_titletag.setText(self.__tag.get("title_tag"))
            index = self.find_index_by_type(self.__tag.get("type_tag"))
            self.ui.combox_typetag.blockSignals(True)
            self.ui.combox_typetag.setCurrentIndex(index)
            self.ui.combox_typetag.blockSignals(False)

    def get_tag_types(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow get_tag_types()")
        # tag_types
        tag_types = [
            TagType(0, "Текст", "TEXT", self.__icons.get("qicon_text")),
            TagType(1, "Дата", "DATE", self.__icons.get("qicon_date")),
            TagType(2, "Таблица", "TABLE", self.__icons.get("qicon_table")),
            TagType(3, "Изображение", "IMAGE", self.__icons.get("qicon_image")),
        ]
        return tag_types

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def update_additional_info(self, index=None):
        self.__obs_manager.obj_l.debug_logger(
            f"NedTagDialogWindow config_additional_info(index):\nindex = {index}"
        )
        # TODO ???
        if index is None:
            index = self.find_index_by_type(self.__tag.get("type_tag"))
        self.clear_layout(self.ui.vbl_additional_info)
        if index == 1:
            new_widget = neddatetag.NedDateTag(self.__obs_manager)
            self.ui.vbl_additional_info.addWidget(new_widget)
        elif index == 2:
            new_widget = nedtabletag.NedTableTag(self.__obs_manager)
            self.ui.vbl_additional_info.addWidget(new_widget)
        elif index == 3:
            new_widget = ...
        QTimer.singleShot(0, self, lambda: self.resize_window())

    def resize_window(self):
        self.__obs_manager.obj_l.debug_logger("NedTagDialogWindow resize_window()")
        width = self.width()
        min_width = self.minimumWidth()
        # self.adjustSize()
        # self.adjustSize()
        # self.resize(width, self.height())
        self.setMinimumWidth(width)
        self.adjustSize()
        self.setMinimumWidth(min_width)

    def find_index_by_type(self, type_tag):
        self.__obs_manager.obj_l.debug_logger(
            f"NedTagDialogWindow find_index_by_type(type_tag):\ntype_tag = {type_tag}"
        )
        tag_types = self.get_tag_types()
        for tag in tag_types:
            if tag.type_tag == type_tag:
                return tag.index
