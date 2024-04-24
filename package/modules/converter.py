import os
import json
import copy
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert

import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.sectionsinfo as seccionsinfo
import package.modules.projectdatabase as projectdatabase

import package.controllers.pdfview as pdfview

import package.modules.log as log

class Converter:

    def __init__(self):
        pass    


    @staticmethod
    def create_and_open_page_pdf(page):
        log.Log.debug_logger(f"IN create_page_pdf(page): page = {page}")
        # ПОРЯДОК ДЕЙСТВИЙ

        # имя файла для открытия
        pdf_name = page.get("template_name") + ".pdf"
        # путь файла для открытия
        page_pdf_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_pdfs_folder_dirpath(), pdf_name
            )
        )  

        # очистить __widget_pdf_view 
        pdfview.PdfView.set_empty_pdf_view()

        if os.path.exists(page_pdf_path):
            # удалить 
            os.remove(page_pdf_path)

              
        # создать docx из данным page
        Converter.create_docx_page(page)
        # создать pdf из docx
        Converter.create_pdf_from_docx_page(page)
        # открыть pdf
        pdfview.PdfView.load_pdf_document(page_pdf_path)


    @staticmethod
    def create_docx_page(page):
        log.Log.debug_logger(f"IN create_docx_page(page): page = {page}")
        # получить docx_template
        form_page_name = page.get("template_name")
        form_page_fullname = form_page_name + ".docx"
        template_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_forms_folder_dirpath(), form_page_fullname
            )
        )
        # создать docx из данным page
        docx_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_temp_dirpath(), form_page_fullname
            )
        )
        # учитывать main или nomain шаблон
        docx_template = DocxTemplate(template_path)

        # создаем context из sections_info
        data_context = dict()
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
                    data_context[name_content] = value
                elif type_content == "IMAGE":
                    # TODO контент для изображения
                    if value:
                        image_dirpath = os.path.abspath(
                            os.path.join(
                                dirpathsmanager.DirPathManager.get_images_folder_dirpath(),
                                value
                            )
                        )
                        image = InlineImage(docx_template, image_dirpath)
                        data_context[name_content] = image
                elif type_content == "DATE":
                    data_context[name_content] = value
                elif type_content == "TABLE":
                    config_table = projectdatabase.Database.get_config_table_by_id(id_content)
                    # узнать content в таблице
                    order_to_content_config_table = dict()
                    object_content = dict()
                    for config in config_table:
                        if config.get("type_config") == "CONTENT":
                            value_config = config.get("value_config")
                            order_config = config.get("order_config")
                            order_to_content_config_table[order_config] = value_config
                            object_content[value_config] = None
                    # заполнять data_context
                    table_values = []
                    if value:
                        table = json.loads(value)                    
                        for row, row_data in enumerate(table):
                            pt = copy.deepcopy(object_content)
                            for col, cell_value in enumerate(row_data):
                                pt[order_to_content_config_table.get(col)] = (cell_value)
                            table_values.append(pt)
                    
                    data_context[name_content] = table_values
                    
    
        print(f"data_context = {data_context}")
        docx_template.render(data_context)
        print(f"docx_path = {docx_path}")
        docx_template.save(docx_path)



    @staticmethod
    def create_pdf_from_docx_page(page):
        log.Log.debug_logger(f"IN create_pdf_from_docx_page(page): page = {page}")
        # создать pdf из docx
        form_page_name = page.get("template_name")
        form_page_fullname = form_page_name + ".docx"
        docx_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_temp_dirpath(), form_page_fullname
            )
        )
        pdf_page_fullname = form_page_name + ".pdf"
        page_pdf_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_pdfs_folder_dirpath(), pdf_page_fullname
            )
        )
        convert(docx_path, page_pdf_path)
