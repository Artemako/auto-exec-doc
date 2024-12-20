class SectionsInfoObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_prodb = osbm.obj_prodb
        self.obj_film = osbm.obj_film

class SectionsInfo:
    def __init__(self):
        self.__sections_info = []

    def setting_osbm(self, osbm):
        self.__osbm = SectionsInfoObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo setting_osbm(): \nself.__osbm = {self.__osbm}")

    def get_sections_info(self):
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo self.__sections_info = {self.__sections_info}")
        return self.__sections_info

    def update_sections_info(self, page):
        # обновить информацию, нужная для создания секций
        self.__sections_info.clear()
        self.add_page_for_sections_info(page)
        template = self.__osbm.obj_prodb.get_parent_template(page)
        self.add_template_for_sections_info(template)
        node = self.__osbm.obj_prodb.get_parent_node_template(template)
        self.add_nodes_for_sections_info(node)
    
    def add_page_for_sections_info(self, page):
        """
        Добавление секции для страницы.
        """
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_page_for_datas(page):\npage = {page}")

        data = self.__osbm.obj_prodb.get_page_data(page)
        if data:
            section = {
                "type": "page",
                "page": page,
                "data": data,
            }
            self.__sections_info.append(section)

    def add_template_for_sections_info(self, template):
        """ """
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_template_for_datas(page):\npage = {template}")
        
        data = self.__osbm.obj_prodb.get_template_data(template)
        if data:
            section = {
                "type": "template",
                "template": template,
                "data": data,
            }
            self.__sections_info.append(section)

    def add_node_for_datas(self, node):
        """
        Добавление секции для вершины: группы или проекта.
        """
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_node_for_datas(node):\nnode = {node}")

        data = self.__osbm.obj_prodb.get_node_data(node)
        if data:
            type_node = node.get("type_node")
            if type_node == "GROUP":
                section = {
                    "type": "group",
                    "group": node,
                    "data": data,
                }
                self.__sections_info.append(section)
            elif type_node == "PROJECT":
                section = {
                    "type": "project",
                    "project": node,
                    "data": data,
                }
                self.__sections_info.append(section)

    def add_nodes_for_sections_info(self, node):
        """ 
        Проход по всем вершинам и добавление секции для них.
        """
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_nodes_for_sections_info(node):\nnode = {node}")
        parent_node = node
        flag = True
        while flag:
            self.add_node_for_datas(parent_node)
            parent_node = self.__osbm.obj_prodb.get_node_parent(parent_node)
            if not parent_node:
                flag = False


    def save_data_to_database(self):
        """
        Cохранение информации в __sections_info в БД
        """
        self.__osbm.obj_logg.debug_logger("SectionsInfo save_data_to_database()")
        sections_info = self.__sections_info
        # перебор секций
        for section_index, section_info in enumerate(sections_info):
            print(f"section_index = {section_index},\n section_info = {section_info}\n")
            # инфо из секции
            section_type = section_info.get("type")
            section_data = section_info.get("data")
            print(f"section_data = {section_data}\n")
            # перебор пар в section_data секции
            for pair_index, pair in enumerate(section_data):
                id_pair = pair.get("id_pair")
                value = pair.get("value_pair")
                old_value = self.update_data_from_pair(section_type, id_pair, value)
                id_variable = pair.get("id_variable")
                self.save_image(id_variable, old_value, value)               

    def update_data_from_pair(self, section_type, id_pair, value):
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo update_data_with_pair(section_type, pair):\nsection_type = {section_type},\nid_pair = {id_pair},\nvalue = {value}")
        old_value = None
        print(f"section_type = {section_type},\nid_pair = {id_pair},\nvalue = {value}")
        if section_type == "page":
            old_value = self.__osbm.obj_prodb.get_page_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_page_data(id_pair, value)
        elif section_type == "template":
            old_value = self.__osbm.obj_prodb.get_template_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_template_data(id_pair, value)
        elif section_type == "group":
            old_value = self.__osbm.obj_prodb.get_node_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_node_data(id_pair, value)
        elif section_type == "project":
            old_value = self.__osbm.obj_prodb.get_node_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_node_data(id_pair, value)
        # так как old_value = {'value_pair': 'img_20240816184801.png'}
        return old_value.get("value_pair")

    def save_image(self, id_variable, old_value, value):
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo save_image(id_variable, old_value, value):\nid_variable = {id_variable},\nold_value = {old_value},\nvalue = {value}")
        current_variable = self.__osbm.obj_prodb.get_variable_by_id(
            id_variable
        )
        print(f"id_variable = {id_variable}\n")
        print(f"current_variable = {current_variable}\n")
        type_variable = current_variable.get("type_variable")
        if type_variable == "IMAGE":
            self.__osbm.obj_film.delete_image_from_project(
                old_value
            )
            self.__osbm.obj_film.move_image_from_temp_to_project(
                value
            )


# obj_seci = SectionsInfo()