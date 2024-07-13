import package.controllers.pagestemplate as pagestemplate

class SectionsInfo:
    # TODO Сделать отдел для группы и для формы (страница есть)
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager 
        self.__sections_info = []

    def get_sections_info(self):
        print(f"self.__sections_info = {self.__sections_info}")
        return self.__sections_info

    def update_sections_info(self, page):
        # обновить информацию, нужная для создания секций
        self.__sections_info.clear()
        # TODO Тут явно переделать/добавить механику добавления информации для группы и для формы
        self.add_page_for_sections_info(page)
        template = self.__obs_manager.obj_pd.get_parent_template(page)
        self.add_template_for_sections_info(template)
        node = self.__obs_manager.obj_pd.get_parent_node(template)
        self.add_nodes_for_sections_info(node)
    
    def add_page_for_sections_info(self, page):
        """
        Добавление секции для страницы.
        """
        self.__obs_manager.obj_l.debug_logger(f"IN add_page_for_datas(page):\npage = {page}")

        data = self.__obs_manager.obj_pd.get_page_data(page)
        if data:
            section = {
                "type": "page",
                "page": page,
                "data": data,
            }
            self.__sections_info.append(section)

    def add_template_for_sections_info(self, template):
        """ """
        self.__obs_manager.obj_l.debug_logger(f"IN add_template_for_datas(page):\npage = {template}")
        # TODO 
        data = self.__obs_manager.obj_pd.get_template_data(template)
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
        self.__obs_manager.obj_l.debug_logger(f"IN add_node_for_datas(node):\nnode = {node}")

        data = self.__obs_manager.obj_pd.get_node_data(node)
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
        self.__obs_manager.obj_l.debug_logger(f"IN add_nodes_for_sections_info(node):\nnode = {node}")
        parent_node = node
        flag = True
        while flag:
            self.add_node_for_datas(parent_node)
            parent_node = self.__obs_manager.obj_pd.get_node_parent(parent_node)
            if not parent_node:
                flag = False


    def save_data_to_database(self):
        """
        Cохранение информации в __sections_info в БД
        """
        self.__obs_manager.obj_l.debug_logger("IN save_data_to_database()")
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
                value = pair.get("value")
                old_value = self.update_data_from_pair(section_type, id_pair, value)
                id_tag = pair.get("id_tag")
                self.save_image(id_tag, old_value, value)               

    def update_data_from_pair(self, section_type, id_pair, value):
        self.__obs_manager.obj_l.debug_logger(f"IN update_data_with_pair(section_type, pair):\nsection_type = {section_type},\nid_pair = {id_pair},\nvalue = {value}")
        old_value = None
        if section_type == "page":
            old_value = self.__obs_manager.obj_pd.get_page_pair_value_by_id(
                id_pair
            )
            self.__obs_manager.obj_pd.update_pages_data(id_pair, value)
        elif section_type == "node":
            old_value = self.__obs_manager.obj_pd.get_node_pair_value_by_id(
                id_pair
            )
            self.__obs_manager.obj_pd.update_nodes_data(id_pair, value)
        return old_value

    def save_image(self, id_tag, old_value, value):
        self.__obs_manager.obj_l.debug_logger(f"IN save_image(id_tag, old_value, value):\nid_tag = {id_tag},\nold_value = {old_value},\nvalue = {value}")
        config_tag = self.__obs_manager.obj_pd.get_config_tag_by_id(
            id_tag
        )
        print(f"id_tag = {id_tag}\n")
        print(f"config_tag = {config_tag}\n")
        type_tag = config_tag.get("type_tag")
        if type_tag == "IMAGE":
            self.__obs_manager.obj_ffm.delete_image_from_project(
                old_value
            )
            self.__obs_manager.obj_ffm.move_image_from_temp_to_project(
                value
            )


# obj_si = SectionsInfo()