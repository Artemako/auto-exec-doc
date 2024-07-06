import package.controllers.pagestemplate as pagestemplate

class SectionsInfo:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager 
        self.__sections_info = []

    def get_sections_info(self):
        return self.__sections_info

    def update_sections_info(self, page):
        # обновить информацию, нужная для создания секций
        self.__sections_info.clear()
        self.add_page_for_sections_info(page)
        self.add_nodes_for_sections_info(page)

    def add_page_for_sections_info(self, page):
        """
        Добавление секции для страницы.
        """
        self.__obs_manager.obj_l.debug_logger(f"IN add_page_for_datas(page): page = {page}")

        data = self.__obs_manager.obj_pd.get_page_data(page)
        if data:
            section = {
                "type": "page",
                "page": page,
                "data": data,
            }
            self.__sections_info.append(section)

    def add_node_for_datas(self, node):
        """ """
        self.__obs_manager.obj_l.debug_logger(f"IN add_node_for_datas(node): node = {node}")

        data = self.__obs_manager.obj_pd.get_node_data(node)
        if data:
            section = {
                "type": "node",
                "node": node,
                "data": data,
            }
            self.__sections_info.append(section)

    def add_nodes_for_sections_info(self, page):
        """ """
        self.__obs_manager.obj_l.debug_logger("IN add_nodes_for_datas()")

        parent_node = self.__obs_manager.obj_pd.get_node_parent_from_pages(page)
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
                print(f"pair = {pair}\n")
                id_pair = pair.get("id_pair")
                value = pair.get("value")
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
                # Сохранения изображения
                id_tag = pair.get("id_tag")
                config_content = self.__obs_manager.obj_pd.get_config_content_by_id(
                    id_tag
                )
                print(f"id_tag = {id_tag}\n")
                print(f"config_content = {config_content}\n")
                type_tag = config_content.get("type_tag")
                if type_tag == "IMAGE":
                    self.__obs_manager.obj_ffm.delete_image_from_project(
                        old_value
                    )
                    self.__obs_manager.obj_ffm.move_image_from_temp_to_project(
                        value
                    )


# obj_si = SectionsInfo()