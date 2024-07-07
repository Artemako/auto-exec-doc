import os

import package.components.customsection as customsection

import package.components.forms.formdate as formdate
import package.components.forms.formimage as formimage
import package.components.forms.formtable as formtable
import package.components.forms.formtext as formtext

from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class ScroolAreaInput:

    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__scrollarea_input = None
        self.__scrollarea_input_layout = None
        
    def connect_inputforms(self, sa_if, sa_ifl):
        """
        Подключить _scrollarea_input и _scrollarea_input_tags
        """
        self.__obs_manager.obj_l.debug_logger("IN connect_inputforms(sa_if, sa_ifl)")
        self.__scrollarea_input = sa_if
        self.__scrollarea_input_layout = sa_ifl

    def delete_all_widgets_in_sa(self):
        """
        Удаление всех виджетов в self
        """
        self.__obs_manager.obj_l.debug_logger("IN delete_all_widgets_in_sa()")

        layout = self.__scrollarea_input_layout.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                del item


    def add_sections_in_sa(self):
        """ """
        self.__obs_manager.obj_l.debug_logger("IN add_sections_in_sa()")

        sections_info = self.__obs_manager.obj_si.get_sections_info()
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
                id_tag = pair.get("id_tag")
                # все свойства основного контента
                config_tag = self.__obs_manager.obj_pd.get_config_tag_by_id(
                    id_tag
                )
                type_tag = config_tag.get("type_tag")

                #Добавление формы в секцию в зависимости от типа контента
                if type_tag == "TEXT":
                    item = formtext.FormText(self.__obs_manager, pair, config_tag)
                    section_layout.addWidget(item)

                elif type_tag == "DATE":
                    config_date = self.__obs_manager.obj_pd.get_config_date_by_id(
                        id_tag
                    )
                    item = formdate.FormDate(self.__obs_manager, pair, config_tag, config_date)
                    section_layout.addWidget(item)

                elif type_tag == "IMAGE":
                    # TODO config_image
                    config_image = []
                    item = formimage.FormImage(self.__obs_manager, pair, config_tag, config_image)
                    section_layout.addWidget(item)

                elif type_tag == "TABLE":
                    config_table = self.__obs_manager.obj_pd.get_config_table_by_id(id_tag)
                    item = formtable.FormTable(self.__obs_manager, pair, config_tag, config_table)
                    section_layout.addWidget(item)

            section.setContentLayout(section_layout)

            self.__scrollarea_input_layout.layout().insertWidget(0, section)

        # Добавление SpacerItem в конец
        self.__scrollarea_input_layout.layout().addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def update_scrollarea(self, page):
        """
        Обновление self
        """
        self.__obs_manager.obj_l.debug_logger("IN update_scrollarea()")
        # Очистка всего и вся 
        self.delete_all_widgets_in_sa()        
        # обновить информацию о секциях
        self.__obs_manager.obj_si.update_sections_info(page)
        # Добавление новых секций в self
        self.add_sections_in_sa()





# obj_sai = ScroolAreaInput()