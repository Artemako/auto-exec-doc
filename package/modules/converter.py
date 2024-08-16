import os
import json
import copy
import functools
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Pt, Inches
import multiprocessing

import comtypes.client
import subprocess


from pypdf import PdfWriter
import datetime

class ConverterPool:
    def process_object_of_project_pages_objects(self, args) -> dict:
        local_obs_manager, object_for_pool = args
        local_obs_manager.obj_l.debug_logger(
            f"Converter process_object_of_project_pages_objects(object_for_pool):\nobject_for_pool = {object_for_pool}"
        )
        object_type = object_for_pool.get("type")
        number_page = object_for_pool.get("number_page")
        if object_type == "page":
            pdf_path = self.create_page_pdf(
                local_obs_manager, object_for_pool.get("page"), True
            )
            return {"number_page": number_page, "pdf_path": pdf_path}
        return dict()

    def create_page_pdf(self, local_obs_manager, page, is_local: bool = False) -> str:
        """
        Создать pdf страницы. Вернуть директорию.
        """
        local_obs_manager.obj_l.debug_logger(
            f"Converter create_page_pdf(page):\npage = {page}"
        )
        # было page.get("filename_page") вместо page.get("id_page")
        form_page_name = page.get("id_page")
        docx_pdf_page_name = f"""page_{page.get("id_page")}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"""
        # добыть информация для SectionInfo
        if is_local:
            local_obs_manager.obj_si.update_sections_info(page)
        sections_info = local_obs_manager.obj_si.get_sections_info()
        print(f"sections_info = {sections_info}")

        # создать docx из данным page
        self.create_docx_page(
            local_obs_manager, sections_info, form_page_name, docx_pdf_page_name
        )
        # создать pdf из docx
        pdf_path = os.path.normpath(
            self.create_pdf_from_docx_page(local_obs_manager, docx_pdf_page_name)
        )
        return pdf_path

    def get_form_page_fullname_and_docx_page_fullname(
        self, local_obs_manager, form_page_name, docx_pdf_page_name
    ):
        local_obs_manager.obj_l.debug_logger(
            f"Converter get_form_page_fullname_and_docx_page_fullname(form_page_name, docx_pdf_page_name):\nform_page_name = {form_page_name},\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # получить docx_template
        form_page_fullname = str(form_page_name) + ".docx"
        docx_page_fullname = docx_pdf_page_name + ".docx"
        return form_page_fullname, docx_page_fullname

    def get_template_path_and_docx_path(
        self, local_obs_manager, form_page_fullname, docx_page_fullname
    ):
        local_obs_manager.obj_l.debug_logger(
            f"Converter get_template_path_and_docx_path(form_page_fullname, docx_page_fullname):\nform_page_fullname = {form_page_fullname},\ndocx_page_fullname = {docx_page_fullname}"
        )
        # путь к шаблону в папке forms проекта
        template_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    local_obs_manager.obj_dpm.get_forms_folder_dirpath(),
                    form_page_fullname,
                )
            )
        )
        # путь к будущему docx файлу
        docx_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    local_obs_manager.obj_dpm.get_temp_dirpath(),
                    docx_page_fullname,
                )
            )
        )
        return template_path, docx_path

    def type_tag_is_text(self, local_obs_manager, data_tag, name_tag, value):
        local_obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_text(data_tag, name_tag, value):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value}"
        )
        try:
            if value:
                data_tag[str(name_tag)] = value
        except Exception as e: 
            self.__obs_manager.obj_l.error_logger(f"Error in type_tag_is_text: {e}")
            

    def type_tag_is_date(self, local_obs_manager, data_tag, name_tag, value):
        local_obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_date(data_tag, name_tag, value):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value}"
        )
        try:
            if value:
                data_tag[str(name_tag)] = value
        except Exception as e: 
            self.__obs_manager.obj_l.error_logger(f"Error in type_tag_is_date: {e}")

    def type_tag_is_image(
        self, local_obs_manager, data_tag, name_tag, value, docx_template
    ):
        local_obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_image(data_tag, name_tag, value, docx_template):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value},\ndocx_template = {docx_template}"
        )
        try:
            if value:
                image_dirpath = os.path.abspath(
                    os.path.join(
                        local_obs_manager.obj_dpm.get_images_folder_dirpath(),
                        value,
                    )
                )
                # TODO контент для изображения Inches, Pt, Cm, Mm
                image = InlineImage(docx_template, image_dirpath)
                data_tag[str(name_tag)] = image
        except Exception as e: 
            self.__obs_manager.obj_l.error_logger(f"Error in type_tag_is_image: {e}")

    def type_tag_is_table(self, local_obs_manager, data_tag, name_tag, value, id_tag):
        local_obs_manager.obj_l.debug_logger(
            f"Converter type_tag_is_table(data_tag, name_tag, value, id_tag):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value},\nid_tag = {id_tag}"
        )
        try:
            if value:
                current_tag = local_obs_manager.obj_pd.get_tag_by_id(id_tag)
                config_tag = current_tag.get("config_tag")
                config_dict = dict()        
                if config_tag:
                    config_dict = json.loads(config_tag)
                print(f"config_dict = {config_dict}")
                # узнать content в таблице
                order_to_tag_config_dict = dict()
                object_tag = dict()
                rowcols = config_dict.get("ROWCOLS")
                for rowcol in rowcols:
                    value_config = rowcol.get("VALUE")
                    order_config = rowcol.get("ORDER")
                    order_to_tag_config_dict[order_config] = value_config
                    object_tag[value_config] = None
                        
                print(f"object_tag = {object_tag}")
                # заполнять data_tag
                table_values = []
                if value:
                    table = json.loads(value)
                    for row, row_data in enumerate(table):
                        pt = copy.deepcopy(object_tag)
                        for col, cell_value in enumerate(row_data):
                            pt[order_to_tag_config_dict.get(col)] = cell_value
                        table_values.append(pt)
                print(f"table_values = {table_values}")
                data_tag[str(name_tag)] = table_values
        except Exception as e: 
            self.__obs_manager.obj_l.error_logger(f"Error in type_tag_is_table: {e}")

    def check_type_tag_and_fill_data_tag(
        self, local_obs_manager, pair, data_tag, docx_template
    ):
        local_obs_manager.obj_l.debug_logger(
            f"Converter check_type_tag_and_fill_data_tag(pair, data_tag, docx_template):\npair = {pair},\ndata_tag = {data_tag},\ndocx_template = {docx_template}"
        )
        id_pair = pair.get("id_pair")
        id_page = pair.get("id_page")
        id_tag = pair.get("id_tag")
        name_tag = pair.get("name_tag")
        value = pair.get("value")
        # current_tag
        current_tag = local_obs_manager.obj_pd.get_tag_by_id(id_tag)
        type_tag = current_tag.get("type_tag")
        if type_tag == "TEXT":
            self.type_tag_is_text(local_obs_manager, data_tag, name_tag, value)
        elif type_tag == "IMAGE":
            self.type_tag_is_image(
                local_obs_manager, data_tag, name_tag, value, docx_template
            )
        elif type_tag == "DATE":
            self.type_tag_is_date(local_obs_manager, data_tag, name_tag, value)
        elif type_tag == "TABLE":
            self.type_tag_is_table(local_obs_manager, data_tag, name_tag, value, id_tag)

    def create_docx_page(
        self, local_obs_manager, sections_info, form_page_name, docx_pdf_page_name
    ):
        local_obs_manager.obj_l.debug_logger(
            f"Converter create_docx_page(sections_info, form_page_name, docx_pdf_page_name):\nsections_info = {sections_info},\nform_page_name = {form_page_name},\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        form_page_fullname, docx_page_fullname = (
            self.get_form_page_fullname_and_docx_page_fullname(
                local_obs_manager, form_page_name, docx_pdf_page_name
            )
        )
        template_path, docx_path = self.get_template_path_and_docx_path(
            local_obs_manager, form_page_fullname, docx_page_fullname
        )
        docx_template = DocxTemplate(template_path)
        # создаем tag из sections_info
        data_tag = dict()
        for section_info in sections_info:
            # инфо из секции
            section_data = section_info.get("data")
            # перебор пар в section_data секции
            for pair in section_data:
                self.check_type_tag_and_fill_data_tag(
                    local_obs_manager, pair, data_tag, docx_template
                )

        print(f"data_tag = {data_tag}")
        docx_template.render(data_tag)
        print(f"docx_path = {docx_path}")
        docx_template.save(docx_path)

    def create_pdf_from_docx_page(self, local_obs_manager, docx_pdf_page_name) -> str:
        local_obs_manager.obj_l.debug_logger(
            f"Converter create_pdf_from_docx_page(docx_pdf_page_name) -> str:\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # пути к docx и к pdf
        docx_page_fullname = docx_pdf_page_name + ".docx"
        pdf_page_fullname = docx_pdf_page_name + ".pdf"
        docx_path = os.path.abspath(
            os.path.join(
                local_obs_manager.obj_dpm.get_temp_dirpath(), docx_page_fullname
            )
        )
        # путь к pdf в temp проекта
        pdf_path = os.path.abspath(
            os.path.join(
                local_obs_manager.obj_dpm.get_temp_dirpath(), pdf_page_fullname
            )
        )
        # преобразовать docx в pdf
        # convert(docx_path, pdf_path)
        self.convert_from_pdf_docx(local_obs_manager, docx_path, pdf_path)
        return pdf_path

    def convert_from_pdf_docx(self, local_obs_manager, docx_path, pdf_path):
        local_obs_manager.obj_l.debug_logger(
            f"Converter convert_from_pdf_docx(docx_path, pdf_path):\ndocx_path = {docx_path},\npdf_path = {pdf_path}"
        )
        try:
            app_converter = local_obs_manager.obj_sd.get_app_converter()
            if app_converter == "MSWORD":
                self.convert_from_pdf_docx_using_msword(
                    local_obs_manager, docx_path, pdf_path
                )
            # elif app_converter == "OPENOFFICE":
            #     self.convert_from_pdf_docx_using_openoffice(docx_path, pdf_path)
            elif app_converter == "LIBREOFFICE":
                self.convert_from_pdf_docx_using_libreoffice(
                    local_obs_manager, docx_path, pdf_path
                )
        except Exception as e:
            raise e
        
    def convert_from_pdf_docx_using_msword(
        self, local_obs_manager, docx_path, pdf_path
    ):
        local_obs_manager.obj_l.debug_logger(
            "Converter convert_from_pdf_docx_using_msword(docx_path, pdf_path)"
        )
        try:
            wdFormatPDF = 17
            word = comtypes.client.GetActiveObject("Word.Application")
            doc = word.Documents.Open(docx_path)
            doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
            doc.Close()
        except Exception as e:
            local_obs_manager.obj_l.error_logger(
                "Error in convert_from_pdf_docx_using_msword(docx_path, pdf_path)"
            )
            raise Exception("MSWORD")

    def convert_from_pdf_docx_using_libreoffice(
        self, local_obs_manager, docx_path, pdf_path
    ):
        local_obs_manager.obj_l.debug_logger(
            "Converter convert_from_pdf_docx_using_libreoffice(docx_path, pdf_path)"
        )
        try:
            libreoffice_path = local_obs_manager.obj_sd.get_libreoffice_path()
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
            local_obs_manager.obj_l.error_logger(
                "Error in convert_from_pdf_docx_using_libreoffice(docx_path, pdf_path)"
            )
            raise Exception("LIBREOFFICE")



class ConverterObjectsManager:
    def __init__(self, obs_manager):
        self.obj_dpm = obs_manager.obj_dpm
        self.obj_l = obs_manager.obj_l
        self.obj_pd = obs_manager.obj_pd
        self.obj_si = obs_manager.obj_si
        self.obj_sd = obs_manager.obj_sd


class Converter:
    def __init__(self):
        pass

    def setting_obs_manager(self, obs_manager):
        self.__obs_manager = ConverterObjectsManager(obs_manager)
        self.__obs_manager.obj_l.debug_logger(
            f"Converter setting_obs_manager():\nself.__obs_manager = {self.__obs_manager}"
        )

    def create_one_page_pdf(self, page) -> str:
        """
        Вызывается при нажатии на кнопку Save и/или выбра новой страницы.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"Converter create_one_page_pdf(page) -> str:\npage = {page}"
        )
        try:
            local_obs_manager = ConverterObjectsManager(self.__obs_manager)
            pdf_path = ConverterPool().create_page_pdf(local_obs_manager, page)
            return pdf_path
        except Exception as e:
            raise e

    def export_to_pdf(self, multipage_pdf_path):
        """
        Вызывается при нажатии на кнопку EXPORT после диалогового окна.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"Converter export_to_pdf(multipage_pdf_path):\nmultipage_pdf_path = {multipage_pdf_path}"
        )
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

    def get_list_of_created_pdf_pages(self, project_pages_objects) -> list:
        """
        Проход по project_pages_objects для преобразования каждой страницы в docx, а потом в pdf
        """
        self.__obs_manager.obj_l.debug_logger(
            f"Converter get_list_of_created_pdf_pages(project_pages_objects):\nproject_pages_objects = {project_pages_objects}"
        )
        list_of_pdf_pages = list()
        # с multiprocessing.Pool
        processes_number = int()
        app_converter = self.__obs_manager.obj_sd.get_app_converter()
        if app_converter == "MSWORD":
            processes_number = max(1, multiprocessing.cpu_count() - 1)
        else:
            processes_number = 1
        #
        print(f"processes_number = {processes_number}")
        args = [
            (ConverterObjectsManager(self.__obs_manager), obj)
            for obj in project_pages_objects
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
        #     args = (ConverterObjectsManager(self.__obs_manager), obj)
        #     result = ConverterPool().process_object_of_project_pages_objects(args)
        #     results.append(result)
        list_of_pdf_pages = [result for result in results if result]
        return list_of_pdf_pages
