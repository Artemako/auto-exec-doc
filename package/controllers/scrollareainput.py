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
    __scrollarea_input = None
    __scrollarea_input_layout = None

    __data = dict()

    def __init__(self):
        pass

        return ScroolAreaInput.__scrollarea_input_layout

    @staticmethod
    def get_data() -> object:
        log.Log.debug_logger("get_data() -> object")
        return ScroolAreaInput.__data

    @staticmethod
    def connect_inputforms(sa_if, sa_ifl):
        """
        Подключить _scrollarea_input и _scrollarea_input_contents
        """
        log.Log.debug_logger("IN connect_pages_template(sa_if, sa_ifl)")
        ScroolAreaInput.__scrollarea_input = sa_if
        ScroolAreaInput.__scrollarea_input_layout = sa_ifl

    @staticmethod
    def delete_all_widgets_in_sa():
        """
        Удаление всех виджетов в ScroolAreaInput
        """
        log.Log.debug_logger("IN delete_all_widgets_in_sa()")

        log.Log.debug_logger("clear_sa()")
        layout = ScroolAreaInput.__scrollarea_input_layout.layout()
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
        ScroolAreaInput.__data = dict()

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
        ScroolAreaInput.__data = data

        section = customsection.Section()
        section_layout = QVBoxLayout()
        for key, value in data.items():
            config_content = projectdatabase.Database.get_config_content(key)
            # print(f"config_content = {config_content}")
            id_content = config_content.get("id_content")
            type_content = config_content.get("type_content")
            if type_content == "TEXT":
                item = formtext.FormText(config_content, value)
                section_layout.addWidget(item)
            # TODO добавить остальные типы форм
            elif type_content == "DATE":
                config_date = projectdatabase.Database.get_config_date(id_content)
                item = formdate.FormDate(config_content, config_date, value)
            # elif type_content == "IMAGE":
            #     item = formimage.FormImage(config_content, value)
            # elif type_content == "TABLE":
            #     item = formtable.FormTable(config_content, value)

        section.setContentLayout(section_layout)

        ScroolAreaInput.__scrollarea_input_layout.layout().addWidget(section)

        ScroolAreaInput.__scrollarea_input_layout.layout().addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
