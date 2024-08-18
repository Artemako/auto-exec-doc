import os
import json

import package.components.widgets.customsection as customsection

import package.components.widgets.forms.formdate as formdate
import package.components.widgets.forms.formimage as formimage
import package.components.widgets.forms.formtable as formtable
import package.components.widgets.forms.formtext as formtext

from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class SAInputForms:

    def __init__(self):
        self.__scrollarea_input = None
        self.__scrollarea_input_layout = None
    
    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("SAInputForms setting_all_osbm()")

    def connect_inputforms(self, sa_if, sa_ifl):
        """
        Подключить _scrollarea_input и _scrollarea_input_tags
        """
        self.__osbm.obj_logg.debug_logger(f"SAInputForms connect_inputforms(sa_if, sa_ifl):\nsa_if = {sa_if},\nsa_ifl = {sa_ifl}")
        self.__scrollarea_input = sa_if
        self.__scrollarea_input_layout = sa_ifl

    def delete_all_widgets_in_sa(self):
        """
        Удаление всех виджетов в self
        """
        self.__osbm.obj_logg.debug_logger("SAInputForms delete_all_widgets_in_sa()")

        layout = self.__scrollarea_input_layout.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                del item

    def get_section_name(self, section_info):
        """
        Определение типа/названия секции
        """
        self.__osbm.obj_logg.debug_logger(f"SAInputForms get_section_name(section_info):\nsection_info = {section_info}") 
        section_type = section_info.get("type")
        section_name = None
        if section_type == "page":
            page = section_info.get("page")
            section_name = page.get("name_page")
        elif section_type == "template":
            template = section_info.get("template")
            section_name = template.get("name_template")
        elif section_type == "group":
            group = section_info.get("group")
            section_name = group.get("name_node")
        elif section_type == "project":
            project = section_info.get("project")
            section_name = project.get("name_node")
        return section_name

    def add_form_in_section(self, pair, section_layout):
        """
        Добавление формы в секцию в зависимости от типа контента.
        НЕ ВКЛЮЧЕН В logger!!!
        """
        id_tag = pair.get("id_tag")
        # все свойства основного контента
        current_tag = self.__osbm.obj_prodb.get_tag_by_id(
            id_tag
        )
        type_tag = current_tag.get("type_tag")
        config_tag = current_tag.get("config_tag")
        config_dict = dict()        
        if config_tag:
            config_dict = json.loads(config_tag)
        if type_tag == "TEXT":
            item = formtext.FormText(self.__osbm, pair, current_tag)
            section_layout.addWidget(item)

        elif type_tag == "DATE":
            item = formdate.FormDate(self.__osbm, pair, current_tag, config_dict)
            section_layout.addWidget(item)

        elif type_tag == "IMAGE":
            item = formimage.FormImage(self.__osbm, pair, current_tag, config_dict)
            section_layout.addWidget(item)

        elif type_tag == "TABLE":
            item = formtable.FormTable(self.__osbm, pair, current_tag, config_dict)
            section_layout.addWidget(item)


    def add_sections_in_sa(self):
        """ """
        self.__osbm.obj_logg.debug_logger("SAInputForms add_sections_in_sa()")

        sections_info = self.__osbm.obj_seci.get_sections_info()
        # перебор секций
        for section_info in sections_info:
            try:
                section_name = self.get_section_name(section_info)
                # Создание секции виджета
                section = customsection.Section(self.__osbm, section_name)
                section_layout = QVBoxLayout()
                section_layout.setSpacing(9)
                # data секции
                section_data = section_info.get("data")
                # перебор пар в section_data секции
                for pair in section_data:
                    self.add_form_in_section(pair, section_layout)
                # Добавление виджета в секцию
                section.setContentLayout(section_layout)
                self.__scrollarea_input_layout.layout().insertWidget(0, section)
            except Exception as e:
                self.__osbm.obj_logg.error_logger(f"Error in add_sections_in_sa(): {e}")
        # Добавление SpacerItem в конец
        self.__scrollarea_input_layout.layout().addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def update_scrollarea(self, page):
        """
        Обновление self
        """
        self.__osbm.obj_logg.debug_logger("SAInputForms update_scrollarea()")
        # Очистка всего и вся 
        self.delete_all_widgets_in_sa()        
        # обновить информацию о секциях
        if page is not None:
            self.__osbm.obj_seci.update_sections_info(page)
            # Добавление новых секций в self
            self.add_sections_in_sa()





# obj_saif = SAInputForms()