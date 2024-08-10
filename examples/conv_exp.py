from PySide6.QtCore import QThread, Signal

import package.modules.sectionsinfo as sectionsinfo

import os
import json
import time
import copy
from docxtpl import DocxTemplate, InlineImage


import threading
from concurrent.futures import ThreadPoolExecutor

from mpire import WorkerPool

# from docx2pdf import convert
import comtypes.client
import pythoncom
import subprocess


from pypdf import PdfWriter
import datetime


class ElementPool:
    def __init__(self, value):
        self.value = value

    def empty_function():
        pass

    def get_value(self):
        return self.value


class MsWordThread(QThread):
    # cигнал для обновления статуса (object - любые объекты, включая None)
    status_changed = Signal(object)

    def __init__(self, obs_manager):
        super().__init__()
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("MsWordThread __init__()")
        self.__status_msword = False

    def run(self):
        self.initialize_msword()

    def initialize_msword(self):
        self.__obs_manager.obj_l.debug_logger("MsWordThread initialize_msword()")
        try:
            pythoncom.CoInitialize()
            self.__status_msword = None
            self.status_changed.emit(self.__status_msword)
            word = comtypes.client.CreateObject("Word.Application")
            self.__status_msword = True
        except Exception as e:
            print(f"Error in initialize_msword(): {e}")
            self.__status_msword = False
        self.status_changed.emit(self.__status_msword)


