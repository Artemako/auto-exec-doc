import os
import json

import package.components.widgets.customsection as customsection

import package.components.widgets.forms.formdate as formdate
import package.components.widgets.forms.formimage as formimage
import package.components.widgets.forms.formtable as formtable
import package.components.widgets.forms.formtext as formtext
import package.components.widgets.forms.formlongtext as formlongtext
import package.components.widgets.forms.formlist as formlist

from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QMenu
from PySide6.QtGui import QAction, Qt

class TabWInputForms:    
    def __init__(self):
        self.__tab_widget = None
    
    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("TabWInputForms setting_all_osbm()")

    def connect_inputforms(self, tab_widget):
        """
        Подключить tab_widget для управления вкладками
        """
        self.__osbm.obj_logg.debug_logger("TabWInputForms connect_inputforms(tab_widget)")
        self.__tab_widget = tab_widget
        self.__icons = self.__osbm.obj_icons.get_icons()        #

    def delete_all_tabs(self):  
        """
        Удаление всех вкладок в tabw_inputforms
        """
        self.__osbm.obj_logg.debug_logger("TabWInputForms delete_all_tabs()")
        self.__tab_widget.clear()

    def get_section_name(self, section_info) -> str:
        """
        Определение типа/названия секции
        """
        self.__osbm.obj_logg.debug_logger(f"TabWInputForms get_section_name(section_info):\nsection_info = {section_info}") 
        section_type = section_info.get("type")
        section_name = None
        if section_type == "page":
            page = section_info.get("page")
            section_name = f'Страница: {page.get("name_page")}'
        elif section_type == "template":
            template = section_info.get("template")
            section_name = f'Шаблон: {template.get("name_template")}'
        elif section_type == "group":
            group = section_info.get("group")
            section_name = f'Группа: {group.get("name_node")}'
        elif section_type == "project":
            project = section_info.get("project")
            section_name = project.get("name_node")
        return section_name
    

    def add_form_in_tab(self, tab_layout, pair, type_section):
        """
        Добавление формы во вкладку в зависимости от типа контента.
        НЕ ВКЛЮЧЕН В logger!!!
        """
        id_variable = pair.get("id_variable")
        current_variable = self.__osbm.obj_prodb.get_variable_by_id(id_variable)
        type_variable = current_variable.get("type_variable")
        config_variable = current_variable.get("config_variable")
        config_dict = dict()        
        if config_variable:
            config_dict = json.loads(config_variable)

        item = None
        if type_variable == "TEXT":
            item = formtext.FormText(self.__osbm, pair, current_variable)
        elif type_variable == "LONGTEXT":
            item = formlongtext.FormLongTextWidget(self.__osbm, pair, current_variable)
        elif type_variable == "DATE":
            item = formdate.FormDate(self.__osbm, pair, current_variable, config_dict)
        elif type_variable == "IMAGE":
            item = formimage.FormImage(self.__osbm, pair, current_variable, config_dict)
        elif type_variable == "TABLE":
            item = formtable.FormTable(self.__osbm, pair, current_variable, config_dict)
        elif type_variable == "LIST":
            item = formlist.FormList(self.__osbm, pair, current_variable)

        if item:
            # setSizePolicy тут нужон 
            item.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            #
            item.setContextMenuPolicy(Qt.CustomContextMenu)
            item.customContextMenuRequested.connect(
                lambda pos: self.context_menu(pos, item, current_variable, type_section)
            )
            tab_layout.addWidget(item)

    def context_menu(self, pos, item, current_variable, type_section, *args):
        """
        Меню по правой кнопки мыши (ui.treewidget_structure_execdoc)
        """
        menu = QMenu(item)
        # action_edit_variables для всех
        action_edit_variables = QAction(
            "Изменить в редакторе переменных", item
        )
        action_edit_variables.setIcon(self.__icons.get("edit_variables"))
        action_edit_variables.triggered.connect(
            lambda: self.__osbm.obj_mw.edit_menu_item("VARIABLE", "EDIT", current_variable, type_section)
        )
        menu.addAction(action_edit_variables)
        #
        menu.exec(item.mapToGlobal(pos))


    def add_sections_in_tabs(self):
        self.__osbm.obj_logg.debug_logger("TabWInputForms add_sections_in_tabs()")
        
        sections_info = self.__osbm.obj_seci.get_sections_info()
        self.__sections = []

        for section_info in sections_info:
            try:
                section_name = self.get_section_name(section_info)

                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

                tab_content = QWidget()
                tab_layout = QVBoxLayout(tab_content)
                tab_layout.setSpacing(9)

                # Добавление форм в вкладку
                data_section = section_info.get("data")
                type_section = section_info.get("type")
                for pair in data_section:
                    self.add_form_in_tab(tab_layout, pair, type_section)

                tab_layout.addItem(
                    QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
                )
                scroll_area.setWidget(tab_content)
                self.__tab_widget.addTab(scroll_area, section_name)
            except Exception as e:
                self.__osbm.obj_logg.error_logger(f"Error in add_sections_in_tabs(): {e}")

    def update_tabs(self, page):
        self.__osbm.obj_logg.debug_logger("TabWInputForms update_tabs()")
        self.delete_all_tabs()        
        if page is not None:
            self.__osbm.obj_seci.update_sections_info(page)
            self.add_sections_in_tabs()
