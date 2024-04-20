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

    __sections_info = []

    def __init__(self):
        pass

        return ScroolAreaInput.__scrollarea_input_layout

    @staticmethod
    def get_sections_info() -> object:
        # TODO
        log.Log.debug_logger("get_data() -> object")
        return ScroolAreaInput.__sections_info

    @staticmethod
    def connect_inputforms(sa_if, sa_ifl):
        """
        Подключить _scrollarea_input и _scrollarea_input_contents
        """
        log.Log.debug_logger("IN connect_inputforms(sa_if, sa_ifl)")
        ScroolAreaInput.__scrollarea_input = sa_if
        ScroolAreaInput.__scrollarea_input_layout = sa_ifl

    @staticmethod
    def delete_all_widgets_in_sa():
        """
        Удаление всех виджетов в ScroolAreaInput
        """
        log.Log.debug_logger("IN delete_all_widgets_in_sa()")

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
    def add_page_for_info_sections(page):
        """
        Добавление форм на ScroolAreaInput
        """
        log.Log.debug_logger("IN add_page_for_datas(page)")

        parent_node = projectdatabase.Database.get_node_parent_from_pages(page)

        id_page = page.get("id_page")
        name_page = page.get("name_page")
        folder_form = parent_node.get("folder_form")
        folder_page = page.get("folder_page")
        name_json = folder_page
        json_dirpath = os.path.normpath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_project_dirpath(),
                "forms",
                folder_form,
                folder_page,
                f"{name_json}.json",
            )
        )

        try:
            data = jsonmanager.JsonManager.get_data_from_json_file(json_dirpath)
            section = {
                "type": "page",
                "id_page": id_page,
                "name_page": name_page,
                "json_dirpath": json_dirpath,
                "data": data,
            }
            ScroolAreaInput.__sections_info.append(section)
        except FileNotFoundError:
                log.Log.error_logger(f"FileNotFoundError: json_dirpath = {json_dirpath}")

    @staticmethod
    def add_node_for_datas(node):
        id_node = node.get("id_node")
        name_node = node.get("name_node")
        folder_node = node.get("folder_form")
        folder_node = "" if not folder_node else folder_node
        name_json = node.get("name_json")
        if name_json:
            json_dirpath = os.path.normpath(
                os.path.join(
                    dirpathsmanager.DirPathManager.get_project_dirpath(),
                    "forms",
                    folder_node,
                    f"{name_json}.json",
                )
            )
            try:
                data = jsonmanager.JsonManager.get_data_from_json_file(json_dirpath)
                section = {
                    "type": "node",
                    "id_node": id_node,
                    "name_node": name_node,
                    "json_dirpath": json_dirpath,
                    "data": data,
                }
                ScroolAreaInput.__sections_info.append(section)
            except FileNotFoundError:
                log.Log.error_logger(f"FileNotFoundError: json_dirpath = {json_dirpath}")

    @staticmethod
    def add_nodes_for_info_sections(page):
        """ """
        log.Log.debug_logger("IN add_nodes_for_datas()")

        parent_node = projectdatabase.Database.get_node_parent_from_pages(page)
        flag = True
        while flag:
            ScroolAreaInput.add_node_for_datas(parent_node)
            parent_node = projectdatabase.Database.get_node_parent(parent_node)
            if not parent_node:
                flag = False

    @staticmethod
    def add_sections_in_sa():
        """ """
        log.Log.debug_logger("IN add_sections_in_sa()")

        sections_info = ScroolAreaInput.__sections_info
        for section_index, section_info in enumerate(sections_info):
            # перебор секций
            section_type = section_info.get("type")
            if section_type == "page":
                section_name = section_info.get("name_page")
            elif section_type == "node":
                section_name = section_info.get("name_node")
            section_data = section_info.get("data")

            section = customsection.Section(section_name)
            section_layout = QVBoxLayout()
            print(f"section_data = {section_data}")
            for key, value in section_data.items():
                # перебор ключа и значения в config_content секции
                config_content = projectdatabase.Database.get_config_content(key)
                type_content = config_content.get("type_content")
                id_content = config_content.get("id_content")
                print(config_content, type_content, id_content)
                if type_content == "TEXT":
                    item = formtext.FormText(section_index, config_content, value)
                    section_layout.addWidget(item)

                elif type_content == "DATE":
                    config_date = projectdatabase.Database.get_config_date(id_content)
                    item = formdate.FormDate(
                        section_index, config_content, config_date, value
                    )
                    section_layout.addWidget(item)

                elif type_content == "IMAGE":
                    config_image = []
                    item = formimage.FormImage(section_index, config_content, config_image, value)
                    section_layout.addWidget(item)

                # elif type_content == "TABLE":
                #     item = formtable.FormTable(section_index, config_content, value)

            section.setContentLayout(section_layout)

            ScroolAreaInput.__scrollarea_input_layout.layout().insertWidget(0, section)

        ScroolAreaInput.__scrollarea_input_layout.layout().addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    @staticmethod
    def update_scrollarea(page):
        """
        Обновление ScroolAreaInput
        """
        log.Log.debug_logger("IN update_scrollarea()")

        ScroolAreaInput.delete_all_widgets_in_sa()
        ScroolAreaInput.__sections_info.clear()

        ScroolAreaInput.add_page_for_info_sections(page)
        ScroolAreaInput.add_nodes_for_info_sections(page)

        ScroolAreaInput.add_sections_in_sa()