class Converter:
    # TODO Доделать конвертер + статусбар
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("Converter __init__()")
        self.__status_msword = False
        self.__status_libreoffice = False
        self.__app_converter = None
        # экземпляр QThread
        self.__msword_thread = MsWordThread(self.__obs_manager)

    def setting_converter(self):
        self.__obs_manager.obj_l.debug_logger("Converter setting_converter()")
        self.run_libreoffice()
        # подключение сигнала к слоту и запуск потока
        self.__msword_thread.status_changed.connect(self.update_status_msword)
        self.__msword_thread.start()

    def update_status_msword(self, status):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter update_status_msword(status):\nstatus = {status}"
        )
        self.__status_msword = status
        if self.__obs_manager.obj_sb.get_is_active():
            self.__obs_manager.obj_sb.update_status_msword_label(self.__status_msword)

    def get_status_msword(self):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter get_status_msword():\nself.__status_msword = {self.__status_msword}"
        )
        return self.__status_msword

    def get_status_libreoffice(self):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter get_status_libreoffice():\nself.__status_libreoffice = {self.__status_libreoffice}"
        )
        return self.__status_libreoffice

    def run_libreoffice(self):
        self.__obs_manager.obj_l.debug_logger("Converter run_libreoffice()")
        self.__libreoffice_path = "C:\Program Files\LibreOffice\program\soffice.exe"
        if os.path.exists(self.__libreoffice_path):
            self.__status_libreoffice = True
        else:
            self.__status_libreoffice = False
        if self.__obs_manager.obj_sb.get_is_active():
            self.__obs_manager.obj_sb.update_status_libreoffice_label(
                self.__status_libreoffice
            )

    def create_and_view_page_pdf(self, page):
        """
        Вызывается при нажатии на кнопку Save.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"Converter create_one_page_pdf(page):\npage = {page}"
        )
        self.__app_converter = self.__obs_manager.obj_sd.get_app_converter()
        if self.__app_converter == "MSWORD" and self.__status_msword:
            pass
        elif self.__app_converter == "LIBREOFFICE" and self.__status_libreoffice:
            pass
        else:
            self.__obs_manager.obj_dw.warning_message(
                "Отображение недоступно! Выбранный конвертер не работает."
            )
        # создать pdf
        pdf_path = self.create_page_pdf(page)
        # открыть pdf
        self.__obs_manager.obj_pv.load_and_show_pdf_document(pdf_path)

    def create_page_pdf(self, page, is_local: bool = False) -> str:
        """
        Создать pdf страницы. Вернуть директорию.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"Converter create_one_page_pdf(page):\npage = {page}"
        )
        # было page.get("filename_page") вместо page.get("id_page")
        form_page_name = page.get("id_page")
        docx_pdf_page_name = f"""page_{page.get("id_page")}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"""
        # добыть информация для SectionInfo
        if not is_local:
            sections_info = self.__obs_manager.obj_si.get_sections_info()
        else:
            object = sectionsinfo.SectionsInfo(self.__obs_manager)
            object.update_sections_info(page)
            sections_info = object.get_sections_info()
            print(f"sections_info = {sections_info}")

        # создать docx из данным page
        self.create_docx_page(sections_info, form_page_name, docx_pdf_page_name)
        # создать pdf из docx
        pdf_path = os.path.normpath(self.create_pdf_from_docx_page(docx_pdf_page_name))
        return pdf_path

    def get_form_page_fullname_and_docx_page_fullname(
        self, form_page_name, docx_pdf_page_name
    ):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter get_form_page_fullname_and_docx_page_fullname(form_page_name, docx_pdf_page_name):\nform_page_name = {form_page_name},\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # получить docx_template
        form_page_fullname = str(form_page_name) + ".docx"
        docx_page_fullname = docx_pdf_page_name + ".docx"
        return form_page_fullname, docx_page_fullname

    def get_template_path_and_docx_path(self, form_page_fullname, docx_page_fullname):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter get_template_path_and_docx_path(form_page_fullname, docx_page_fullname):\nform_page_fullname = {form_page_fullname},\ndocx_page_fullname = {docx_page_fullname}"
        )
        # путь к шаблону в папке forms проекта
        template_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    self.__obs_manager.obj_dpm.get_forms_folder_dirpath(),
                    form_page_fullname,
                )
            )
        )
        # путь к будущему docx файлу
        docx_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    self.__obs_manager.obj_dpm.get_temp_dirpath(),
                    docx_page_fullname,
                )
            )
        )
        return template_path, docx_path

    def type_tag_is_text(self, data_tag, name_tag, value):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_text(data_tag, name_tag, value):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value}"
        )
        if value:
            data_tag[str(name_tag)] = value

    def type_tag_is_date(self, data_tag, name_tag, value):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_date(data_tag, name_tag, value):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value}"
        )
        if value:
            data_tag[str(name_tag)] = value

    def type_tag_is_image(self, data_tag, name_tag, value, docx_template):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_image(data_tag, name_tag, value, docx_template):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value},\ndocx_template = {docx_template}"
        )
        if value:
            image_dirpath = os.path.abspath(
                os.path.join(
                    self.__obs_manager.obj_dpm.get_images_folder_dirpath(),
                    value,
                )
            )
            # TODO контент для изображения
            image = InlineImage(docx_template, image_dirpath)
            data_tag[str(name_tag)] = image

    def type_tag_is_table(self, data_tag, name_tag, value, id_tag):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_table(data_tag, name_tag, value, id_tag):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value},\nid_tag = {id_tag}"
        )
        config_table = self.__obs_manager.obj_pd.get_config_table_by_id(id_tag)
        print(f"config_table = {config_table}")
        # узнать content в таблице
        order_to_tag_config_table = dict()
        object_tag = dict()
        for config in config_table:
            if config.get("type_config") == "ROWCOL":
                value_config = config.get("value_config")
                order_config = config.get("order_config")
                order_to_tag_config_table[order_config] = value_config
                object_tag[value_config] = None
        print(f"object_tag = {object_tag}")
        # заполнять data_tag
        table_values = []
        if value:
            table = json.loads(value)
            for row, row_data in enumerate(table):
                pt = copy.deepcopy(object_tag)
                for col, cell_value in enumerate(row_data):
                    pt[order_to_tag_config_table.get(col)] = cell_value
                table_values.append(pt)
        print(f"table_values = {table_values}")
        data_tag[str(name_tag)] = table_values

    def check_type_tag_and_fill_data_tag(self, pair, data_tag, docx_template):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter check_type_tag_and_fill_data_tag(pair, data_tag, docx_template):\npair = {pair},\ndata_tag = {data_tag},\ndocx_template = {docx_template}"
        )
        id_pair = pair.get("id_pair")
        id_page = pair.get("id_page")
        id_tag = pair.get("id_tag")
        name_tag = pair.get("name_tag")
        value = pair.get("value")
        # config_tag
        config_tag = self.__obs_manager.obj_pd.get_config_tag_by_id(id_tag)
        type_tag = config_tag.get("type_tag")
        if type_tag == "TEXT":
            self.type_tag_is_text(data_tag, name_tag, value)
        elif type_tag == "IMAGE":
            self.type_tag_is_image(data_tag, name_tag, value, docx_template)
        elif type_tag == "DATE":
            self.type_tag_is_date(data_tag, name_tag, value)
        elif type_tag == "TABLE":
            self.type_tag_is_table(data_tag, name_tag, value, id_tag)

    def create_docx_page(self, sections_info, form_page_name, docx_pdf_page_name):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter create_docx_page(sections_info, form_page_name, docx_pdf_page_name):\nsections_info = {sections_info},\nform_page_name = {form_page_name},\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        form_page_fullname, docx_page_fullname = (
            self.get_form_page_fullname_and_docx_page_fullname(
                form_page_name, docx_pdf_page_name
            )
        )
        template_path, docx_path = self.get_template_path_and_docx_path(
            form_page_fullname, docx_page_fullname
        )
        docx_template = DocxTemplate(template_path)
        # создаем tag из sections_info
        data_tag = dict()
        for section_info in sections_info:
            # инфо из секции
            section_data = section_info.get("data")
            # перебор пар в section_data секции
            for pair in section_data:
                self.check_type_tag_and_fill_data_tag(pair, data_tag, docx_template)

        print(f"data_tag = {data_tag}")
        docx_template.render(data_tag)
        print(f"docx_path = {docx_path}")
        docx_template.save(docx_path)

    def create_pdf_from_docx_page(self, docx_pdf_page_name) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"Converter create_pdf_from_docx_page(docx_pdf_page_name) -> str:\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # пути к docx и к pdf
        docx_page_fullname = docx_pdf_page_name + ".docx"
        pdf_page_fullname = docx_pdf_page_name + ".pdf"
        docx_path = os.path.abspath(
            os.path.join(
                self.__obs_manager.obj_dpm.get_temp_dirpath(), docx_page_fullname
            )
        )
        # путь к pdf в temp проекта
        pdf_path = os.path.abspath(
            os.path.join(
                self.__obs_manager.obj_dpm.get_temp_dirpath(), pdf_page_fullname
            )
        )
        # преобразовать docx в pdf
        # convert(docx_path, pdf_path)
        self.convert_from_pdf_docx(docx_path, pdf_path)
        return pdf_path

    def convert_from_pdf_docx(self, docx_path, pdf_path):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter convert_from_pdf_docx(docx_path, pdf_path):\ndocx_path = {docx_path},\npdf_path = {pdf_path}"
        )
        if self.__app_converter == "MSWORD":
            self.convert_from_pdf_docx_using_msword(docx_path, pdf_path)
        # elif self.__app_converter == "OPENOFFICE":
        #     self.convert_from_pdf_docx_using_openoffice(docx_path, pdf_path)
        elif self.__app_converter == "LIBREOFFICE":
            self.convert_from_pdf_docx_using_libreoffice(docx_path, pdf_path)

    def convert_from_pdf_docx_using_msword(self, docx_path, pdf_path):
        self.__obs_manager.obj_l.debug_logger(
            "Converter convert_from_pdf_docx_using_msword(docx_path, pdf_path)"
        )
        try:
            wdFormatPDF = 17
            word = comtypes.client.GetActiveObject("Word.Application")
            doc = word.Documents.Open(docx_path)
            doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
            doc.Close()
        except Exception:
            # TODO Статус бар - подумать
            self.__obs_manager.obj_l.error_logger(
                "Error in convert_from_pdf_docx_using_msword(docx_path, pdf_path)"
            )
        # word.Quit()

    def convert_from_pdf_docx_using_libreoffice(self, docx_path, pdf_path):
        self.__obs_manager.obj_l.debug_logger(
            "Converter convert_from_pdf_docx_using_libreoffice(docx_path, pdf_path)"
        )
        try:
            command = [
                self.__libreoffice_path,
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                os.path.dirname(pdf_path),
                docx_path,
            ]
            subprocess.run(command)
        except Exception:
            self.__obs_manager.obj_l.error_logger(
                "Error in convert_from_pdf_docx_using_libreoffice(docx_path, pdf_path)"
            )

    def export_to_pdf(self, multipage_pdf_path) -> None:
        """
        Вызывается при нажатии на кнопку EXPORT после диалогового окна.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"Converter export_to_pdf(multipage_pdf_path):\nmultipage_pdf_path = {multipage_pdf_path}"
        )
        # проверка на доступность конвертера
        flag_export = False
        self.__app_converter = self.__obs_manager.obj_sd.get_app_converter()
        if self.__app_converter == "MSWORD" and self.__status_msword:
            flag_export = True
        elif self.__app_converter == "LIBREOFFICE" and self.__status_libreoffice:
            flag_export = True
        if flag_export:
            # проход по всем вершинам дерева для заполенения project_pages_objects
            project_pages_objects = list()
            number_page = 0
            self.dfs(
                self.__obs_manager.obj_pd.get_project_node(),
                project_pages_objects,
                number_page,
            )
            self.__obs_manager.obj_l.debug_logger(
                f"Converter project_pages_objects = {project_pages_objects}"
            )
            # проход по project_pages_objects для преобразования каждой страницы в docx, а потом в pdf
            list_of_pdf_pages = self.get_list_of_created_pdf_pages(
                project_pages_objects
            )
            print(f"list_of_pdf_pages = {list_of_pdf_pages}")
            # объеденить несколько pdf файлов в один
            self.merge_pdfs_and_create(multipage_pdf_path, list_of_pdf_pages)
            # закрыть диалоговое окно
            self.__obs_manager.obj_sb.set_message_for_statusbar(
                f"Экспорт завершен. Файл {multipage_pdf_path} готов."
            )
            # открыть pdf
            os.startfile(os.path.dirname(multipage_pdf_path))
            self.__obs_manager.obj_sb.set_message_for_statusbar(
                "Преобразование завершено."
            )
        else:
            self.__obs_manager.obj_dw.warning_message(
                "Эскпорт отменён! Выбранный конвертер не работает."
            )

    def dfs(self, parent_node, project_pages_objects, number_page):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter dfs(node, project_pages_objects):\nparent_node = {parent_node},\nnumber_page = {number_page}"
        )
        childs = self.__obs_manager.obj_pd.get_childs(parent_node)
        if childs:
            for child in childs:
                # TODO подумать про PDF node, загруженный пользователем
                child_included = int(child.get("included"))
                print("included = ", child_included, type(child_included))
                if not child_included == 0:
                    # проход по страницам node
                    # TODO
                    id_active_template = child.get("id_active_template")
                    if id_active_template:
                        template = {"id_template": id_active_template}
                        pages = self.__obs_manager.obj_pd.get_pages_by_template(
                            template
                        )
                        for page in pages:
                            object = {
                                "type": "page",
                                "page": page,
                                "number_page": number_page,
                            }
                            print(f"object = {object}")
                            project_pages_objects.append(object)
                            number_page += 1
                    # проход по дочерним вершинам
                    self.dfs(child, project_pages_objects, number_page)

    # def get_list_of_created_pdf_pages(self, project_pages_objects) -> list:
    #     """
    #     Проход по project_pages_objects для преобразования каждой страницы в docx, а потом в pdf
    #     """
    #     self.__obs_manager.obj_l.debug_logger(
    #         f"Converter get_list_of_created_pdf_pages(project_pages_objects):\nproject_pages_objects = {project_pages_objects}"
    #     )

    #     list_of_pdf_pages = list()
    #     project_pages_objects_for_pool = list()
    #     for object in project_pages_objects:
    #         project_pages_objects_for_pool.append(ElementPool(object))
    #     # с WorkerPool
    #     with WorkerPool(n_jobs=1, use_dill=True) as pool:
    #         results = pool.map(
    #             self.process_object_of_project_pages_objects,
    #             project_pages_objects_for_pool,
    #         )
    #     # без WorkerPool
    #     # results = []
    #     # for obj in project_pages_objects_for_pool:
    #     #     result = self.process_object_of_project_pages_objects(obj)
    #     #     results.append(result)

    #     list_of_pdf_pages = [result for result in results if result]
    #     return list_of_pdf_pages

    # def process_object_of_project_pages_objects(self, object_for_pool) -> dict:
    #     self.__obs_manager.obj_l.debug_logger(
    #         f"Converter process_object_of_project_pages_objects(object_for_pool):\nobject_for_pool = {object_for_pool}"
    #     )
    #     object = object_for_pool.get_value()
    #     object_type = object.get("type")
    #     number_page = object.get("number_page")
    #     if object_type == "page":
    #         pdf_path = self.create_page_pdf(
    #             object.get("page"), True
    #         )
    #         return {"number_page": number_page, "pdf_path": pdf_path}
    #     return dict()

    def merge_pdfs_and_create(self, multipage_pdf_path, list_of_pdf_pages):
        self.__obs_manager.obj_l.debug_logger(
            f"Converter merge_pdfs(multipage_pdf_path, list_of_pdf_pages):\nmultipage_pdf_path = {multipage_pdf_path},\nlist_of_pdf_pages = {list_of_pdf_pages}"
        )
        # объединить несколько pdf файлов в один
        merger = PdfWriter()
        for pdf in sorted(list_of_pdf_pages, key=lambda x: x.get("number_page")):
            pdf_path = pdf.get("pdf_path")
            if os.path.exists(pdf_path):
                merger.append(pdf_path)
            else:
                self.__obs_manager.obj_l.error_logger(
                    f"Converter merge_pdfs(multipage_pdf_path, list_of_pdf_pages):\npdf_path = {pdf_path} не существует."
                )

        merger.write(multipage_pdf_path)
        merger.close()

    # ПОЛЕ ЭКПИРИМЕНТА
    # TODO Проверить его на работоспособностбь
    def get_list_of_created_pdf_pages(self, project_pages_objects) -> list:
        """
        Проход по project_pages_objects для преобразования каждой страницы в docx, а потом в pdf
        """
        self.__obs_manager.obj_l.debug_logger(
            f"Converter get_list_of_created_pdf_pages(project_pages_objects):\nproject_pages_objects = {project_pages_objects}"
        )
        DELAY = 0.5

        list_of_pdf_pages = list()
        project_pages_objects_for_pool = [
            ElementPool(obj) for obj in project_pages_objects
        ]

        with ThreadPoolExecutor() as executor:
            futures = []
            for obj in project_pages_objects_for_pool:
                # Запускаем асинхронную задачу
                future = executor.submit(
                    self.process_object_of_project_pages_objects, obj
                )
                futures.append(future)
                time.sleep(DELAY)  # Пауза перед запуском следующей задачи

        # Собираем результаты
        for future in futures:
            result = future.result()
            if result:
                list_of_pdf_pages.append(result)

        return list_of_pdf_pages

    def process_object_of_project_pages_objects(self, object_for_pool) -> dict:
        self.__obs_manager.obj_l.debug_logger(
            f"Converter process_object_of_project_pages_objects(object_for_pool):\nobject_for_pool = {object_for_pool}"
        )
        object = object_for_pool.get_value()
        object_type = object.get("type")
        number_page = object.get("number_page")
        if object_type == "page":
            pdf_path = self.create_page_pdf(object.get("page"), True)
            return {"number_page": number_page, "pdf_path": pdf_path}
        return dict()
