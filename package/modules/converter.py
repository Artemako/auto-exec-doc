import os
import json
import copy
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
import datetime

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

        form_page_name = page.get("template_name")
        docx_pdf_page_name = f"page_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        # создать docx из данным page
        Converter.create_docx_page(form_page_name, docx_pdf_page_name)
        # создать pdf из docx
        pdf_path = Converter.create_pdf_from_docx_page(docx_pdf_page_name)
        # открыть pdf
        pdfview.PdfView.load_pdf_document(pdf_path)

    @staticmethod
    def create_docx_page(form_page_name, docx_pdf_page_name):
        log.Log.debug_logger(
            f"IN create_docx_page(page): form_page_name = {form_page_name}, docx_pdf_page_name = {docx_pdf_page_name}"
        )
        # получить docx_template
        form_page_fullname = form_page_name + ".docx"
        docx_page_fullname = docx_pdf_page_name + ".docx"
        # путь к шаблону в папке forms проекта
        template_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_forms_folder_dirpath(),
                form_page_fullname,
            )
        )
        # путь к будущему docx файлу
        docx_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_temp_dirpath(), docx_page_fullname
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
                                value,
                            )
                        )
                        image = InlineImage(docx_template, image_dirpath)
                        data_context[name_content] = image
                elif type_content == "DATE":
                    data_context[name_content] = value
                elif type_content == "TABLE":
                    config_table = projectdatabase.Database.get_config_table_by_id(
                        id_content
                    )
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
                                pt[order_to_content_config_table.get(col)] = cell_value
                            table_values.append(pt)

                    data_context[name_content] = table_values

        print(f"data_context = {data_context}")
        docx_template.render(data_context)
        print(f"docx_path = {docx_path}")
        docx_template.save(docx_path)

    @staticmethod
    def create_pdf_from_docx_page(docx_pdf_page_name) -> str:
        log.Log.debug_logger(
            f"IN create_pdf_from_docx_page(docx_pdf_page_name) -> str: docx_pdf_page_name = {docx_pdf_page_name}"
        )
        # пути к docx и к pdf
        docx_page_fullname = docx_pdf_page_name + ".docx"
        pdf_page_fullname = docx_pdf_page_name + ".pdf"
        docx_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_temp_dirpath(), docx_page_fullname
            )
        )
        # путь к pdf в temp проекта
        pdf_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_temp_dirpath(), pdf_page_fullname
            )
        )
        # преобразовать docx в pdf
        convert(docx_path, pdf_path)

        return pdf_path
