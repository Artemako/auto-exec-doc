import os

import package.modules.log as log
import package.modules.projectdatabase as projectdatabase
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.filefoldermanager as filefoldermanager
import package.modules.sectionsinfo as sectionsinfo

import package.components.customsection as customsection

import package.components.forms.formdate as formdate
import package.components.forms.formimage as formimage
import package.components.forms.formtable as formtable
import package.components.forms.formtext as formtext

from PySide2.QtWidgets import QLabel, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class ScroolAreaInput:
    __scrollarea_input = None
    __scrollarea_input_layout = None

    

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
    def add_sections_in_sa():
        """ """
        log.Log.debug_logger("IN add_sections_in_sa()")

        sections_info = sectionsinfo.SectionsInfo.get_sections_info()
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
        # обновить информацию о секциях
        sectionsinfo.SectionsInfo.update_sections_info(page)
        # Добавление новых секций в ScroolAreaInput
        ScroolAreaInput.add_sections_in_sa()
