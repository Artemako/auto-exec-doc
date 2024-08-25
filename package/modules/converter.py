import os
import json
import copy
import functools
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import multiprocessing

import comtypes.client
import subprocess

from PySide6.QtCore import QDate, QLocale

from pypdf import PdfWriter
import datetime

import package.modules.convertervarimage as convertervarimage


class ConverterPool:
    def process_object_of_project_pages_objects(self, args) -> dict:
        local_osbm, object_for_pool = args
        local_osbm.obj_logg.debug_logger(
            f"Converter process_object_of_project_pages_objects(object_for_pool):\nobject_for_pool = {object_for_pool}"
        )
        object_type = object_for_pool.get("type")
        number_page = object_for_pool.get("number_page")
        if object_type == "page":
            pdf_path = self.create_page_pdf(
                local_osbm, object_for_pool.get("page"), True
            )
            return {"number_page": number_page, "pdf_path": pdf_path}
        return dict()

    def create_page_pdf(self, local_osbm, page, is_local: bool = False) -> str:
        """
        Создать pdf страницы. Вернуть директорию.
        """
        local_osbm.obj_logg.debug_logger(
            f"Converter create_page_pdf(page):\npage = {page}"
        )
        # проверка на DOCX или PDF
        typefile_page = page.get("typefile_page")
        if typefile_page == "DOCX":
            form_page_name = page.get("filename_page")
            docx_pdf_page_name = f"""page_{page.get("id_page")}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S%f')}"""
            # добыть информация для SectionInfo
            if is_local:
                local_osbm.obj_seci.update_sections_info(page)
            sections_info = local_osbm.obj_seci.get_sections_info()
            print(f"sections_info = {sections_info}")

            # создать docx из данным page
            self.create_docx_page(
                local_osbm, sections_info, form_page_name, docx_pdf_page_name
            )
            # создать pdf из docx
            pdf_path = os.path.normpath(
                self.create_pdf_from_docx_page(local_osbm, docx_pdf_page_name)
            )
        elif typefile_page == "PDF":
            pdf_page_name = page.get("filename_page")
            pdfs_folder_dirpath = local_osbm.obj_dirm.get_pdfs_folder_dirpath()
            pdf_path = os.path.join(pdfs_folder_dirpath, pdf_page_name + ".pdf")
        return pdf_path

    def get_form_page_fullname_and_docx_page_fullname(
        self, local_osbm, form_page_name, docx_pdf_page_name
    ):
        local_osbm.obj_logg.debug_logger(
            f"Converter get_form_page_fullname_and_docx_page_fullname(form_page_name, docx_pdf_page_name):\nform_page_name = {form_page_name},\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # получить docx_template
        form_page_fullname = str(form_page_name) + ".docx"
        docx_page_fullname = docx_pdf_page_name + ".docx"
        return form_page_fullname, docx_page_fullname

    def get_template_path_and_docx_path(
        self, local_osbm, form_page_fullname, docx_page_fullname
    ):
        local_osbm.obj_logg.debug_logger(
            f"Converter get_template_path_and_docx_path(form_page_fullname, docx_page_fullname):\nform_page_fullname = {form_page_fullname},\ndocx_page_fullname = {docx_page_fullname}"
        )
        # путь к шаблону в папке forms проекта
        template_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    local_osbm.obj_dirm.get_forms_folder_dirpath(),
                    form_page_fullname,
                )
            )
        )
        # путь к будущему docx файлу
        docx_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    local_osbm.obj_dirm.get_temp_dirpath(),
                    docx_page_fullname,
                )
            )
        )
        return template_path, docx_path

    def type_variable_is_text(self, local_osbm, data_variable, name_variable, value):
        local_osbm.obj_logg.debug_logger(
            f"Converter type_variable_is_text(data_variable, name_variable, value):\ndata_variable = {data_variable},\nname_variable = {name_variable},\nvalue = {value}"
        )
        try:
            if value:
                data_variable[str(name_variable)] = value
        except Exception as e:
            local_osbm.obj_logg.error_logger(f"Error in type_variable_is_text: {e}")

    def type_variable_is_date(
        self, local_osbm, data_variable, name_variable, value, config_variable
    ):
        local_osbm.obj_logg.debug_logger(
            f"Converter type_variable_is_date(data_variable, name_variable, value):\ndata_variable = {data_variable},\nname_variable = {name_variable},\nvalue = {value},\nconfig_variable = {config_variable}"
        )

        try:
            if value:
                str_format = config_variable.get("FORMAT", "")
                language = config_variable.get("LANGUAGE", "ru_RU")
                #
                locale = QLocale(language)
                qdate = QDate.fromString(value, "yyyy-MM-dd")
                current_value = locale.toString(qdate, str_format)
                data_variable[str(name_variable)] = current_value
        except Exception as e:
            print(f"{e}")
            local_osbm.obj_logg.error_logger(f"Error in type_variable_is_date: {e}")

    def type_variable_is_image(
        self,
        local_osbm,
        data_variable,
        name_variable,
        value,
        config_variable,
        docx_template,
    ):
        local_osbm.obj_logg.debug_logger(
            f"Converter type_variable_is_image(data_variable, name_variable, value, config_variable, docx_template):\n data_variable = {data_variable},\n name_variable = {name_variable},\n value = {value},\n config_variable = {config_variable},\n docx_template = {docx_template}"
        )
        try:
            if value:
                convvarimg = convertervarimage.ConverterVarImage(local_osbm)
                #
                unit = config_variable.get("UNIT", "MM")
                sizing_mode = config_variable.get("SIZINGMODE", "NOCHANGES")
                width = config_variable.get("WIDTH", 0)
                height = config_variable.get("HEIGHT", 0)
                #
                emu_sizes = convvarimg.get_emu_width_and_height_by_unit(
                    unit, width, height
                )
                emu_width = emu_sizes[0]
                emu_height = emu_sizes[1]
                #
                mm_sizes = convvarimg.get_mm_width_and_height_by_emu(
                    emu_width, emu_height
                )
                mm_width = mm_sizes[0]
                mm_height = mm_sizes[1]
                #
                temp_image = convvarimg.get_temp_image(value)
                inline_image = InlineImage(docx_template, temp_image)
                # TODO
                if sizing_mode == "NOCHANGES":
                    pass
                elif sizing_mode == "CONTAIN":
                    ...
                elif sizing_mode == "COVER":
                    ...
                elif sizing_mode == "FILL":
                    inline_image.width = Mm(mm_width)
                    inline_image.height = Mm(mm_height)
                print(f"mm_width = {mm_width}, mm_height = {mm_height}")
                data_variable[str(name_variable)] = inline_image
        except Exception as e:
            print(e)
            local_osbm.obj_logg.error_logger(f"Error in type_variable_is_image: {e}")

    def type_variable_is_table(
        self, local_osbm, data_variable, name_variable, value, id_variable
    ):
        local_osbm.obj_logg.debug_logger(
            f"Converter type_variable_is_table(data_variable, name_variable, value, id_variable):\ndata_variable = {data_variable},\nname_variable = {name_variable},\nvalue = {value},\nid_variable = {id_variable}"
        )
        try:
            # TODO Таблица
            if value:
                current_variable = local_osbm.obj_prodb.get_variable_by_id(id_variable)
                config_variable = current_variable.get("config_variable")
                config_dict = dict()
                if config_variable:
                    config_dict = json.loads(config_variable)
                print(f"config_dict = {config_dict}")
                # узнать content в таблице
                order_to_variable_config_dict = dict()
                object_variable = dict()
                rowcols = config_dict.get("ROWCOLS")
                for rowcol in rowcols:
                    value_config = rowcol.get("VALUE")
                    order_config = rowcol.get("ORDER")
                    order_to_variable_config_dict[order_config] = value_config
                    object_variable[value_config] = None

                print(f"object_variable = {object_variable}")
                # заполнять data_variable
                table_values = []
                if value:
                    table = json.loads(value)
                    for row, row_data in enumerate(table):
                        pt = copy.deepcopy(object_variable)
                        for col, cell_value in enumerate(row_data):
                            pt[order_to_variable_config_dict.get(col)] = cell_value
                        table_values.append(pt)
                print(f"table_values = {table_values}")
                data_variable[str(name_variable)] = table_values
        except Exception as e:
            local_osbm.obj_logg.error_logger(f"Error in type_variable_is_table: {e}")

    def check_type_variable_and_fill_data_variable(
        self, local_osbm, pair, data_variable, docx_template, is_rerender=False
    ):
        local_osbm.obj_logg.debug_logger(
            f"Converter check_type_variable_and_fill_data_variable(pair, data_variable, docx_template, is_rerender):\npair = {pair},\ndata_variable = {data_variable},\ndocx_template = {docx_template} \nis_rerender = {is_rerender}"
        )
        id_pair = pair.get("id_pair")
        id_page = pair.get("id_page")
        id_variable = pair.get("id_variable")
        value = pair.get("value_pair")
        # current_variable
        current_variable = local_osbm.obj_prodb.get_variable_by_id(id_variable)
        print(f"current_variable = {current_variable}")
        type_variable = current_variable.get("type_variable")
        name_variable = current_variable.get("name_variable")
        # из строки в json
        str_config_variable = current_variable.get("config_variable")
        config_variable = (
            json.loads(str_config_variable) if str_config_variable else dict()
        )
        # скипаем если is_rerender
        if not is_rerender and type_variable == "TEXT" or type_variable == "LONGTEXT":
            self.type_variable_is_text(local_osbm, data_variable, name_variable, value)
        elif not is_rerender and type_variable == "DATE":
            self.type_variable_is_date(
                local_osbm, data_variable, name_variable, value, config_variable
            )
        elif not is_rerender and type_variable == "TABLE":
            self.type_variable_is_table(
                local_osbm, data_variable, name_variable, value, id_variable
            )
        # общий для всех
        elif type_variable == "IMAGE":
            self.type_variable_is_image(
                local_osbm,
                data_variable,
                name_variable,
                value,
                config_variable,
                docx_template,
            )

    def create_docx_page(
        self, local_osbm, sections_info, form_page_name, docx_pdf_page_name
    ):
        local_osbm.obj_logg.debug_logger(
            f"Converter create_docx_page(sections_info, form_page_name, docx_pdf_page_name):\nsections_info = {sections_info},\nform_page_name = {form_page_name},\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # пути
        form_page_fullname, docx_page_fullname = (
            self.get_form_page_fullname_and_docx_page_fullname(
                local_osbm, form_page_name, docx_pdf_page_name
            )
        )
        template_path, docx_path = self.get_template_path_and_docx_path(
            local_osbm, form_page_fullname, docx_page_fullname
        )
        # TODO ReRender ???
        self.rerender(local_osbm, template_path, docx_path, sections_info)

    def rerender(self, local_osbm, template_path, docx_path, sections_info):
        local_osbm.obj_logg.debug_logger(
            f"Converter rerender(template_path, docx_path, sections_info):\ntemplate_path = {template_path},\ndocx_path = {docx_path},\nsections_info = {sections_info}"
        )
        current_path = template_path
        flag = 50
        is_rerender = False
        # создаем variable из sections_info
        data_variable = dict()
        while flag:
            docx_template = DocxTemplate(current_path)
            set_of_variables = docx_template.get_undeclared_template_variables()
            # обновляем variable из sections_info (из-за InlaneImage)
            for section_info in sections_info:
                # инфо из секции
                section_data = section_info.get("data")
                # перебор пар в section_data секции
                for pair in section_data:
                    self.check_type_variable_and_fill_data_variable(
                        local_osbm, pair, data_variable, docx_template, is_rerender
                    )
            print(f"data variable = {data_variable}")
            # первый render
            docx_template.render(data_variable)
            # узнаем новый список переменных
            new_set_of_variables = docx_template.get_undeclared_template_variables()
            # сохраняем документ
            print(f"BEFORE SAVE data_variable = {data_variable}")
            docx_template.save(docx_path)
            # если список переменных изменился
            if (
                len(new_set_of_variables) == 0
                or new_set_of_variables == set_of_variables
            ):
                flag = False
            else:
                current_path = docx_path
                is_rerender = True
                flag -= 1

    def create_pdf_from_docx_page(self, local_osbm, docx_pdf_page_name) -> str:
        local_osbm.obj_logg.debug_logger(
            f"Converter create_pdf_from_docx_page(docx_pdf_page_name) -> str:\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # пути к docx и к pdf
        docx_page_fullname = docx_pdf_page_name + ".docx"
        pdf_page_fullname = docx_pdf_page_name + ".pdf"
        docx_path = os.path.abspath(
            os.path.join(local_osbm.obj_dirm.get_temp_dirpath(), docx_page_fullname)
        )
        # путь к pdf в temp проекта
        pdf_path = os.path.abspath(
            os.path.join(local_osbm.obj_dirm.get_temp_dirpath(), pdf_page_fullname)
        )
        # преобразовать docx в pdf
        # convert(docx_path, pdf_path)
        self.convert_from_docx_to_pdf(local_osbm, docx_path, pdf_path)
        return pdf_path

    def convert_from_docx_to_pdf(self, local_osbm, docx_path, pdf_path):
        local_osbm.obj_logg.debug_logger(
            f"Converter convert_from_docx_to_pdf(docx_path, pdf_path):\ndocx_path = {docx_path},\npdf_path = {pdf_path}"
        )
        app_converter = local_osbm.obj_setdb.get_app_converter()
        if app_converter == "MSWORD":
            self.convert_from_docx_to_pdf_using_msword(local_osbm, docx_path, pdf_path)
        # elif app_converter == "OPENOFFICE":
        #     self.convert_from_docx_to_pdf_using_openoffice(docx_path, pdf_path)
        elif app_converter == "LIBREOFFICE":
            self.convert_from_docx_to_pdf_using_libreoffice(
                local_osbm, docx_path, pdf_path
            )

    def convert_from_docx_to_pdf_using_msword(self, local_osbm, docx_path, pdf_path):
        local_osbm.obj_logg.debug_logger(
            "Converter convert_from_docx_to_pdf_using_msword(docx_path, pdf_path)"
        )
        try:
            wdFormatPDF = 17
            word = comtypes.client.GetActiveObject("Word.Application")
            doc = word.Documents.Open(docx_path)
            doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
            doc.Close()
        except Exception as e:
            local_osbm.obj_logg.error_logger(
                f"Error in convert_from_docx_to_pdf_using_msword(docx_path, pdf_path): {e}"
            )
            raise local_osbm.obj_com.errors.MsWordError(e)

    def convert_from_docx_to_pdf_using_libreoffice(
        self, local_osbm, docx_path, pdf_path
    ):
        local_osbm.obj_logg.debug_logger(
            "Converter convert_from_docx_to_pdf_using_libreoffice(docx_path, pdf_path)"
        )
        try:
            libreoffice_path = local_osbm.obj_setdb.get_libreoffice_path()
            command = [
                libreoffice_path,
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                os.path.dirname(pdf_path),
                docx_path,
            ]
            subprocess.run(command)
        except Exception as e:
            local_osbm.obj_logg.error_logger(
                "Error in convert_from_docx_to_pdf_using_libreoffice(docx_path, pdf_path)"
            )
            raise local_osbm.obj_com.errors.LibreOfficeError(e)


class ConverterObjectsManager:
    def __init__(self, osbm):
        self.obj_dirm = osbm.obj_dirm
        self.obj_logg = osbm.obj_logg
        self.obj_prodb = osbm.obj_prodb
        self.obj_seci = osbm.obj_seci
        self.obj_setdb = osbm.obj_setdb
        self.obj_imgr = osbm.obj_imgr
        self.obj_film = osbm.obj_film
        # общее
        self.obj_com = osbm.obj_com


class Converter:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = ConverterObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(
            f"Converter setting_osbm():\nself.__osbm = {self.__osbm}"
        )

    def create_one_page_pdf(self, page) -> str:
        """
        Вызывается при нажатии на кнопку Save и/или выбра новой страницы.
        """
        self.__osbm.obj_logg.debug_logger(
            f"Converter create_one_page_pdf(page) -> str:\npage = {page}"
        )
        local_osbm = ConverterObjectsManager(self.__osbm)
        pdf_path = ConverterPool().create_page_pdf(local_osbm, page)
        return pdf_path

    def export_to_pdf(self, multipage_pdf_path):
        """
        Вызывается при нажатии на кнопку EXPORT после диалогового окна.
        """
        self.__osbm.obj_logg.debug_logger(
            f"Converter export_to_pdf(multipage_pdf_path):\nmultipage_pdf_path = {multipage_pdf_path}"
        )
        # проход по всем вершинам дерева для заполенения project_pages_objects
        project_pages_objects = list()
        self.__number_page = 0
        self.dfs(self.__osbm.obj_prodb.get_project_node(), project_pages_objects)
        print(f"self.__number_page = {self.__number_page}")
        self.__osbm.obj_logg.debug_logger(
            f"Converter project_pages_objects = {project_pages_objects}"
        )
        # проход по project_pages_objects для преобразования каждой страницы в docx, а потом в pdf
        list_of_pdf_pages = self.get_list_of_created_pdf_pages(project_pages_objects)
        print(f"list_of_pdf_pages = {list_of_pdf_pages}")
        # объеденить несколько pdf файлов в один
        self.merge_pdfs_and_create(multipage_pdf_path, list_of_pdf_pages)

    def dfs(self, parent_node, project_pages_objects):
        self.__osbm.obj_logg.debug_logger(
            f"Converter dfs(node, project_pages_objects):\nparent_node = {parent_node}"
        )
        childs = self.__osbm.obj_prodb.get_childs(parent_node)
        if childs:
            for child in childs:
                child_included = int(child.get("included"))
                print("included = ", child_included, type(child_included))
                if child_included:
                    # проход по страницам node
                    # TODO
                    id_active_template = child.get("id_active_template")
                    if id_active_template:
                        template = {"id_template": id_active_template}
                        pages = self.__osbm.obj_prodb.get_pages_by_template(template)
                        for page in pages:
                            object = {
                                "type": "page",
                                "page": page,
                                "number_page": self.__number_page,
                            }
                            print(f"object = {object}")
                            project_pages_objects.append(object)
                            self.__number_page += 1
                    # проход по дочерним вершинам
                    self.dfs(child, project_pages_objects)

    def merge_pdfs_and_create(self, multipage_pdf_path, list_of_pdf_pages):
        self.__osbm.obj_logg.debug_logger(
            f"Converter merge_pdfs(multipage_pdf_path, list_of_pdf_pages):\nmultipage_pdf_path = {multipage_pdf_path},\nlist_of_pdf_pages = {list_of_pdf_pages}"
        )
        # объединить несколько pdf файлов в один
        merger = PdfWriter()
        for pdf in sorted(list_of_pdf_pages, key=lambda x: x.get("number_page")):
            pdf_path = pdf.get("pdf_path")
            if os.path.exists(pdf_path):
                merger.append(pdf_path)
            else:
                self.__osbm.obj_logg.error_logger(
                    f"Converter merge_pdfs(multipage_pdf_path, list_of_pdf_pages):\npdf_path = {pdf_path} не существует."
                )

        merger.write(multipage_pdf_path)
        merger.close()

    def get_list_of_created_pdf_pages(self, project_pages_objects) -> list:
        """
        Проход по project_pages_objects для преобразования каждой страницы в docx, а потом в pdf
        """
        self.__osbm.obj_logg.debug_logger(
            f"Converter get_list_of_created_pdf_pages(project_pages_objects):\nproject_pages_objects = {project_pages_objects}"
        )
        list_of_pdf_pages = list()
        # с multiprocessing.Pool
        processes_number = int()
        app_converter = self.__osbm.obj_setdb.get_app_converter()
        if app_converter == "MSWORD":
            processes_number = max(1, multiprocessing.cpu_count() - 1)
        else:
            processes_number = 1
        #
        print(f"processes_number = {processes_number}")
        args = [
            (ConverterObjectsManager(self.__osbm), obj) for obj in project_pages_objects
        ]
        with multiprocessing.Pool(processes=processes_number) as pool:
            results = pool.map(
                functools.partial(
                    ConverterPool().process_object_of_project_pages_objects
                ),
                args,
            )
        # без WorkerPool
        # results = []
        # for obj in project_pages_objects:
        #     args = (ConverterObjectsManager(self.__osbm), obj)
        #     result = ConverterPool().process_object_of_project_pages_objects(args)
        #     results.append(result)
        print(f"results = {results}")
        list_of_pdf_pages = [result for result in results if result]
        return list_of_pdf_pages
