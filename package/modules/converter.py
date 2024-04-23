import os
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.sectionsinfo as seccionsinfo
import package.modules.projectdatabase as projectdatabase

import package.modules.log as log

class Converter:

    def __init__(self):
        pass    


    @staticmethod
    def create_page_pdf(page):
        log.Log.debug_logger(f"IN create_page_pdf(page): page = {page}")
        # создать docx из данным page
        Converter.create_docx_page(page)
        # создать pdf из docx
        Converter.create_pdf_from_docx_page(page)


    @staticmethod
    def create_docx_page(page):
        log.Log.debug_logger(f"IN create_docx_page(page): page = {page}")
        # создать docx из данным page
        docx_name = page.get_name() + ".docx"
        docx_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_temp_dirpath(), docx_name
            )
        )

        # создаем context из sections_info
        context = dict()
        sections_info = seccionsinfo.SectionsInfo.get_sections_info()

        for section_index, section_info in enumerate(sections_info):
            # инфо из секции
            section_data = section_info.get("data")
            # перебор пар в section_data секции
            for pair_index, pair in enumerate(section_data):
                id_pair = pair.get("id_pair")
                id_page = pair.get("id_page")
                id_content = pair.get("id_content")
                name_content = pair.get("name_content")
                value = pair.get("value")
                # config_content
                config_content = projectdatabase.Database.get_config_content_by_id(
                    id_content
                )
                type_content = config_content.get("type_content")
                if type_content == "TEXT":
                    ...
                elif type_content == "IMAGE":
                    ...
                elif type_content == "TABLE":
                    ...
                elif type_content == "DATE":
                    ...














    @staticmethod
    def create_pdf_from_docx_page(page):
        log.Log.debug_logger(f"IN create_pdf_from_docx_page(page): page = {page}")
        # создать pdf из docx
        pass