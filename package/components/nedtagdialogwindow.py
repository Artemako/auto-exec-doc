from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QWidget,
)

import package.ui.nedtagdialogwindow_ui as nedtagdialogwindow_ui


class TagType:
    def __init__(self, index, name_type_tag, type_tag):
        self.index = index
        self.name_type_tag = name_type_tag
        self.type_tag = type_tag


class NedTagDialogWindow(QDialog):
    def __init__(self, obs_manager, type_window, tag=None):
        self.__obs_manager = obs_manager
        self.__type_window = type_window
        self.__tag = tag
        super(NedTagDialogWindow, self).__init__()
        self.ui = nedtagdialogwindow_ui.Ui_NedTagDialogWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        # Подключаем действия
        self.congig_combobox()
        # определить тип окна
        self.config()

    def get_tag_types(self):
        tag_types = [
            TagType(0, "Текст", "TEXT"),
            TagType(1, "Дата", "DATE"),
            TagType(2, "Таблица", "TABLE"),
            TagType(2, "Изображение", "IMAGE")
        ]
        return tag_types

    def congig_combobox(self):
        self.ui.combox_typetag.blockSignals(True)
        self.ui.combox_typetag.clear()
        tag_types = self.get_tag_types()
        for tag in tag_types:
            self.ui.combox_typetag.addItem(tag.name_type_tag, tag.type_tag)
        self.ui.combox_typetag.blockSignals(False)

    def config(self):
        if self.__type_window == "create":
            self.ui.btn_nestag.setText("Добавить тэг")
        elif self.__type_window == "edit":
            self.ui.btn_nestag.setText("Сохранить тэг")
            self.fill_data()
            self.config_additional_info()

    def config_additional_info(self):
        type_tag = self.__tag.get("type_tag")
        if type_tag == "TEXT":
            self.ui.additional_info.setVisible(False)
        elif type_tag == "DATE":
            # TODO
            self.ui.additional_info.setVisible(True)
        elif type_tag == "TABLE":
            # TODO
            self.ui.additional_info.setVisible(True)
        elif type_tag == "IMAGE":
            # TODO
            self.ui.additional_info.setVisible(True)

    def find_index_by_type(self, type_tag):
        tag_types = self.get_tag_types()
        for tag in tag_types:
            if tag.type_tag == type_tag:
                return tag.index

    def fill_data(self):
        print(f"tag = {self.__tag}")
        self.ui.lineedit_nametag.setText(self.__tag.get("name_tag"))
        self.ui.lineedit_titletag.setText(self.__tag.get("title_tag"))
        index = self.find_index_by_type(self.__tag.get("type_tag"))
        self.ui.combox_typetag.setCurrentIndex(index)
