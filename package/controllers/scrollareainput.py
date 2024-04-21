import os

import package.modules.log as log
import package.components.customsection as customsection
import package.modules.projectdatabase as projectdatabase
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.filefoldermanager as filefoldermanager
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
        # сохранение data в json
        for sections_info in ScroolAreaInput.__sections_info:
            jsonmanager.JsonManager.save_data_to_json_file(
                sections_info.get("json_dirpath"), sections_info.get("data")
            )
        # сохранение изображений
        sections_info = ScroolAreaInput.__sections_info
        for section_index, section_info in enumerate(sections_info):
            section_data = section_info.get("data")
            for key, value in section_data.items():
                config_content = projectdatabase.Database.get_config_content_by_id(key)
                type_content = config_content.get("type_content")
                if type_content == "IMAGE":
                    # TODO ЗАМЕНЯТЬ ИЗОБРАЖЕНИЕ С ДРУГИМ РАСШИРЕНЕНИЕМ
                    filefoldermanager.FileFolderManager.move_from_temp_to_project(
                        section_info.get("json_dirpath"),
                        section_data[config_content.get("name_content")],
                    )

    @staticmethod
    def add_page_for_info_sections(page):
        """
        Добавление форм на ScroolAreaInput
        """
        log.Log.debug_logger(f"IN add_page_for_datas(page): page = {page}")

        data = projectdatabase.Database.get_page_data(page)
        if data:
            section = {
                "type": "page",
                "page": page,
                "data": data,
            }
            ScroolAreaInput.__sections_info.append(section)

    @staticmethod
    def add_node_for_datas(node):
        """ """
        log.Log.debug_logger(f"IN add_node_for_datas(node): node = {node}")

        data = projectdatabase.Database.get_node_data(node)
        if data:
            section = {
                "type": "node",
                "node": node,
                "data": data,
            }
            ScroolAreaInput.__sections_info.append(section)

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
        # перебор секций
        for section_index, section_info in enumerate(sections_info):
            print(f"section_index = {section_index},\n section_info = {section_info}\n")
            # тип секции: страница или вершина
            section_type = section_info.get("type")
            if section_type == "page":
                page = section_info.get("page")
                section_name = page.get("page_name")
            elif section_type == "node":
                node = section_info.get("node")
                section_name = node.get("name_node")

            # Создание секции виджета
            section = customsection.Section(section_name)
            section_layout = QVBoxLayout()
            # data секции
            section_data = section_info.get("data")
            print(f"section_data = {section_data}\n")
            # перебор пар в section_data секции
            for pair_index, pair in enumerate(section_data):
                print(f"pair = {pair}\n")
                id_content = pair.get("id_content")
                # все свойства основного контента
                config_content = projectdatabase.Database.get_config_content_by_id(
                    id_content
                )
                type_content = config_content.get("type_content")

                #Добавление формы в секцию в зависимости от типа контента
                if type_content == "TEXT":
                    item = formtext.FormText(pair, config_content)
                    section_layout.addWidget(item)

                elif type_content == "DATE":
                    config_date = projectdatabase.Database.get_config_date_by_id(
                        id_content
                    )
                    item = formdate.FormDate(pair, config_content, config_date)
                    section_layout.addWidget(item)

                elif type_content == "IMAGE":
                    # TODO config_image
                    config_image = []
                    item = formimage.FormImage(pair, config_content, config_image)
                    section_layout.addWidget(item)

                elif type_content == "TABLE":
                    config_table = projectdatabase.Database.get_config_table_by_id(id_content)
                    item = formtable.FormTable(pair, config_content, config_table)
                    section_layout.addWidget(item)

            section.setContentLayout(section_layout)

            ScroolAreaInput.__scrollarea_input_layout.layout().insertWidget(0, section)

        # Добавление SpacerItem в конец
        ScroolAreaInput.__scrollarea_input_layout.layout().addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    @staticmethod
    def update_scrollarea(page):
        """
        Обновление ScroolAreaInput
        """
        log.Log.debug_logger("IN update_scrollarea()")
        # Очистка всего и вся
        ScroolAreaInput.delete_all_widgets_in_sa()
        ScroolAreaInput.__sections_info.clear()
        filefoldermanager.FileFolderManager.clear_temp_folder()

        # информация нужная для создания секции
        ScroolAreaInput.add_page_for_info_sections(page)
        ScroolAreaInput.add_nodes_for_info_sections(page)

        # Добавление новых секций
        ScroolAreaInput.add_sections_in_sa()
