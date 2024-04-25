import os
import json
import copy
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
from pypdf import PdfWriter
import datetime
import concurrent.futures

from PySide6.QtWidgets import QProgressDialog

from PySide6.QtCore import Qt

import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.sectionsinfo as seccionsinfo
import package.modules.projectdatabase as projectdatabase
import package.components.dialogwindows as dialogwindows

import package.controllers.statusbar as statusbar
import package.controllers.pdfview as pdfview

import package.modules.log as log


class Converter:
    def __init__(self):
        pass

    @staticmethod
    def create_and_open_page_pdf(page):
        log.Log.debug_logger(f"IN create_page_pdf(page): page = {page}")
        # создать pdf
        pdf_path = Converter.create_page_pdf(page)
        # открыть pdf
        pdfview.PdfView.load_and_show_pdf_document(pdf_path)

    @staticmethod
    def create_page_pdf(page) -> str:
        """
        Создать pdf страницы. Вернуть директорию.
        """
        form_page_name = page.get("template_name")
        docx_pdf_page_name = f"""page_{page.get("id_page")}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"""

        # создать docx из данным page
        Converter.create_docx_page(form_page_name, docx_pdf_page_name)
        # создать pdf из docx
        pdf_path = os.path.normpath(
            Converter.create_pdf_from_docx_page(docx_pdf_page_name)
        )
        return pdf_path

    @staticmethod
    def create_docx_page(form_page_name, docx_pdf_page_name):
        log.Log.debug_logger(
            f"IN create_docx_page(page): form_page_name = {form_page_name}, docx_pdf_page_name = {docx_pdf_page_name}"
        )
        # получить docx_template
        form_page_fullname = form_page_name + ".docx"
        docx_page_fullname = docx_pdf_page_name + ".docx"
        # путь к шаблону в папке forms проекта
        template_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    dirpathsmanager.DirPathManager.get_forms_folder_dirpath(),
                    form_page_fullname,
                )
            )
        )
        # путь к будущему docx файлу
        docx_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    dirpathsmanager.DirPathManager.get_temp_dirpath(),
                    docx_page_fullname,
                )
            )
        )
        try:
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
                        print(f"config_table = {config_table}")
                        # узнать content в таблице
                        order_to_content_config_table = dict()
                        object_content = dict()
                        for config in config_table:
                            if config.get("type_config") == "CONTENT":
                                value_config = config.get("value_config")
                                order_config = config.get("order_config")
                                order_to_content_config_table[order_config] = value_config
                                object_content[value_config] = None
                        print(f"object_content = {object_content}")
                        # заполнять data_context
                        table_values = []
                        if value:
                            table = json.loads(value)
                            for row, row_data in enumerate(table):
                                pt = copy.deepcopy(object_content)
                                for col, cell_value in enumerate(row_data):
                                    pt[order_to_content_config_table.get(col)] = cell_value
                                table_values.append(pt)
                        print(f"table_values = {table_values}")
                        data_context[name_content] = table_values

            print(f"data_context = {data_context}")
            docx_template.render(data_context)
            print(f"docx_path = {docx_path}")
            docx_template.save(docx_path)

        except Exception as e:
            log.Log.error_logger(e)

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

    @staticmethod
    def export_to_pdf(multipage_pdf_path) -> None:
        log.Log.debug_logger(
            f"IN export_to_pdf(multipage_pdf_path): multipage_pdf_path = {multipage_pdf_path}"
        )

        # проход по всем вершинам дерева для заполенения project_pages_objects
        project_pages_objects = list()
        number_page = 0
        Converter.dfs(
            projectdatabase.Database.get_project_node(),
            project_pages_objects,
            number_page,
        )
        log.Log.debug_logger(f"project_pages_objects = {project_pages_objects}")
        # проход по project_pages_objects для преобразования каждой страницы в pdf
        list_of_pdf_pages = Converter.get_list_of_created_pdf_pages(
            project_pages_objects
        )
        print(f"list_of_pdf_pages = {list_of_pdf_pages}")
        # объеденить несколько pdf файлов в один
        Converter.merge_pdfs_and_create(multipage_pdf_path, list_of_pdf_pages)
        # закрыть диалоговое окно
        statusbar.StatusBar.set_message_for_statusbar(f"Экспорт завершен. Файл {multipage_pdf_path} готов.")
        # открыть pdf
        os.startfile(os.path.dirname(multipage_pdf_path))
        statusbar.StatusBar.set_message_for_statusbar("Преобразование завершено.")
        

    @staticmethod
    def dfs(parent_node, project_pages_objects, number_page):
        log.Log.debug_logger(
            f"IN dfs(node, project_pages_objects): parent_node = {parent_node}, number_page = {number_page}"
        )
        childs = projectdatabase.Database.get_childs(parent_node)
        if childs:
            for child in childs:
                # TODO подумать про PDF node, загруженный пользователем
                # проход по страницам node
                pages = projectdatabase.Database.get_pages_by_node(child)
                for page in pages:
                    # TODO Included
                    object = {"type": "page", "page": page, "number_page": number_page}
                    project_pages_objects.append(object)
                    number_page += 1
                # проход по дочерним вершинам
                Converter.dfs(child, project_pages_objects, number_page)

    @staticmethod
    def get_list_of_created_pdf_pages(project_pages_objects) -> list:
        list_of_pdf_pages = list()
        # создание пула потоков с автоматическим количеством потоков
        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            # создание списка задач, которые будут выполнены параллельно
            tasks = [
                executor.submit(
                    Converter.process_object_of_project_pages_objects,
                    object,
                    list_of_pdf_pages,
                )
                for object in project_pages_objects
            ]
            # ожидание завершения всех задач
            concurrent.futures.wait(tasks)
        return list_of_pdf_pages

    @staticmethod
    def process_object_of_project_pages_objects(object, list_of_pdf_pages):
        log.Log.debug_logger(
            f"IN process_object_of_project_pages_objects(object): object = {object}"
        )
        object_type = object.get("type")
        number_page = object.get("number_page")
        if object_type == "page":
            pdf_path = Converter.create_page_pdf(object.get("page"))
            list_of_pdf_pages.append({"number_page": number_page, "pdf_path": pdf_path})


    @staticmethod
    def merge_pdfs_and_create(multipage_pdf_path, list_of_pdf_pages):
        log.Log.debug_logger(
            f"IN merge_pdfs(multipage_pdf_path, list_of_pdf_pages): multipage_pdf_path = {multipage_pdf_path}, list_of_pdf_pages = {list_of_pdf_pages}"
        )
        # объединить несколько pdf файлов в один
        merger = PdfWriter()
        for pdf in sorted(list_of_pdf_pages, key=lambda x: x["number_page"]):
            merger.append(pdf.get("pdf_path"))

        merger.write(multipage_pdf_path)
        merger.close()