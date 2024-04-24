import package.modules.log as log
import package.modules.projectdatabase as projectdatabase

import package.modules.filefoldermanager as filefoldermanager
import package.controllers.pagestemplate as pagestemplate


class SectionsInfo:
    __sections_info = []

    @staticmethod
    def get_sections_info():
        return SectionsInfo.__sections_info
    
    @staticmethod
    def clear_sections_info():
        SectionsInfo.__sections_info.clear()

    @staticmethod
    def update_sections_info(page):
        # обновить информацию, нужная для создания секций
        SectionsInfo.clear_sections_info()
        SectionsInfo.add_page_for_sections_info(page)
        SectionsInfo.add_nodes_for_sections_info(page)


    @staticmethod
    def add_page_for_sections_info(page):
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
            SectionsInfo.__sections_info.append(section)

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
            SectionsInfo.__sections_info.append(section)

    @staticmethod
    def add_nodes_for_sections_info(page):
        """ """
        log.Log.debug_logger("IN add_nodes_for_datas()")

        parent_node = projectdatabase.Database.get_node_parent_from_pages(page)
        flag = True
        while flag:
            SectionsInfo.add_node_for_datas(parent_node)
            parent_node = projectdatabase.Database.get_node_parent(parent_node)
            if not parent_node:
                flag = False
    
    @staticmethod
    def save_data_to_database():
        """
        Cохранение информации в __sections_info в БД
        """
        log.Log.debug_logger("IN save_data_to_database()")
        sections_info = SectionsInfo.__sections_info
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
                    old_value = projectdatabase.Database.get_page_pair_value_by_id(id_pair)                    
                    projectdatabase.Database.update_pages_data(id_pair, value)
                elif section_type == "node":
                    old_value = projectdatabase.Database.get_node_pair_value_by_id(id_pair)   
                    projectdatabase.Database.update_nodes_data(id_pair, value)
                # Сохранения изображения
                id_content = pair.get("id_content")
                config_content = projectdatabase.Database.get_config_content_by_id(
                    id_content
                )
                print(f"id_content = {id_content}\n")
                print(f"config_content = {config_content}\n")
                type_content = config_content.get("type_content")
                if type_content == "IMAGE":
                    filefoldermanager.FileFolderManager.delete_image_from_project(old_value)
                    filefoldermanager.FileFolderManager.move_image_from_temp_to_project(value)

        pagestemplate.PagesTemplate.current_page_to_pdf()   
        