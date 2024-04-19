import os

import package.modules.log as log
import package.components.customsection as customsection
import package.modules.projectdatabase as projectdatabase
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.jsonmanager as jsonmanager

import package.components.customsection as customsection

import package.components.forms.formdate as formdate
import package.components.forms.formimage as formimage
import package.components.forms.formtable as formtable
import package.components.forms.formtext as formtext

from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class ScroolAreaInput:
    _scrollarea_input = None
    _scrollarea_input_layout = None

    _data = dict()

    def __init__(self):
        pass

    @staticmethod
    def set_sa(sa_if, sa_ifl):
        ScroolAreaInput._scrollarea_input = sa_if
        ScroolAreaInput._scrollarea_input_layout = sa_ifl
        sa_if.setWidget(sa_ifl)
        log.Log.debug_logger("set_sa()")

    @staticmethod
    def get_sa_if() -> object:
        log.Log.debug_logger("get_sa_if() -> object")
        return ScroolAreaInput._scrollarea_input

    @staticmethod
    def get_sa_ifl() -> object:
        log.Log.debug_logger("get_sa_ifl() -> object")
        return ScroolAreaInput._scrollarea_input_layout

    @staticmethod
    def get_data() -> object:
        log.Log.debug_logger("get_data() -> object")
        return ScroolAreaInput._data

    @staticmethod
    def set_data(data):
        log.Log.debug_logger("set_data(data)")
        ScroolAreaInput._data = data

    @staticmethod
    def clear_data():
        log.Log.debug_logger("clear_data()")
        ScroolAreaInput._data = dict()

    @staticmethod
    def connect_inputforms(sa_if, sa_ifl):
        """
        Подключить _scrollarea_input и _scrollarea_input_contents
        """
        log.Log.debug_logger("IN connect_pages_template(sa_if, sa_ifl)")
        ScroolAreaInput.set_sa(sa_if, sa_ifl)

    @staticmethod
    def delete_all_widgets_in_sa():
        """
        Удаление всех виджетов в ScroolAreaInput
        """
        log.Log.debug_logger("IN delete_all_widgets_in_sa()")

        log.Log.debug_logger("clear_sa()")
        layout = ScroolAreaInput.get_sa_ifl().layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                del item

    @staticmethod
    def save_data():
        """
        Cохранение _data
        """
        log.Log.debug_logger("IN save_data()")
        # TODO Сделать сохранение

    @staticmethod
    def update_scrollarea(page):
        """
        Обновление ScroolAreaInput
        """
        log.Log.debug_logger("IN update_scrollarea()")

        ScroolAreaInput.delete_all_widgets_in_sa()
        ScroolAreaInput.clear_data()

        parent_node = projectdatabase.Database.get_node_parent_from_pages(page)
        folder_form = parent_node.get("folder_form")
        folder_page = page.get("folder_page")
        json_dirpath = os.path.normpath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_project_dirpath(),
                "forms",
                folder_form,
                folder_page,
                f"{folder_page}.json",
            )
        )
        # получаем данные с json
        # TODO Подумать про _data
        data = jsonmanager.JsonManager.get_data_from_json_file(json_dirpath)
        ScroolAreaInput.set_data(data)

        section = customsection.Section()
        section_layout = QVBoxLayout()
        for key, value in data.items():
            config_content = projectdatabase.Database.get_content_config(key)
            # print(f"config_content = {config_content}")
            type_content = config_content.get("type_content")
            if type_content == "TEXT":
                item = formtext.FormText(config_content, value)
                section_layout.addWidget(item)
            # TODO добавить остальные типы форм
            # elif type_content == "DATE":
            #     item = formdate.FormDate(config_content, value)
            # elif type_content == "IMAGE":
            #     item = formimage.FormImage(config_content, value)
            # elif type_content == "TABLE":
            #     item = formtable.FormTable(config_content, value)

        section.setContentLayout(section_layout)

        ScroolAreaInput.get_sa_ifl().layout().addWidget(section)

        ScroolAreaInput.get_sa_ifl().layout().addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
