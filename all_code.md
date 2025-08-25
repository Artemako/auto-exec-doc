### D:\vs_projects\auto-exec-doc\examples\better_spoiler.py
``python
"""
Elypson/qt-collapsible-section
(c) 2016 Michael A. Voelkel - michael.alexander.voelkel@gmail.com

This file is part of Elypson/qt-collapsible section.

Elypson/qt-collapsible-section is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, version 3 of the License, or
(at your option) any later version.

Elypson/qt-collapsible-section is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with Elypson/qt-collapsible-section. If not, see <http:#www.gnu.org/licenses/>.
"""

import PySide6.QtCore as cr
import PySide6.QtWidgets as wd

import sys


class Section(wd.QWidget):
    def __init__(self, title="", animationDuration=100, parent=None):
        super().__init__(parent)
        self.animationDuration = animationDuration
        self.toggleButton = wd.QToolButton(self)
        self.headerLine = wd.QFrame(self)
        self.toggleAnimation = cr.QParallelAnimationGroup(self)
        self.contentArea = wd.QScrollArea(self)
        self.mainLayout = wd.QGridLayout(self)

        self.toggleButton.setStyleSheet("QToolButton {border: none;}")
        self.toggleButton.setToolButtonStyle(cr.Qt.ToolButtonTextBesideIcon)
        self.toggleButton.setArrowType(cr.Qt.RightArrow)
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)

        self.headerLine.setFrameShape(wd.QFrame.HLine)
        self.headerLine.setFrameShadow(wd.QFrame.Sunken)
        self.headerLine.setSizePolicy(wd.QSizePolicy.Expanding, wd.QSizePolicy.Maximum)

        # self.contentArea.setLayout(wd.QHBoxLayout())
        self.contentArea.setSizePolicy(wd.QSizePolicy.Expanding, wd.QSizePolicy.Fixed)

        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)

        # let the entire widget grow and shrink with its content
        self.toggleAnimation.addAnimation(cr.QPropertyAnimation(self, b"minimumHeight"))
        self.toggleAnimation.addAnimation(cr.QPropertyAnimation(self, b"maximumHeight"))
        self.toggleAnimation.addAnimation(
            cr.QPropertyAnimation(self.contentArea, b"maximumHeight")
        )

        self.mainLayout.setVerticalSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        row = 0
        self.mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, cr.Qt.AlignLeft)
        self.mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        self.mainLayout.addWidget(self.contentArea, row + 1, 0, 1, 3)
        self.setLayout(self.mainLayout)

        self.toggleButton.toggled.connect(self.toggle)

    def setContentLayout(self, contentLayout):
        layout = self.contentArea.layout()
        del layout
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(0, self.toggleAnimation.animationCount() - 1):
            SectionAnimation = self.toggleAnimation.animationAt(i)
            SectionAnimation.setDuration(self.animationDuration)
            SectionAnimation.setStartValue(collapsedHeight)
            SectionAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1
        )
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

    def toggle(self, collapsed):
        if collapsed:
            self.toggleButton.setArrowType(cr.Qt.DownArrow)
            self.toggleAnimation.setDirection(cr.QAbstractAnimation.Forward)
        else:
            self.toggleButton.setArrowType(cr.Qt.RightArrow)
            self.toggleAnimation.setDirection(cr.QAbstractAnimation.Backward)
        self.toggleAnimation.start()


# if __name__ == "__main__":

#     class Window(wd.QMainWindow):
#         def __init__(self, parent=None):
#             super().__init__(parent)
#             section = Section("Section", 100, self)

#             anyLayout = wd.QVBoxLayout()
#             anyLayout.addWidget(wd.QLabel("Some Text in Section", section))
#             anyLayout.addWidget(wd.QPushButton("Button in Section", section))

#             section.setContentLayout(anyLayout)

#             self.place_holder = wd.QWidget()  # placeholder widget, only used to get acces to wd.QMainWindow functionalities
#             mainLayout = wd.QHBoxLayout(self.place_holder)
#             mainLayout.addWidget(section)
#             mainLayout.addStretch(1)
#             self.setCentralWidget(self.place_holder)

#     app = wd.QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())

``
### D:\vs_projects\auto-exec-doc\examples\conv_exp.py
``python
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

    def __init__(self, osbm):
        super().__init__()
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("MsWordThread __init__()")
        self.__status_msword = False

    def run(self):
        self.initialize_msword()

    def initialize_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread initialize_msword()")
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
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("Converter __init__()")
        self.__status_msword = False
        self.__status_libreoffice = False
        self.__app_converter = None
        # экземпляр QThread
        self.__msword_thread = MsWordThread(self.__osbm)

    def setting_converter(self):
        self.__osbm.obj_logg.debug_logger("Converter setting_converter()")
        self.run_libreoffice()
        # подключение сигнала к слоту и запуск потока
        self.__msword_thread.status_changed.connect(self.update_status_msword)
        self.__msword_thread.start()

    def update_status_msword(self, status):
        self.__osbm.obj_logg.debug_logger(
            f"Converter update_status_msword(status):\nstatus = {status}"
        )
        self.__status_msword = status
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_msword_label(self.__status_msword)

    def get_status_msword(self):
        self.__osbm.obj_logg.debug_logger(
            f"Converter get_status_msword():\nself.__status_msword = {self.__status_msword}"
        )
        return self.__status_msword

    def get_status_libreoffice(self):
        self.__osbm.obj_logg.debug_logger(
            f"Converter get_status_libreoffice():\nself.__status_libreoffice = {self.__status_libreoffice}"
        )
        return self.__status_libreoffice

    def run_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("Converter run_libreoffice()")
        self.__libreoffice_path = "C:\Program Files\LibreOffice\program\soffice.exe"
        if os.path.exists(self.__libreoffice_path):
            self.__status_libreoffice = True
        else:
            self.__status_libreoffice = False
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_libreoffice_label(
                self.__status_libreoffice
            )

    def create_and_view_page_pdf(self, page):
        """
        Вызывается при нажатии на кнопку Save.
        """
        self.__osbm.obj_logg.debug_logger(
            f"Converter create_one_page_pdf(page):\npage = {page}"
        )
        self.__app_converter = self.__osbm.obj_setdb.get_app_converter()
        if self.__app_converter == "MSWORD" and self.__status_msword:
            pass
        elif self.__app_converter == "LIBREOFFICE" and self.__status_libreoffice:
            pass
        else:
            self.__osbm.obj_dw.warning_message(
                "Отображение недоступно! Выбранный конвертер не работает."
            )
        # создать pdf
        pdf_path = self.create_page_pdf(page)
        # открыть pdf
        self.__osbm.obj_pdfv.load_and_show_pdf_document(pdf_path)

    def create_page_pdf(self, page, is_local: bool = False) -> str:
        """
        Создать pdf страницы. Вернуть директорию.
        """
        self.__osbm.obj_logg.debug_logger(
            f"Converter create_one_page_pdf(page):\npage = {page}"
        )
        # было page.get("filename_page") вместо page.get("id_page")
        form_page_name = page.get("id_page")
        docx_pdf_page_name = f"""page_{page.get("id_page")}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"""
        # добыть информация для SectionInfo
        if not is_local:
            sections_info = self.__osbm.obj_seci.get_sections_info()
        else:
            object = sectionsinfo.SectionsInfo(self.__osbm)
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
        self.__osbm.obj_logg.debug_logger(
            f"Converter get_form_page_fullname_and_docx_page_fullname(form_page_name, docx_pdf_page_name):\nform_page_name = {form_page_name},\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # получить docx_template
        form_page_fullname = str(form_page_name) + ".docx"
        docx_page_fullname = docx_pdf_page_name + ".docx"
        return form_page_fullname, docx_page_fullname

    def get_template_path_and_docx_path(self, form_page_fullname, docx_page_fullname):
        self.__osbm.obj_logg.debug_logger(
            f"Converter get_template_path_and_docx_path(form_page_fullname, docx_page_fullname):\nform_page_fullname = {form_page_fullname},\ndocx_page_fullname = {docx_page_fullname}"
        )
        # путь к шаблону в папке forms проекта
        template_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    self.__osbm.obj_dirm.get_forms_folder_dirpath(),
                    form_page_fullname,
                )
            )
        )
        # путь к будущему docx файлу
        docx_path = os.path.normpath(
            os.path.abspath(
                os.path.join(
                    self.__osbm.obj_dirm.get_temp_dirpath(),
                    docx_page_fullname,
                )
            )
        )
        return template_path, docx_path

    def type_tag_is_text(self, data_tag, name_tag, value):
        self.__osbm.obj_logg.debug_logger(
            f"Converter type_tag_is_text(data_tag, name_tag, value):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value}"
        )
        if value:
            data_tag[str(name_tag)] = value

    def type_tag_is_date(self, data_tag, name_tag, value):
        self.__osbm.obj_logg.debug_logger(
            f"Converter type_tag_is_date(data_tag, name_tag, value):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value}"
        )
        if value:
            data_tag[str(name_tag)] = value

    def type_tag_is_image(self, data_tag, name_tag, value, docx_template):
        self.__osbm.obj_logg.debug_logger(
            f"Converter type_tag_is_image(data_tag, name_tag, value, docx_template):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value},\ndocx_template = {docx_template}"
        )
        if value:
            image_dirpath = os.path.abspath(
                os.path.join(
                    self.__osbm.obj_dirm.get_images_folder_dirpath(),
                    value,
                )
            )
            # TODO контент для изображения
            image = InlineImage(docx_template, image_dirpath)
            data_tag[str(name_tag)] = image

    def type_tag_is_table(self, data_tag, name_tag, value, id_tag):
        self.__osbm.obj_logg.debug_logger(
            f"Converter type_tag_is_table(data_tag, name_tag, value, id_tag):\ndata_tag = {data_tag},\nname_tag = {name_tag},\nvalue = {value},\nid_tag = {id_tag}"
        )
        config_table = self.__osbm.obj_prodb.get_config_table_by_id(id_tag)
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
        self.__osbm.obj_logg.debug_logger(
            f"Converter check_type_tag_and_fill_data_tag(pair, data_tag, docx_template):\npair = {pair},\ndata_tag = {data_tag},\ndocx_template = {docx_template}"
        )
        id_pair = pair.get("id_pair")
        id_page = pair.get("id_page")
        id_tag = pair.get("id_tag")
        name_tag = pair.get("name_tag")
        value = pair.get("value")
        # config_tag
        config_tag = self.__osbm.obj_prodb.get_config_tag_by_id(id_tag)
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
        self.__osbm.obj_logg.debug_logger(
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
        self.__osbm.obj_logg.debug_logger(
            f"Converter create_pdf_from_docx_page(docx_pdf_page_name) -> str:\ndocx_pdf_page_name = {docx_pdf_page_name}"
        )
        # пути к docx и к pdf
        docx_page_fullname = docx_pdf_page_name + ".docx"
        pdf_page_fullname = docx_pdf_page_name + ".pdf"
        docx_path = os.path.abspath(
            os.path.join(
                self.__osbm.obj_dirm.get_temp_dirpath(), docx_page_fullname
            )
        )
        # путь к pdf в temp проекта
        pdf_path = os.path.abspath(
            os.path.join(
                self.__osbm.obj_dirm.get_temp_dirpath(), pdf_page_fullname
            )
        )
        # преобразовать docx в pdf
        # convert(docx_path, pdf_path)
        self.convert_from_pdf_docx(docx_path, pdf_path)
        return pdf_path

    def convert_from_pdf_docx(self, docx_path, pdf_path):
        self.__osbm.obj_logg.debug_logger(
            f"Converter convert_from_pdf_docx(docx_path, pdf_path):\ndocx_path = {docx_path},\npdf_path = {pdf_path}"
        )
        if self.__app_converter == "MSWORD":
            self.convert_from_pdf_docx_using_msword(docx_path, pdf_path)
        # elif self.__app_converter == "OPENOFFICE":
        #     self.convert_from_pdf_docx_using_openoffice(docx_path, pdf_path)
        elif self.__app_converter == "LIBREOFFICE":
            self.convert_from_pdf_docx_using_libreoffice(docx_path, pdf_path)

    def convert_from_pdf_docx_using_msword(self, docx_path, pdf_path):
        self.__osbm.obj_logg.debug_logger(
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
            self.__osbm.obj_logg.error_logger(
                "Error in convert_from_pdf_docx_using_msword(docx_path, pdf_path)"
            )
        # word.Quit()

    def convert_from_pdf_docx_using_libreoffice(self, docx_path, pdf_path):
        self.__osbm.obj_logg.debug_logger(
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
            self.__osbm.obj_logg.error_logger(
                "Error in convert_from_pdf_docx_using_libreoffice(docx_path, pdf_path)"
            )

    def export_to_pdf(self, multipage_pdf_path) -> None:
        """
        Вызывается при нажатии на кнопку EXPORT после диалогового окна.
        """
        self.__osbm.obj_logg.debug_logger(
            f"Converter export_to_pdf(multipage_pdf_path):\nmultipage_pdf_path = {multipage_pdf_path}"
        )
        # проверка на доступность конвертера
        flag_export = False
        self.__app_converter = self.__osbm.obj_setdb.get_app_converter()
        if self.__app_converter == "MSWORD" and self.__status_msword:
            flag_export = True
        elif self.__app_converter == "LIBREOFFICE" and self.__status_libreoffice:
            flag_export = True
        if flag_export:
            # проход по всем вершинам дерева для заполенения project_pages_objects
            project_pages_objects = list()
            number_page = 0
            self.dfs(
                self.__osbm.obj_prodb.get_project_node(),
                project_pages_objects,
                number_page,
            )
            self.__osbm.obj_logg.debug_logger(
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
            self.__osbm.obj_stab.set_message_for_statusbar(
                f"Экспорт завершен. Файл {multipage_pdf_path} готов."
            )
            # открыть pdf
            os.startfile(os.path.dirname(multipage_pdf_path))
            self.__osbm.obj_stab.set_message_for_statusbar(
                "Преобразование завершено."
            )
        else:
            self.__osbm.obj_dw.warning_message(
                "Эскпорт отменён! Выбранный конвертер не работает."
            )

    def dfs(self, parent_node, project_pages_objects, number_page):
        self.__osbm.obj_logg.debug_logger(
            f"Converter dfs(node, project_pages_objects):\nparent_node = {parent_node},\nnumber_page = {number_page}"
        )
        childs = self.__osbm.obj_prodb.get_childs(parent_node)
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
                        pages = self.__osbm.obj_prodb.get_pages_by_template(
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
    #     self.__osbm.obj_logg.debug_logger(
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
    #     self.__osbm.obj_logg.debug_logger(
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

    # ПОЛЕ ЭКПИРИМЕНТА
    # TODO Проверить его на работоспособностбь
    def get_list_of_created_pdf_pages(self, project_pages_objects) -> list:
        """
        Проход по project_pages_objects для преобразования каждой страницы в docx, а потом в pdf
        """
        self.__osbm.obj_logg.debug_logger(
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
        self.__osbm.obj_logg.debug_logger(
            f"Converter process_object_of_project_pages_objects(object_for_pool):\nobject_for_pool = {object_for_pool}"
        )
        object = object_for_pool.get_value()
        object_type = object.get("type")
        number_page = object.get("number_page")
        if object_type == "page":
            pdf_path = self.create_page_pdf(object.get("page"), True)
            return {"number_page": number_page, "pdf_path": pdf_path}
        return dict()

``
### D:\vs_projects\auto-exec-doc\examples\custom_list.py
``python
import sys
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel

class ListItem(QWidget):
    def __init__(self, text):
        super().__init__()
        
        layout = QHBoxLayout()
        
        # Текстовый элемент
        self.label = QLabel(text)
        
        # Кнопка в конце
        self.button = QPushButton("Click Me")
        
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()

        for i in range(5):
            item = ListItem(f"Item {i + 1}")
            list_widget_item = QListWidgetItem()
            list_widget_item.setSizeHint(item.sizeHint())
            
            self.list_widget.addItem(list_widget_item)
            self.list_widget.setItemWidget(list_widget_item, item)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.resize(300, 400)
    main_window.show()
    
    sys.exit(app.exec())

``
### D:\vs_projects\auto-exec-doc\examples\docx-tpl-table_in_table.py
``python
from docxtpl import DocxTemplate
import os

input_path = os.path.normpath("examples/parent_child_table.docx")
output_path = os.path.normpath("examples/result_parent_child_table.docx")

tpl = DocxTemplate(input_path)

context = {
    "parent_table": [
        {
            "label": "yellow",
            "child_table": ["child1", "child2"],
        },
        {
            "label": "red",
            "child_table": ["child3", "child4"],
        },
        {
            "label": "green",
            "child_table": ["child5", "child6"],
        },
    ],
}


tpl.render(context)
tpl.save(output_path)

``
### D:\vs_projects\auto-exec-doc\examples\docx-tpl-черновик.py
``python
from docxtpl import DocxTemplate, InlineImage
import os
# tpl = DocxTemplate("example.docx")

input_path = os.path.normpath("examples/3-ПТ2-1.docx")
output_path = os.path.normpath("examples/output.docx")

tpl = DocxTemplate(input_path)

context = {
    "col_labels": ["fruit", "vegetable", "stone", "thing"],
    "tbl_tags": [
        {"label": "yellow", "cols": ["banana", "capsicum", "pyrite", "taxi"]},
        {"label": "red", "cols": ["apple", "tomato", "cinnabar", "doubledecker"]},
        {"label": "green", "cols": ["guava", "cucumber", "aventurine", "card"]},
    ],
}


data_tag = {
    "кабеля": [{"марка": "ываыа", "длина_всего": "выаыа", "длина_опт": "", "инфо": ""}],
    "общая_физ_длина": "выыа",
    "общая_опт_длина": "{{ Привет }}",
    "год_прокладки_кабеля": None,
    "год_составления_паспорта": "2023",
    "отв_пред_орг_фио": "ыва",
    "название_объекта": "Приозерск",
    "участок": "Рай \n Привет мой дивный уголок хаха\n ваы а"
}


# set_of_variables = tpl.get_undeclared_template_variables()
# print(set_of_variables)
tpl.render(data_tag)

tpl.save(output_path)

# tpl = DocxTemplate(output_path)

# data_tag = {
#     "кабеля": [{"марка": "ываыа", "длина_всего": "выаыа", "длина_опт": "", "инфо": ""}],
#     "общая_физ_длина": "выыа",
#     "общая_опт_длина": "{{ Привет }}",
#     "год_прокладки_кабеля": None,
#     "год_составления_паспорта": "2023",
#     "отв_пред_орг_фио": "ыва",
#     "название_объекта": "Приозерск",
#     "участок": "Рай"
# }

# tpl.render(data_tag)
# tpl.save(output_path)

``
### D:\vs_projects\auto-exec-doc\examples\docx_to_img.py
``python
import subprocess

command = ['unoconv', '-f', 'png', 'examples/example.docx']
subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
``
### D:\vs_projects\auto-exec-doc\examples\docx_to_pdf.py
``python

from docx2pdf import convert

convert("D:\work\project\AutoExecDoc\examples/3-ПТ3-1.docx", "D:\work\project\AutoExecDoc\examples\output.pdf")

``
### D:\vs_projects\auto-exec-doc\examples\drag.py
``python
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

class DraggableTableWidget(QTableWidget):
    def __init__(self, parent = None):
        self.__parent = parent
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dropEvent(self, event):
        if event.source() == self:
            drop_row = self.rowAt(event.position().y())
            if drop_row == -1:
                drop_row = self.rowCount() - 1

            drag_row = self.currentRow()

            if drag_row != drop_row and drag_row != -1:
                row_data = []
                for column in range(self.columnCount()):
                    item = self.item(drag_row, column)
                    row_data.append(item.text() if item else "")

                self.insertRow(drop_row)

                for column in range(self.columnCount()):
                    self.setItem(drop_row, column, QTableWidgetItem(row_data[column]))
                    
                self.removeRow(drag_row if drag_row < drop_row else drag_row + 1)
        event.accept()
        # TODO self.__parent сделать перестановку компонентов
        # self.__parent.drop_changed(item)

    def dragMoveEvent(self, event):
        if event.source() == self:
            event.accept()


    from PySide6.QtWidgets import QTreeWidget, QAbstractItemView
from PySide6.QtCore import Qt


class DraggableTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        self.__parent = parent
        super().__init__()
        self.setDragDropMode(QTreeWidget.InternalMove)

    def set_parent(self, parent):
        self.__parent = parent

    def dragMoveEvent(self, event):
        if self.canDrop(event):
            super().dragMoveEvent(event)
        else:
            event.ignore()

    def dropEvent(self, event):
        if self.canDrop(event):
            item = self.itemAt(event.pos())
            item_from = self.currentItem()
            item_to = item
            super().dropEvent(event)
            self.__parent.drop_changed(item)
        else:
            event.ignore()

    def canDrop(self, event):
        target = self.itemAt(event.pos())
        if target is not None:
            index = self.indexFromItem(target)
            indicator = self.dragIndicator(
                event.pos(), self.visualItemRect(target), index
            )
            return (
                indicator == QAbstractItemView.AboveItem
                or indicator == QAbstractItemView.BelowItem
            )
        return False

    def dragIndicator(self, pos, rect, index):
        indicator = QAbstractItemView.OnViewport
        if not self.dragDropOverwriteMode():
            margin = int(max(2, min(rect.height() / 5.5, 12)))
            if pos.y() - rect.top() < margin:
                indicator = QAbstractItemView.AboveItem
            elif rect.bottom() - pos.y() < margin:
                indicator = QAbstractItemView.BelowItem
            elif rect.contains(pos, True):
                indicator = QAbstractItemView.OnItem
        else:
            touching = rect.adjust(-1, -1, 1, 1)
            if touching.contains(pos, False):
                indicator = QAbstractItemView.OnItem
        if (
            indicator == QAbstractItemView.OnItem
            and not self.model().flags(index) & Qt.ItemIsDropEnabled
        ):
            if pos.y() < rect.center().y():
                indicator = QAbstractItemView.AboveItem
            else:
                indicator = QAbstractItemView.BelowItem
        return indicator




    def drop_changed(self, item):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow drop_changed(item):\nitem = {item}"
        )
        # узнать вершину
        current_node = item.data(0, Qt.UserRole)
        print(f"current_node = {current_node}")
        old_id_parent = current_node.get("id_parent")
        # родитель
        parent_item = item.parent()
        if parent_item is None:
            parent_node = self.__osbm.obj_prodb.get_project_node()
        else:
            parent_node = parent_item.data(0, Qt.UserRole)
        id_parent_node = parent_node.get("id_node")
        if old_id_parent == id_parent_node:
            # только в одной группе
            self.update_order_for_parent_item_childs(parent_item, parent_node)
        else:
            # в разных группах (сначала в новой, потом в старой)
            self.update_order_for_parent_item_childs(parent_item)
            self.update_order_for_old_parent_node_childs(old_id_parent)
    

    def update_order_for_parent_item_childs(self, parent_item, parent_node):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow update_order_for_parent_item_childs(parent_item, parent_node):\nparent_item = {parent_item}\nparent_node = {parent_node}"
        )
        # получить дочерние элементы
        if parent_item is None:
            children_items = [child_item for child_item in self.ui.tw_nodes.invisibleRootItem().takeChildren()]
        else:
            children_items = parent_item.takeChildren()
        # обновить порядок
        for index, child_item in enumerate(children_items):
            child_node = child_item.data(0, Qt.UserRole)
            # поставить родителя и порядок
            self.__osbm.obj_prodb.set_new_parent_for_child_node(parent_node, child_node)
            self.__osbm.obj_prodb.set_order_for_node(child_node, index)

    def update_order_for_old_parent_node_childs(self, old_id_parent):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow update_order_for_old_parent_node_childs(old_id_parent):\nold_id_parent = {old_id_parent}"
        )
        parent_node = {
            "id_node": old_id_parent,
        }
        childs_nodes = self.__osbm.obj_prodb.get_childs(parent_node)
        for index, child_node in enumerate(childs_nodes):
            # поставить порядок
            self.__osbm.obj_prodb.set_order_for_node(child_node, index)
``
### D:\vs_projects\auto-exec-doc\examples\extract_tags.py
``python
import re
from docx import Document

def extract_jinja_tags(docx_path):
    # Загружаем документ
    doc = Document(docx_path)
    
    # Регулярное выражение для поиска Jinja тегов
    jinja_pattern = r'\{\%.*?\%\}|\{\{.*?\}\}'
    
    jinja_tags = []
    
    # Обходим все параграфы в документе
    for para in doc.paragraphs:
        jinja_tags.extend(re.findall(jinja_pattern, para.text))
    
    # Обходим все таблицы в документе
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                jinja_tags.extend(re.findall(jinja_pattern, cell.text))

    # Обходим колонтитулы
    for section in doc.sections:
        for header in section.header.paragraphs:
            jinja_tags.extend(re.findall(jinja_pattern, header.text))
        for footer in section.footer.paragraphs:
            jinja_tags.extend(re.findall(jinja_pattern, footer.text))

    # Поиск в фигурах (шапках с рисованием, если поддерживаются)
    for shape in doc.inline_shapes:
        if shape.type == 3:  # 3 - тип 'Picture'
            continue
        jinja_tags.extend(re.findall(jinja_pattern, shape.text))
    
    return jinja_tags

# Пример использования
tags = extract_jinja_tags('examples/3-ПТ2-1.docx')
for tag in tags:
    print(tag)
``
### D:\vs_projects\auto-exec-doc\examples\mainwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(200, 268)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = QListWidget(self.centralWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 200, 17))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Test Window", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"some", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"list", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"with", None));
        ___qlistwidgetitem3 = self.listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"items", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"SomeButton", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\examples\new_collapsebutton.py
``python
from PySide6.QtWidgets import QToolButton, QApplication, QMainWindow
from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QAbstractAnimation
import sys

class CollapseButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.content_ = None
        self.setCheckable(True)
        self.setStyleSheet("background:none")
        self.setIconSize(QSize(8, 8))
        self.setFont(QApplication.font())
        self.toggled.connect(self.on_toggled)

    def setText(self, text):
        QToolButton.setText(self, " " + text)

    def setContent(self, content):
        assert(content is not None)
        self.content_ = content
        animation = QPropertyAnimation(content, b"maximumHeight")
        animation.setStartValue(0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.setDuration(300)
        animation.setEndValue(content.geometry().height() + 10)
        self.animator_.addAnimation(animation)
        if not self.isChecked():
            content.setMaximumHeight(0)

    def hideContent(self):
        self.animator_.setDirection(QAbstractAnimation.Backward)
        self.animator_.start()

    def showContent(self):
        self.animator_.setDirection(QAbstractAnimation.Forward)
        self.animator_.start()

    def on_toggled(self, checked):
        self.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        if checked and self.content_ is not None:
            self.showContent()
        else:
            self.hideContent()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.animator_ = QParallelAnimationGroup(self)


if __name__ == "__main__":
    app = QApplication([])
    window = CollapseButton()
    window.show()
    sys.exit(app.exec())
``
### D:\vs_projects\auto-exec-doc\examples\pil_in_multiproccesing.py
``python
from multiprocessing import Pool
from PIL import Image
from PIL import ExifTags
import os

def process_image(file_path):
    image = Image.open(file_path)

    # Получение EXIF данных
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if exif is not None:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == 'Orientation':
                    orientation = value
                    break
            
            # Корректировка ориентации
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)

    # Пример обработки: изменение размера
    image = image.resize((100, 100))
    
    # Сохранение обработанного изображения
    output_path = os.path.join('output', os.path.basename(file_path))
    image.save(output_path)

def main():
    # Получение списка файлов изображений
    image_folder = 'images'
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('JPG', 'JPEG', 'PNG'))]

    # Создание папки для сохранения обработанных изображений, если она не существует
    os.makedirs('output', exist_ok=True)

    # Использование Pool для обработки изображений
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_image, image_files)

if __name__ == '__main__':
    main()

``
### D:\vs_projects\auto-exec-doc\examples\qtree-черноввик.py
``python
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QTreeWidget, QTreeWidgetItem, QMessageBox
)

class TreeEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tree Editor")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout(self)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Items"])
        self.layout.addWidget(self.tree_widget)

        self.add_group_button = QPushButton("Добавить группу", self)
        self.add_group_button.clicked.connect(self.add_group)
        self.layout.addWidget(self.add_group_button)

        self.add_item_button = QPushButton("Добавить элемент", self)
        self.add_item_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_item_button)

        self.remove_button = QPushButton("Удалить", self)
        self.remove_button.clicked.connect(self.remove_item)
        self.layout.addWidget(self.remove_button)

        self.move_up_button = QPushButton("Переместить вверх", self)
        self.move_up_button.clicked.connect(self.move_up)
        self.layout.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("Переместить вниз", self)
        self.move_down_button.clicked.connect(self.move_down)
        self.layout.addWidget(self.move_down_button)

    def add_group(self):
        name = f"Группа {self.tree_widget.topLevelItemCount() + 1}"
        QTreeWidgetItem(self.tree_widget, [name])

    def add_item(self):
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите группу.")
            return
        name = f"Элемент {current_item.childCount() + 1}"
        QTreeWidgetItem(current_item, [name])

    def remove_item(self):
        current_item = self.tree_widget.currentItem()
        if current_item:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            if index != -1:  # Удаление группы
                self.tree_widget.takeTopLevelItem(index)
            else:  # Удаление элемента
                parent_item = current_item.parent()
                if parent_item:
                    parent_item.removeChild(current_item)
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите элемент или группу.")

    def move_up(self):
        current_item = self.tree_widget.currentItem()
        if current_item:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            if index > 0:  # Перемещение группы вверх
                self.tree_widget.insertTopLevelItem(index - 1, self.tree_widget.takeTopLevelItem(index))
            else:  
                parent_item = current_item.parent()
                if parent_item:
                    parent_index = parent_item.indexOfChild(current_item)
                    if parent_index > 0:
                        parent_item.insertChild(parent_index - 1, parent_item.takeChild(parent_index))

    def move_down(self):
        current_item = self.tree_widget.currentItem()
        if current_item:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            if index < self.tree_widget.topLevelItemCount() - 1:  # Перемещение группы вниз
                self.tree_widget.insertTopLevelItem(index + 1, self.tree_widget.takeTopLevelItem(index))
            else:  
                parent_item = current_item.parent()
                if parent_item:
                    parent_index = parent_item.indexOfChild(current_item)
                    if parent_index < parent_item.childCount() - 1:
                        parent_item.insertChild(parent_index + 1, parent_item.takeChild(parent_index))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TreeEditor()
    editor.show()
    sys.exit(app.exec())

``
### D:\vs_projects\auto-exec-doc\examples\scrolltop.py
``python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QScrollArea, QVBoxLayout, QWidget, QPushButton

app = QApplication([])

# Create a QScrollArea
scroll_area = QScrollArea()

# Create a QWidget to put in the scroll area
widget = QWidget()

# Create a QVBoxLayout for the widget
layout = QVBoxLayout(widget)

# Add some widgets to the layout
layout.addWidget(QPushButton("Button 1"))
layout.addWidget(QPushButton("Button 2"))
layout.addWidget(QPushButton("Button 3"))

# Set the widget of the QScrollArea
scroll_area.setWidget(widget)

# Set the alignment of the QScrollArea
#scroll_area.setAlignment(Qt.AlignTop)

# Show the QScrollArea
scroll_area.show()

app.exec()
``
### D:\vs_projects\auto-exec-doc\examples\search_jinja.py
``python
import re
from docx import Document

def find_jinja_tags(docx_path):
    # Загружаем документ
    doc = Document(docx_path)
    jinja_tags = []
    # Регулярное выражение для поиска тегов Jinja
    jinja_pattern = re.compile(r'\{\{.*?\}\}|\{%.*?%\}')

    # Функция для поиска тегов в текстах
    def search_tags_in_texts(texts):
        for text in texts:
            matches = jinja_pattern.findall(text)
            jinja_tags.extend(matches)

    # Ищем теги в параграфах
    search_tags_in_texts(paragraph.text for paragraph in doc.paragraphs)
    
    # Ищем теги в колонтитулах
    for section in doc.sections:
        search_tags_in_texts(paragraph.text for paragraph in section.header.paragraphs)  # В верхнем колонтитуле
        search_tags_in_texts(paragraph.text for paragraph in section.footer.paragraphs)  # В нижнем колонтитуле

    # Ищем теги в фигурных элементах документа
    for shape in doc.inline_shapes:
        if shape.type == 1:  # Проверка на тип "текстовое поле" (1 соответствует текстовым полям)
            search_tags_in_texts([shape.text])

    return set(jinja_tags)

# Пример использования
docx_file = 'C:/Users/hayar/Documents/AutoExecDoc Projects/gdgffdg/forms/10.docx'
tags = find_jinja_tags(docx_file)
print("Найденные Jinja теги:")
for tag in tags:
    print(tag)

``
### D:\vs_projects\auto-exec-doc\examples\spoiler_with_button.py
``python
from PySide6.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spoiler Widget")

        # Create the spoiler group box
        self.spoiler_group_box = QGroupBox("Click to reveal content")
        layout = QVBoxLayout()
        self.spoiler_group_box.setLayout(layout)

        # Create a label to hold the content
        self.content_label = QLabel("This is the spoiler content.")
        layout.addWidget(self.content_label)

        # Create a button to toggle the visibility of the content
        self.toggle_button = QPushButton("Show/Hide")
        self.toggle_button.clicked.connect(self.toggle_tag)
        layout.addWidget(self.toggle_button)

        # Hide the content initially
        self.content_label.hide()

        # Set the central widget
        self.setCentralWidget(self.spoiler_group_box)

    def toggle_tag(self):
        if self.content_label.isVisible():
            self.content_label.hide()
            self.toggle_button.setText("Show")
        else:
            self.content_label.show()
            self.toggle_button.setText("Hide")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

``
### D:\vs_projects\auto-exec-doc\examples\sql_table_dict_tree.py
``python
import sqlite3


def dfs(id_parent_node):
    childs = get_childs(id_parent_node)
    if childs:
        for child in childs:
            print(child)
            dfs(child[0])


def DFGH():
    conn = sqlite3.connect("example.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM Project_structure_of_nodes;
    """)
    
    return [dict(row) for row in cursor.fetchall()]


def get_childs(id_parent_node):
    conn = sqlite3.connect("example.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = """
    SELECT id_node FROM Project_structure_of_nodes
    WHERE id_parent = ?
    """
    cursor.execute(sql, [id_parent_node])
    result = cursor.fetchall()
    conn.close()
    return result


def main():
    #dfs(get_project_node())
    print(DFGH())


main()


#
'''
conn.row_factory = sqlite3.Row
result = [dict(row) for row in cursor.fetchall()]
'''
``
### D:\vs_projects\auto-exec-doc\examples\tableeditor.py
``python
from PySide6.QtWidgets import (
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QInputDialog,
)

class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        self.add_button = QPushButton("Add Row")
        self.delete_button = QPushButton("Delete Row")
        #self.edit_button = QPushButton("Edit Cell")
        self.to_json_button = QPushButton("to_json_button")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        hbox = QHBoxLayout()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.delete_button)
        #hbox.addWidget(self.edit_button)
        hbox.addWidget(self.to_json_button)
        self.layout.addLayout(hbox)
        self.setLayout(self.layout)
        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)
        #self.edit_button.clicked.connect(self.edit_cell)
        self.table.cellChanged.connect(self.update_cell)
        self.to_json_button.clicked.connect(self.to_json)

    def add_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        for column in range(self.table.columnCount()):
            item = QTableWidgetItem()
            self.table.setItem(row_count, column, item)

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    # def edit_cell(self):
    #     current_row = self.table.currentRow()
    #     current_column = self.table.currentColumn()
    #     if current_row >= 0 and current_column >= 0:
    #         item = self.table.item(current_row, current_column)
    #         if item:
    #             text, ok = QInputDialog.getText(
    #                 self, "Edit Cell", "Enter new value:", QLineEdit.Normal, item.text()
    #             )
    #             if ok and text != "":
    #                 item.setText(text)

    def update_cell(self, row, column):
        item = self.table.item(row, column)
        if item:
            print(f"Cell ({row}, {column}) changed to {item.text()}")

    def to_json(self):
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        print(f"data = {data}")

    

if __name__ == "__main__":
    app = QApplication([])
    table_editor = TableEditor()
    table_editor.show()
    app.exec()

``
### D:\vs_projects\auto-exec-doc\examples\table_dict_tree.py
``python
nodes = [
    
    (0, "Проект", None, "PROJECT", None, None, ""),
    (1204, "ПТ-4", 12, "FORM", 1203, 1205, "main"),
    (1205, "ПТ-5", 12, "FORM", 1204, 1206, "main"),
    (1206, "ПТ-6", 12, "FORM", 1205, 1207, "main"),
    (1207, "ПТ-7", 12, "FORM", 1206, 1208, "main"),
    (1208, "ПТ-8", 12, "FORM", 1207, 1209, "main"),
    (12, "Паспорт трассы", 0, "GROUP", 11, None, None),
    (1201, "ПТ-1", 12, "FORM", None, 1202, "main"),
    (1202, "ПТ-2", 12, "FORM", 1201, 1203, "main"),
    (1203, "ПТ-3", 12, "FORM", 1202, 1204, "main"),
    (1205, "ПТ-5", 12, "FORM", 1204, 1206, "main"),
    (1206, "ПТ-6", 12, "FORM", 1205, 1207, "main"),
    (1207, "ПТ-7", 12, "FORM", 1206, 1208, "main"),
    (1209, "ПТ-9", 12, "FORM", 1208, 1210, "main"),
    (1210, "ПТ-10", 12, "FORM", 1209, 1211, "main"),
    (10, "Титульный лист", 0, "FORM", None, 11, "main"),
    (11, "Реестр документации", 0, "FORM", 10, 12, "main"),    
    (1204, "ПТ-4", 12, "FORM", 1203, 1205, "main"),
    (1208, "ПТ-8", 12, "FORM", 1207, 1209, "main"),
    (1209, "ПТ-9", 12, "FORM", 1208, 1210, "main"),
    (1210, "ПТ-10", 12, "FORM", 1209, 1211, "main"),
]
# "id_node": elem[0],
# "name_node": elem[1],
# "id_parent": elem[2],
# "type_node": elem[3],
# "id_left": elem[4],
# "id_right": elem[5],
# "template_name": elem[6],

def traversal(parent_node):
    print(parent_node)
    childs = list(filter(lambda node: node[2] == parent_node[0], nodes))
    #print(parent_node, childs)
    if childs:
        node = get_left_child(childs)
        while id_right_node(node):
            traversal(node)
            node = nodes[]
    return None


def get_left_child(childs):
    left_child = None
    for child in childs:
        if not child[4]:
            left_child = child
            return left_child

def id_right_node(node):
    return node[5]




traversal(nodes[0])
``
### D:\vs_projects\auto-exec-doc\examples\дерево перетаскивания.py
``python
import sys
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.InternalMove)

        for i in range(3):
            parent = QTreeWidgetItem(self, [f'Parent {i}'])
            for j in range(3):
                QTreeWidgetItem(parent, [f'Child {i}-{j}'])

        self.setHeaderLabels(['Tree'])

    def dropEvent(self, event):
        super().dropEvent(event)
        item = self.itemAt(event.position().toPoint())
        if item:
            print(f'Item dropped: {item.text(0)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = TreeWidget()
    tree.show()
    sys.exit(app.exec())

``
### D:\vs_projects\auto-exec-doc\examples\очередь.py
``python
import sys
import multiprocessing
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QAction

def worker():
    import time
    time.sleep(5)
    return "Работа завершена"

def start_worker(result_queue):
    result = worker()
    result_queue.put(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Пример PySide6 и Multiprocessing")
        self.setGeometry(100, 100, 300, 200)
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        action = QAction("Запустить процесс", self)
        action.triggered.connect(self.run_process)
        file_menu.addAction(action)
        
    def run_process(self):
        self.result_queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=start_worker, args=(self.result_queue,))
        self.process.start()
        self.process.join()  # Ждать, пока процесс завершится
        # Получить результат
        result = self.result_queue.get()
        self.show_message(result)

    def show_message(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

``
### D:\vs_projects\auto-exec-doc\package\app.py
``python
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

import package.components.mainwindow as mainwindow

import package.controllers.icons as icons

# Импорт всех miodules
import package.modules.converter as converter
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.filefoldermanager as filefoldermanager
import package.modules.log as log
import package.modules.project as project
import package.modules.projectdatabase as projectdatabase
import package.modules.sectionsinfo as sectionsinfo
# import package.modules.settingsdatabase as settingsdatabase
import package.modules.settingsmanager as settingsmanager
import package.modules.officepackets as officepackets
import package.modules.imageresizer as imageresizer

import package.common as common
import package.commonwithosbm as commonwithosbm

# Импорт всех controllers
import package.controllers.lwpagestemplate as lwpagestemplate
import package.controllers.pdfview as pdfview
import package.controllers.tabwinputforms as tabwinputforms
import package.controllers.statusbar as statusbar
import package.controllers.twstructureexecdoc as twstructureexecdoc
import package.controllers.comboxtemplates as comboxtemplates

# Импорт всех components
import package.controllers.style as style
import package.components.dialogwindow.dialogwindows as dialogwindows

class ObjectsManager:
    """
    Мененджер объектов.
    """
    def __init__(self):
        # modules
        self.obj_conv = None
        self.obj_dirm = None
        self.obj_film = None
        self.obj_logg = None
        self.obj_proj = None
        self.obj_prodb = None
        self.obj_seci = None
        self.obj_settings = None
        self.obj_offp = None
        self.obj_imgr = None
        # controllers
        self.obj_lwpt = None
        self.obj_pdfv = None
        self.obj_tabwif = None
        self.obj_stab = None
        self.obj_twsed = None
        self.obj_comt = None
        # components (windows)
        self.obj_style = None
        self.obj_dw = None
        self.obj_mw = None
        self.obj_nedtdw = None
        self.obj_nedndw = None
        self.obj_variablesldw = None
        self.obj_nedw = None
        self.obj_convsdw = None
        self.obj_templdw = None
        self.obj_nedtempdw = None
        self.obj_nedpagedw = None
        self.obj_nedrowcoldw = None
        self.obj_formtabledw = None
        self.obj_formlistdw = None
        self.obj_setdw = None
        
        # общее
        self.obj_com = None
        self.obj_comwith = None

    def initialize_all(self):
        """
        Инициализация всех объектов, кроме MainWindow.
        """
        self.initialize_modules()
        self.initialize_controllers()
        self.initialize_components()
        self.obj_com = common.Common()
        self.obj_comwith = commonwithosbm.CommonWithOsmb()
        
    def initialize_modules(self):
        self.obj_logg = log.Log()
        self.obj_conv = converter.Converter()
        self.obj_dirm = dirpathsmanager.DirPathManager()
        self.obj_film = filefoldermanager.FileFolderManager()        
        self.obj_proj = project.Project()
        self.obj_prodb = projectdatabase.ProjectDatabase()
        self.obj_seci = sectionsinfo.SectionsInfo()
        self.obj_settings = settingsmanager.SettingsManager()
        self.obj_offp = officepackets.OfficePackets()        
        self.obj_imgr = imageresizer.ImageResizer()

    def initialize_controllers(self):
        self.obj_lwpt = lwpagestemplate.LWPagesTemplate()
        self.obj_pdfv = pdfview.PdfView()
        self.obj_tabwif = tabwinputforms.TabWInputForms()
        self.obj_stab = statusbar.StatusBar()
        self.obj_twsed = twstructureexecdoc.TWStructureExecDoc()
        self.obj_icons = icons.Icons()
        self.obj_comt = comboxtemplates.ComboxTemplates()

    def initialize_components(self):
        self.obj_style = style.Style()
        self.obj_dw = dialogwindows.DialogWindows()

class App:
    def __init__(self, current_directory):
        self.current_directory = current_directory
        self.check_before_run()
        self.start_app()

    def setting_osbm(self):
        self.setting_osbm_for_modules()
        self.setting_osbm_for_controllers()
        self.setting_osbm_for_components()
        self.osbm.obj_comwith.setting_all_osbm(self.osbm)

    def setting_osbm_for_modules(self):
        self.osbm.obj_conv.setting_osbm(self.osbm)
        self.osbm.obj_dirm.setting_osbm(self.osbm)
        self.osbm.obj_film.setting_osbm(self.osbm)
        self.osbm.obj_logg.setting_osbm(self.osbm)
        self.osbm.obj_proj.setting_all_osbm(self.osbm)
        self.osbm.obj_prodb.setting_osbm(self.osbm)
        self.osbm.obj_seci.setting_osbm(self.osbm)
        self.osbm.obj_settings.setting_osbm(self.osbm)
        self.osbm.obj_offp.setting_all_osbm(self.osbm)
        self.osbm.obj_imgr.setting_osbm(self.osbm)

    def setting_osbm_for_controllers(self):    
        self.osbm.obj_lwpt.setting_all_osbm(self.osbm)
        self.osbm.obj_pdfv.setting_all_osbm(self.osbm)
        self.osbm.obj_tabwif.setting_all_osbm(self.osbm)
        self.osbm.obj_stab.setting_all_osbm(self.osbm)
        self.osbm.obj_twsed.setting_all_osbm(self.osbm)
        self.osbm.obj_icons.setting_all_osbm(self.osbm)
        self.osbm.obj_comt.setting_all_osbm(self.osbm)

    def setting_osbm_for_components(self):
        self.osbm.obj_dw.setting_all_osbm(self.osbm)

    def check_before_run(self):
        """
        Проверить и наcтроить до запуска.
        """
        # настройка хранилища экземпляров модулей
        self.osbm = ObjectsManager()
        self.osbm.initialize_all()
        self.setting_osbm()
        # настройка путей
        self.osbm.obj_dirm.setting_paths(
            self.current_directory
        )
        # настроить loggerpy
        self.osbm.obj_logg.setting_logger()
        self.osbm.obj_logg.debug_logger(f"self.current_directory = {self.current_directory}")
        # Проверка наличия папок.
        self.osbm.obj_film.create_and_setting_files_and_folders()
        # настроить БД
        self.osbm.obj_settings.initialize_default_settings()
        # настройка officepackets
        self.osbm.obj_offp.resetting_office_packets()

    def start_app(self):
        """
        Запуск фронта.
        """
        try:
            self.app = QApplication(sys.argv)
            # настройка шрифтов
            self.__font_main = QFontDatabase.addApplicationFont(":/fonts/resources/fonts/OpenSans-VariableFont_wdth,wght.ttf")
            self.__font_italic = QFontDatabase.addApplicationFont(":/fonts/resources/fonts/OpenSans-Italic-VariableFont_wdth,wght.ttf")
            # Получаем название шрифта
            try:
                font_families = QFontDatabase.applicationFontFamilies(self.__font_main)
                if font_families:
                    self.__size_font = 10
                    self.__custom_font = QFont(font_families[0], self.__size_font)
                    self.app.setFont(self.__custom_font) 
            except Exception as e:
                self.osbm.obj_logg.error_logger(f"Error: {e}")
            # создание окна
            self.window = mainwindow.MainWindow(self.osbm)
            # подключение MainWindow к osbm
            self.osbm.obj_mw = self.window
            self.window.show()
            # sys.exit(self.app.exec())
            self.app.exec_()
        except Exception as e:
            self.osbm.obj_logg.error_logger(f"Error: {e}")

    

``
### D:\vs_projects\auto-exec-doc\package\common.py
``python
# Ошибки
class Errors:
    class MsWordError(Exception):
        pass

    class LibreOfficeError(Exception):
        pass

    def __init__(self):
        self.MsWordError = Errors.MsWordError
        self.LibreOfficeError = Errors.LibreOfficeError

# class DefaultValue:

#     def __init__(self):
#         self.default_value = None


class Common:
    def __init__(self):
        self.errors = Errors()
        self.default_value = None


``
### D:\vs_projects\auto-exec-doc\package\commonwithosbm.py
``python
from PySide6.QtWidgets import QSizePolicy


class VariableType:
    def __init__(self, index, name, data, icon, is_block):
        self.index = index
        self.name = name
        self.data = data
        self.icon = icon
        self.is_block = is_block


class VariableTypes:
    def __init__(self, osbm, icons):
        self.__osbm = osbm
        self.__icons = icons
        self.__variable_types = [
            VariableType(0, "Текст", "TEXT", self.__icons.get("text"), False),
            VariableType(
                1, "Длинный текст", "LONGTEXT", self.__icons.get("longtext"), False
            ),
            VariableType(2, "Дата", "DATE", self.__icons.get("date"), False),
            VariableType(3, "Таблица", "TABLE", self.__icons.get("table-columns"), True),
            VariableType(4, "Список", "LIST", self.__icons.get("list"), True),
            VariableType(5, "Изображение", "IMAGE", self.__icons.get("image"), False),
        ]
    
    def get_icon_by_type_variable(self, type_variable):
        result = None
        for variable in self.__variable_types:
            if variable.data == type_variable:
                result = variable.icon
                break
        # self.__osbm.obj_logg.debug_logger(f"VariableTypes get_icon_by_type_variable(type_variable):\ntype_variable = {type_variable}\n result = {result}")
        return result

    def get_variable_types(self):
        self.__osbm.obj_logg.debug_logger("VariableTypes get_variable_types()")
        return self.__variable_types

    def get_data_by_index(self, index):
        result = None
        for variable in self.__variable_types:
            if variable.index == index:
                result = variable.data
                break
        self.__osbm.obj_logg.debug_logger(
            f"VariableTypes get_data_by_index(index):\nindex = {index}\n result = {result}"
        )
        return result

    def get_index_by_data(self, data):
        result = None
        for variable in self.__variable_types:
            if variable.data == data:
                result = variable.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"VariableTypes get_index_by_data(data):\ntype_variable = {data}\n result = {result}"
        )
        return result


#
#
#


class Unit:
    def __init__(self, index, name, data):
        self.index = index
        self.name = name
        self.data = data


class Units:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__units = [
            Unit(0, "Миллиметр (Millimeter)", "MM"),
            Unit(1, "Сантиметр (Centimeter)", "CM"),
            Unit(2, "Дюйм (Inch)", "INCH"),
            Unit(3, "Пункт (Point)", "PT"),
        ]

    def get_units(self):
        self.__osbm.obj_logg.debug_logger("Units get_units()")
        return self.__units

    def get_index_unit_by_data(self, data):
        result = 0
        for unit in self.__units:
            if unit.data == data:
                result = unit.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"Units get_index_unit_by_data(data):\ndata_unit = {data}\n result = {result}"
        )
        return result


#
#
#


class SizingMode:
    def __init__(self, index, name, data, is_wh):
        self.index = index
        self.name = name
        self.data = data
        self.is_wh = is_wh


class SizingModes:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__sizing_modes = [
            SizingMode(0, "Без изменений", "NOCHANGES", False),
            SizingMode(1, "Вместить без изменения пропорций", "CONTAIN", True),
            SizingMode(2, "Заполнить без изменения пропорций", "COVER", True),
            SizingMode(3, "Растянуть с изменением пропорций", "FILL", True),
        ]

    def get_sizing_modes(self):
        self.__osbm.obj_logg.debug_logger("SizingModes get_sizing_modes()")
        return self.__sizing_modes

    def get_index_sizing_mode_by_data(self, data):
        result = 0
        for sizing_mode in self.__sizing_modes:
            if sizing_mode.data == data:
                result = sizing_mode.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"SizingModes get_index_sizing_mode_by_data(data):\ndata_sizing_mode = {data}\n result = {result}"
        )
        return result

    def get_is_wh_by_index(self, index):
        sizing_mode = self.__sizing_modes[index]
        result = sizing_mode.is_wh
        self.__osbm.obj_logg.debug_logger(
            f"SizingModes get_is_wh_by_index(index):\nindex = {index}\n result = {result}"
        )
        return result


#
#
#


class TableType:
    def __init__(self, index, name, data, icon, is_edit_rowcols):
        self.index = index
        self.name = name
        self.data = data
        self.icon = icon
        self.is_edit_rowcols = is_edit_rowcols


class TableTypes:
    def __init__(self, osbm, icons):
        self.__osbm = osbm
        self.__icons = icons
        self.__table_types = [
            # TableType(0, "Произвольный", "FULL", False),
            TableType(0, "Настройка столбцов таблицы", "COL", self.__icons.get("table-columns"), True),
            TableType(1, "Настройка строк таблицы", "ROW", self.__icons.get("table-rows"), True),
        ]
        self.__text_btns = {
            # "0": ("Строки/Столбцы", "Добавить строку/столбец"),
            "0": ("Столбцы", "Добавить столбец"),
            "1": ("Строки", "Добавить строку"),
        }

    def get_table_types(self):
        self.__osbm.obj_logg.debug_logger("TableTypes get_table_types()")
        return self.__table_types

    def get_is_edit_rowcols_by_index(self, index):
        table_type = self.__table_types[index]
        result = table_type.is_edit_rowcols
        self.__osbm.obj_logg.debug_logger(
            f"TableTypes get_is_edit_rowcols_by_index(index):\nindex = {index}\n result = {result}"
        )
        return result

    def get_text_btns_by_index(self, index):
        result = 0
        for key, value in self.__text_btns.items():
            if int(key) == index:
                result = value
                break
        self.__osbm.obj_logg.debug_logger(
            f"TableTypes get_text_btns_by_data(data):\index = {index}\n result = {result}"
        )
        return result

    def get_index_by_data(self, data):
        result = 0
        for table_type in self.__table_types:
            if table_type.data == data:
                result = table_type.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"TableTypes get_index_by_data(data):\ndata = {data}\n result = {result}"
        )
        return result


#
#
#


class PageType:
    def __init__(self, index, name, data, icon):
        self.index = index
        self.name = name
        self.data = data
        self.icon = icon


class PageTypes:
    def __init__(self, osbm, icons):
        self.__osbm = osbm
        self.__icons = icons
        self.__page_types = [
            PageType(0, "Файл DOCX", "DOCX", self.__icons.get("page")),
            PageType(1, "Файл PDF", "PDF", self.__icons.get("pdf")),
        ]

    def get_page_types(self):
        self.__osbm.obj_logg.debug_logger("PageTypes get_page_types()")
        return self.__page_types

    def get_index_by_data(self, data):
        result = 0
        for page_type in self.__page_types:
            if page_type.data == data:
                result = page_type.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"PageTypes get_index_by_data(data):\ndata = {data}\n result = {result}"
        )
        return result


#
#
#


class language:
    def __init__(self, index, name, data, emoji):
        self.index = index
        self.name = name
        self.data = data
        self.emoji = emoji


class Languages:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__languages = [
            language(0, "Русский", "ru_RU", "🇷🇺"),
            language(1, "English", "en_US", "🇬🇧"),  # ,
            # language(2, "Chinese", "zh_CN", "🇨🇳"),
            # language(3, "French", "fr_FR", "🇫🇷"),
            # language(4, "German", "de_DE", "🇩🇪"),
            # language(5, "Spanish", "es_ES", "🇪🇸"),
            # language(6, "Portuguese", "pt_BR", "🇵🇹"),
            # language(7, "Italian", "it_IT", "🇮🇹"),
            # language(8, "Japanese", "ja_JP", "🇯🇵"),
            # language(9, "Korean", "ko_KR", "🇰🇷"),
        ]

    def get_languages(self):
        self.__osbm.obj_logg.debug_logger("Languages get_languages()")
        return self.__languages


#
#
#


class ResizeQt:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("ResizeQt __init__(osbm)")

    def set_temp_max_height(self, widget):
        width = widget.width()
        widget.setMaximumSize(width, 5000)
        widget.setMinimumWidth(width)
        widget.adjustSize()
        widget.setMaximumSize(5000, widget.height())
        self.__osbm.obj_logg.debug_logger("ResizeQt set_resize(widget)")


class CommonWithOsmb:
    def __init__(self):
        self.__osbm = None
        self.__icons = None
        #
        self.variable_types = None
        self.sizing_modes = None
        self.units = None
        self.table_types = None
        self.page_types = None
        self.languages = None
        self.resizeqt = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("CommonWithOsmb setting_all_osbm()")

    def run(self):
        self.__osbm.obj_logg.debug_logger("CommonWithOsmb run()")
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        #
        self.variable_types = VariableTypes(self.__osbm, self.__icons)
        self.sizing_modes = SizingModes(self.__osbm)
        self.units = Units(self.__osbm)
        self.table_types = TableTypes(self.__osbm, self.__icons)
        self.page_types = PageTypes(self.__osbm, self.__icons)
        self.languages = Languages(self.__osbm)
        self.resizeqt = ResizeQt(self.__osbm)

``
### D:\vs_projects\auto-exec-doc\package\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\components\mainwindow.py
``python
from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QShortcut, QKeySequence, QAction, Qt
from PySide6.QtCore import QTimer

import package.ui.mainwindow_ui as mainwindow_ui

import package.components.dialogwindow.variableslistdialogwindow as variableslistdialogwindow
import package.components.dialogwindow.nodeseditordialogwindow as nodeseditordialogwindow
import package.components.dialogwindow.templateslistsialogwindow as templateslistsialogwindow
import package.components.dialogwindow.settingsdialogwindow as settingsdialogwindow

import os
from functools import partial


class MainWindow(QMainWindow):
    def __init__(self, osbm):
        self.__osbm = osbm
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        # config
        self.config()
        # настройка контроллеров
        self.config_controllers()
        # Подключаем действия
        self.connecting_actions()
        # Запускаем Common после инициализации QGuiApplication + dialogWindows
        self.__osbm.obj_comwith.run()
        self.__osbm.obj_dw.run()

    def config(self):
        self.__osbm.obj_logg.debug_logger("MainWindow config()")
        self.ui.centralwidget_splitter.setSizes([280, 460, 626])
        self.start_qt_actions()
        self.update_menu_recent_projects()

    def config_controllers(self):
        """
        Method to configure controllers.
        """
        self.__osbm.obj_logg.debug_logger("MainWindow config_controllers()")
        # настройка статус бара
        self.__osbm.obj_stab.connect_statusbar(self.ui.status_bar)
        # настройка structureexecdoc
        self.__osbm.obj_twsed.connect_structureexecdoc(
            self.ui.treewidget_structure_execdoc
        )
        # настройка pagestemplate
        self.__osbm.obj_lwpt.connect_pages_template(self.ui.lw_pages_template)
        # настройка comboboxtemplates
        self.__osbm.obj_comt.connect_combox_templates(self.ui.combox_templates)
        # настройка inputforms
        self.__osbm.obj_tabwif.connect_inputforms(self.ui.tabw_inputforms)
        # ПОДКЛЮЧИТЬ PDF
        self.__osbm.obj_pdfv.connect_pdfview(self.ui.widget_pdf_view)

        # окно по правой кнопки мыши (ui.treewidget_structure_execdoc)
        self.ui.treewidget_structure_execdoc.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treewidget_structure_execdoc.customContextMenuRequested.connect(
            self.context_menu_node
        )
        # окно по правой кнопки мыши (ui.combox_templates)
        self.ui.combox_templates.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.combox_templates.customContextMenuRequested.connect(
            self.context_menu_template
        )
        # окно по правой кнопки мыши (ui.lw_pages_template)
        self.ui.lw_pages_template.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.lw_pages_template.customContextMenuRequested.connect(
            self.context_menu_page
        )

    def context_menu_node(self, pos):
        current_widget = self.ui.treewidget_structure_execdoc
        current_item = current_widget.currentItem()
        if current_item:
            self.general_nenu(current_widget, pos, "NODE")

    def context_menu_template(self, pos):
        current_widget = self.ui.combox_templates
        index = current_widget.currentIndex()
        if index != -1:
            self.general_nenu(current_widget, pos, "TEMPLATE")

    def context_menu_page(self, pos):
        current_widget = self.ui.lw_pages_template
        current_item = current_widget.currentItem()
        if current_item:
            self.general_nenu(current_widget, pos, "PAGE")

    def general_nenu(self, current_widget, pos, type_item):
        menu = QMenu(current_widget)
        # action_edit_composition ТОЛЬКО для NODE
        if type_item == "NODE":
            action_edit_composition = QAction(
                "Изменить в редакторе состава ИД", current_widget
            )
            action_edit_composition.setIcon(self.__icons.get("edit_composition"))
            action_edit_composition.triggered.connect(
                partial(self.edit_menu_item, "COMPOSITION", type_item)
            )
            menu.addAction(action_edit_composition)
        # action_edit_templates для всех
        action_edit_templates = QAction("Изменить в редакторе шаблонов", current_widget)
        action_edit_templates.setIcon(self.__icons.get("edit_templates"))
        action_edit_templates.triggered.connect(
            partial(self.edit_menu_item, "TEMPLATE", type_item)
        )
        menu.addAction(action_edit_templates)
        # action_edit_variables для всех
        action_edit_variables = QAction(
            "Изменить в редакторе переменных", current_widget
        )
        action_edit_variables.setIcon(self.__icons.get("edit_variables"))
        action_edit_variables.triggered.connect(
            partial(self.edit_menu_item, "VARIABLE", type_item)
        )
        menu.addAction(action_edit_variables)
        #
        menu.exec(current_widget.mapToGlobal(pos))

    def edit_menu_item(
        self, type_edit, type_item, edit_variable=None, type_section=None
    ):
        item_node = self.ui.treewidget_structure_execdoc.currentItem()
        open_node = item_node.data(0, Qt.UserRole) if item_node else None
        #
        index_template = self.ui.combox_templates.currentIndex()
        open_template = (
            self.ui.combox_templates.itemData(index_template)
            if index_template != -1
            else None
        )
        #
        item_page = self.ui.lw_pages_template.currentItem()
        open_page = item_page.data(Qt.UserRole) if item_page else None
        #
        if type_edit == "VARIABLE":
            if type_item == "NODE":
                self.edit_variables(open_node)
            elif type_item == "TEMPLATE":
                self.edit_variables(open_node, open_template)
            elif type_item == "PAGE":
                self.edit_variables(open_node, open_template, open_page)
            elif type_item == "EDIT":
                # для TabWInputForms
                if type_section == "project":
                    self.edit_variables(None, None, None, edit_variable)
                elif type_section == "group":
                    self.edit_variables(open_node, None, None, edit_variable)
                elif type_section == "template":
                    self.edit_variables(open_node, open_template, None, edit_variable)
                elif type_section == "page":
                    self.edit_variables(
                        open_node, open_template, open_page, edit_variable
                    )

        elif type_edit == "TEMPLATE":
            if type_item == "NODE":
                self.edit_templates(open_node)
            elif type_item == "TEMPLATE":
                self.edit_templates(open_node, open_template)
            elif type_item == "PAGE":
                self.edit_templates(open_node, open_template, open_page)
        elif type_edit == "COMPOSITION":
            # только для NODE
            if type_item == "NODE":
                self.edit_structure_nodes(open_node)
        print(
            f"open_node = {open_node} \n open_template = {open_template} \n open_page = {open_page}"
        )

    def clear_before_end(self):
        self.__osbm.obj_logg.debug_logger("MainWindow ()")
        # удаление pdf из виджета pdfview
        self.__osbm.obj_pdfv.set_empty_pdf_view()
        # очистка временных файлов
        self.__osbm.obj_film.clear_temp_folder(True)
        # очистка word из памяти
        self.__osbm.obj_offp.terminate_msword()

    def closeEvent(self, event):
        self.clear_before_end()

    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        self.__osbm.obj_logg.debug_logger("MainWindow connecting_actions()")
        # QAction имеет шорткаты в Qt Designer
        self.ui.action_new.triggered.connect(lambda: self.__osbm.obj_proj.new_project())
        self.ui.action_open.triggered.connect(
            lambda: self.__osbm.obj_proj.open_project()
        )
        self.ui.action_save.triggered.connect(
            lambda: self.__osbm.obj_proj.save_project()
        )
        self.ui.action_saveas.triggered.connect(
            lambda: self.__osbm.obj_proj.saveas_project()
        )
        self.ui.action_export_to_pdf.triggered.connect(
            lambda: self.__osbm.obj_proj.export_to_pdf()
        )
        # self.ui.action_zoomin.triggered.connect(lambda: self.__osbm.obj_pdfv.zoom_in())
        # self.ui.action_zoomout.triggered.connect(
        #     lambda: self.__osbm.obj_pdfv.zoom_out()
        # )
        self.ui.action_zoomfitpage.triggered.connect(
            lambda checked: self.__osbm.obj_pdfv.set_zoom_to_fit_width()
            if checked
            else self.__osbm.obj_pdfv.set_zoom_custom()
        )
        self.ui.action_edit_variables.triggered.connect(lambda: self.edit_variables())
        self.ui.action_edit_templates.triggered.connect(lambda: self.edit_templates())
        self.ui.action_edit_composition.triggered.connect(
            lambda: self.edit_structure_nodes()
        )
        #
        self.ui.action_settings.triggered.connect(self.open_settings)
        self.ui.action_clear_trash.triggered.connect(lambda: self.clear_trash())
        #

    def start_qt_actions(self):
        self.ui.action_new.setEnabled(True)
        self.ui.action_open.setEnabled(True)
        self.ui.action_save.setEnabled(False)
        self.ui.action_saveas.setEnabled(False)
        self.ui.action_export_to_pdf.setEnabled(False)
        self.ui.action_edit_variables.setEnabled(False)
        self.ui.action_edit_composition.setEnabled(False)
        self.ui.action_edit_templates.setEnabled(False)
        self.ui.action_zoomfitpage.setEnabled(False)
        self.ui.action_clear_trash.setEnabled(False)

    def enable_qt_actions(self):
        """
        Активирует кнопки в статусбаре при открытии проекта
        """
        self.ui.action_save.setEnabled(True)
        self.ui.action_saveas.setEnabled(True)
        self.ui.action_edit_variables.setEnabled(True)
        self.ui.action_edit_composition.setEnabled(True)
        self.ui.action_zoomfitpage.setEnabled(True)
        self.ui.action_export_to_pdf.setEnabled(True)
        self.ui.action_edit_templates.setEnabled(True)
        self.ui.action_clear_trash.setEnabled(True)

    def edit_variables(
        self, open_node=None, open_template=None, open_page=None, edit_variable=None
    ):
        """Редактирование переменных."""
        self.__osbm.obj_logg.debug_logger("MainWindow edit_variables()")
        self.__osbm.obj_variablesldw = (
            variableslistdialogwindow.VariablesListDialogWindow(
                self.__osbm, open_node, open_template, open_page, edit_variable
            )
        )
        self.__osbm.obj_variablesldw.exec()
        self.update_main_window()

    def edit_templates(self, open_node=None, open_template=None, open_page=None):
        """Редактирование шаблонов."""
        self.__osbm.obj_logg.debug_logger("MainWindow edit_templates()")
        self.__osbm.obj_templdw = templateslistsialogwindow.TemplatesListDialogWindow(
            self.__osbm, open_node, open_template, open_page
        )
        self.__osbm.obj_templdw.exec()
        self.update_main_window()

    def edit_structure_nodes(self, open_node=None):
        """Редактирование структуры узлов."""
        self.__osbm.obj_logg.debug_logger("MainWindow edit_structure_nodes()")
        self.__osbm.obj_nedw = nodeseditordialogwindow.NodesEditorDialogWindow(
            self.__osbm, open_node
        )
        self.__osbm.obj_nedw.exec()
        self.update_main_window()

    def update_main_window(self):
        self.__osbm.obj_logg.debug_logger("MainWindow update_main_window()")
        # дерево
        self.__osbm.obj_twsed.update_structure_exec_doc()
        # combox_templates + lw_pages_template (внутри combox_templates)
        node = self.__osbm.obj_twsed.get_current_node()
        self.__osbm.obj_comt.update_combox_templates(node)
        # widget_pdf_view
        self.__osbm.obj_pdfv.set_empty_pdf_view()
        # scrollarea_inputforms
        page = self.__osbm.obj_lwpt.get_page_by_current_item()
        self.__osbm.obj_tabwif.update_tabs(page)

    def update_menu_recent_projects(self):
        self.__osbm.obj_logg.debug_logger("MainWindow update_menu_recent_projects()")
        self.ui.menu_recent_projects.clear()
        last_projects = self.__osbm.obj_settings.get_last_projects()
        for project in last_projects:
            name_project = project.get("name_project")
            action = self.ui.menu_recent_projects.addAction(name_project)
            action.setData(project)
            action.triggered.connect(partial(self.menu_recent_projects_action, action))

    def menu_recent_projects_action(self, item):
        self.__osbm.obj_logg.debug_logger(
            f"MainWindow menu_recent_projects_action(item):\nitem = {item}"
        )
        project = item.data()
        self.__osbm.obj_proj.open_recent_project(project)

    def open_settings(self):
        """Открыть диалог настроек"""
        self.__osbm.obj_logg.debug_logger("MainWindow open_settings()")
        self.__osbm.obj_setdw = settingsdialogwindow.SettingsDialogWindow(self.__osbm)
        self.__osbm.obj_setdw.exec()

    def clear_trash(self):
        self.__osbm.obj_logg.debug_logger("MainWindow clear_trash()")
        #
        self.__osbm.obj_dw.process_delete_trash_start()
        try:
            # временные файлы в проекте
            list_of_pages = self.__osbm.obj_prodb.get_all_pages()
            list_of_images = self.__osbm.obj_prodb.get_all_images()
            #
            list_of_docx_in_forms = (
                self.__osbm.obj_film.get_list_of_docx_in_forms_folder()
            )
            list_of_pdfs_in_pdfs = (
                self.__osbm.obj_film.get_list_of_pdfs_in_pdfs_folder()
            )
            list_of_images_in_images = (
                self.__osbm.obj_film.get_list_of_images_in_images_folder()
            )
            #
            active_docx_pages = dict()
            active_pdfs_pages = dict()
            active_images = dict()
            #
            for page in list_of_pages:
                filename_page = page.get("filename_page")
                typefile_page = page.get("typefile_page")
                if typefile_page == "DOCX":
                    active_docx_pages[filename_page] = True
                elif typefile_page == "PDF":
                    active_pdfs_pages[filename_page] = True
            #
            for image in list_of_images:
                value_pair = image.get("value_pair")
                active_images[value_pair] = True
            #
            for docx in list_of_docx_in_forms:
                filename_without_format = os.path.splitext(docx)[0]
                if not active_docx_pages.get(filename_without_format):
                    self.__osbm.obj_film.delete_page_from_project(
                        filename_without_format, "DOCX"
                    )
            #
            for pdf in list_of_pdfs_in_pdfs:
                filename_without_format = os.path.splitext(pdf)[0]
                if not active_pdfs_pages.get(filename_without_format):
                    self.__osbm.obj_film.delete_page_from_project(
                        filename_without_format, "PDF"
                    )
            #
            print(f"list_of_images = {list_of_images}")
            print(f"list_of_images_in_images = {list_of_images_in_images}")
            for image in list_of_images_in_images:
                if not active_images.get(image):
                    self.__osbm.obj_film.delete_image_from_project(image)

        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in clear_trash(): {e}")
        #
        self.__osbm.obj_dw.process_delete_trash_end()

    def config_combox_default(self):
        self.__osbm.obj_logg.debug_logger("MainWindow config_combox_default()")
        combobox = self.ui.combox_default
        combobox.blockSignals(True)
        combobox.clear()
        combobox.addItem("Пустое значение", "null")
        combobox.addItem("Переменная", "variable")
        combobox.blockSignals(False)
        combobox.currentIndexChanged.connect(self.combox_default_changed)
        combobox.setCurrentIndex(0)

    def combox_default_changed(self):
        self.__osbm.obj_logg.debug_logger("MainWindow combox_default_changed()")
        self.__osbm.obj_com.default_value = self.ui.combox_default.currentData()

``
### D:\vs_projects\auto-exec-doc\package\components\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\convertersettingsdialogwindow.py
``python
from PySide6.QtWidgets import (
    QDialog
)
from PySide6.QtCore import Qt

from functools import partial

import package.ui.convertersettingsdialogwindow_ui as convertersettingsdialogwindow_ui

class ConverterSettingsDialogWindow(QDialog):
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow __init__(osbm)")
        super(ConverterSettingsDialogWindow, self).__init__()
        self.ui = convertersettingsdialogwindow_ui.Ui_ConverterSettingsDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        # конфигурация
        self.config()
        # подключаем деействия
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def config(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow config()")
        # постоянный размер
        self.setFixedSize(self.sizeHint())
        app_converter = self.__osbm.obj_settings.get_app_converter()
        if app_converter == "MSWORD":
            self.ui.radbtn_msword.setChecked(True)
        # elif app_converter == "OPENOFFICE":
        #     self.ui.radbtn_openoffice.setChecked(True)
        elif app_converter == "LIBREOFFICE":
            self.ui.radbtn_libreoffice.setChecked(True)
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow connecting_actions()")
        self.ui.btn_close.clicked.connect(self.close_window)
        self.ui.btn_save.clicked.connect(self.save_converter)
        self.ui.btn_save.setShortcut("Ctrl+S")
        self.ui.btn_close.setShortcut("Ctrl+Q")


    def get_active_radiobutton(self) -> str:
        result = None
        if self.ui.radbtn_msword.isChecked():
            result = "MSWORD"
        # elif self.ui.radbtn_openoffice.isChecked():
        #     result = "OPENOFFICE"
        elif self.ui.radbtn_libreoffice.isChecked():
            result = "LIBREOFFICE"
        self.__osbm.obj_logg.debug_logger(f"ConverterSettingsDialogWindow get_active_radiobutton() -> str:\nresult = {result}")
        return result


    def save_converter(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow save()")
        result = self.get_active_radiobutton()
        if result:
            self.__osbm.obj_settings.set_app_converter(result)
            self.__osbm.obj_offp.resetting_office_packets()
            self.__osbm.obj_stab.set_message(f"{self.windowTitle()}: сохранение прошло успешно!")
        else:
            self.__osbm.obj_dw.error_message("Не выбран конвертер.")
        self.__osbm.obj_stab.update_name_app_converter()
        

    def close_window(self):
        self.__osbm.obj_logg.debug_logger("ConverterSettingsDialogWindow close_window()")
        self.close()

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\dialogwindows.py
``python
import os

from PySide6.QtWidgets import QMessageBox, QFileDialog, QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

class ProcessWindow(QWidget):
    def __init__(self, title, icon):
        super().__init__()
        self.__is_close = False
        self.setWindowTitle(title)
        self.setWindowIcon(icon)
        self.setFixedSize(300, 100)  # Минимальные размеры окна
        layout = QVBoxLayout()
        label = QLabel("Пожалуйста, подождите...")
        layout.addWidget(label)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Индикатор загрузки в бесконечном режиме
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def close_window(self):
        self.__is_close = True
        self.close()

    def closeEvent(self, event):
        if self.__is_close:
            event.accept()
        else:
            event.ignore() 


class DialogWindows:
    def __init__(self):
        self.__dw = None
        self.__miniw = None
        self.__icons = None
        #
        self.__formimage_dirpath = None
        self.__select_docxpdf_dirpath = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm

    def run(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows run()")
        self.__icons = self.__osbm.obj_icons.get_icons()     

    def get_new_prepare_dw(self) -> object:
        self.__osbm.obj_logg.debug_logger(
            "DialogWindows get_new_prepare_dw() -> object"
        )
        dw = QMessageBox()
        self.__osbm.obj_style.set_style_for(dw)
        dw.setWindowIcon(self.__icons.get("logo"))
        return dw

    def process_save_start(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_save_start()")
        self.__miniw = ProcessWindow("Идет процесс сохранения", self.__icons.get("logo"))
        self.__miniw.show()

    def process_save_end(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_save_end()")
        self.__miniw.close_window()

    def process_export_start(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_export_start()")
        self.__miniw = ProcessWindow("Идет процесс экспорта", self.__icons.get("logo"))
        self.__miniw.show()

    def process_export_end(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_export_end()")
        self.__miniw.close_window()

    def process_show_start(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_show_start()")
        self.__miniw = ProcessWindow("Идет процесс отображения", self.__icons.get("logo"))
        self.__miniw.show()
    
    def process_show_end(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_show_end()")
        self.__miniw.close_window()

    def process_delete_trash_start(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_delete_trash_start()")
        self.__miniw = ProcessWindow("Идет процесс удаления", self.__icons.get("logo"))
        self.__miniw.show()

    # todo Выбор изображения в форме

    def process_delete_trash_end(self):
        self.__osbm.obj_logg.debug_logger("DialogWindows process_delete_trash_end()")
        self.__miniw.close_window()

    def save_active_project(self) -> str:
        """Диалоговое окно 'Вы не сохранили текущий проект. Сохранить?'."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows save_active_project() -> str"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Сохранение текущего проекта")
        self.__dw.setText("Вы не сохранили текущий проект. Сохранить?")
        self.__dw.setIcon(QMessageBox.Warning)

        self.__dw.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        self.__dw.setButtonText(QMessageBox.Yes, "Да")
        self.__dw.setButtonText(QMessageBox.No, "Нет")

        return_value = self.__dw.exec()

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows save_active_project() -> return_value = {return_value}"
        )

        if return_value == QMessageBox.Yes:
            return "Yes"
        elif return_value == QMessageBox.No:
            return "No"
        elif return_value == QMessageBox.Cancel:
            return "Cancel"

    def select_empty_folder(self):
        """Диалоговое окно 'Пожалуйста, выберите пустую папку'."""

        self.__osbm.obj_logg.debug_logger("DialogWindows select_empty_folder()")

        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Ошибка")
        self.__dw.setText("Пожалуйста, выберите пустую папку.")
        self.__dw.setIcon(QMessageBox.Critical)

        self.__dw.exec()

    def select_folder_for_new_project(self) -> str:
        """Диалоговое окно выбора папки для нового проекта."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_folder_for_new_project() -> str"
        )

        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки для нового проекта",
                self.__osbm.obj_dirm.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                if not os.listdir(folder_path):
                    self.__osbm.obj_logg.debug_logger(
                        f"DialogWindows select_folder_for_new_project() -> {folder_path}"
                    )
                    return folder_path
                else:
                    self.select_empty_folder()
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_new_project() -> {None}"
                )
                return None

    def select_folder_for_saveas_project(self) -> str:
        """Диалоговое окно выбора папки для нового проекта."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_folder_for_new_project() -> str"
        )

        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки для сохранения проекта",
                self.__osbm.obj_dirm.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                if not os.listdir(folder_path):
                    self.__osbm.obj_logg.debug_logger(
                        f"select_folder_for_new_project() -> {folder_path}"
                    )
                    return folder_path
                else:
                    self.select_empty_folder()
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_new_project() -> {None}"
                )
                return None

    def select_folder_for_open_project(self) -> str:
        """Диалоговое окно выбора папки для открытия проекта."""
        while True:
            folder_path = QFileDialog.getOpenFileName(
                None,
                "Выбор aed файла проекта для его открытия",
                self.__osbm.obj_dirm.get_default_folder_projects_dirpath(),
                "Project files (*.aed)",
            )
            if folder_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_open_project() -> {folder_path[0]}"
                )
                return os.path.dirname(folder_path[0])
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_open_project() -> {None}"
                )
                return None

    def select_image_for_formimage_in_project(self) -> str:
        """Диалоговое окно выбора изображения для формы."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_image_for_formimage_in_project() -> str"
        )
        while True:
            if self.__formimage_dirpath and os.path.exists(self.__formimage_dirpath): 
                pass
            else:
                self.__formimage_dirpath = self.__osbm.obj_dirm.get_pictures_dirpath()
            image_path = QFileDialog.getOpenFileName(
                None,
                "Выбор изображения",
                self.__formimage_dirpath,
                "Изображения (*.png *.jpg *.jpeg)",
            )
            if image_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_image_for_formimage_in_project() -> {image_path[0]}"
                )
                self.__formimage_dirpath = os.path.dirname(image_path[0])
                return image_path[0]
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_image_for_formimage_in_project() -> {None}"
                )
                return None

    def select_docx_or_pdf_file(self) -> str:
        """Диалоговое окно выбора документа."""

        self.__osbm.obj_logg.debug_logger("DialogWindows select_docx_or_pdf_file() -> str")

        while True:
            if self.__select_docxpdf_dirpath and os.path.exists(self.__select_docxpdf_dirpath): 
                pass
            else:
                self.__select_docxpdf_dirpath = self.__osbm.obj_dirm.get_documents_dirpath()
            docx_path = QFileDialog.getOpenFileName(
                None,
                "Выбор документа",
                self.__select_docxpdf_dirpath,
                "Документы (*.docx *.pdf)",
            )
            if docx_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_docx_or_pdf_file() -> {docx_path[0]}"
                )
                self.__select_docxpdf_dirpath = os.path.dirname(docx_path[0])
                return docx_path[0]
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_docx_or_pdf_file() -> {None}"
                )
                return None

    def warning_message(self, message: str):
        """Диалоговое окно 'Предупреждение'."""

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows warning_message(message: str):\nmessage = {message}"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Предупреждение")
        self.__dw.setText(message)
        self.__dw.setIcon(QMessageBox.Warning)
        response = self.__dw.exec()
        return response

    def error_message(self, message: str):
        """Диалоговое окно 'Ошибка'."""

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows error_message(message: str):\nmessage = {message}"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Ошибка")
        self.__dw.setText(message)
        self.__dw.setIcon(QMessageBox.Critical)
        response = self.__dw.exec()
        return response

    def question_message(self, message: str):
        """Диалоговое окно 'Вопрос'."""

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows question_message(message: str):\nmessage = {message}"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Вопрос")
        self.__dw.setText(message)
        self.__dw.setIcon(QMessageBox.Question)
        self.__dw.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.__dw.setButtonText(QMessageBox.Yes, "Да")
        self.__dw.setButtonText(QMessageBox.No, "Нет")
        response = self.__dw.exec()
        if response == QMessageBox.Yes:
            return True
        elif response == QMessageBox.No:
            return False
        else:
            return None

    def select_name_and_dirpath_export_pdf(self) -> str:
        """Диалоговое окно 'Выберите имя и путь для экспорта в PDF'."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_name_and_dirpath_export_pdf() -> str"
        )

        while True:
            multipage_pdf_path = QFileDialog.getSaveFileName(
                None,
                "Выберите имя и путь для экспорта в PDF",
                self.__osbm.obj_dirm.get_documents_dirpath(),
                "PDF (*.pdf)",
            )
            if multipage_pdf_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_name_and_dirpath_export_pdf() -> {multipage_pdf_path[0]}"
                )
                return multipage_pdf_path[0]
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_name_and_dirpath_export_pdf() -> {None}"
                )
                return None


# obj_dw = DialogWindows()

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\nodeseditordialogwindow.py
``python
from PySide6.QtWidgets import QDialog, QTreeWidgetItem
from PySide6.QtCore import Qt

import package.ui.nodeseditordialogwindow_ui as nodeseditordialogwindow_ui

import package.components.dialogwindow.neddw.nednodedialogwindow as nednodedialogwindow


class NodesEditorDialogWindow(QDialog):
    def __init__(self, osbm, open_node):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow __init__(osbm, open_node): \nopen_node = {open_node}"
        )
        super(NodesEditorDialogWindow, self).__init__()
        self.ui = nodeseditordialogwindow_ui.Ui_NodesEditorDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.config()
        self.reconfig(open_node)
        #
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def config(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow config()")
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def reconfig(self, open_node=None):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow reconfig()")
        #
        tree_widget = self.ui.tw_nodes
        self.__nodes_to_items = dict()
        self.__open_node_flag = False
        # очистка tw_nodes
        tree_widget.blockSignals(True)
        tree_widget.clear()
        tree_widget.setHeaderLabels(["Проект"])
        # заполнения вершинами
        self.__nodes = self.__osbm.obj_prodb.get_nodes()
        print(f"NodesEditorDialogWindow self.__nodes = {self.__nodes}")
        # запуск
        project_node = self.find_project_node()
        self.dfs(project_node, open_node)
        #
        if tree_widget.topLevelItemCount() > 0 and not self.__open_node_flag:
            tree_widget.setCurrentItem(tree_widget.topLevelItem(0))
        # включение сигналов
        tree_widget.expandAll()
        tree_widget.blockSignals(False)

    def find_project_node(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow find_project_node()")
        for node in self.__nodes:
            if node.get("type_node") == "PROJECT":
                return node
        return None

    def set_text_and_icon_for_item_by_node(self, item, node):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow get_text_by_node(item, node):\nitem = {item},\nnode = {node}"
        )
        # иконки
        if node.get("type_node") == "FORM":
            icon = self.__icons.get("form")
            icon = item.setIcon(0, icon)
        elif node.get("type_node") == "GROUP":
            icon = self.__icons.get("group")
            icon = item.setIcon(0, icon)
        # текст
        text = node.get("name_node")
        item.setText(0, text)

    def dfs(self, parent_node, open_node=None):
        """
        АНАЛОГ (почти). Проход по всем вершинам.
        """
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow dfs(parent_node, open_node):\nparent_node = {parent_node}\nopen_node = {open_node}"
        )
        childs = self.get_childs(parent_node)
        if childs:
            for child in childs:
                # действие
                self.set_item_in_nodes_to_items(child, open_node)
                # проход по дочерним вершинам
                self.dfs(child, open_node)

    def get_childs(self, parent_node):
        childs = list(
            filter(
                lambda node: node.get("id_parent") == parent_node.get("id_node"),
                self.__nodes,
            )
        )
        childs.sort(key=lambda node: int(node.get("order_node")))

        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow get_childs(parent_node):\nparent_node = {parent_node}\nchilds = {childs}"
        )
        return childs

    def set_item_in_nodes_to_items(self, node, open_node=None):
        """
        АНАЛОГ. Поставить item в nodes_to_items.
        """
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow set_item_in_nodes_to_items(node):\nnode = {node}\nopen_node = {open_node}"
        )
        tree_widget = self.ui.tw_nodes
        item = None
        if node.get("id_parent") == 0:
            item = QTreeWidgetItem(tree_widget)
            item.setData(0, Qt.UserRole, node)
        else:
            item = QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])
            item.setData(0, Qt.UserRole, node)
        self.set_text_and_icon_for_item_by_node(item, node)
        self.__nodes_to_items[node.get("id_node")] = item
        # Выбор
        if open_node and node.get("id_node") == open_node.get("id_node"):
            tree_widget.setCurrentItem(item)
            self.__open_node_flag = True

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow config_actions()")
        self.ui.btn_add_form.clicked.connect(self.add_form)
        self.ui.btn_add_form.setShortcut("Ctrl+F")
        self.ui.btn_add_group.clicked.connect(self.add_group)
        self.ui.btn_add_group.setShortcut("Ctrl+G")
        self.ui.btn_delete_item.clicked.connect(self.delete_item)
        self.ui.btn_delete_item.setShortcut("Ctrl+D")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_edit.clicked.connect(self.edit_current)
        self.ui.btn_edit.setShortcut("Ctrl+E")

    def update_edit_nodes(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow update_bd()")
        edit_nodes = self.__osbm.obj_nedndw.get_data()
        # for edit_node in edit_nodes:
        #     print(f"-> edit_node = {edit_node}")
        for edit_node in edit_nodes:
            if edit_node != "WRAPPER":
                id_node = edit_node.get("id_node")
                if id_node == -111:
                    # print(f"ADD, edit_node = {edit_node}")
                    self.__osbm.obj_prodb.add_node(edit_node)
                else:
                    # update данные по id
                    # print(f"UPDATE, edit_node = {edit_node}")
                    self.__osbm.obj_prodb.update_node(edit_node)

    def edit_current(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow edit_current()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("edit", node.get("type_node"), node)
            if result:
                # обновление данных в БД
                self.update_edit_nodes()
                # перерисовка
                self.reconfig(node)
        else:
            self.__osbm.obj_dw.warning_message("Выберите элемент для редактирования!")

    def delete_item(self):
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            type_node = node.get("type_node")
            name_node = node.get("name_node")
            result = self.__osbm.obj_dw.question_message(
                f'Вы действительно хотите удалить:\n"{name_node}"?'
            )
            if result:
                if type_node == "GROUP":
                    self.delete_group_node(node)
                else:
                    self.__osbm.obj_prodb.delete_node(node)
                self.reconfig(node)
                print("УДАЛЕНИЕ")
        else:
            self.__osbm.obj_dw.warning_message("Выберите элемент для удаления!")

    def delete_group_node(self, node):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow delete_group_node(node):\nnode = {node}"
        )

        childs = self.get_childs(node)
        if childs:
            # переопределяем родительскую вершину для дочерних вершин
            for child in childs:
                self.__osbm.obj_prodb.set_new_parent_for_child_node(node, child)
            # удаляем вершину из БД
            self.__osbm.obj_prodb.delete_node(node)
            # дети не должны удаляться так как не прописан для id_parent ON DELETE CASCADE
            # перевыставляем order_node соседям вершины
            parent_node = self.__osbm.obj_prodb.get_node_parent(node)
            parent_childs = self.__osbm.obj_prodb.get_childs(parent_node)
            if parent_childs:
                for index, parent_child in enumerate(parent_childs):
                    self.__osbm.obj_prodb.set_order_for_node(parent_child, index)
        else:
            self.__osbm.obj_prodb.delete_node(node)

    def add_group(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow add_group()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        result = False
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("create", "GROUP", node)
        else:
            result = self.ned_node_dw("create", "GROUP")
        if result:
            # обновление данных в БД
            self.update_edit_nodes()
            # перерисовка
            self.reconfig()

    def add_form(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow add_form()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        result = False
        node = None
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("create", "FORM", node)
        else:
            result = self.ned_node_dw("create", "FORM")
        if result:
            # обновление данных в БД
            self.update_edit_nodes()
            # перерисовка
            self.reconfig(node)

    def ned_node_dw(self, type_window, type_node, node=None) -> bool:
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow ned_node_dw()")
        self.__osbm.obj_nedndw = nednodedialogwindow.NedNodeDialogWindow(
            self.__osbm, type_window, type_node, self.__nodes, node
        )
        result = self.__osbm.obj_nedndw.exec()
        return result == QDialog.Accepted

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\settingsdialogwindow.py
``python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt

class SettingsDialogWindow(QDialog):
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("SettingsDialogWindow __init__()")
        super(SettingsDialogWindow, self).__init__()
        
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        self.setWindowTitle("Настройки приложения")
        
        # Конфигурация
        self.config_ui()
        self.load_settings()
        self.connecting_actions()
        
        # Свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def config_ui(self):
        """Настройка пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Путь к LibreOffice
        libreoffice_layout = QHBoxLayout()
        libreoffice_layout.addWidget(QLabel("Путь к LibreOffice:"))
        self.libreoffice_path_edit = QLineEdit()
        libreoffice_layout.addWidget(self.libreoffice_path_edit)
        self.browse_libreoffice_btn = QPushButton("Обзор...")
        libreoffice_layout.addWidget(self.browse_libreoffice_btn)
        main_layout.addLayout(libreoffice_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        self.resize(500, 100)

    def load_settings(self):
        """Загрузка текущих настроек"""
        libreoffice_path = self.__osbm.obj_settings.get_libreoffice_path()
        self.libreoffice_path_edit.setText(libreoffice_path)

    def connecting_actions(self):
        """Подключение обработчиков событий"""
        self.browse_libreoffice_btn.clicked.connect(self.browse_libreoffice)
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Горячие клавиши
        self.save_btn.setShortcut("Ctrl+S")
        self.cancel_btn.setShortcut("Ctrl+Q")

    def browse_libreoffice(self):
        """Выбор пути к LibreOffice"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите исполняемый файл LibreOffice",
            self.libreoffice_path_edit.text(),
            "Исполняемые файлы (*.exe)"
        )
        
        if file_path:
            self.libreoffice_path_edit.setText(file_path)

    def save_settings(self):
        """Сохранение настроек"""
        try:
            libreoffice_path = self.libreoffice_path_edit.text().strip()
            
            # Проверка валидности пути
            if libreoffice_path and not libreoffice_path.endswith("soffice.exe"):
                QMessageBox.warning(
                    self,
                    "Предупреждение",
                    "Путь должен указывать на исполняемый файл soffice.exe"
                )
                return
            
            # Сохранение настроек
            self.__osbm.obj_settings.set_libreoffice_path(libreoffice_path)
            self.__osbm.obj_settings.sync()
            
            # Обновление статуса LibreOffice в главном окне
            self.__osbm.obj_offp.resetting_office_packets()
            if self.__osbm.obj_stab.get_is_active():
                self.__osbm.obj_stab.update_status_libreoffice_label(
                    self.__osbm.obj_offp.get_status_libreoffice()
                )
            
            self.accept()
            
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error saving settings: {e}")
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при сохранении настроек: {str(e)}"
            )
``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\templateslistsialogwindow.py
``python
from PySide6.QtWidgets import QDialog, QListWidgetItem, QListWidget, QAbstractItemView
from PySide6.QtCore import Qt, QTimer, QSize, QRect


from functools import partial

import package.ui.templateslistsialogwindow_ui as templateslistsialogwindow_ui

import package.components.dialogwindow.neddw.nedtemplatedialogwindow as nedtemplatedialogwindow
import package.components.dialogwindow.neddw.nedpagedialogwindow as nedpagedialogwindow
import package.components.widgets.customitemqlistwidget as customitemqlistwidget


class TemplatesListDialogWindow(QDialog):
    def __init__(self, osbm, open_node, open_template, open_page):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow __init__(osbm, open_node, open_template, open_page):\nopen_node = {open_node}\nopen_template = {open_template}\nopen_page = {open_page}"
        )
        super(TemplatesListDialogWindow, self).__init__()
        self.ui = templateslistsialogwindow_ui.Ui_TemplatesListDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.__templates = []
        self.__pages = []
        self.__templates_items = []
        self.__pages_items = []

        # конфигурация
        self.config_lws()
        #
        self.reconfig("REFORM", open_node, open_template, open_page)
        # # подключаем деействия
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event):
        super(TemplatesListDialogWindow, self).resizeEvent(event)
        QTimer.singleShot(0, self, self.update_sizes)

    def update_sizes(self):
        # resize_templates_items
        for item in self.__templates_items:
            widget = self.ui.lw_templates.itemWidget(item)
            item.setSizeHint(item.sizeHint().boundedTo(self.ui.lw_templates.sizeHint()))
            if widget is not None:
                widget_size = widget.sizeHint()
                widget.setFixedSize(
                    QSize(self.ui.lw_pages.size().width() - 2, widget_size.height())
                )
        # resize_pages_items
        for item in self.__pages_items:
            widget = self.ui.lw_pages.itemWidget(item)
            item.setSizeHint(item.sizeHint().boundedTo(self.ui.lw_pages.sizeHint()))
            if widget is not None:
                widget_size = widget.sizeHint()
                widget.setFixedSize(
                    QSize(self.ui.lw_pages.size().width() - 44, widget_size.height())
                )

    def reconfig(
        self, type_reconfig="", open_form=None, open_template=None, open_page=None
    ):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow reconfig(type_reconfig): type_reconfig = {type_reconfig}"
        )
        if type_reconfig == "REFORM":
            self.config_forms(open_form)
            self.config_templates(open_template)
            self.config_pages(open_page)
        elif type_reconfig == "RETEMPLATE":
            self.config_templates(open_template)
            self.config_pages(open_page)
        elif type_reconfig == "REPAGE":
            self.config_pages(open_page)

    def config_lws(self):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow config_lws()")
        for list_widget in [self.ui.lw_templates, self.ui.lw_pages]:
            list_widget.setResizeMode(QListWidget.Adjust)
            list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ui.lw_pages.itemPressed.connect(self.on_item_pressed)

    def on_item_pressed(self, item):
        """Странный баг, который можно обойти чере этот костыль"""
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow on_item_pressed(item):\nitem = {item}"
        )
        # проверка на чекбокс
        item_rect = self.ui.lw_pages.visualItemRect(item)
        mouse_position = self.ui.lw_pages.mapFromGlobal(
            self.ui.lw_pages.cursor().pos()
        )
        # Определяем область чекбокса
        checkbox_rect = QRect(item_rect.topLeft(), item_rect.size())
        checkbox_rect.setWidth(
            20
        )  # ширина области чекбокса, измените при необходимости
        if checkbox_rect.contains(mouse_position):
            self.checkbox_changing_state(item)


    def config_forms(self, open_form=None):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow config_forms()")
        #
        forms = self.__osbm.obj_prodb.get_form_nodes()
        combobox = self.ui.combox_forms
        combobox.blockSignals(True)
        combobox.clear()
        for index, form in enumerate(forms):
            combobox.addItem(form.get("name_node"), form)
        #
        if combobox.count() > 0:
            if open_form:
                index_form = next(
                    (
                        i
                        for i, form in enumerate(forms)
                        if form.get("id_node") == open_form.get("id_node")
                    ),
                    0,
                )
                if index_form is not None:
                    combobox.setCurrentIndex(index_form)
                else:
                    combobox.setCurrentIndex(0)
            else:
                combobox.setCurrentIndex(0)
        combobox.blockSignals(False)

    def config_templates(self, open_template=None):
        self.__osbm.obj_logg.debug_logger(
            "TemplatesListDialogWindow config_templates()"
        )
        #
        list_widget = self.ui.lw_templates
        list_widget.blockSignals(True)
        list_widget.clear()
        #
        form = self.ui.combox_forms.currentData()
        print(f"form = {form}")
        if form:
            templates = self.__osbm.obj_prodb.get_templates_by_form(form)
            self.__templates = templates
            self.__templates_items = []

            #
            id_active_template = form.get("id_active_template")
            print(f"form = {form}")
            print(f"templates = {templates}")

            for template in templates:
                is_active = False
                if template.get("id_template") == id_active_template:
                    is_active = True
                custom_widget = customitemqlistwidget.CustomItemQListWidget(
                    self.__osbm, "TEMPLATE", template, is_active
                )
                item = QListWidgetItem()
                item.setData(0, template)
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())
                item.setSizeHint(item.sizeHint().boundedTo(list_widget.sizeHint()))
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget)
                # кнопки
                self.config_buttons_for_item(custom_widget)
                #
                self.__templates_items.append(item)
            print(f"self.__templates = {self.__templates}")
            if self.__templates_items:
                # выбор нужного шаблона
                if open_template:
                    index_template = next(
                        (
                            i
                            for i, template in enumerate(templates)
                            if template.get("id_template")
                            == open_template.get("id_template")
                        ),
                        0,
                    )
                    list_widget.setCurrentRow(index_template)
                else:
                    list_widget.setCurrentRow(0)
        list_widget.blockSignals(False)

    def config_pages(self, open_page=None):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow config_pages()")
        #
        list_widget = self.ui.lw_pages
        # list_widget.blockSignals(True)
        list_widget.clear()
        #
        item_template = self.ui.lw_templates.currentItem()
        if item_template is not None:
            print("if item_template is not None:")
            template = item_template.data(0)
            # сортированный список страниц
            pages = self.__osbm.obj_prodb.get_pages_by_template(template)
            self.__pages = pages
            self.__pages_items = []
            for page in pages:
                custom_widget = customitemqlistwidget.CustomItemQListWidget(
                    self.__osbm, "PAGE", page, is_active=False
                )
                item = QListWidgetItem()
                item.setData(0, page)
                item.setCheckState(Qt.Checked if page.get("included") else Qt.Unchecked)
                #
                typefile_page = page.get("typefile_page")
                if typefile_page == "PDF":
                    item.setIcon(self.__icons.get("pdf"))
                else:  # "DOCX"
                    item.setIcon(self.__icons.get("page"))
                #
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())
                item.setSizeHint(item.sizeHint().boundedTo(list_widget.sizeHint()))
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget)
                # кнопки
                self.config_buttons_for_item(custom_widget)
                #
                self.__pages_items.append(item)
            #
            if self.__pages_items:
                if open_page:
                    index_template = next(
                        (
                            i
                            for i, page in enumerate(pages)
                            if page.get("id_page") == open_page.get("id_page")
                        ),
                        0,
                    )
                    list_widget.setCurrentRow(index_template)
                elif self.__templates_items:
                    list_widget.setCurrentRow(0)
            #
        # list_widget.blockSignals(False)
        

    def config_buttons_for_item(self, item_widget):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow config_buttons_for_item(item_widget)\nitem_widget = {item_widget}"
        )
        edit_button = item_widget.get_btn_edit()
        delete_button = item_widget.get_btn_delete()
        type_window = item_widget.get_type_window()
        edit_button.clicked.connect(
            partial(
                self.edit_item,
                type_window=type_window,
                data=item_widget.get_data(),
                is_active=item_widget.get_is_active(),
            )
        )
        delete_button.clicked.connect(
            partial(
                self.delete_item,
                type_window=type_window,
                data=item_widget.get_data(),
                is_active=item_widget.get_is_active(),
            )
        )

    def checkbox_changing_state(self, item):
        """Странный баг, который можно обойти чере этот костыль"""
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow checkbox_changing_state(item)\nitem = {item}"
        )
        if item.checkState() == Qt.Checked:
            new_state = Qt.Unchecked
            self.__osbm.obj_prodb.set_included_for_page(item.data(0), 0)
        else:
            new_state = Qt.Checked
            self.__osbm.obj_prodb.set_included_for_page(item.data(0), 1)
        # Устанавливаем новое состояние
        item.setCheckState(new_state)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger(
            "TemplatesListDialogWindow connecting_actions()"
        )
        # кнопки
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_add_page.clicked.connect(self.add_page)
        self.ui.btn_add_page.setShortcut("Ctrl+P")
        self.ui.btn_add_template.clicked.connect(self.add_template)
        self.ui.btn_add_template.setShortcut("Ctrl+T")
        # смена индекса
        self.ui.combox_forms.currentIndexChanged.connect(
            lambda index: self.reconfig("RETEMPLATE")
        )
        self.ui.lw_templates.currentItemChanged.connect(
            lambda item: self.reconfig("REPAGE")
        )

    def edit_item(self, type_window, data, is_active=False):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow edit_item(btn):\ntype_window = {type_window}\n data = {data}"
        )
        if type_window == "TEMPLATE":
            template = data
            result = self.ned_temp_dw("edit", template, is_active)
            if result:
                # СТРАНИЦА obj_nedtempdw
                data = self.__osbm.obj_nedtempdw.get_data()
                name_template = data.get("name_template")
                self.__osbm.obj_prodb.set_new_name_for_template(template, name_template)
                # is_active
                # order у template остутсвует
                is_active = data.get("IS_ACTIVE")
                if is_active:
                    id_parent_node = template.get("id_parent_node")
                    id_template = template.get("id_template")
                    self.__osbm.obj_prodb.set_active_template_for_node_by_id(
                        id_parent_node, id_template
                    )
                # было: self.reconfig("RETEMPLATE", None, data, None)
                open_form = self.ui.combox_forms.currentData()
                self.reconfig("REFORM", open_form, data, None)

        elif type_window == "PAGE":
            self.edit_page(data)

    def update_order_pages(self, editpage, new_order_page):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow update_order_pages(editpage, new_order_page):\n editpage = {editpage}\n new_order_page = {new_order_page}"
        )
        # подготовка данных (-11 - спец значение)
        id_editpage = editpage.get("id_page", -111)
        pages = [page for page in self.__pages if page.get("id_page") != id_editpage]
        pages = sorted(pages, key=lambda x: x.get("order_page"))
        pages.insert(new_order_page, editpage)
        # обновить значения
        for index, page in enumerate(pages):
            # order_page = page.get("order_page")
            self.__osbm.obj_prodb.set_order_for_page(page, index)

    def delete_item(self, type_window, data, is_active=False):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow delete_item(btn):\ntype_window = {type_window}\n data = {data}"
        )
        if type_window == "TEMPLATE":
            name_template = data.get("name_template")
            result = self.__osbm.obj_dw.question_message(
                f'Вы действительно хотите удалить этот шаблон:\n"{name_template}"?'
            )
            if result:
                self.__osbm.obj_prodb.delete_template(data)
                open_form = self.ui.combox_forms.currentData()
                if is_active:
                    self.set_active_template_after_delete(data, open_form)
                # было: self.reconfig("RETEMPLATE")
                self.reconfig("REFORM", open_form, None, None)

        elif type_window == "PAGE":
            name_page = data.get("name_page")
            result = self.__osbm.obj_dw.question_message(
                f'Вы действительно хотите удалить эту страницу:\n"{name_page}"?'
            )
            if result:
                self.delete_page(data)
                self.reconfig("REPAGE")

    def set_active_template_after_delete(self, old_data, form):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow set_active_template_after_delete(data):\nold_data = {old_data}"
        )
        self.__templates.remove(old_data)
        if self.__templates:
            id_new_template = self.__templates[0].get("id_template")
            id_parent_node = form.get("id_node")
            self.__osbm.obj_prodb.set_active_template_for_node_by_id(
                id_parent_node, id_new_template
            )

    def delete_page(self, page):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow delete_page(page):\npage = {page}"
        )
        filename_page = page.get("filename_page")
        typefile_page = page.get("typefile_page")
        self.__osbm.obj_film.delete_page_from_project(filename_page, typefile_page)
        self.__osbm.obj_prodb.delete_page(page)

    def add_page(self):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow add_page()")
        result = self.ned_page_dw("create")
        item_template = self.ui.lw_templates.currentItem()
        if result and item_template:
            template = item_template.data(0)
            id_parent_template = template.get("id_template")
            #
            data = self.__osbm.obj_nedpagedw.get_data()
            filename_page = data.get("filename_page")
            name_page = data.get("name_page")
            typefile_page = data.get("typefile_page")
            order_page = data.get("order_page")
            copy_page = data.get("copy_page")
            # "order_page": -111, ТАК ДОЛЖНО БЫТЬ!!!
            # копировать?
            if copy_page == "empty":
                new_page = {
                    "id_parent_template": id_parent_template,
                    "name_page": name_page,
                    "filename_page": filename_page,
                    "typefile_page": typefile_page,
                    "order_page": -111,
                    "included": 1,
                }
            else:
                # копирование
                new_page_filename = self.__osbm.obj_film.copynew_page_for_new_template(
                    copy_page.get("filename_page"), copy_page.get("typefile_page")
                )
                #
                new_page = {
                    "id_parent_template": copy_page.get("id_parent_template"),
                    "name_page": name_page,
                    "filename_page": new_page_filename,
                    "typefile_page": copy_page.get("typefile_page"),
                    "order_page": -111,
                    "included": 1,
                }
            # добавляем вершину
            primary_key = self.__osbm.obj_prodb.insert_page(new_page)
            new_page["id_page"] = primary_key
            # обновляем order
            page_for_order = self.__osbm.obj_prodb.get_page_by_id(primary_key)
            self.update_order_pages(page_for_order, order_page)
            # копирование
            if copy_page == "empty":
                # перемещение из temp в forms
                temp_copy_file_path = data.get("TEMP_COPY_FILE_PATH")
                if typefile_page == "DOCX":
                    self.__osbm.obj_film.docx_from_temp_to_forms(
                        temp_copy_file_path, filename_page
                    )
                elif typefile_page == "PDF":
                    self.__osbm.obj_film.pdf_from_temp_to_pdfs(
                        temp_copy_file_path, filename_page
                    )
            else:
                self.copy_page(copy_page, new_page)
            #
            self.reconfig("REPAGE")

    def copy_page(self, copy_page, new_page):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow copy_page(copy_page, new_page):\ncopy_page = {copy_page}\nnew_page = {new_page}"
        )
        pd_pairs = self.__osbm.obj_prodb.get_page_data(copy_page)
        for pd_pair in pd_pairs:
            pair = {
                "id_variable": pd_pair.get("id_variable"),
                "value_pair": pd_pair.get("value_pair"),
            }
            self.__osbm.obj_prodb.insert_page_data(new_page, pair)

    def edit_page(self, data):
        page = data
        result = self.ned_page_dw("edit", page)
        if result:
            # СТРАНИЦА obj_nedpagedw
            data = self.__osbm.obj_nedpagedw.get_data()
            # Обновить в БД страницу
            typefile_page = data.get("typefile_page")
            edit_page = {
                "id_page": page.get("id_page"),
                "name_page": data.get("name_page"),
                "filename_page": data.get("filename_page"),
                "typefile_page": typefile_page,
            }
            self.__osbm.obj_prodb.update_page(edit_page)
            # обновить order
            self.update_order_pages(data, data.get("order_page"))
            # перемещение из temp в forms
            new_filename_page = data.get("filename_page")
            temp_copy_file_path = data.get("TEMP_COPY_FILE_PATH")
            if typefile_page == "DOCX":
                self.__osbm.obj_film.docx_from_temp_to_forms(
                    temp_copy_file_path, new_filename_page
                )
            elif typefile_page == "PDF":
                self.__osbm.obj_film.pdf_from_temp_to_pdfs(
                    temp_copy_file_path, new_filename_page
                )
            #
            self.reconfig("REPAGE", None, None, data)

    def add_template(self):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow add_template()")
        result = self.ned_temp_dw("create")
        if result:
            data = self.__osbm.obj_nedtempdw.get_data()
            name_template = data.get("name_template")
            copy_template = data.get("copy_template")
            # добавить
            form = self.ui.combox_forms.currentData()
            if form:
                id_new_template = self.__osbm.obj_prodb.add_template(
                    name_template, form
                )
                # копирование
                if copy_template != "empty":
                    id_copy_template = copy_template.get("id_template")
                    new_template = {
                        "id_template": id_new_template,
                        "name_template": name_template,
                        "id_parent_node": form.get("id_node"),
                    }
                    old_template = self.__osbm.obj_prodb.get_template_by_id(
                        id_copy_template
                    )
                    self.copy_template(old_template, new_template)
                # активность для текущего
                is_active = data.get("IS_ACTIVE")
                if is_active:
                    id_parent_node = form.get("id_node")
                    id_template = id_new_template
                    self.__osbm.obj_prodb.set_active_template_for_node_by_id(
                        id_parent_node, id_template
                    )

                # было: self.reconfig("RETEMPLATE")
                open_form = self.ui.combox_forms.currentData()
                self.reconfig("REFORM", open_form, None, None)

    def copy_template(self, old_template, new_template):
        self.__osbm.obj_logg.debug_logger(
            f"copy_template():\nold_template = {old_template}\nnew_template = {new_template}"
        )
        # поэтапно
        self.copy_template_templates_data(old_template, new_template)
        old_to_new_pages = self.copy_template_pages(old_template, new_template)
        self.copy_pages_data(old_to_new_pages)

    def copy_template_templates_data(self, old_template, new_template):
        self.__osbm.obj_logg.debug_logger(
            f"copy_template_templates_data():\nold_template = {old_template}\nnew_template = {new_template}"
        )
        td_pairs = self.__osbm.obj_prodb.get_template_data(old_template)
        for td_pair in td_pairs:
            self.__osbm.obj_prodb.insert_template_data(new_template, td_pair)

    def copy_template_pages(self, old_template, new_template) -> dict:
        self.__osbm.obj_logg.debug_logger(
            f"copy_template_pages() -> dict:\nold_template = {old_template}\nnew_template = {new_template}"
        )
        old_to_new_pages = dict()
        id_parent_template = new_template.get("id_template")
        p_pairs = self.__osbm.obj_prodb.get_pages_by_template(old_template)
        for p_pair in p_pairs:
            self.copy_template_page(p_pair, id_parent_template, old_to_new_pages)
        return old_to_new_pages

    def copy_template_page(self, p_pair, id_parent_template, old_to_new_pages):
        old_page_filename = p_pair.get("filename_page")
        typefile_page = p_pair.get("typefile_page")
        # копирование
        new_page_filename = self.__osbm.obj_film.copynew_page_for_new_template(
            old_page_filename, typefile_page
        )
        # добавление в бд
        new_page = {
            "id_parent_template": id_parent_template,
            "name_page": p_pair.get("name_page"),
            "filename_page": new_page_filename,
            "typefile_page": typefile_page,
            "order_page": p_pair.get("order_page"),
            "included": p_pair.get("included"),
        }
        new_id_page = self.__osbm.obj_prodb.insert_page(new_page)
        old_to_new_pages[p_pair.get("id_page")] = new_id_page

    def copy_pages_data(self, old_to_new_pages):
        self.__osbm.obj_logg.debug_logger(
            f"copy_pages_data():\nold_to_new_pages = {old_to_new_pages}"
        )
        for old_id_page, new_id_page in old_to_new_pages.items():
            old_page = {
                "id_page": old_id_page,
            }
            new_page = {
                "id_page": new_id_page,
            }
            pd_pairs = self.__osbm.obj_prodb.get_page_data(old_page)
            for pd_pair in pd_pairs:
                pair = {
                    "id_variable": pd_pair.get("id_variable"),
                    "value_pair": pd_pair.get("value_pair"),
                }
                self.__osbm.obj_prodb.insert_page_data(new_page, pair)

    def ned_temp_dw(self, type_ned, template=None, is_active=False) -> bool:
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow ned_temp_dw()")
        self.__osbm.obj_nedtempdw = nedtemplatedialogwindow.NedTemplateDialogWindow(
            self.__osbm, type_ned, self.__templates, template, is_active
        )
        result = self.__osbm.obj_nedtempdw.exec()
        return result == QDialog.Accepted

    def ned_page_dw(self, type_ned, page=None) -> bool:
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow ned_page_dw()")
        self.__osbm.obj_nedpagedw = nedpagedialogwindow.NedPageDialogWindow(
            self.__osbm, type_ned, self.__pages, page
        )
        result = self.__osbm.obj_nedpagedw.exec()
        return result == QDialog.Accepted

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\variableslistdialogwindow.py
``python
import json

from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QWidget,
    QHeaderView,
)
from PySide6.QtCore import Qt, QTimer

from functools import partial

import package.components.dialogwindow.neddw.nedvariabledialogwindow as nedvariabledialogwindow

import package.ui.variableslistdialogwindow_ui as variableslistdialogwindow_ui


class Obj:
    pass


class NumericItem(QTableWidgetItem):
    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)


class VariablesListDialogWindow(QDialog):
    def __init__(self, osbm, open_node, open_template, open_page, edit_variable=None):
        self.__osbm = osbm
        self.__edit_variable = edit_variable
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow __init__(osbm, open_node, open_template, open_page): \nopen_node = {open_node}\nopen_template = {open_template}\nopen_page = {open_page}"
        )
        self.initalizate_tabs_objects()
        super(VariablesListDialogWindow, self).__init__()
        self.ui = variableslistdialogwindow_ui.Ui_VariablesListDialog()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.__all_variables = None
        self.__vertical_scroll_position_by_parameters = {}
        self.__qtimer = None
        self.__edit_button = None
        # config
        self.config()
        self.config_tws()
        # Подключаем действия
        self.connecting_actions()
        # отобразить (в нём caf - reconfig)
        self.show_config(open_node, open_template, open_page)

    def showEvent(self, event):
        super().showEvent(event)
        print("showEvent showEvent showEvent")
        # Вызов функции edit_variable
        print(f"self.__edit_variable = {self.__edit_variable} self.__edit_button = {self.__edit_button}")
        if self.__edit_variable and self.__edit_button:
            self.edit_variable(self.__edit_button)
        self.__edit_variable = None
        self.__edit_button = None

        
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def initalizate_tabs_objects(self):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow initalizate_tabs_objects()"
        )
        self.obj_projroject = Obj()
        self.obj_group = Obj()
        self.obj_form_template_page = Obj()
        # Списки с данными
        setattr(
            self.obj_projroject,
            "project_node",
            self.__osbm.obj_prodb.get_project_node(),
        )
        setattr(
            self.obj_group,
            "list_of_group_node",
            self.__osbm.obj_prodb.get_group_nodes(),
        )
        setattr(
            self.obj_form_template_page,
            "list_of_form_node",
            self.__osbm.obj_prodb.get_form_nodes(),
        )

    def config(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow config()")
        self.ui.splitter_ftp.setSizes([500, 300])
        self.ui.splitter_group.setSizes([500, 300])
        self.ui.splitter_project.setSizes([500, 300])
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow connecting_actions()"
        )
        # смена tab
        self.ui.tabwidget.currentChanged.connect(self.on_tab_changed)
        # КОМБОБОКСЫ
        # combox_groups
        self.ui.combox_groups.currentIndexChanged.connect(
            self.combox_groups_index_changed
        )
        # combox_forms
        self.ui.combox_forms.currentIndexChanged.connect(
            self.combox_forms_index_changed
        )
        # combox_templates
        self.ui.combox_templates.currentIndexChanged.connect(
            self.combox_templates_index_changed
        )
        # combox_pages
        self.ui.combox_pages.currentIndexChanged.connect(
            self.combox_pages_index_changed
        )
        self.ui.btn_create_variable.clicked.connect(self.create_variable)
        self.ui.btn_create_variable.setShortcut("Ctrl+N")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_save.clicked.connect(self.save_changes)
        self.ui.btn_save.setShortcut("Ctrl+S")

    def get_typetable(self):
        type_table = None
        index = self.ui.tabwidget.currentIndex()
        if index == 0:
            type_table = "project_variables"
        elif index == 1:
            type_table = "group_variables"
        elif index == 2:
            type_table = "form_template_page_variables"
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_typetable():\ntype_table = {type_table}"
        )
        return type_table

    def combox_groups_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"combox_groups_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_forms_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow combox_forms_index_changed(index):\nindex = {index}"
        )
        self.caf_combobox_template()
        self.caf_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_templates_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow combox_templates_index_changed(index):\nindex = {index}"
        )
        self.caf_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_pages_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow combox_pages_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def show_config(self, open_node, open_template, open_page):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow show_config()")
        if open_node:
            type_node = open_node.get("type_node")
            if type_node == "GROUP":
                self.show_tab_group(open_node)
            elif type_node == "FORM":
                if open_template:
                    if open_page:
                        self.show_tab_form_template_page(
                            open_node, open_template, open_page
                        )
                    else:
                        self.show_tab_form_template_page(open_node, open_template)
                else:
                    self.show_tab_form_template_page(open_node)

        else:
            self.show_tab_project()
            

    def show_tab_project(self):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow show_tab_project()"
        )
        self.ui.tabwidget.setCurrentIndex(0)
        self.caf_two_tables("project_variables")

    def show_tab_group(self, open_node=None):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow show_tab_group()")
        self.ui.tabwidget.setCurrentIndex(1)
        self.caf_combobox_group(open_node)
        self.caf_two_tables("group_variables")
        pass

    def show_tab_form_template_page(
        self, open_node=None, open_template=None, open_page=None
    ):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow show_tab_form_template_page()"
        )
        self.ui.tabwidget.setCurrentIndex(2)
        self.caf_combobox_form(open_node)
        self.caf_combobox_template(open_template)
        self.caf_combobox_page(open_page)
        self.caf_two_tables("form_template_page_variables")
        pass

    def on_tab_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow on_tab_changed(self, index):\nindex = {index}"
        )
        if index == 0:
            self.show_tab_project()
        elif index == 1:
            self.show_tab_group()
        elif index == 2:
            self.show_tab_form_template_page()

    def get_table_by_parameters(self, type_table, editor):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_table_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        # получение таблицы
        table_widget = None
        if type_table == "project_variables":
            if editor:
                table_widget = self.ui.table_editor_project_variables
            else:
                table_widget = self.ui.table_project_variables
        elif type_table == "group_variables":
            if editor:
                table_widget = self.ui.table_editor_group_variables
            else:
                table_widget = self.ui.table_group_variables
        elif type_table == "form_template_page_variables":
            if editor:
                table_widget = self.ui.table_editor_ftp_variables
            else:
                table_widget = self.ui.table_ftp_variables
        return table_widget

    def get_data_by_parameters(self, type_table, editor):
        # получение данных
        data = []
        if type_table == "project_variables":
            node_data = self.__osbm.obj_prodb.get_node_data(
                self.obj_projroject.project_node
            )
            print(f"node_data = {node_data}")
            for pair in node_data:
                data.append(
                    self.__osbm.obj_prodb.get_variable_by_id(pair.get("id_variable"))
                )
            print(f"data = {data}")
        elif type_table == "group_variables":
            group_node = self.ui.combox_groups.currentData()
            # проверка на наличия групп
            if group_node:
                node_data = self.__osbm.obj_prodb.get_node_data(group_node)
                for pair in node_data:
                    data.append(
                        self.__osbm.obj_prodb.get_variable_by_id(
                            pair.get("id_variable")
                        )
                    )
        elif type_table == "form_template_page_variables":
            page = self.ui.combox_pages.currentData()
            if page is None:
                pass
            elif page == "all_pages":
                template = self.ui.combox_templates.currentData()
                if template:
                    template_data = self.__osbm.obj_prodb.get_template_data(template)
                    for pair in template_data:
                        data.append(
                            self.__osbm.obj_prodb.get_variable_by_id(
                                pair.get("id_variable")
                            )
                        )
            else:
                page_data = self.__osbm.obj_prodb.get_page_data(page)
                for pair in page_data:
                    data.append(
                        self.__osbm.obj_prodb.get_variable_by_id(
                            pair.get("id_variable")
                        )
                    )
        if editor:
            editor_data = []
            cashe = dict()
            for pair in data:
                cashe[pair.get("id_variable")] = pair
            # self.__all_variables отсортирован по order_variable
            self.__all_variables = self.__osbm.obj_prodb.get_variables()
            for pair in self.__all_variables:
                if cashe.get(pair.get("id_variable")):
                    pair["_checked"] = True
                else:
                    pair["_checked"] = False
                editor_data.append(pair)
            #
            self.__osbm.obj_logg.debug_logger(
                f"VariablesListDialogWindow get_data_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}\neditor_data = {editor_data}"
            )
            return editor_data
        #
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_data_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}\ndata = {data}"
        )
        return data

    def caf_combobox_group(self, open_node=None):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow caf_combobox_group()"
        )
        if open_node:
            current_text = open_node.get("name_node")
        else:
            current_text = self.ui.combox_groups.currentText()
        #
        self.ui.combox_groups.blockSignals(True)
        self.ui.combox_groups.clear()
        for group_node in self.obj_group.list_of_group_node:
            self.ui.combox_groups.addItem(group_node.get("name_node"), group_node)
        #
        index = self.ui.combox_groups.findText(current_text)
        if index != -1:
            self.ui.combox_groups.setCurrentIndex(index)
        #
        self.ui.combox_groups.blockSignals(False)
        self.ui.combox_groups.show()

    def caf_combobox_form(self, open_node):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow caf_combobox_form()"
        )
        if open_node:
            current_text = open_node.get("name_node")
        else:
            current_text = self.ui.combox_forms.currentText()
        #
        self.ui.combox_forms.blockSignals(True)
        self.ui.combox_forms.clear()
        #
        for form_node in self.obj_form_template_page.list_of_form_node:
            self.ui.combox_forms.addItem(form_node.get("name_node"), form_node)
        #
        index = self.ui.combox_forms.findText(current_text)
        if index != -1:
            self.ui.combox_forms.setCurrentIndex(index)
        #
        self.ui.combox_forms.blockSignals(False)
        self.ui.combox_forms.show()

    def caf_combobox_template(self, open_template=None):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow caf_combobox_template()"
        )
        if open_template:
            current_text = open_template.get("name_template")
        else:
            current_text = self.ui.combox_templates.currentText()
        #
        self.ui.combox_templates.blockSignals(True)
        self.ui.combox_templates.clear()
        #
        form = self.ui.combox_forms.currentData()
        templates = []
        if form:
            templates = self.__osbm.obj_prodb.get_templates_by_form(form)
            for template in templates:
                self.ui.combox_templates.addItem(
                    template.get("name_template"), template
                )
            #
            index = self.ui.combox_templates.findText(current_text)
            if index != -1:
                self.ui.combox_templates.setCurrentIndex(index)
            #
        self.ui.combox_templates.blockSignals(False)
        self.ui.combox_templates.show()

    def caf_combobox_page(self, open_page=None):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow caf_combobox_page()"
        )
        if open_page:
            current_text = open_page.get("name_page")
        else:
            current_text = self.ui.combox_pages.currentText()
        # очистка
        self.ui.combox_pages.blockSignals(True)
        self.ui.combox_pages.clear()
        #
        template = self.ui.combox_templates.currentData()
        pages = []
        if template:
            pages = self.__osbm.obj_prodb.get_pages_by_template(template)
            # пункт - Для всех страниц
            self.ui.combox_pages.addItem("- Для всех страниц -", "all_pages")
            for page in pages:
                self.ui.combox_pages.addItem(page.get("name_page"), page)
            #
            index = self.ui.combox_pages.findText(current_text)
            if index != -1:
                self.ui.combox_pages.setCurrentIndex(index)
        #
        self.ui.combox_pages.blockSignals(False)
        self.ui.combox_pages.show()

    def caf_two_tables(self, type_table, open_variable=None):
        """
        Логика такая же, что и в reconfig в других QDialogs.
        """
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow caf_two_tables(self, type_table):\ntype_table = {type_table}"
        )
        self.caf_table(type_table, False, open_variable)
        self.caf_table(type_table, True, open_variable)

    def config_tws(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow config_tws()")
        tws_no_editor = [
            self.ui.table_project_variables,
            self.ui.table_group_variables,
            self.ui.table_ftp_variables,
        ]
        tws_editor = [
            self.ui.table_editor_project_variables,
            self.ui.table_editor_group_variables,
            self.ui.table_editor_ftp_variables,
        ]
        for tw in tws_no_editor:
            self.config_tw(tw, editor=False)
        for tw in tws_editor:
            self.config_tw(tw, editor=True)

    def config_tw(self, table_widget, editor):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow config_tw(self, tw):\ntable_widget = {table_widget}"
        )
        # заголовки/столбцы
        table_widget.verticalHeader().hide()
        if editor:
            headers = ["№", "Переменная", "Название", "Тип", "Кол", "Вкл", "Действия"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
        else:
            headers = ["№", "Переменная", "Название", "Тип"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
        #
        table_widget.setRowCount(0)
        # Настраиваем режимы изменения размера для заголовков
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        if editor:
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        # Включение сортировки
        table_widget.setSortingEnabled(True)
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        # Отключаем возможность выделения
        # table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        # table_widget.sortByColumn(0, Qt.AscendingOrder)
            

    def caf_table(self, type_table, editor, open_variable=None):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow caf_table(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        table_widget = self.get_table_by_parameters(type_table, editor)
        #
        if editor:
            count_all_variable_usages = (
                self.__osbm.obj_prodb.count_all_variable_usages()
            )
            print("f count_all_variable_usages = ", count_all_variable_usages)
        # вертикальный ползунок
        vertical_scroll_position = table_widget.verticalScrollBar().value()
        self.__vertical_scroll_position_by_parameters[type_table, editor] = (
            vertical_scroll_position
        )
        # очистка таблицы
        table_widget.clearContents()
        table_widget.setRowCount(0)
        table_widget.setSortingEnabled(False)
        # данные
        data = self.get_data_by_parameters(type_table, editor)
        header = table_widget.horizontalHeaderItem(0)
        header.setData(1000, data)
        table_widget.setRowCount(len(data))
        for row, item in enumerate(data):
            # получение данных
            order_variable = item.get("order_variable") + 1
            name_variable = item.get("name_variable")
            title_variable = item.get("title_variable")
            type_variable = item.get("type_variable")
            # setData для строки
            qtwt_order_variable = NumericItem(str(order_variable))
            qtwt_order_variable.setData(Qt.UserRole, order_variable)
            qtwt_name_variable = QTableWidgetItem(name_variable)
            qtwt_name_variable.setData(1001, item)
            qtwt_title_variable = QTableWidgetItem(title_variable)
            qtwt_type_variable = QTableWidgetItem(type_variable)
            # Иконка и текст в зависимости от типа переменной
            qicon = self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(
                type_variable
            )
            qtwt_type_variable.setIcon(qicon)
            qtwt_type_variable.setText(type_variable)
            # Добавляем виджеты в ячейки таблицы
            table_widget.setItem(row, 0, qtwt_order_variable)
            table_widget.setItem(row, 1, qtwt_name_variable)
            table_widget.setItem(row, 2, qtwt_title_variable)
            table_widget.setItem(row, 3, qtwt_type_variable)
            #
            table_widget.item(row, 0).setTextAlignment(Qt.AlignCenter)
            # если editor
            if editor:
                self.item_tw_editor(
                    table_widget, item, row, type_table, count_all_variable_usages
                )
                table_widget.item(row, 4).setTextAlignment(Qt.AlignCenter)
                table_widget.item(row, 5).setTextAlignment(Qt.AlignCenter)
            # если open_variable
            if open_variable and open_variable.get("id_variable") == item.get(
                "id_variable"
            ):
                table_widget.selectRow(row)
                try:
                    if self.__qtimer:
                        self.__qtimer.stop()
                except Exception as e:
                    pass
                finally:
                    self.__qtimer = QTimer.singleShot(3000, lambda: table_widget.clearSelection())
        # включить сортировку после заполнения данных
        table_widget.setSortingEnabled(True)
        table_widget.sortByColumn(0, Qt.AscendingOrder)
        # Изменение размеров столбцов
        table_widget.resizeColumnsToContents()
        # Вертикальный ползунок
        vertical_scroll_position = self.__vertical_scroll_position_by_parameters.get(
            (type_table, editor), 0
        )
        table_widget.verticalScrollBar().setValue(vertical_scroll_position)


    def item_tw_editor(
        self, table_widget, item, row, type_table, count_all_variable_usages
    ):
        # количество использований
        id_variable = item.get("id_variable")
        usage_summary_by_id_variable = count_all_variable_usages.get(id_variable, 0)
        nodes_count = usage_summary_by_id_variable.get("nodes_count", 0)
        pages_count = usage_summary_by_id_variable.get("pages_count", 0)
        templates_count = usage_summary_by_id_variable.get("templates_count", 0)
        all_count = int(nodes_count) + int(pages_count) + int(templates_count)
        table_widget.setItem(row, 4, QTableWidgetItem(f"{all_count}"))
        # checkbox
        checkbtn = QCheckBox(text="вкл.")
        is_checked = item.get("_checked")
        if is_checked is None:
            is_checked = False
        checkbtn.setChecked(is_checked)
        # Добавляем значение для сортировки
        sort_value = "ДА" if is_checked else "НЕТ"
        table_widget.setItem(row, 5, QTableWidgetItem(sort_value))
        # кнопки
        edit_button = QPushButton()
        qicon_edit_button = self.__icons.get("pen")
        edit_button.setIcon(qicon_edit_button)
        #
        delete_button = QPushButton()
        qicon_delete_button = self.__icons.get("trash")
        delete_button.setIcon(qicon_delete_button)
        #
        edit_button.custom_data = item
        delete_button.custom_data = item
        # добавление кнопок в layout
        layout = QHBoxLayout()
        layout.addWidget(checkbtn)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.setContentsMargins(4, 0, 4, 0)
        widget = QWidget()
        widget.setLayout(layout)
        table_widget.setCellWidget(row, 6, widget)

        # обработчики
        edit_button.clicked.connect(partial(self.edit_variable, btn=edit_button))
        delete_button.clicked.connect(
            partial(self.delete_variable, btn=delete_button, type_table=type_table)
        )
        # для edit_variable
        if self.__edit_variable and id_variable == self.__edit_variable.get("id_variable"):
            self.__edit_button = edit_button


    def create_variable(self):
        """
        Похожий код у NedPageDialogWindow.
        """
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow create_variable()")
        result = self.ned_variable_dw("create")
        if result:
            # получить data
            data = self.__osbm.obj_nedtdw.get_data()
            name_variable = data.get("NAME")
            type_variable = data.get("TYPE")
            title_variable = data.get("TITLE")
            order_variable = data.get("ORDER")
            config_variable = data.get("CONFIG")
            config_variable = json.dumps(config_variable) if config_variable else None
            description_variable = data.get("DESCRIPTION")
            create_variable = {
                "name_variable": name_variable,
                "type_variable": type_variable,
                "title_variable": title_variable,
                "order_variable": order_variable,
                "config_variable": config_variable,
                "description_variable": description_variable,
            }
            # вставка
            self.__all_variables.insert(order_variable, create_variable)
            self.__osbm.obj_prodb.insert_variable(create_variable)
            # Меняем порядок в БД - кому нужно
            for index, variable in enumerate(self.__all_variables):
                order = variable.get("order_variable")
                if order != index:
                    self.__osbm.obj_prodb.set_order_for_variable(variable, index)
            # обновление таблиц + self.__all_variables
            type_table = self.get_typetable()
            self.caf_two_tables(type_table, create_variable)

    def edit_variable(self, btn):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow edit_variable(btn):\n btn = {btn}"
        )
        item = btn.custom_data
        result = self.ned_variable_dw("edit", item)
        if result:
            # получить data
            data = self.__osbm.obj_nedtdw.get_data()
            name_variable = data.get("NAME")
            type_variable = data.get("TYPE")
            title_variable = data.get("TITLE")
            order_variable = data.get("ORDER")
            config_variable = data.get("CONFIG")
            config_variable = json.dumps(config_variable) if config_variable else None
            description_variable = data.get("DESCRIPTION")
            edit_variable = {
                "id_variable": item.get("id_variable"),
                "name_variable": name_variable,
                "type_variable": type_variable,
                "title_variable": title_variable,
                "order_variable": order_variable,
                "config_variable": config_variable,
                "description_variable": description_variable,
            }
            # сортировочный процесс
            self.__all_variables.insert(order_variable, edit_variable)
            self.__all_variables.remove(item)
            # замена информации
            self.__osbm.obj_prodb.update_variable(edit_variable)
            # Меняем порядок в БД - кому нужно
            for index, variable in enumerate(self.__all_variables):
                order = variable.get("order_variable")
                if order != index:
                    self.__osbm.obj_prodb.set_order_for_variable(variable, index)
            # обновление таблиц + self.__all_variables
            type_table = self.get_typetable()
            self.caf_two_tables(type_table, edit_variable)

    def ned_variable_dw(self, type_window, variable=None):
        self.__osbm.obj_nedtdw = nedvariabledialogwindow.NedVariableDialogWindow(
            self.__osbm, type_window, self.__all_variables, variable
        )
        result = self.__osbm.obj_nedtdw.exec()
        return result == QDialog.Accepted

    def delete_variable(self, btn, type_table):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow delete_variable(btn, type_table):\nbtn = {btn}\ntype_table = {type_table}"
        )
        item = btn.custom_data
        title_variable = item.get("title_variable")
        name_variable = item.get("name_variable")
        question = self.__osbm.obj_dw.question_message(
            f'Вы действительно хотите удалить эту переменную:\n"{title_variable}" ({name_variable})?'
        )
        if question:
            # удалить из БД
            self.__all_variables.remove(item)
            self.__osbm.obj_prodb.delete_variable(item)
            # обновить порядок в БД - кому нужно
            for index, variable in enumerate(self.__all_variables):
                order = variable.get("order_variable")
                if order != index:
                    self.__osbm.obj_prodb.set_order_for_variable(variable, index)
            self.caf_two_tables(type_table)

    def get_current_data_table(self, type_table, editor=False):
        table_widget = self.get_table_by_parameters(type_table, editor)
        header = table_widget.horizontalHeaderItem(0)
        data = header.data(1000)
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_current_data_table(type_table, editor) -> list:\ntype_table = {type_table}\neditor = {editor}\ndata = {data}"
        )
        return data

    def get_new_data_editor_table(self, type_table):
        new_data = []
        table_widget_editor = self.get_table_by_parameters(type_table, True)
        row_count = table_widget_editor.rowCount()
        for row in range(row_count):
            item = table_widget_editor.item(row, 1).data(1001)
            checked = (
                table_widget_editor.cellWidget(row, 6).findChild(QCheckBox).isChecked()
            )
            if checked:
                item.pop("_checked")
                new_data.append(item)
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_new_data_editor_table(type_table) -> list:\ntype_table = {type_table}\nnew_data = {new_data}"
        )
        return new_data

    def save_changes(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow save_changes()")
        type_table = self.get_typetable()
        # получить данные
        new_data = self.get_new_data_editor_table(type_table)
        old_data = self.get_current_data_table(type_table, editor=False)
        # данные для удаления
        ids_new_data = {item.get("id_variable") for item in new_data}
        data_for_delete = [
            item for item in old_data if item.get("id_variable") not in ids_new_data
        ]
        # данные для добавления
        ids_old_data = {item.get("id_variable") for item in old_data}
        data_for_insert = [
            item for item in new_data if item.get("id_variable") not in ids_old_data
        ]
        # удаление и добавление
        if type_table == "project_variables":
            project_node = self.obj_projroject.project_node
            self.__osbm.obj_prodb.insert_node_datas(project_node, data_for_insert)
            self.__osbm.obj_prodb.delete_node_datas(project_node, data_for_delete)
        elif type_table == "group_variables":
            group_node = self.ui.combox_groups.currentData()
            if group_node:
                self.__osbm.obj_prodb.insert_node_datas(group_node, data_for_insert)
                self.__osbm.obj_prodb.delete_node_datas(group_node, data_for_delete)
        elif type_table == "form_template_page_variables":
            page = self.ui.combox_pages.currentData()
            if page is None:
                pass
            elif page == "all_pages":
                template = self.ui.combox_templates.currentData()
                if template:
                    self.__osbm.obj_prodb.insert_template_datas(
                        template, data_for_insert
                    )
                    self.__osbm.obj_prodb.delete_template_datas(
                        template, data_for_delete
                    )
            else:
                self.__osbm.obj_prodb.insert_page_datas(page, data_for_insert)
                self.__osbm.obj_prodb.delete_page_datas(page, data_for_delete)

        # обновление таблиц
        self.caf_two_tables(type_table)

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\neddw\nednodedialogwindow.py
``python
from PySide6.QtWidgets import QDialog, QSizePolicy
from PySide6.QtCore import Qt

import package.ui.nednodedialogwindow_ui as nednodedialogwindow_ui

class NedNodeDialogWindow(QDialog):
    def __init__(self, osbm, type_window, type_node, nodes, node=None):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow __init__(osbm, type_window, type_node, nodes, node):\ntype_window = {type_window}\ntype_node = {type_node}\nnodes = {nodes}\nnode = {node}"
        )
        self.__type_window = type_window
        self.__type_node = type_node
        self.__nodes = nodes
        self.__node = node
        super(NedNodeDialogWindow, self).__init__()
        self.ui = nednodedialogwindow_ui.Ui_NedNodeDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__osbm.obj_comwith.resizeqt.set_temp_max_height(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.__data = []
        # одноразовые действия
        self.config_maindata()
        self.fill_combox_parent()
        self.fill_combox_neighboor()
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def get_project_and_group_nodes(self) -> list:
        nodes = []
        for node in self.__nodes:
            if node.get("type_node") == "PROJECT" or node.get("type_node") == "GROUP":
                nodes.append(node)
        # сортирока
        nodes.sort(key=lambda node: int(node.get("order_node")))
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_project_and_group_nodes nodes = {nodes}"
        )
        return nodes


    def config_maindata(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow config_maindata()")
        if self.__type_window == "create":
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название новой формы")
                self.ui.btn_nesvariable.setText("Добавить форму")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название новой группы")
                self.ui.btn_nesvariable.setText("Добавить группу")
        elif self.__type_window == "edit":
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название формы")
                self.ui.btn_nesvariable.setText("Сохранить форму")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название группы")
                self.ui.btn_nesvariable.setText("Сохранить группу")
            # заполняем форму
            self.ui.lineedit_namenode.setText(self.__node.get("name_node"))


    def fill_combox_parent(self):
        self.__osbm.obj_logg.debug_logger(
            "NedNodeDialogWindow fill_combox_parent()"
        )
        combobox = self.ui.combox_parent
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        index = 0
        project_and_group_nodes = self.get_project_and_group_nodes()
        for prgr_node in project_and_group_nodes:
            # если create и вершины нет, то в добавить с корень дерева (Project) and not self.__node
            if self.__type_window == "create":
                combobox.addItem(prgr_node.get("name_node"), prgr_node)
                if self.__node and prgr_node.get("id_node") == self.__node.get(
                    "id_parent"
                ):
                    current_index = index
                index += 1
            elif self.__type_window == "edit":
                # поиск соседа
                if prgr_node.get("id_node") == self.__node.get("id_parent"):
                    current_index = index
                # проверка на одинаковые вершины
                if prgr_node.get("id_node") != self.__node.get("id_node"):
                    combobox.addItem(prgr_node.get("name_node"), prgr_node)
                    index += 1
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def get_childs(self, parent_node):
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_childs(parent_node):\nparent_node = {parent_node}"
        )
        # сортировка была сделана при получении данных с БД
        childs = list(
            filter(
                lambda node: node.get("id_parent") == parent_node.get("id_node"),
                self.__nodes,
            )
        )
        # сортировка тут нужна из-за reconfig()
        childs.sort(key=lambda node: int(node.get("order_node")))

        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_childs(parent_node):\nparent_node = {parent_node}\nchilds = {childs}"
        )
        return childs

    def fill_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow combox_neighboor()")
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        parent_node = self.ui.combox_parent.currentData()
        if parent_node:
            combobox.addItem("- В начало -", "START")
            childs_nodes = self.get_childs(parent_node)
            if self.__type_window == "create":
                for index, child_node in enumerate(childs_nodes):
                    combobox.addItem("После: " + child_node.get("name_node"), child_node)
                    # добавить в конец
                    current_index = index + 1
            else:
                for index, child_node in enumerate(childs_nodes):
                    if self.__node.get("id_node") != child_node.get("id_node"):
                        combobox.addItem("После: " + child_node.get("name_node"), child_node)
                    else:
                        current_index = index
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def connecting_actions(self):
        self.ui.btn_nesvariable.clicked.connect(self.action_nesvariable)
        self.ui.btn_nesvariable.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.combox_parent.currentIndexChanged.connect(self.fill_combox_neighboor)
        
    def action_nesvariable(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow action_nesvariable()")
        name_node = self.ui.lineedit_namenode.text()
        if len(name_node) > 0:
            node_by_name = self.__osbm.obj_prodb.get_node_by_name(name_node)
            print(f"node_by_name = {node_by_name}")
            if self.__type_window == "create":
                if not node_by_name:
                    self.add_new_node()
                    self.accept()
                else:
                    msg = "Другая вершина с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)
                
            elif self.__type_window == "edit":
                if not node_by_name:
                    self.save_edit_node()
                    self.accept()
                elif self.__node.get("name_node") == name_node:
                    # ↑ если имя переменной не изменилось
                    self.save_edit_node()
                    self.accept()
                else:
                    msg = "Другая вершина с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)
        else:
            msg = "Заполните поле названия!"
            self.__osbm.obj_dw.warning_message(msg)

    def save_edit_node(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow save_edit_node()")
        self.__data = []
        self.edit_data(True)

    def get_edit_old_nodes_when_is_edit(self, id_old_parent_node) -> list:
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_edit_old_nodes_when_is_edit(id_old_parent_node):\nid_old_parent_node = {id_old_parent_node}"
        )
        edit_old_nodes = []
        # обертка для функции
        old_parent_wrap_node = {
            "id_node": id_old_parent_node
        }
        old_childs_nodes = self.get_childs(old_parent_wrap_node)
        # цикл по старой группе
        index = 0
        for child_node in old_childs_nodes:
            if child_node.get("id_node") != self.__node.get("id_node"):
                child_node["order_node"] = index
                edit_old_nodes.append(child_node)
                index += 1
            else:
                # заменить пустышкой для childs_nodes.insert()
                edit_old_nodes.append("WRAPPER")
        return edit_old_nodes

    def edit_data(self, is_edit = True): 
        self.__osbm.obj_logg.debug_logger(f"NedNodeDialogWindow edit_data(is_edit):\nis_edit = {is_edit}")
        #
        id_old_parent_node = self.__node.get("id_parent")
        edit_old_nodes = []
        # для edit
        if is_edit:
            edit_old_nodes = self.get_edit_old_nodes_when_is_edit(id_old_parent_node)
        # для create
        new_parent_node = self.ui.combox_parent.currentData()
        if new_parent_node:
            id_new_parent_node = new_parent_node.get("id_node")
            # проверка на одинаковых родитилей
            childs_nodes = []
            if id_new_parent_node == id_old_parent_node:
                childs_nodes = edit_old_nodes
            else:
                # не забудем про изменения в старой группе
                for node in edit_old_nodes:
                    self.__data.append(node)
                # новая группа
                childs_nodes = self.get_childs(new_parent_node)
            # сосед в новой группе
            neighboor_node = self.ui.combox_neighboor.currentData()
            if neighboor_node:
                # вставка вершины в группу
                self.__node["name_node"] = self.ui.lineedit_namenode.text()
                self.__node["id_parent"] = new_parent_node.get("id_node")
                if neighboor_node == "START":
                    # вставить в самое начало
                    childs_nodes.insert(0, self.__node)
                else:
                    # вставить после соседа
                    neighboor_index = int(neighboor_node.get("order_node")) + 1
                    childs_nodes.insert(neighboor_index, self.__node)
                # цикл по новой группе
                index = 0
                for child_node in childs_nodes:
                    if child_node != "WRAPPER":
                        child_node["order_node"] = index
                        self.__data.append(child_node)
                        index += 1
        

    def add_new_node(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow add_new_node()")
        # подготовка данных
        self.__node = {
            "id_active_template": None,
            "id_node": -111,
            "id_parent": None,
            "included": 1,
            "name_node": None,
            "order_node": None,
            "type_node": self.__type_node,
        }
        # 
        self.__data = []
        self.edit_data(False)

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\neddw\nedpagedialogwindow.py
``python
from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QHeaderView,
)

from PySide6.QtCore import Qt

import package.ui.nedpagedialogwindow_ui as nedpagedialogwindow_ui

import package.components.dialogwindow.neddw.nedvariabledialogwindow as nedvariabledialogwindow

import json
import os
import datetime
from docxtpl import DocxTemplate
from functools import partial


class NedPageDialogWindow(QDialog):
    def __init__(self, osbm, type_ned, pages, page=None):
        self.__osbm = osbm
        self.__type_ned = type_ned
        self.__pages = pages
        self.__page = page
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow __init__(osbm, type_ned, page):\ntype_ned = {self.__type_ned}\npages = {self.__pages}\npage = {self.__page}"
        )
        super(NedPageDialogWindow, self).__init__()
        self.ui = nedpagedialogwindow_ui.Ui_NedPageDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.__select_filename = str()
        self.__temp_copy_file_path = str()
        self.__data = {
            "TEMP_COPY_FILE_PATH": None,
            "copy_page": None,
            "id_parent_template": None,
            "name_page": None,
            "filename_page": None,
            "typefile_page": None,
            "order_page": None,
            "included": 1,
        }
        self.__variables_for_add = []
        if self.__type_ned == "edit":
            self.__is_edit = True
        elif self.__type_ned == "create":
            self.__is_edit = False
        self.__typefile_page = None
        # одноразовые действия
        self.config_by_type_window()
        self.config_combox_neighboor()
        self.config_combox_pages()
        self.reconfig_is_edit()
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def set_active_find_variables(self, state):
        """найденные переменные"""
        self.ui.label_variables.setEnabled(state)
        self.ui.tw_variables.setEnabled(state)
        self.ui.btn_findvariables.setEnabled(state)

    def config_by_type_window(self):
        """
        по умолчанию
        """
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow config_by_type_window()")
        if self.__type_ned == "create":
            self.ui.lineedit_namepage.setText("")
            self.ui.btn_nedvariable.setText("Добавить страницу")
            self.__typefile_page = "DOCX"  # по умолчанию

        elif self.__type_ned == "edit":
            self.ui.lineedit_namepage.setText(self.__page.get("name_page"))
            self.ui.btn_nedvariable.setText("Сохранить страницу")
            # формат
            self.__typefile_page = self.__page.get("typefile_page")
            # Создать копию для редактирования
            self.do_temp_copy_for_edit(self.__page.get("filename_page"))

        # отключить найденные переменные
        self.set_active_find_variables(False)

    def reconfig_is_edit(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow reconfig_is_edit()")
        print(f"self.__is_edit = {self.__is_edit}")
        if not self.__is_edit:
            self.ui.btn_select.setText("Выбрать файл")
            self.ui.label_file.setText("Файл не выбран")
            self.ui.btn_open_docx.setEnabled(False)
        elif self.__is_edit:
            self.ui.btn_select.setText("Выбрать новый файл")
            self.ui.label_file.setText("Файл выбран")
            self.ui.btn_open_docx.setEnabled(True)
            # первоначальный self.__type_page определен в do_temp_copy_for_edit
            if self.__typefile_page == "DOCX":
                self.ui.btn_open_docx.setText("Открыть и редактировать docx")
                self.set_active_find_variables(True)
            elif self.__typefile_page == "PDF":
                self.ui.btn_open_docx.setText("Открыть pdf")
                self.set_active_find_variables(False)

    def config_combox_pages(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow config_combox_pages()")
        combobox = self.ui.combox_pages
        if self.__type_ned == "create":
            combobox.blockSignals(True)
            combobox.clear()
            combobox.addItem("- Пустая страница -", "empty")
            for elem in self.__pages:
                combobox.addItem(elem.get("name_page"), elem)
            combobox.setCurrentIndex(0)
            combobox.blockSignals(False)
            combobox.currentIndexChanged.connect(self.select_copy_page)
            self.select_copy_page(0)

        elif self.__type_ned == "edit":
            # комбобокс отключить
            self.ui.label_copyfrom.setEnabled(False)
            self.ui.combox_pages.setEnabled(False)

    def select_copy_page(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow select_copy_page():\nindex = {index}"
        )
        if index == 0:
            self.ui.label_document.setEnabled(True)
            self.ui.btn_select.setEnabled(True)
            if self.__is_edit:
                self.ui.btn_open_docx.setEnabled(True)
            else:
                self.ui.btn_open_docx.setEnabled(False)
            self.ui.label_file.setEnabled(True)
            self.ui.label_variables.setEnabled(True)
            self.ui.tw_variables.setEnabled(True)
            self.ui.btn_findvariables.setEnabled(True)
        else:
            self.ui.label_document.setEnabled(False)
            self.ui.btn_select.setEnabled(False)
            self.ui.btn_open_docx.setEnabled(False)
            self.ui.label_file.setEnabled(False)
            self.ui.label_variables.setEnabled(False)
            self.ui.tw_variables.setEnabled(False)
            self.ui.btn_findvariables.setEnabled(False)

    def config_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger(
            "NedPageDialogWindow config_combox_neighboor()"
        )
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        # по умолчанию - в конец
        flag = True
        combobox.addItem("- В начало -", "START")
        for index, page in enumerate(self.__pages):
            if self.__page and self.__page.get("id_page") == page.get("id_page"):
                flag = False
            else:
                combobox.addItem(page.get("name_page"), page)
            if flag:
                current_index = index + 1
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow connecting_actions()")
        self.ui.btn_select.clicked.connect(self.select_new_file)
        self.ui.btn_open_docx.setShortcut("Ctrl+O")
        self.ui.btn_open_docx.clicked.connect(self.open_edit_docxpdf)
        self.ui.btn_open_docx.setShortcut("Ctrl+E")
        self.ui.btn_nedvariable.clicked.connect(self.btn_nedvariable_clicked)
        self.ui.btn_nedvariable.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_findvariables.clicked.connect(self.reconfig_tw_variables)
        self.ui.btn_findvariables.setShortcut("Ctrl+F")

    def reconfig_tw_variables(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow reconfig_tw_variables()")
        tablewidget = self.ui.tw_variables
        scroll_value = tablewidget.verticalScrollBar().value()
        tablewidget.blockSignals(True)
        tablewidget.clearContents()
        tablewidget.setRowCount(0)
        # если выбран временный файл
        if self.__temp_copy_file_path and self.__typefile_page == "DOCX":
            jinja_variables = self.extract_jinja_variables(self.__temp_copy_file_path)
            if jinja_variables:
                self.fill_tw_variables(jinja_variables)
        tablewidget.verticalScrollBar().setValue(scroll_value)
        tablewidget.blockSignals(False)

    def clear_tw_variables(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow clear_tw_variables()")
        tablewidget = self.ui.tw_variables
        tablewidget.blockSignals(True)
        tablewidget.clearContents()
        tablewidget.setRowCount(0)
        tablewidget.blockSignals(False)

    def fill_tw_variables(self, jinja_variables):
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow fill_tw_variables(jinja_variables):\njinja_variables = {jinja_variables}"
        )
        tablewidget = self.ui.tw_variables
        tablewidget.setColumnCount(2)
        tablewidget.setHorizontalHeaderLabels(["Переменная", "Действия"])
        tablewidget.setRowCount(len(jinja_variables))
        for row, name_variable in enumerate(jinja_variables):
            qtwt_name_variable = QTableWidgetItem(name_variable)
            tablewidget.setItem(row, 0, qtwt_name_variable)
            # кнопка действия
            layout = QHBoxLayout()
            add_button = QPushButton("...")
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(add_button)
            widget = QWidget()
            widget.setLayout(layout)
            #
            result_bd = self.__osbm.obj_prodb.get_variable_by_name(name_variable)
            result_variables_for_add = self.get_variable_by_name(name_variable)
            if result_bd:
                tablewidget.setItem(row, 1, QTableWidgetItem("Имеется"))
            elif result_variables_for_add:
                tablewidget.setItem(row, 1, QTableWidgetItem("Добавлена"))
            else:
                add_button.setText("Добавить переменную")
                add_button.clicked.connect(partial(self.add_variable, name_variable))
                tablewidget.setCellWidget(row, 1, widget)
        # Настраиваем режимы изменения размера для заголовков
        header = tablewidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #
        tablewidget.setSortingEnabled(True)
        tablewidget.resizeColumnsToContents()
        tablewidget.setEditTriggers(QTableWidget.NoEditTriggers)
        tablewidget.setSelectionMode(QAbstractItemView.NoSelection)

    def get_variable_by_name(self, name_variable) -> dict:
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow get_variable_by_name(name_variable) -> dict:\nname_variable = {name_variable}"
        )
        variables = self.__variables_for_add
        result = None
        for variable in variables:
            if variable.get("name_variable") == name_variable:
                result = variable
                break
        return result

    def add_variable(self, name_variable):
        """
        Похожий код у VariablesListDialogWindow.
        """
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow add_variable(variable, name_variable):\nname_variable = {name_variable}"
        )
        self.__all_variables = self.__osbm.obj_prodb.get_variables()
        # окно
        self.__osbm.obj_nedtdw = nedvariabledialogwindow.NedVariableDialogWindow(
            self.__osbm, "create", self.__all_variables, None, name_variable
        )
        result = self.__osbm.obj_nedtdw.exec()
        # результат
        if result == QDialog.Accepted:
            # получить data
            data = self.__osbm.obj_nedtdw.get_data()
            name_variable = data.get("NAME")
            type_variable = data.get("TYPE")
            title_variable = data.get("TITLE")
            order_variable = data.get("ORDER")
            config_variable = data.get("CONFIG")
            config_variable = json.dumps(config_variable) if config_variable else None
            description_variable = data.get("DESCRIPTION")
            create_variable = {
                "name_variable": name_variable,
                "type_variable": type_variable,
                "title_variable": title_variable,
                "order_variable": order_variable,
                "config_variable": config_variable,
                "description_variable": description_variable,
            }
            # вставка
            self.__all_variables.insert(order_variable, create_variable)
            self.__osbm.obj_prodb.insert_variable(create_variable)
            # Меняем порядок в БД - кому нужно
            for index, variable in enumerate(self.__all_variables):
                order = variable.get("order_variable")
                if order != index:
                    self.__osbm.obj_prodb.set_order_for_variable(variable, index)
            # обновляем таблицу
            self.reconfig_tw_variables()

    def extract_jinja_variables(self, docx_path) -> set:
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow extract_jinja_variables(docx_path) -> set:\ndocx_path = {docx_path}"
        )
        try:
            docx_template = DocxTemplate(docx_path)
            set_of_variables = docx_template.get_undeclared_template_variables()
            sorted_set_of_variables = sorted(
                set_of_variables, key=lambda x: x.lower()
            )
            return sorted_set_of_variables
        except Exception as error:
            self.__osbm.obj_logg.error_logger(
                f"NedPageDialogWindow extract_jinja_variables(docx_path) -> set:\nerror = {error}"
            )
            self.__osbm.obj_dw.warning_message(
                f"Ошибка в поиске переменных в выбранном документе:\n{error}"
            )
            return set()

    def do_temp_copy_for_edit(self, old_filename_page):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow do_copy_for_edit()")
        try:
            # определить формат
            if self.__typefile_page == "DOCX":
                file_format = ".docx"
            elif self.__typefile_page == "PDF":
                file_format = ".pdf"
            # образуем новое название документа
            file_name = f"{self.__typefile_page}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            self.__select_filename = file_name
            file_name_with_format = f"{file_name}{file_format}"
            # edit документ - как бы старый
            old_page_path = str()
            if self.__typefile_page == "DOCX":
                forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
                old_page_path = os.path.join(
                    forms_folder_dirpath, old_filename_page + ".docx"
                )
            elif self.__typefile_page == "PDF":
                pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
                old_page_path = os.path.join(
                    pdfs_folder_dirpath, old_filename_page + ".pdf"
                )
            # временный - как бы новый
            temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
            self.__temp_copy_file_path = os.path.join(temp_dir, file_name_with_format)
            # копирование
            self.__osbm.obj_film.copy_file(old_page_path, self.__temp_copy_file_path)
        except Exception as error:
            self.__osbm.obj_logg.error_logger(
                f"NedPageDialogWindow do_temp_copy_for_edit():\nerror = {error}"
            )
            self.__osbm.obj_dw.warning_message(
                f"Ошибка копирования документа:\n{error}"
            )

    def select_new_file(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow select_new_file()")
        docxpdf_path = self.__osbm.obj_dw.select_docx_or_pdf_file()
        if docxpdf_path:
            try:
                # формат
                file_format = os.path.splitext(docxpdf_path)[1]
                if file_format == ".docx":
                    self.__typefile_page = "DOCX"
                elif file_format == ".pdf":
                    self.__typefile_page = "PDF"
                # образуем новое название документа
                file_name = f"{self.__typefile_page}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
                self.__select_filename = file_name
                file_name_with_format = f"{file_name}{file_format}"
                # пути + копирование
                temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
                self.__temp_copy_file_path = os.path.join(
                    temp_dir, file_name_with_format
                )
                self.__osbm.obj_film.copy_file(docxpdf_path, self.__temp_copy_file_path)
                # файл выбран
                self.__is_edit = True
                self.ui.label_file.setText("Файл выбран")
                self.reconfig_is_edit()
                if self.__typefile_page == "DOCX":
                    self.reconfig_tw_variables()
                else:
                    self.clear_tw_variables()
            except Exception as error:
                self.__osbm.obj_logg.error_logger(
                    f"NedPageDialogWindow select_new_file():\nerror = {error}"
                )
                self.__osbm.obj_dw.warning_message(
                    f"Ошибка копирования документа:\n{error}"
                )

    def open_edit_docxpdf(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow open_edit_docx()")
        try:
            # путь к документу
            docx_path = self.__temp_copy_file_path
            # открытие
            if os.path.exists(docx_path):
                app_converter = self.__osbm.obj_settings.get_app_converter()
                try:
                    if self.__typefile_page == "DOCX" and app_converter == "MSWORD":
                        # запустить в отдельном потоке
                        self.__osbm.obj_offp.run_individual_msword()
                    os.startfile(docx_path)
                except OSError:
                    raise Exception("Не удалось открыть.")
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)
            self.__osbm.obj_dw.warning_message("Не удалось открыть документ")

    def find_page_by_namepage_in_pages(self, namepage) -> object:
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow find_page_by_namepage_in_pages(namepage):\nnamepage = {namepage}"
        )
        for current_page in self.__pages:
            if current_page.get("name_page") == namepage:
                return current_page
        return None

    def btn_nedvariable_clicked(self):
        self.__osbm.obj_logg.debug_logger(
            "NedPageDialogWindow btn_nedvariable_clicked()"
        )
        select_filename_page = self.__select_filename
        namepage = self.ui.lineedit_namepage.text()
        copy_page = self.ui.combox_pages.currentData()
        if len(namepage) > 0 and (
            len(select_filename_page) > 0 or copy_page != "empty"
        ):
            # поиск по имени
            find_page = self.find_page_by_namepage_in_pages(namepage)
            # выбранный сосед
            neighboor_page = self.ui.combox_neighboor.currentData()
            order_page = (
                0 if neighboor_page == "START" else neighboor_page.get("order_page") + 1
            )
            if self.__type_ned == "create":
                if find_page is None:
                    self.__data["name_page"] = namepage
                    self.__data["filename_page"] = select_filename_page
                    self.__data["typefile_page"] = self.__typefile_page
                    self.__data["order_page"] = order_page
                    self.__data["TEMP_COPY_FILE_PATH"] = self.__temp_copy_file_path
                    self.__data["copy_page"] = copy_page
                    self.accept()
                else:
                    msg = "Другая страница с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)

            elif self.__type_ned == "edit":
                if find_page is None:
                    self.__data = self.__page
                    self.__data["name_page"] = namepage
                    self.__data["filename_page"] = select_filename_page
                    self.__data["typefile_page"] = self.__typefile_page
                    self.__data["order_page"] = order_page
                    self.__data["TEMP_COPY_FILE_PATH"] = self.__temp_copy_file_path
                    self.accept()
                elif namepage == self.__page.get("name_page"):
                    self.__data = self.__page
                    self.__data["name_page"] = namepage
                    self.__data["filename_page"] = select_filename_page
                    self.__data["typefile_page"] = self.__typefile_page
                    self.__data["order_page"] = order_page
                    self.__data["TEMP_COPY_FILE_PATH"] = self.__temp_copy_file_path
                    self.accept()
                else:
                    msg = "Другая страница с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)
        elif namepage == "":
            self.__osbm.obj_dw.warning_message("Заполните поле названия")
        elif select_filename_page is None or len(select_filename_page) == 0:
            self.__osbm.obj_dw.warning_message("Выберите документ")
        else:
            self.__osbm.obj_dw.warning_message(
                "Заполните поле названия и выберите документ"
            )

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\neddw\nedrowcoldialogwindow.py
``python
import re

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

import package.ui.nedrowcoldialogwindow_ui as nedrowcoldialogwindow_ui

class NedRowcolDialogWindow(QDialog):
    def __init__(self, osbm, type_ned, type_rowcol, rowcols, rowcol=None):
        self.__osbm = osbm
        self.__type_ned = type_ned
        self.__type_rowcol = type_rowcol
        self.__rowcols = rowcols
        self.__rowcol = rowcol
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow __init__(osbm, type_ned, rowcols, rowcol): \n self.__type_ned = {self.__type_ned} \n self.__rowcols = {self.__rowcols} \n self.__rowcol = {self.__rowcol}"
        )
        super(NedRowcolDialogWindow, self).__init__()
        self.ui = nedrowcoldialogwindow_ui.Ui_NedRowcolDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__osbm.obj_comwith.resizeqt.set_temp_max_height(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.__data = dict()
        # одноразовые действия
        self.config_by_type_window()
        self.config_combox_neighboor()
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger(
            "NedRowcolDialogWindow config_by_type_window()"
        )
        if self.__type_ned == "create":
            if self.__type_rowcol == "ROW":
                self.ui.label_attr.setText("<b>Атрибут новой строки</b>")
                self.ui.label_rowcol.setText("Название (заголовок) новой строки")
                self.ui.btn_nesvariable.setText("Добавить строку")
            elif self.__type_rowcol == "COL":
                self.ui.label_attr.setText("<b>Атрибут нового столбца</b>")
                self.ui.label_rowcol.setText("Название (заголовок) нового столбца")
                self.ui.btn_nesvariable.setText("Добавить столбец")
        elif self.__type_ned == "edit":
            if self.__type_rowcol == "ROW":
                self.ui.label_attr.setText("<b>Атрибут строки</b>")
                self.ui.label_rowcol.setText("Название (заголовок) строки")
                self.ui.btn_nesvariable.setText("Изменить строку")
            elif self.__type_rowcol == "COL":
                self.ui.label_attr.setText("<b>Атрибут столбца</b>")
                self.ui.label_rowcol.setText("Название (заголовок) столбца")
                self.ui.btn_nesvariable.setText("Изменить столбец")
            #
            self.ui.lineedit_attr.setText(self.__rowcol.get("ATTR"))
            self.ui.lineedit_rowcoltitle.setText(self.__rowcol.get("TITLE"))

    def get_order_rowcol(self, current_rowcol):
        result = -1
        for index, rowcol in enumerate(self.__rowcols):
            if rowcol.get("ID") == current_rowcol.get("ID"):
                result = index
                break
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow get_order_rowcol():\n current_rowcol = {current_rowcol} \n result = {result}"
        )
        return result

    def config_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger(
            "NedRowcolDialogWindow config_combox_templates()"
        )
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        # по умолчанию - в конец
        current_index = 0
        flag = True
        combobox.addItem("- В начало -", "START")
        for index, rowcol in enumerate(self.__rowcols):
            if self.__rowcol and rowcol.get("ID") == self.__rowcol.get("ID"):
                flag = False
            else:
                combobox.addItem(rowcol.get("ATTR"), rowcol)
            if flag:
                current_index = index + 1
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow connecting_actions()")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_nesvariable.clicked.connect(self.btn_nesvariable_clicked)
        self.ui.btn_nesvariable.setShortcut("Ctrl+S")

    def get_is_valid_jinja_attr(self, name_attr):
        pattern = r'^[А-яЁёA-z0-9_]+$'
        result = bool(re.match(pattern, name_attr))
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow get_is_valid_jinja_attr(name_variable):\n name_attr = {name_attr} \n result = {result}"
        )
        return result

    def btn_nesvariable_clicked(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow btn_nesvariable_clicked()")
        le_attr = self.ui.lineedit_attr.text()
        le_rowcoltitle = self.ui.lineedit_rowcoltitle.text()
        # проверка на пустоту (уникальность присутствует)
        is_valid_jinja_attr = self.get_is_valid_jinja_attr(le_attr)
        if len(le_attr) > 0 and len(le_rowcoltitle) > 0 and is_valid_jinja_attr:
            # заполняем словарь
            data = self.ui.combox_neighboor.currentData()
            order = data.get("ORDER") + 1 if data != "START" else 0
            self.__data = {
                "ATTR": le_attr,
                "TITLE": le_rowcoltitle,
                "ORDER": order                                                                                                                                                            
            }
            # пытаемся accept()
            if self.__type_ned == "create":
                self.add_new_rowcol()
            elif self.__type_ned == "edit":
                self.save_edit_rowcol()
        elif le_attr == "" and le_rowcoltitle == "" and is_valid_jinja_attr:
            self.__osbm.obj_dw.warning_message("Заполните все поля")
        elif le_attr == "":
            self.__osbm.obj_dw.warning_message("Заполните поле атрибута")
        elif le_rowcoltitle == "":
            self.__osbm.obj_dw.warning_message("Заполните поле названия атрибута")
        elif not is_valid_jinja_attr:
            self.__osbm.obj_dw.warning_message(
                "Атрибут переменной содержит недопустимые символы."
            )

    def get_rowcol_by_name(self, name_attr):
        for rowcol in self.__rowcols:
            if rowcol.get("ATTR") == name_attr:
                return rowcol
        return None

    def add_new_rowcol(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow add_new_rowcol()")
        le_attr = self.ui.lineedit_attr.text()
        # Проверка на уникальность
        name_attr = self.get_rowcol_by_name(le_attr)
        if name_attr:
            self.__osbm.obj_dw.warning_message("Такой атрибут уже существует.")
        else:
            self.accept()

    def save_edit_rowcol(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow save_edit_rowcol()")
        # Проверка на уникальность
        le_attr = self.ui.lineedit_attr.text()
        old_le_attr = self.__rowcol.get("ATTR")
        name_attr = self.get_rowcol_by_name(le_attr)
        if le_attr == old_le_attr:
            # ↑ если имя переменной не изменилось
            self.accept()
        elif name_attr:
            self.__osbm.obj_dw.warning_message("Такой атрибут уже существует.")
        else:
            self.accept()

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\neddw\nedtemplatedialogwindow.py
``python
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

import package.ui.nedtemplatedialogwindow_ui as nedtemplatedialogwindow_ui

class NedTemplateDialogWindow(QDialog):
    def __init__(self, osbm, type_ned, templates, template=None, is_active = False):
        self.__osbm = osbm
        self.__type_ned = type_ned
        self.__templates = templates
        self.__template = template
        self.__is_active = is_active
        self.__osbm.obj_logg.debug_logger(
            f"NedTemplateDialogWindow __init__(osbm, type_ned):\ntype_ned = {type_ned},\ntemplates = {templates}\ntemplate = {template}"
        )
        super(NedTemplateDialogWindow, self).__init__()
        self.ui = nedtemplatedialogwindow_ui.Ui_NedTemplateDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__osbm.obj_comwith.resizeqt.set_temp_max_height(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.__data = dict()
        # одноразовые действия
        self.config_by_type_window()
        self.config_is_active()
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedTemplateDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow config_by_type_window()"
        )
        if self.__type_ned == "create":
            self.ui.label_nametemplate.setText("Название нового шаблона")
            self.ui.btn_nesvariable.setText("Добавить шаблон")
            # предложение включено
            self.ui.label_copyfrom.setEnabled(True)
            self.ui.combox_templates.setEnabled(True)
            # заполнить комбобокс
            self.config_combox_templates()
        elif self.__type_ned == "edit":
            self.ui.label_nametemplate.setText("Название шаблона")
            self.ui.lineedit_nametemplate.setText(self.__template.get("name_template"))
            self.ui.btn_nesvariable.setText("Сохранить шаблон")
            # предложение отключено
            self.ui.label_copyfrom.setEnabled(False)
            self.ui.combox_templates.setEnabled(False)

    def config_is_active(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow config_is_active()"
        )
        if self.__type_ned == "create":
            if self.__templates:
                self.ui.checkbox_is_active.setChecked(False)
                self.ui.checkbox_is_active.setEnabled(True)
            else:
                # если self.__templates пуст, то автоматически включено
                self.ui.checkbox_is_active.setChecked(True)
                self.ui.checkbox_is_active.setEnabled(False)

        elif self.__type_ned == "edit":
            if self.__is_active:
                self.ui.checkbox_is_active.setChecked(True)
                self.ui.checkbox_is_active.setEnabled(False)
            else:
                self.ui.checkbox_is_active.setChecked(False)
                self.ui.checkbox_is_active.setEnabled(True)

            
            
            # id_template = template.get("id_template")
            
    
    def config_combox_templates(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow config_combox_templates()"
        )
        combobox = self.ui.combox_templates
        combobox.blockSignals(True)
        combobox.clear()
        combobox.addItem("- Пустой шаблон -", "empty")
        for elem in self.__templates:
            combobox.addItem(elem.get("name_template"), elem)
        combobox.blockSignals(False)


    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow connecting_actions()"
        )
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_nesvariable.clicked.connect(self.btn_nesvariable_clicked)
        self.ui.btn_nesvariable.setShortcut("Ctrl+S")

    def btn_nesvariable_clicked(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow btn_nesvariable_clicked()"
        )
        nametemplate = self.ui.lineedit_nametemplate.text()
        self.__data["IS_ACTIVE"] = self.ui.checkbox_is_active.isChecked()
        self.__data["name_template"] = nametemplate
        # для create
        if self.__type_ned == "create":
            copytemplate = self.ui.combox_templates.currentData()
            if copytemplate:
                self.__data["copy_template"] = copytemplate
        # проверка ОБЩАЯ
        if len(nametemplate) > 0:
            self.accept()
        else:
            self.__osbm.obj_dw.warning_message("Заполните поле названия")
``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\neddw\nedvariabledialogwindow.py
``python
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, Qt

import re
import json

import package.ui.nedvariabledialogwindow_ui as nedvariabledialogwindow_ui

import package.components.widgets.nedvariables.neddatevariable as neddatevariable
import package.components.widgets.nedvariables.nedtablevariable as nedtablevariable
import package.components.widgets.nedvariables.nedimagevariable as nedimagevariable

class NedVariableDialogWindow(QDialog):
    def __init__(self, osbm, type_window, variables, variable=None, name_variable = None):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow(osbm, type_window):\ntype_window = {type_window}\nvariable = {variable}"
        )
        self.__type_window = type_window
        self.__variables = variables
        self.__variable = variable
        self.__name_variable = name_variable
        super(NedVariableDialogWindow, self).__init__()
        self.ui = nedvariabledialogwindow_ui.Ui_NedVariableDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        # одноразовые действия
        self.__additional_widget = None
        self.__data = {
            "NAME": None,
            "TYPE": None,
            "TITLE": None,
            "ORDER": None,
            "CONFIG": {},
            "DESCRIPTION": {},
            "copy_variable": None,
        }
        self.config_combox_typevariable()
        self.config_combox_neighboor()
        self.config_combox_copyvariables()
        self.config_by_type_window()
        # многоразовые действия
        self.update_additional_info()
        # подключаем действия
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger(
            "NedVariableDialogWindow config_combox_neighboor()"
        )
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        # по умолчанию - в конец
        current_index = 0
        flag = True
        combobox.addItem("- В начало -", "START")
        for index, variable in enumerate(self.__variables):
            if self.__variable and self.__variable.get("id_variable") == variable.get("id_variable"):
                flag = False
            else:
                combobox.addItem(f'{variable.get("order_variable")+1}) {variable.get("name_variable")}', variable)
            if flag:
                current_index = index + 1
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def config_combox_copyvariables(self):
        if self.__type_window == "create":
            self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow config_combox_copyvariables()")
            combobox = self.ui.combox_copyvariables
            combobox.blockSignals(True)
            combobox.clear()
            # по умолчанию - начало
            combobox.addItem("- Пустая переменная -", "empty")
            for index, variable in enumerate(self.__variables):
                combobox.addItem(f'{variable.get("order_variable")+1}) {variable.get("name_variable")}', variable)
            combobox.setCurrentIndex(0)
            combobox.blockSignals(False)
        else:
            self.ui.label_copyfrom.setEnabled(False)
            self.ui.combox_copyvariables.setEnabled(False)


    def on_combox_copyvariables_changed(self, index):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow on_combox_copyvariables_changed()")
        copy_variable = self.ui.combox_copyvariables.itemData(index)
        if index == 0:
            self.ui.typevariable.setEnabled(True)
            self.ui.combox_typevariable.setEnabled(True)
            self.update_additional_info()
        else:
            self.ui.typevariable.setEnabled(False)
            self.ui.combox_typevariable.setEnabled(False)
            index = self.__osbm.obj_comwith.variable_types.get_index_by_data(
                copy_variable.get("type_variable")
            )
            self.ui.combox_typevariable.setCurrentIndex(index)
            self.update_additional_info(None, False)
            

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow connecting_actions()")
        self.ui.combox_typevariable.currentIndexChanged.connect(
            self.on_combox_typevariable_changed
        )
        #
        self.ui.combox_copyvariables.currentIndexChanged.connect(
            self.on_combox_copyvariables_changed
        )
        #
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_nesvariable.clicked.connect(self.btn_nesvariable_clicked)
        self.ui.btn_nesvariable.setShortcut("Ctrl+S")


    def get_is_valid_jinja_variable(self, name_variable):
        pattern = r'^[А-яЁёA-z0-9_]+$' 
        result = bool(re.match(pattern, name_variable))
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow get_is_valid_jinja_variable(name_variable):\name_variable = {name_variable}\n result = {result}"
        )
        return result


    def btn_nesvariable_clicked(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow btn_nesvariable_clicked()")
        le_namevariable = self.ui.lineedit_namevariable.text()
        le_titlevariable = self.ui.lineedit_titlevariable.text()
        # проверка на пустоту (уникальность присутствует)
        is_valid_jinja_variable = self.get_is_valid_jinja_variable(le_namevariable)
        if len(le_namevariable) > 0 and len(le_titlevariable) > 0 and is_valid_jinja_variable:
            # copy_variable 
            copy_variable = self.ui.combox_copyvariables.currentData()
            print(f"copy_variable = {copy_variable}")
            if copy_variable == "empty" or copy_variable is None:
                # получит config_variable в зависимости от типа переменной
                type_variable = self.ui.combox_typevariable.currentData()
                if type_variable == "TEXT" or type_variable == "LONGTEXT" or type_variable == "LIST":
                    config_variable = {}
                else:
                    config_variable = self.__additional_widget.get_save_data()
            else:
                type_variable = copy_variable.get("type_variable")
                config_copy_variable = copy_variable.get("config_variable")
                config_copy_variable = config_copy_variable if config_copy_variable else "{}"
                config_variable = json.loads(config_copy_variable)
            neighboor_data = self.ui.combox_neighboor.currentData()
            print(f"neighboor_data = {neighboor_data}")
            order_variable = int(neighboor_data.get("order_variable")) + 1 if neighboor_data != "START" else 0
            self.__data = {
                "NAME": le_namevariable,
                "TYPE": type_variable,
                "TITLE": le_titlevariable,
                "ORDER": order_variable,
                "CONFIG": config_variable,
                "DESCRIPTION": ""
            }
            # пытаемся accept
            if self.__type_window == "create":
                self.add_new_variable()
            elif self.__type_window == "edit":
                self.save_edit_variable()
        elif le_namevariable == "" and le_titlevariable == "" and is_valid_jinja_variable:
            self.__osbm.obj_dw.warning_message("Заполните все поля.")
        elif le_namevariable == "":
            self.__osbm.obj_dw.warning_message("Заполните поле переменной.")
        elif le_titlevariable == "":
            self.__osbm.obj_dw.warning_message("Заполните поле названия переменной.")
        elif not is_valid_jinja_variable:
            self.__osbm.obj_dw.warning_message("Переменная содержит недопустимые символы.")

    def add_new_variable(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow add_new_variable()")
        # проверка на уникальность
        le_namevariable = self.ui.lineedit_namevariable.text()
        name_variable = self.__osbm.obj_prodb.get_variable_by_name(le_namevariable)
        if name_variable:
            self.__osbm.obj_dw.warning_message("Переменная с таким именем уже существует.")
        else:
            self.accept()

    def save_edit_variable(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow save_edit_variable()")
        # проверка на уникальность
        le_namevariable = self.ui.lineedit_namevariable.text()
        old_name_variable = self.__variable.get("name_variable")
        name_variable = self.__osbm.obj_prodb.get_variable_by_name(le_namevariable)
        if le_namevariable == old_name_variable:
            # ↑ если имя переменной не изменилось
            self.accept()
        elif name_variable:
            self.__osbm.obj_dw.warning_message("Переменная с таким именем уже существует.")
        else:
            self.accept()

    def on_combox_typevariable_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow on_combox_typevariable_changed(index):\nindex = {index}"
        )
        self.update_additional_info(index)

    def config_combox_typevariable(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow config_combox_typevariable()")
        self.ui.combox_typevariable.blockSignals(True)
        self.ui.combox_typevariable.clear()
        variable_types = self.__osbm.obj_comwith.variable_types.get_variable_types()
        for variable in variable_types:
            self.ui.combox_typevariable.addItem(variable.icon, variable.name, variable.data)
        #
        if self.__variable:
            index = self.__osbm.obj_comwith.variable_types.get_index_by_data(
                self.__variable.get("type_variable")
            )
            self.ui.combox_typevariable.setCurrentIndex(index)
        self.ui.combox_typevariable.blockSignals(False)

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow config_by_type_window()")
        if self.__type_window == "create":
            self.ui.btn_nesvariable.setText("Добавить переменную")
            # для NedPageDialogWindow
            if self.__name_variable:
                self.ui.lineedit_namevariable.setText(self.__name_variable)

        elif self.__type_window == "edit":
            self.ui.btn_nesvariable.setText("Сохранить переменную")
            self.ui.lineedit_namevariable.setText(self.__variable.get("name_variable"))
            self.ui.lineedit_titlevariable.setText(self.__variable.get("title_variable"))



    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def update_additional_info(self, index=None, is_show = True):
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow config_additional_info(index):\nindex = {index}"
        )
        self.clear_layout(self.ui.vbl_additional_info)
        self.__additional_widget = None
        if is_show:
            if index is None:
                if self.__variable:
                    index = self.__osbm.obj_comwith.variable_types.get_index_by_data(
                        self.__variable.get("type_variable")
                    )
                else:
                    index = 0
            #
            data = self.__osbm.obj_comwith.variable_types.get_data_by_index(index)
            if data == "DATE":
                self.__additional_widget = neddatevariable.NedDateVariable(
                    self.__osbm, self.__type_window, self.__variable
                )
                self.ui.vbl_additional_info.addWidget(self.__additional_widget)
            elif data == "TABLE":
                self.__additional_widget = nedtablevariable.NedTableVariable(
                    self.__osbm, self.__type_window, self.__variable
                )
                self.ui.vbl_additional_info.addWidget(self.__additional_widget)
            elif data == "IMAGE":
                self.__additional_widget = nedimagevariable.NedImageVariable(
                    self.__osbm, self.__type_window, self.__variable
                )
                self.ui.vbl_additional_info.addWidget(self.__additional_widget)
            #
        QTimer.singleShot(
            0, self, lambda: self.__osbm.obj_comwith.resizeqt.set_temp_max_height(self)
        )

``
### D:\vs_projects\auto-exec-doc\package\components\dialogwindow\neddw\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\customitemqlistwidget.py
``python
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

import package.ui.customitemqlistwidget_ui as customitemqlistwidget_ui


class CustomItemQListWidget(QWidget):
    def __init__(self, osbm, type_window, data, is_active=False):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__data = data
        self.__is_active = is_active
        self.__osbm.obj_logg.debug_logger(
            f"CustomItemQListWidget __init__(osbm, data):\nosbm = {osbm}\ntype_window = {type_window}\ndata = {data}"
        )
        super(CustomItemQListWidget, self).__init__()
        self.ui = customitemqlistwidget_ui.Ui_CustomItemQListWidget()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        # конфигурация
        self.config()

    def config(self):
        text = str()
        self.ui.horizontalLayout.setContentsMargins(4, 2, 2, 2)
        self.ui.horizontalLayout.setSpacing(2)
        #
        if self.__type_window == "TEMPLATE":
            text = self.__data.get("name_template")
        #
        elif self.__type_window == "PAGE":
            text = self.__data.get("name_page")
        #
        elif self.__type_window == "ROWCOLS":
            text = f'{self.__data.get("TITLE")} ({self.__data.get("ATTR")})'
        # формат
        if self.__is_active:
            self.ui.label_text.setText(f"<b><u>{text}</u></b>")
        else:
            self.ui.label_text.setText(text)


    def get_btn_edit(self):
        self.__osbm.obj_logg.debug_logger("CustomItemQListWidget get_btn_edit()")
        return self.ui.btn_edit

    def get_btn_delete(self):
        self.__osbm.obj_logg.debug_logger("CustomItemQListWidget get_btn_delete()")
        return self.ui.btn_delete

    def get_type_window(self):
        self.__osbm.obj_logg.debug_logger(
            f"CustomItemQListWidget get_type_window():\nself.__type_window = {self.__type_window}"
        )
        return self.__type_window
    
    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"CustomItemQListWidget get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def get_is_active(self):
        self.__osbm.obj_logg.debug_logger(
            f"CustomItemQListWidget get_is_active():\nself.__is_active = {self.__is_active}"
        )
        return self.__is_active

    
``
### D:\vs_projects\auto-exec-doc\package\components\widgets\customsection.py
``python
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QWidget,
    QScrollArea,
    QFrame,
    QToolButton,
    QGridLayout,
    QSizePolicy,
)
from PySide6 import QtGui


class Section(QWidget):
    def __init__(self, osbm, section_id, section_name, sections_checked, is_checked):
        """
        References:
            # Adapted from c++ version
            http://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
        """
        self.__osbm = osbm
        self.__section_id = section_id
        self.__section_name = section_name
        self.__sections_checked = sections_checked
        self.__is_checked = is_checked
        super(Section, self).__init__(None)

        self.__osbm.obj_style.set_style_for(self)

        self.animationDuration = 50
        self.toggleAnimation = QtCore.QParallelAnimationGroup()
        self.contentArea = QScrollArea()
        self.headerLine = QFrame()
        self.toggleButton = QToolButton()
        self.mainLayout = QGridLayout()

        toggleButton = self.toggleButton
        toggleButton.setStyleSheet("QToolButton { border: none; }")
        toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toggleButton.setArrowType(QtCore.Qt.RightArrow)

        metrics = QtGui.QFontMetrics(self.toggleButton.font())
        toggleButton.setText(
            metrics.elidedText(self.__section_name, QtCore.Qt.ElideRight, 300)
        )
        toggleButton.setCheckable(True)
        toggleButton.setChecked(self.__is_checked)

        headerLine = self.headerLine
        headerLine.setFrameShape(QFrame.HLine)
        headerLine.setFrameShadow(QFrame.Sunken)
        headerLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        headerLine.setStyleSheet("QFrame { background-color: #3F3F46; }")

        self.contentArea.setStyleSheet("QScrollArea { border: none; }")
        self.contentArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self.contentArea, b"maximumHeight")
        )
        # don't waste space
        mainLayout = self.mainLayout
        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        row = 0
        mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        row += 1
        mainLayout.addWidget(self.contentArea, row, 0, 1, 3)
        self.setLayout(self.mainLayout)

        def start_animation(checked):
            print(f"checked = {checked}")
            arrow_type = QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
            direction = (
                QtCore.QAbstractAnimation.Forward
                if checked
                else QtCore.QAbstractAnimation.Backward
            )
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()
            self.__sections_checked[self.__section_id] = checked

        self.toggleButton.clicked.connect(start_animation)

        if self.__is_checked:
            start_animation(self.__is_checked)

    def setContentLayout(self, contentLayout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount() - 1):
            SectionAnimation = self.toggleAnimation.animationAt(i)
            SectionAnimation.setDuration(self.animationDuration)
            SectionAnimation.setStartValue(collapsedHeight)
            SectionAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1
        )
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formdate.py
``python
import json

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDate, QLocale

import package.ui.formdate_ui as formdate_ui


class FormDate(QWidget):
    def __init__(self, osbm, pair, current_variable, config_dict):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__config_dict = config_dict
        self.__osbm.obj_logg.debug_logger(
            f"FormDate __init__(self, pair, current_variable, config_dict):\npair = {pair},\ncurrent_variable = {current_variable},\nconfig_dict = {config_dict}"
        )
        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)
        # ИКОНКИ
        self.__icons = self.__osbm.obj_icons.get_icons()
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        # по умолчанию сначала
        self.__str_format = "dd.MM.yyyy"
        self.__language = "ru_RU"
        #
        self.config()

    def config(self):
        self.__osbm.obj_logg.debug_logger("FormDate config()")
        # ПО УМОЛЧАНИЮ из current_variable
        # тип переменной
        qicon_type_variable = (
            self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(
                self.__current_variable.get("type_variable")
            )
        )
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get("title_variable"))
        self.ui.label_variable.setText(
            f"<i>{self.__current_variable.get('name_variable')}</i>"
        )

        # описание
        description_variable = self.__current_variable.get("description_variable")
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из config_dict
        format_date = self.__config_dict.get("FORMAT")
        if format_date:
            self.__str_format = format_date

        language = self.__config_dict.get("LANGUAGE")
        if format_date:
            self.__language = language

        self.ui.dateedit.setLocale(QLocale(self.__language))

        # поле ввода
        value = self.__pair.get("value_pair")
        if value:
            # получить ISO дату и преобразовать
            self.ui.dateedit.setDate(QDate.fromString(value, "yyyy-MM-dd"))
        else:
            self.reset_value()

        self.ui.dateedit.setDisplayFormat(self.__str_format)
        # self.ui.dateedit.editingFinished.connect(self.set_new_value_in_pair)
        self.ui.dateedit.dateChanged.connect(self.set_new_value_in_pair)
        #
        self.ui.btn_set_current.clicked.connect(lambda: self.ui.dateedit.setDate(QDate.currentDate()))

    # def qdate_to_string(self, date, str_format) -> str:
    #     self.__osbm.obj_logg.debug_logger(
    #         f"FormDate date_to_string(self, date) -> str:\ndate = {date}"
    #     )
    #     return str(date.toString(str_format))


    def set_new_value_in_pair(self):
        # self.__pair["value_pair"] = new_value
        current_date = self.ui.dateedit.date()
        iso_date = current_date.toString("yyyy-MM-dd")
        self.__pair["value_pair"] = iso_date

    def reset_value(self):
        self.ui.dateedit.setDate(QDate.currentDate())
        self.set_new_value_in_pair()

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formimage.py
``python
import os
import datetime


from PySide6.QtWidgets import QWidget

import package.ui.formimage_ui as formimage_ui


class FormImage(QWidget):
    def __init__(self, osbm, pair, current_variable, config_dict):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__config_dict = config_dict
        self.__osbm.obj_logg.debug_logger(
            f"FormImage __init__(self, pair, current_variable, config_dict):\npair = {pair},\ncurrent_variable = {current_variable},\nconfig_dict = {config_dict}"
        )
        super(FormImage, self).__init__()
        self.ui = formimage_ui.Ui_FormImageWidget()
        self.ui.setupUi(self)
        # ИКОНКИ
        self.__icons = self.__osbm.obj_icons.get_icons()
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.config()

    def config(self):
        self.__osbm.obj_logg.debug_logger("FormImage config()")
        # тип переменной
        qicon_type_variable = self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(
            self.__current_variable.get("type_variable")
        )
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get('title_variable'))
        self.ui.label_variable.setText(f"<i>{self.__current_variable.get('name_variable')}</i>")
        # поле ввода
        image_path = self.__pair.get("value_pair")
        self.ui.label.setText(
            "Изображение успешно выбрано"
            if image_path and image_path.endswith(".png")
            else "Выберите изображение"
        )
        # масштаб
        if True:
            for i in range(self.ui.scale_layout.count()):
                widget = self.ui.scale_layout.itemAt(i).widget()
                if widget is not None:
                    widget.hide()

        # описание
        description_variable = self.__current_variable.get("description_variable")
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()

        # connect
        self.ui.select_button.clicked.connect(lambda: self.set_new_value_in_pair())
        #
        self.ui.btn_reset.clicked.connect(lambda: self.reset_image())

    def reset_image(self):
        self.__osbm.obj_logg.debug_logger("FormImage reset_image()")
        self.ui.label.setText("Выберите изображение")
        self.__pair["value_pair"] = ""

    def set_new_value_in_pair(self):
        self.__osbm.obj_logg.debug_logger("FormImage set_new_value_in_pair()")
        image_dirpath = self.__osbm.obj_dw.select_image_for_formimage_in_project()
        if image_dirpath:
            # текст выбранного изображения
            self.ui.label.setText(os.path.basename(image_dirpath))
            # имя нового изображения
            file_name = f"img_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            file_name_with_format = f"{file_name}.png"
            # сохранение изображения
            self.__osbm.obj_imgr.save_image_then_selected(image_dirpath, file_name_with_format)
            #
            self.__pair["value_pair"] = file_name_with_format

    def reset_value(self):
        self.reset_image()

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formlist.py
``python
from PySide6.QtWidgets import QWidget, QDialog

import package.ui.formlist_ui as formlist_ui
import package.components.widgets.forms.formlistdialogwindow as formlistdialogwindow


class FormList(QWidget):
    def __init__(self, osbm, pair, current_variable):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__osbm.obj_logg.debug_logger(
            f"FormList(pair, current_variable):\n pair = {pair}, \n current_variable = {current_variable}"
        )
        super(FormList, self).__init__()
        self.ui = formlist_ui.Ui_FormListWidget()
        self.ui.setupUi(self)
        # ИКОНКИ
        self.__icons = self.__osbm.obj_icons.get_icons()
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.config()
        #
        self.ui.btn_edittable.clicked.connect(self.btn_edittable_clicked)

    def btn_edittable_clicked(self, is_fake = False):
        result = self.formlistdw(is_fake)
        if result:
            data = self.__osbm.obj_formlistdw.get_data()
            print(f"obj_formlistdw data = {data}")
            self.set_new_value_in_pair(data)

    def config(self):
        # тип переменной
        qicon_type_variable = (
            self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(
                self.__current_variable.get("type_variable")
            )
        )
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get("title_variable"))
        self.ui.label_variable.setText(
            f"<i>{self.__current_variable.get('name_variable')}</i>"
        )
        # описание
        description_variable = self.__current_variable.get("description_variable")
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()

    def formlistdw(self, is_fake) -> bool:
        self.__osbm.obj_logg.debug_logger("FormList formlistdw()")
        self.__osbm.obj_formlistdw = formlistdialogwindow.FormListDialogWindow(
            self.__osbm, self.__current_variable, self.__pair.get("value_pair")
        )
        if is_fake:
            self.__osbm.obj_formlistdw.save()
            return True
        else:
            result = self.__osbm.obj_formlistdw.exec_()
            return result == QDialog.Accepted

    def set_new_value_in_pair(self, new_value):
        self.__osbm.obj_logg.debug_logger(
            f"FormList set_new_value_in_pair(new_value):\nnew_value = {new_value}"
        )
        self.__pair["value_pair"] = new_value
        print(self.__pair)

    def reset_value(self):
        self.__pair["value_pair"] = ""
        self.btn_edittable_clicked(is_fake=True)

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formlistdialogwindow.py
``python
import json

from PySide6.QtWidgets import QDialog, QListWidget, QListWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import package.ui.formlistdialogwindow_ui as formlistdialogwindow_ui


class FormListDialogWindow(QDialog):
    def __init__(self, osbm, current_variable, value_pair):
        self.__osbm = osbm
        self.__current_variable = current_variable
        self.__value_pair = value_pair
        self.__osbm.obj_logg.debug_logger(
            f"FormListDialogWindow __init__(osbm, current_variable, value_pair): \n current_variable = {current_variable}, \n value_pair = {value_pair}"
        )
        super(FormListDialogWindow, self).__init__()
        self.ui = formlistdialogwindow_ui.Ui_FormListDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__data = []
        #
        self.config_and_lw()
        #
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_and_lw(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config_and_lw()")
        #
        self.ui.label_nametable.setText(
            self.__current_variable.get("name_variable", "Список")
        )
        #
        self.ui.lw.blockSignals(True)
        self.ui.lw.clear()
        #
        list_data = self.get_list_data_from_value_pair()
        for data in list_data:
            self.ui.lw.addItem(data)
        if list_data:
            self.ui.lw.setCurrentRow(0)
        #
        self.ui.lw.blockSignals(False)
        #
        self.edit_all_items()
        


    def edit_all_items(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow edit_all_items()")
        for index in range(self.ui.lw.count()):
            item = self.ui.lw.item(index)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        #

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow connecting_actions()")
        #
        self.ui.add_button.clicked.connect(self.add_item)
        self.ui.delete_button.clicked.connect(self.delete_item)
        self.ui.btn_up.clicked.connect(self.move_item_up)
        self.ui.btn_down.clicked.connect(self.move_item_down)
        #
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_save.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")

    def add_item(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow add_item()")
        item_text = f"Элемент {self.ui.lw.count() + 1}"  # Предустановленный текст
        new_item = QListWidgetItem(item_text)
        current_row = self.ui.lw.currentRow()
        if current_row != -1:  # Если элемент выделен
            self.ui.lw.insertItem(
                current_row + 1, new_item
            )  # Вставляем после выделенного элемента
        else:
            self.ui.lw.addItem(new_item)  # В противном случае добавляем в конец
        #
        self.edit_all_items()

    def delete_item(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow delete_item()")
        current_item = self.ui.lw.currentItem()
        if current_item:
            self.ui.lw.takeItem(self.ui.lw.row(current_item))

    def move_item_up(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow move_item_up()")
        current_row = self.ui.lw.currentRow()
        if current_row > 0:
            item = self.ui.lw.takeItem(current_row)
            self.ui.lw.insertItem(current_row - 1, item)
            self.ui.lw.setCurrentRow(current_row - 1)

    def move_item_down(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow move_item_down()")
        current_row = self.ui.lw.currentRow()
        if current_row < self.ui.lw.count() - 1:
            item = self.ui.lw.takeItem(current_row)
            self.ui.lw.insertItem(current_row + 1, item)
            self.ui.lw.setCurrentRow(current_row + 1)

    def get_list_data_from_value_pair(self):
        self.__osbm.obj_logg.debug_logger(
            "FormListDialogWindow get_list_data_from_value_pair()"
        )
        json_data = self.__value_pair
        if json_data:
            data = json.loads(json_data)
        else:
            data = []
        return data

    def get_data_from_list(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow get_data_from_list()")
        data = []
        for i in range(self.ui.lw.count()):
            data.append(self.ui.lw.item(i).text())
        print("LALA data = ", data, json.dumps(data))
        return json.dumps(data)

    def save(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow save()")
        self.__data = self.get_data_from_list()
        self.accept()

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formlongtext.py
``python
from PySide6.QtWidgets import QWidget

import package.ui.formlongtext_ui as formlongtext_ui


class FormLongText(QWidget):
    def __init__(self, osbm, pair, current_variable):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__osbm.obj_logg.debug_logger(
            f"FormLongTextWidget __init__(pair, current_variable): pair = {pair},\ncurrent_variable = {current_variable}"
        )

        super(FormLongText, self).__init__()
        self.ui = formlongtext_ui.Ui_FormLongText()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        #
        self.config()

    def config(self):
        # тип переменной
        qicon_type_variable = (
            self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(
                self.__current_variable.get("type_variable")
            )
        )
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get("title_variable"))
        self.ui.label_variable.setText(
            f"<i>{self.__current_variable.get('name_variable')}</i>"
        )
        # поле ввода
        self.ui.textedit.setText(self.__pair.get("value_pair"))
        # описание
        description_variable = self.__current_variable.get("description_variable")
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()
        #
        self.ui.textedit.setTabStopDistance(27)
        # connect
        self.ui.textedit.textChanged.connect(self.set_new_value_in_pair)

    def set_new_value_in_pair(self):
        self.__pair["value_pair"] = self.ui.textedit.toPlainText()

    def reset_value(self):
        self.__pair["value_pair"] = ""
        self.ui.textedit.setText(self.__pair.get("value_pair"))

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formtable.py
``python
from PySide6.QtWidgets import QWidget, QDialog

import package.ui.formtable_ui as formtable_ui
import package.components.widgets.forms.formtabledialogwindow as formtabledialogwindow


class FormTable(QWidget):
    def __init__(self, osbm, pair, current_variable, config_dict):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__config_dict = config_dict
        self.__osbm.obj_logg.debug_logger(
            f"FormTable(pair, current_variable, config_dict):\npair = {pair},\ncurrent_variable = {current_variable},\nconfig_dict = {config_dict}"
        )
        super(FormTable, self).__init__()
        self.ui = formtable_ui.Ui_FormTableWidget()
        self.ui.setupUi(self)
        # ИКОНКИ
        self.__icons = self.__osbm.obj_icons.get_icons()
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.config()
        #
        self.ui.btn_edittable.clicked.connect(self.btn_edittable_clicked)

    def btn_edittable_clicked(self, is_fake = False):
        result = self.formtabledw(is_fake)
        if result:
            data = self.__osbm.obj_formtabledw.get_data()
            print(f"obj_formtabledw data = {data}")
            self.set_new_value_in_pair(data)

    def config(self):
        # тип переменной
        qicon_type_variable = self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(
            self.__current_variable.get("type_variable")
        )
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get('title_variable'))
        self.ui.label_variable.setText(f"<i>{self.__current_variable.get('name_variable')}</i>")
        # описание
        description_variable = self.__current_variable.get("description_variable")
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()

    def formtabledw(self, is_fake) -> bool:
        self.__osbm.obj_logg.debug_logger("FormTable formtabledw()")
        self.__osbm.obj_formtabledw = formtabledialogwindow.FormTableDialogWindow(
            self.__osbm, self.__current_variable, self.__config_dict, self.__pair.get("value_pair")
        )
        if is_fake:
            self.__osbm.obj_formtabledw.save()
            return True
        else:
            result = self.__osbm.obj_formtabledw.exec_()
            return result == QDialog.Accepted
    

    def set_new_value_in_pair(self, new_value):
        self.__osbm.obj_logg.debug_logger(
            f"FormTable set_new_value_in_pair(new_value):\nnew_value = {new_value}"
        )
        self.__pair["value_pair"] = new_value
        print(f"set_new_value_in_pair pair = {self.__pair}") 


    def reset_value(self):
        self.__pair["value_pair"] = ""
        self.btn_edittable_clicked(is_fake=True)
        
``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formtabledialogwindow.py
``python
import json

from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QHeaderView,
    QMenu,
    QApplication,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import package.ui.formtabledialogwindow_ui as formtabledialogwindow_ui


class FormTableDialogWindow(QDialog):
    def __init__(self, osbm, current_variable, config_dict, value_pair):
        self.__osbm = osbm
        self.__current_variable = current_variable
        self.__config_dict = config_dict
        self.__value_pair = value_pair
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow __init__(osbm, current_variable, config_dict, value_pair): \n current_variable = {current_variable}, \n config_dict = {config_dict}, \n value_pair = {value_pair}"
        )
        super(FormTableDialogWindow, self).__init__()
        self.ui = formtabledialogwindow_ui.Ui_FormTableDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__typetable = None
        self.__rowcols = []
        #
        self.__data = []
        #
        self.config()
        self.config_tw()
        self.config_context_menu()
        #
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config()")
        #
        self.ui.label_nametable.setText(
            self.__current_variable.get("name_variable", "Таблица")
        )
        #
        self.ui.table.clear()
        #
        self.__typetable = self.__config_dict.get("TYPETABLE")
        self.__rowcols = self.__config_dict.get("ROWCOLS")
        #
        if self.__typetable == "COL":
            self.ui.add_button.setText("Добавить строку")
            self.ui.delete_button.setText("Удалить строку")
        elif self.__typetable == "ROW":
            self.ui.add_button.setText("Добавить столбец")
            self.ui.delete_button.setText("Удалить столбец")
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def config_tw(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config_tw()")
        #
        self.ui.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        # self.ui.table.horizontalHeader().setSectionResizeMode(
        #     QHeaderView.ResizeMode.ResizeToContents
        # )
        #
        headers = []
        ids_rowcols = []
        self.__rowcols = sorted(self.__rowcols, key=lambda x: x.get("ORDER"))
        for rowcol in self.__rowcols:
            headers.append(f'{rowcol.get("TITLE")} ({rowcol.get("ATTR")})')
            ids_rowcols.append(rowcol.get("ID"))
        #
        table_data, len_data = self.get_table_data_from_value_pair(ids_rowcols)
        self.fill_tw_table(table_data, headers, len_data)
        self.resize_headers_tw_table(headers)


    def config_context_menu(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config_context_menu()")
        # контекстное меню
        self.context_menu = QMenu(self)
        self.context_menu.addSeparator()
        # Вырезать - cut_values_to_clipboard
        self.cut_action = QAction("Вырезать", self)
        self.cut_action.triggered.connect(lambda: self.cut_values_to_clipboard())
        self.context_menu.addAction(self.cut_action)
        # Копировать - copy_values_to_clipboard
        self.copy_action = QAction("Копировать", self)
        self.copy_action.triggered.connect(lambda: self.copy_values_to_clipboard())
        self.context_menu.addAction(self.copy_action)        
        #
        self.context_menu.addSeparator()
        #
        self.paste_action = QAction("Вставить ", self)
        self.paste_action.triggered.connect(lambda: self.paste_values_from_clipboard())
        self.context_menu.addAction(self.paste_action)
        #
        self.context_menu.addSeparator()
        # Очистиь значения выделенного
        self.clear_action = QAction("Очистить выделенное", self)
        self.clear_action.triggered.connect(lambda: self.clear_selected_values())
        self.context_menu.addAction(self.clear_action)
        # контекстное меню по правой кнопкой мыши по таблице.
        self.ui.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # Show the context menu at the mouse position
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow show_context_menu(position):\nposition = {position}"
        )
        self.context_menu.exec_(self.ui.table.mapToGlobal(position))

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow connecting_actions()")
        # действия в завимости от типа таблицы
        if self.__typetable == "COL":
            self.ui.add_button.clicked.connect(self.add_row)
            self.ui.delete_button.clicked.connect(self.delete_row)
        elif self.__typetable == "ROW":
            self.ui.add_button.clicked.connect(self.add_column)
            self.ui.delete_button.clicked.connect(self.delete_column)
        #
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_save.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")

    def add_row(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow add_row()")
        selected_row = self.ui.table.currentRow()
        if selected_row == -1:
            row_count = self.ui.table.rowCount()
        else:
            row_count = selected_row + 1
        self.ui.table.insertRow(row_count)
        for column in range(self.ui.table.columnCount()):
            item = QTableWidgetItem()
            self.ui.table.setItem(row_count, column, item)

    def add_column(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow add_column()")
        # column_count = self.ui.table.columnCount()
        # self.ui.table.insertColumn(column_count)
        # for row in range(self.ui.table.rowCount()):
        #     item = QTableWidgetItem()
        #     self.ui.table.setItem(row, column_count, item)

    def delete_row(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow delete_row()")
        current_row = self.ui.table.currentRow()
        if current_row >= 0:
            self.ui.table.removeRow(current_row)

    def delete_column(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow delete_column()")
        # current_column = self.ui.table.currentColumn()
        # if current_column >= 0:
        #     self.ui.table.removeColumn(current_column)

    # def update_cell(self, row, column):
    #     item = self.ui.table.item(row, column)
    #     if item:
    #         print(f"Cell ({row}, {column}) changed to {item.text()}")

    def clear_selected_values(self):
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow clear_selected_values()"
        )
        selected_items = self.ui.table.selectedItems()
        for item in selected_items:
            item.setText("")


    def cut_values_to_clipboard(self):
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow cut_values_to_clipboard()"
        )
        self.copy_values_to_clipboard()
        self.clear_selected_values()


    def copy_values_to_clipboard(self):
        """
        Копирование значения в буфер обмена
        """
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow copy_values_to_clipboard()"
        )
        selected_items = self.ui.table.selectedItems()
        if not selected_items:
            return
        clipboard = QApplication.clipboard()
        clipboard.clear()
        # Сортируем элементы по строкам и колонкам
        selected_items.sort(key=lambda item: (item.row(), item.column()))
        # Формируем текст для вставки в буфер обмена
        rows = []
        current_row = -1
        current_row_values = []
        for item in selected_items:
            if item.row() != current_row:
                if current_row != -1:
                    rows.append("\t".join(current_row_values))
                current_row_values = []
                current_row = item.row()
            current_row_values.append(item.text())
        if current_row_values:
            rows.append("\t".join(current_row_values))
        clipboard.setText("\n".join(rows))

    # def copy_qtable_values_to_clipboard(self):
    #     """
    #     Копирование значения в буфер обмена
    #     """
    #     self.__osbm.obj_logg.debug_logger(
    #         "FormTableDialogWindow copy_qtable_values_to_clipboard()"
    #     )
    #     selected_items = self.ui.table.selectedItems()
    #     values_array = {}

    #     # Формируем словарь значений для хранения строк и их значений
    #     for item in selected_items:
    #         row = item.row()
    #         col = item.column()
    #         if row not in values_array:
    #             values_array[row] = {}
    #         values_array[row][col] = item.text()

    #     # Преобразуем словарь в JSON
    #     text = json.dumps(values_array)

    #     self.__clipboard = QApplication.clipboard()
    #     self.__clipboard.clear()
    #     self.__clipboard.setText(text)
    #     print(f"text = {text}")

    def paste_values_from_clipboard(self):
        """
        Вставка значения из буфера обмена
        """
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow paste_from_clipboard()"
        )
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        row_start = self.ui.table.currentRow()
        column_start = self.ui.table.currentColumn()
        for row, line in enumerate(text.split("\n")):
            for column, item in enumerate(line.split("\t")):
                if (
                    item
                    and (row + row_start < self.ui.table.rowCount())
                    and (column + column_start < self.ui.table.columnCount())
                ):
                    self.ui.table.setItem(
                        row + row_start, column + column_start, QTableWidgetItem(item)
                    )

    # def paste_qtable_values_from_clipboard(self):
    #     """
    #     Вставка выделенного из буфера обмена
    #     """
    #     self.__osbm.obj_logg.debug_logger(
    #         "FormTableDialogWindow paste_qtable_values_from_clipboard()"
    #     )
    #     if self.__clipboard:
    #         text = self.__clipboard.text()
    #     else:
    #         return

    #     # Декодируем JSON
    #     values_dict = json.loads(text) if text else {}
    #     selected_items = self.ui.table.selectedItems()
    #     start_row = selected_items[0].row() if selected_items else 0
    #     start_col = selected_items[0].column() if selected_items else 0

    #     for row, columns in values_dict.items():
    #         row_index = int(row)  # Преобразуем строку в целое число
    #         if start_row + row_index < self.ui.table.rowCount():
    #             for col, value in columns.items():
    #                 col_index = int(col)  # Преобразуем строку в целое число
    #                 if start_col + col_index < self.ui.table.columnCount():
    #                     item = self.ui.table.item(
    #                         start_row + row_index, start_col + col_index
    #                     )
    #                     if item:
    #                         item.setText(value)

    def get_table_data_from_value_pair(self, ids_rowcols):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow get_table_data_from_value_pair(ids_rowcols):\nids_rowcols = {ids_rowcols}"
        )
        json_data = self.__value_pair
        if json_data:
            data = json.loads(json_data)
            # заполнить информацией исходя из ID
            table_data = []
            # словарь ключ-значение
            data_rowcol_by_id_rowcol = dict()
            for elem_data in data:
                data_rowcol_by_id_rowcol[elem_data.get("id_rowcol")] = elem_data.get(
                    "data_rowcol"
                )
            #
            len_data = 0
            for ids_rowcol in ids_rowcols:
                data_rowcol = data_rowcol_by_id_rowcol.get(ids_rowcol, [])
                len_data = max(len_data, len(data_rowcol))
                table_data.append(data_rowcol)
            return (table_data, len_data)
        return ([[]], 0)

    def fill_tw_table(self, table_data, headers, len_data):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow fill_tw_table(table_data, headers, len_data):\n table_data = {table_data}\n headers = {headers}\n len_data = {len_data}"
        )
        if self.__typetable == "COL":
            # заголовки
            self.ui.table.setRowCount(len_data)
            self.ui.table.setColumnCount(len(headers))
            self.ui.table.setHorizontalHeaderLabels(headers)
            self.ui.table.verticalHeader().setVisible(False)
            #
            for col, col_data in enumerate(table_data):
                for row, value in enumerate(col_data):
                    item = QTableWidgetItem(value)
                    self.ui.table.setItem(row, col, item)

        elif self.__typetable == "ROW":
            # заголовки
            self.ui.table.setRowCount(len(headers))
            self.ui.table.setColumnCount(len_data)
            self.ui.table.setVerticalHeaderLabels(headers)
            self.ui.table.horizontalHeader().setVisible(False)
            #
            for row, row_data in enumerate(table_data):
                for col, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    self.ui.table.setItem(row, col, item)

    def resize_headers_tw_table(self, headers):
        self.__osbm.obj_logg.debug_logger(f"FormTableDialogWindow resize_cols_tw_table(headers): \n headers = {headers}")
        table_widget = self.ui.table
        for index in range(len(headers)):
            header_width = table_widget.horizontalHeader().fontMetrics().horizontalAdvance(headers[index])
            table_widget.setColumnWidth(index, header_width + 20)

    def get_data_from_table(self) -> list:
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow to_json() -> list:")
        data = [
            {"id_rowcol": rowcol.get("ID"), "data_rowcol": []}
            for rowcol in self.__rowcols
        ]
        for row in range(self.ui.table.rowCount()):
            for column in range(self.ui.table.columnCount()):
                item = self.ui.table.item(row, column)
                text = item.text() if item else ""
                #
                if self.__typetable == "COL":
                    data[column]["data_rowcol"].append(text)
                elif self.__typetable == "ROW":
                    data[row]["data_rowcol"].append(text)
        print(f"table_data = {data}")
        return json.dumps(data)

    def save(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow save()")
        self.__data = self.get_data_from_table()
        self.accept()

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\formtext.py
``python
from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.tabwinputforms as tabwinputforms


class FormText(QWidget):
    def __init__(self, osbm, pair, current_variable):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__osbm.obj_logg.debug_logger(f"FormText __init__(pair, current_variable): pair = {pair},\ncurrent_variable = {current_variable}")        
        
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        # 
        self.config()

    def config(self):
        # тип переменной
        qicon_type_variable = self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(self.__current_variable.get("type_variable"))
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get('title_variable'))
        self.ui.label_variable.setText(f"<i>{self.__current_variable.get('name_variable')}</i>")
        # поле ввода
        self.ui.lineedit.setText(self.__pair.get("value_pair"))
        # описание
        description_variable = self.__current_variable.get('description_variable')
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()
        # connect
        self.ui.lineedit.textChanged.connect(lambda text: self.set_new_value_in_pair(text))

    def set_new_value_in_pair(self, new_value):
        self.__pair["value_pair"] = new_value


    def reset_value(self):
        self.__pair["value_pair"] = ""
        self.ui.lineedit.setText(self.__pair.get("value_pair"))
``
### D:\vs_projects\auto-exec-doc\package\components\widgets\forms\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\nedvariables\neddatevariable.py
``python
import json

from PySide6.QtWidgets import (
    QWidget
)
from PySide6.QtCore import QDate, QLocale

import package.ui.neddatevariable_ui as neddatevariable_ui

class NedDateVariable(QWidget):
    def __init__(self, osbm, type_window, variable=None):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__variable = variable
        self.__osbm.obj_logg.debug_logger(f"NedDateVariable __init__(osbm, type_window, variable=None):\ntype_window = {type_window}\nvariable = {variable}")
        super(NedDateVariable, self).__init__()
        self.ui = neddatevariable_ui.Ui_NedDateVariable()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__config_dict = dict()
        if self.__variable and self.__variable.get("type_variable") == "DATE":
            self.__config_variable = self.__variable.get("config_variable")
            if self.__config_variable:
                self.__config_dict = json.loads(self.__config_variable)
        #
        self.config_by_type()
        self.config_lineedit_format()  
        self.config_combox_language()      
        self.text_changed()

    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(f"NedDateVariable get_save_data():\nself.__data = {self.__data}")
        return self.__data
    
    def save_data(self):
        str_format = self.ui.lineedit_format.text()
        language = self.ui.combox_language.currentData()
        self.__data = {
            "FORMAT": str_format,
            "LANGUAGE": language,
        }

    def config_by_type(self):
        if self.__type_window == "create":
            self.__str_format = "dd.MM.yyyy"
            self.__language = "ru_RU"
        elif self.__type_window == "edit":
            self.__str_format = self.__config_dict.get("FORMAT")
            self.__language = self.__config_dict.get("LANGUAGE")

    def config_lineedit_format(self):
        self.__osbm.obj_logg.debug_logger("config_lineedit_format config()")
        
        self.ui.lineedit_format.setText(self.__str_format)
        # события
        self.ui.lineedit_format.textChanged.connect(self.text_changed)
        self.ui.dateedit_check.dateChanged.connect(self.text_changed)

    def config_combox_language(self):
        self.__osbm.obj_logg.debug_logger("NedDateVariable config_combox_language()")
        combobox = self.ui.combox_language
        combobox.blockSignals(True)
        combobox.clear()
        languages = self.__osbm.obj_comwith.languages.get_languages()
        for language in languages:
            combobox.addItem(language.name, language.data)
        #
        if self.__type_window == "create":
            combobox.setCurrentIndex(0)
        elif self.__type_window == "edit":
            index_by_data = combobox.findData(self.__language)
            if index_by_data == -1:
                index_by_data = 0
            combobox.setCurrentIndex(index_by_data)
        #
        combobox.blockSignals(False)
        #
        self.language_changed()
        combobox.currentIndexChanged.connect(self.language_changed)

    def language_changed(self, index = None):
        print("language_changed КОКОКОКО")
        self.ui.dateedit_check.setLocale(QLocale(self.ui.combox_language.currentData()))

    def text_changed(self):
        try:
            self.ui.dateedit_check.setDisplayFormat(self.ui.lineedit_format.text())
            self.ui.label_result.setText(self.ui.dateedit_check.text())
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"NedDateVariable text_changed():\n{e}")


    


``
### D:\vs_projects\auto-exec-doc\package\components\widgets\nedvariables\nedimagevariable.py
``python
import json

from PySide6.QtWidgets import (
    QWidget
)

import package.ui.nedimagevariable_ui as nedimagevariable_ui

class NedImageVariable(QWidget):
    def __init__(self, osbm, type_window, variable=None):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__variable = variable
        self.__osbm.obj_logg.debug_logger(f"NedImageVariable __init__(osbm, type_window, variable=None):\ntype_window = {type_window}\nvariable = {variable}")
        super(NedImageVariable, self).__init__()
        self.ui = nedimagevariable_ui.Ui_NedImageVariable()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__data = {}
        self.__config_dict = dict()
        if self.__variable and self.__variable.get("type_variable") == "IMAGE": 
            self.__config_variable = self.__variable.get("config_variable")
            if self.__config_variable:
                self.__config_dict = json.loads(self.__config_variable)
        # config
        self.config_combox_units()
        self.config_combox_sms()
        self.config_by_type_window()
        #
        self.connecting_actions()

    def config_combox_units(self):
        self.__osbm.obj_logg.debug_logger("NedImageVariable config_combox_units()")
        combobox = self.ui.combox_units
        combobox.blockSignals(True)
        combobox.clear()
        units = self.__osbm.obj_comwith.units.get_units()
        for unit in units:
            combobox.addItem(unit.name, unit.data)
        combobox.blockSignals(False)

    def config_combox_sms(self):
        self.__osbm.obj_logg.debug_logger("NedImageVariable config_combox_sms()")
        combobox = self.ui.combox_sms
        combobox.blockSignals(True)
        combobox.clear()
        sizing_modes = self.__osbm.obj_comwith.sizing_modes.get_sizing_modes()
        for sizing_mode in sizing_modes:
            combobox.addItem(sizing_mode.name, sizing_mode.data)
        combobox.blockSignals(False)

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger("NedImageVariable config_by_type_window()")
        if self.__type_window == "create":
            self.ui.combox_units.setCurrentIndex(0)
            self.ui.combox_sms.setCurrentIndex(0)
            self.set_enabled_for_width_height(False)

        elif self.__type_window == "edit":
            # получение данных
            unit = self.__config_dict.get("UNIT")
            sizing_mode = self.__config_dict.get("SIZINGMODE")
            width = self.__config_dict.get("WIDTH")
            height = self.__config_dict.get("HEIGHT")
            # узнаем индексы по значению для комбобоксов
            index_unit = self.__osbm.obj_comwith.units.get_index_unit_by_data(unit)
            index_unit = index_unit if index_unit else 0
            index_sizing_mode = self.__osbm.obj_comwith.sizing_modes.get_index_sizing_mode_by_data(sizing_mode)
            index_sizing_mode = index_sizing_mode if index_sizing_mode else 0
            #
            self.ui.combox_units.setCurrentIndex(index_unit)
            self.ui.combox_sms.setCurrentIndex(index_sizing_mode)
            # установка значений ширины и высоты
            if width:
                self.ui.dsb_width.setValue(width)
            if height:
                self.ui.dsb_height.setValue(height)
            # установка активности
            self.set_enabled_wh_by_index(index_sizing_mode)

    def set_enabled_for_width_height(self, state):
        self.ui.title_wh.setEnabled(state)
        self.ui.dsb_width.setEnabled(state)
        self.ui.dsb_height.setEnabled(state)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedImageVariable connecting_actions()")
        self.ui.combox_sms.currentIndexChanged.connect(self.set_enabled_wh_by_index)


    def set_enabled_wh_by_index(self, index): 
        self.__osbm.obj_logg.debug_logger(f"NedImageVariable combox_sms_index_changed(index): index = {index}")
        is_wh = self.__osbm.obj_comwith.sizing_modes.get_is_wh_by_index(index)
        if is_wh:
            self.set_enabled_for_width_height(True)
        else:
            self.set_enabled_for_width_height(False)


    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(f"NedImageVariable get_save_data():\nself.__data = {self.__data}")
        return self.__data


    def save_data(self):
        self.__osbm.obj_logg.debug_logger("NedImageVariable save_data()")
        unit_data = self.ui.combox_units.currentData()
        sizing_mode_data = self.ui.combox_sms.currentData()
        width = float(self.ui.dsb_width.text().replace(",","."))
        height = float(self.ui.dsb_height.text().replace(",","."))
        self.__data = {
            "UNIT": unit_data,
            "SIZINGMODE": sizing_mode_data,
            "WIDTH": width,
            "HEIGHT": height,
        }



``
### D:\vs_projects\auto-exec-doc\package\components\widgets\nedvariables\nedtablevariable.py
``python
import json
import copy
import uuid

from functools import partial

from PySide6.QtWidgets import QWidget, QListWidgetItem, QListWidget, QDialog
from PySide6.QtCore import QTimer, QSize

import package.ui.nedtablevariable_ui as nedtablevariable_ui

import package.components.dialogwindow.neddw.nedrowcoldialogwindow as nedrowcoldialogwindow

import package.components.widgets.customitemqlistwidget as customitemqlistwidget


class NedTableVariable(QWidget):
    def __init__(self, osbm, type_window, variable=None):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__variable = variable
        self.__osbm.obj_logg.debug_logger("NedTableVariable __init__(osbm, type_window)")
        super(NedTableVariable, self).__init__()
        self.ui = nedtablevariable_ui.Ui_NedTableVariable()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__data = {
            "TYPETABLE": None,
            "ROWCOLS": [{"ID": None, "ATTR": None, "TITLE": None, "ORDER": None}],
        }
        self.__config_dict = dict()
        self.__rowcols_items = []
        #
        if self.__variable and self.__variable.get("type_variable") == "TABLE":
            self.__config_variable = self.__variable.get("config_variable")
            if self.__config_variable:
                self.__config_dict = json.loads(self.__config_variable)
        #
        self.ui.label_rowcol.setText("Столбцы")
        self.ui.btn_addrowcol.setText("Добавить столбец")
        #
        # self.config_combox_typetable()
        self.config_lw_attrs()        
        # self.config_by_type_window()
        #
        self.connecting_actions()

    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedTableVariable connecting_actions()")
        # self.ui.combox_typetable.currentIndexChanged.connect(self.typetable_changed)
        self.ui.btn_addrowcol.clicked.connect(self.add_item)

    # def config_combox_typetable(self):
    #     self.__osbm.obj_logg.debug_logger("NedTableVariable config_combox_typetable()")
    #     combobox = self.ui.combox_typetable
    #     combobox.blockSignals(True)
    #     combobox.clear()
    #     self.__table_types = self.__osbm.obj_comwith.table_types.get_table_types()
    #     for table_type in self.__table_types:
    #         combobox.addItem(table_type.icon, table_type.name, table_type.data)
    #     combobox.blockSignals(False)

    def config_lw_attrs(self, open_rowcol = None):
        self.__osbm.obj_logg.debug_logger("NedTableVariable config_lw_attrs()")
        list_widget = self.ui.lw_attrs
        list_widget.blockSignals(True)
        list_widget.clear()
        self.__rowcols_items = []
        rowcols = self.get_sorted_rowcols()
        for rowcol in rowcols:
            custom_widget = customitemqlistwidget.CustomItemQListWidget(
                self.__osbm, "ROWCOLS", rowcol
            )
            item = QListWidgetItem()
            item.setData(0, rowcol)
            # Указываем размер элемента
            item.setSizeHint(custom_widget.sizeHint())
            item.setSizeHint(item.sizeHint().boundedTo(list_widget.sizeHint()))
            list_widget.addItem(item)
            # Устанавливаем виджет для элемента
            list_widget.setItemWidget(item, custom_widget)
            # кнопки
            self.config_buttons_for_item(custom_widget)
            #
            self.__rowcols_items.append(item)
        #
        if self.__rowcols_items:
            if open_rowcol:
                index_template = next(
                    (
                        i
                        for i, rowcol in enumerate(rowcols)
                        if open_rowcol.get("ID") == rowcol.get("ID")
                    ),
                    0,
                )
                list_widget.setCurrentRow(index_template)
            else:
                list_widget.setCurrentRow(0)

        list_widget.blockSignals(False)

    def config_buttons_for_item(self, item_widget):
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable config_buttons_for_item(item_widget)\nitem_widget = {item_widget}"
        )
        edit_button = item_widget.get_btn_edit()
        delete_button = item_widget.get_btn_delete()
        edit_button.clicked.connect(
            partial(self.edit_item, data=item_widget.get_data())
        )
        delete_button.clicked.connect(
            partial(self.delete_item, data=item_widget.get_data())
        )

    def delete_item(self, data):
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable delete_item(data):\ndata = {data}"
        )
        title_rowcol = data.get("TITLE")
        name_rowcol = data.get("ATTR")
        result = self.__osbm.obj_dw.question_message(
            f'Вы действительно удалить этот атрибут:\n"{title_rowcol}" ({name_rowcol})?'
        )
        if result:
            # удаление
            rowcols = self.get_sorted_rowcols()
            index = next((i for i, rowcol in enumerate(rowcols) if rowcol.get("ID") == data.get("ID")), None)
            if index is not None:
                rowcols.pop(index)
                for index, rowcol in enumerate(rowcols):
                    rowcol["ORDER"] = index
                self.__config_dict["ROWCOLS"] = rowcols
            self.config_lw_attrs()

    def edit_item(self, data):
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable edit_item(data):\ndata = {data}"
        )
        self.__osbm.obj_logg.debug_logger("NedTableVariable add_item()")
        # type_rowcol = self.ui.combox_typetable.currentData()
        type_rowcol = "COL"
        rowcols = self.get_sorted_rowcols()
        result = self.nedrowcoldw("edit", type_rowcol, rowcols, data)
        if result:
            current_rowcol = self.__osbm.obj_nedrowcoldw.get_data()
            attr_current_rowcol = current_rowcol.get("ATTR")
            title_current_rowcol = current_rowcol.get("TITLE")
            order_current_rowcol = current_rowcol.get("ORDER")
            rowcol = {
                "ID": data.get("ID"),
                "ATTR": attr_current_rowcol,
                "TITLE": title_current_rowcol,
                "ORDER": order_current_rowcol
            }
            # удалить из списка
            order_old_rowcol = data.get("ORDER")
            del rowcols[order_old_rowcol]
            # добавить в список
            rowcols.insert(order_current_rowcol, rowcol)
            for index, rowcol in enumerate(rowcols):
                rowcol["ORDER"] = index
            self.__config_dict["ROWCOLS"] = rowcols
            self.config_lw_attrs(data)

    def add_item(self):
        self.__osbm.obj_logg.debug_logger("NedTableVariable add_item()")
        # type_rowcol = self.ui.combox_typetable.currentData()
        type_rowcol = "COL"
        rowcols = self.get_sorted_rowcols()
        result = self.nedrowcoldw("create", type_rowcol, rowcols, None)
        if result:
            current_rowcol = self.__osbm.obj_nedrowcoldw.get_data()
            attr_current_rowcol = current_rowcol.get("ATTR")
            title_current_rowcol = current_rowcol.get("TITLE")
            order_current_rowcol = current_rowcol.get("ORDER")
            rowcol = {
                "ID": uuid.uuid1().hex,
                "ATTR": attr_current_rowcol,
                "TITLE": title_current_rowcol,
                "ORDER": order_current_rowcol
            }
            rowcols.insert(order_current_rowcol, rowcol)
            for index, rowcol in enumerate(rowcols):
                rowcol["ORDER"] = index
            self.__config_dict["ROWCOLS"] = rowcols
            self.config_lw_attrs(rowcol)
            



    def nedrowcoldw(self, type_ned, type_rowcol, rowcols, rowcol = None):
        self.__osbm.obj_logg.debug_logger("NedTableVariable nedrowcoldw()")
        self.__osbm.obj_nedrowcoldw = nedrowcoldialogwindow.NedRowcolDialogWindow(
            self.__osbm, type_ned, type_rowcol, rowcols, rowcol
        )
        result = self.__osbm.obj_nedrowcoldw.exec()
        return result == QDialog.Accepted

    # def config_by_type_window(self):
    #     self.__osbm.obj_logg.debug_logger("NedTableVariable config_by_type_window()")
    #     index = 0
    #     if self.__type_window == "edit":
    #         typetable = self.__config_dict.get("TYPETABLE")
    #         index = self.__osbm.obj_comwith.table_types.get_index_by_data(typetable)
    #     self.typetable_changed(index)

    # def typetable_changed(self, index):
    #     self.__osbm.obj_logg.debug_logger(
    #         f"NedTableVariable typetable_changed(index):\nindex = {index}"
    #     )
    #     #
    #     is_view_rowcols = self.__osbm.obj_comwith.table_types.get_is_edit_rowcols_by_index(
    #         index
    #     )
    #     self.ui.label_rowcol.setEnabled(is_view_rowcols)
    #     self.ui.lw_attrs.setEnabled(is_view_rowcols)
    #     self.ui.btn_addrowcol.setEnabled(is_view_rowcols)
    #     #
    #     if is_view_rowcols:
    #         text_btns = self.__osbm.obj_comwith.table_types.get_text_btns_by_index(index)
    #         if text_btns:
    #             self.ui.label_rowcol.setText(text_btns[0])
    #             self.ui.btn_addrowcol.setText(text_btns[1])
    #         self.ui.combox_typetable.setCurrentIndex(index)

    def save_data(self):

        self.__osbm.obj_logg.debug_logger("NedTableVariable save_data()")
        # typetable = self.ui.combox_typetable.currentData()
        typetable = "COL"
        rowcols = self.get_sorted_rowcols()
        self.__data = {
            "TYPETABLE": typetable,
            "ROWCOLS": rowcols,
        }

    def get_sorted_rowcols(self):
        rowcols = self.__config_dict.get("ROWCOLS", [])
        return sorted(rowcols, key=lambda x: x.get("ORDER"))

``
### D:\vs_projects\auto-exec-doc\package\components\widgets\nedvariables\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\controllers\comboxtemplates.py
``python


import resources_rc

class ComboxTemplates:
    def __init__(self):
        self.__combox_templates = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("ComboxTemplates setting_all_osbm()")

    def connect_combox_templates(self, combox_templates):
        self.__osbm.obj_logg.debug_logger(f"ComboxTemplates connect_combox_templates(combox_templates):\ncombox_templates = {combox_templates}")
        self.__combox_templates = combox_templates
        # Очистить при запуске
        self.clear_comboxts()
        # Подключение сигналов
        self.__combox_templates.currentIndexChanged.connect(lambda index: self.combox_templates_changed(index))

    def combox_templates_changed(self, index):
        self.__osbm.obj_logg.debug_logger(f"ComboxTemplates combox_templates_changed(index):\nindex = {index}")
        template = self.__combox_templates.itemData(index)
        if template:
            # сохранить активный шаблон для БД вершины 
            id_parent_node = template.get("id_parent_node")
            id_template = template.get("id_template")
            self.__osbm.obj_prodb.set_active_template_for_node_by_id(id_parent_node, id_template)
            # обновить cтраницы
            self.__osbm.obj_lwpt.update_pages_template(template)
        else:
            self.__osbm.obj_lwpt.update_pages_template(None)

    def clear_comboxts(self):
        self.__combox_templates.blockSignals(True)
        self.__combox_templates.clear()
        self.__combox_templates.blockSignals(False)

    def update_combox_templates(self, node):
        """
        Извне обновляют список шаблонов
        """
        self.__osbm.obj_logg.debug_logger(f"ComboxTemplates update_combox_templates(node):\nnode = {node}")
        self.clear_comboxts()
        self.__combox_templates.blockSignals(True)
        if node:
            id_node = node.get("id_node")
            id_active_template = node.get("id_active_template")
            wrap_node = {
                "id_node": id_node
            }
            templates = self.__osbm.obj_prodb.get_templates_by_form(wrap_node)
            index = 0
            for i, template in enumerate(templates):
                if template.get("id_template") == id_active_template:
                    index = i
                self.__combox_templates.addItem(template.get("name_template"), template)
            #
            self.__combox_templates.setCurrentIndex(index)
            # обновить cтраницы
            self.combox_templates_changed(index)
        else:
            self.__osbm.obj_lwpt.update_pages_template(None)
        self.__combox_templates.blockSignals(False)  

``
### D:\vs_projects\auto-exec-doc\package\controllers\icons.py
``python

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

import resources_rc

class Icons:
    def __init__(self):
        self.__icons_cache = dict()

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(f"Icons setting_osbm():\nself.__osbm = {self.__osbm}")

        
    def get_icons(self, size = 16) -> dict:
        self.__osbm.obj_logg.debug_logger(f"Icons get_icons(size):\nsize = {size}")
        result = self.__icons_cache.get(size)
        if result:
            return result
        else:
            icons = dict()
            # типы переменных
            icons["text"] = QIcon(":/white-icons/resources/white-icons/text.svg")
            icons["longtext"] = QIcon(":/white-icons/resources/white-icons/longtext.svg")
            icons["date"] = QIcon(":/white-icons/resources/white-icons/calendar.svg")
            icons["table"] = QIcon(":/white-icons/resources/white-icons/table.svg")
            icons["list"] = QIcon(":/white-icons/resources/white-icons/items-list.svg")
            icons["image"] = QIcon(":/white-icons/resources/white-icons/picture.svg")
            # прочее
            icons["save"] = QIcon(":/white-icons/resources/white-icons/save.svg")
            icons["close"] = QIcon(":/white-icons/resources/white-icons/close.svg")
            icons["add"] = QIcon(":/white-icons/resources/white-icons/plus.svg")
            # круги 
            icons["red_circle"] = QIcon(":/color-icons/resources/color-icons/red-circle.svg")
            icons["yellow_circle"] = QIcon(":/color-icons/resources/color-icons/yellow-circle.svg")
            icons["green_circle"] = QIcon(":/color-icons/resources/color-icons/green-circle.svg")
            # word, libreoffice
            icons["libreoffice"] = QIcon(":/color-icons/resources/color-icons/libreoffice.svg")
            icons["msword"] = QIcon(":/color-icons/resources/color-icons/msword.svg")
            # иконка
            icons["logo"] = QIcon(":/color-icons/resources/color-icons/logo.svg")
            # ручка и корзина
            icons["pen"] = QIcon(":/white-icons/resources/white-icons/pen.svg")
            icons["trash"] = QIcon(":/white-icons/resources/white-icons/trash.svg")
            # группа и форма
            icons["form"] = QIcon(":/white-icons/resources/white-icons/page.svg")
            icons["group"] = QIcon(":/white-icons/resources/white-icons/folder.svg")
            # страница
            icons["page"] = QIcon(":/white-icons/resources/white-icons/file-text.svg")
            # pdf
            icons["pdf"] = QIcon(":/white-icons/resources/white-icons/pdf.svg")
            # actions
            icons["edit_composition"] = QIcon(":/white-icons/resources/white-icons/items-tree.svg")
            icons["edit_templates"] = QIcon(":/white-icons/resources/white-icons/template.svg")
            icons["edit_variables"] = QIcon(":/white-icons/resources/white-icons/text-editor.svg")
            #
            icons["table-rows"] = QIcon(":/white-icons/resources/white-icons/table-rows.svg")
            icons["table-columns"] = QIcon(":/white-icons/resources/white-icons/table-columns.svg")
            #
            for key, elem in icons.items():
                if key in ["red_circle", "yellow_circle", "green_circle"]:
                    icons[key] = icons[key].pixmap(QSize(size / 2, size / 2))
                else:
                    icons[key] = elem.pixmap(QSize(size, size))
            self.__icons_cache[size] = icons
            return icons
``
### D:\vs_projects\auto-exec-doc\package\controllers\lwpagestemplate.py
``python
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QRect


class LWPagesTemplate:
    def __init__(self):
        self.__lw_pages_template = None
        self.__icons = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate setting_all_osbm()")

    def connect_pages_template(self, lw_pt):
        """
        Подключить _lw_pages_template.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate connect_pages_template(lw_pt):\nlw_pt = {lw_pt}"
        )
        self.__lw_pages_template = lw_pt
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.clear_pt()
        # Подключение сигналов
        self.__lw_pages_template.itemClicked.connect(self.on_item_clicked)
        self.__lw_pages_template.itemChanged.connect(self.on_item_changed)

    def on_item_clicked(self, item):
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate on_item_clicked(item):\nitem = {item}"
        )
        # проверка на чекбокс
        item_rect = self.__lw_pages_template.visualItemRect(item)
        mouse_position = self.__lw_pages_template.mapFromGlobal(self.__lw_pages_template.cursor().pos())
        # Определяем область чекбокса
        checkbox_rect = QRect(item_rect.topLeft(), item_rect.size())
        checkbox_rect.setWidth(20)
        if checkbox_rect.contains(mouse_position):
            return 
        else:
            # открываем страницу
            self.item_page_updated(item)

    def on_item_changed(self, item):
        """
        Слот для обработки изменений состояния чекбокса.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate on_item_changed(item):\nitem = {item}"
        )
        if item.checkState() in (Qt.Checked, Qt.Unchecked):
            self.__osbm.obj_prodb.set_included_for_page(
                item.data(Qt.UserRole), int(item.checkState() == Qt.Checked)
            )

    def is_page_template_selected(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate get_lw_pages_template()")
        return self.__lw_pages_template.currentItem()

    def get_page_by_current_item(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate get_page_by_current_item()")
        current = self.__lw_pages_template.currentItem()
        return current.data(Qt.UserRole) if current else None

    def item_page_updated(self, current):
        """
        Слот для сигнала itemClicked.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate item_page_updated(current):\ncurrent = {current}"
        )
        page = current.data(Qt.UserRole)
        # Обновить TabWInputForms
        self.__osbm.obj_tabwif.update_tabs(page)
        # открыть pdf форму для текущей страницы
        self.create_and_view_current_page(page)

    def create_and_view_current_page(self, page):
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate create_and_view_current_page(page):\npage = {page}"
        )
        app_converter = self.__osbm.obj_settings.get_app_converter()
        status_msword = self.__osbm.obj_offp.get_status_msword()
        status_libreoffice = self.__osbm.obj_offp.get_status_libreoffice()
        is_convert_flag = True
        if app_converter == "MSWORD" and status_msword:
            pass
        elif app_converter == "LIBREOFFICE" and status_libreoffice:
            pass
        else:
            msg = "Отображение недоступно! Выбранный конвертер не работает. Сохранение при этом доступно."
            self.__osbm.obj_dw.warning_message(msg)
            self.__osbm.obj_stab.set_message(msg)
            is_convert_flag = False
        #
        if is_convert_flag:
            pdf_path = str()
            is_error = False
            self.__osbm.obj_dw.process_show_start()
            try:
                pdf_path = self.__osbm.obj_conv.create_one_page_pdf(page)
            except self.__osbm.obj_com.errors.MsWordError:
                self.__osbm.obj_offp.terminate_msword()
                self.__osbm.obj_stab.update_status_msword_label(False)
                if is_convert_flag:
                    msg = "Отображение недоступно! Выбранный конвертер перестал работать. Сохранение при этом доступно."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                is_error = True

            except self.__osbm.obj_com.errors.LibreOfficeError:
                self.__osbm.obj_offp.terminate_libreoffice()
                self.__osbm.obj_stab.update_status_libreoffice_label(False)
                if is_convert_flag:
                    msg = "Отображение недоступно! Выбранный конвертер перестал работать. Сохранение при этом доступно."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                is_error = True

            except Exception as e:
                self.__osbm.obj_logg.error_logger(
                    f"Error in create_and_view_current_page(page): {e}"
                )
                self.__osbm.obj_dw.warning_message(f"Ошибка: {e}")
                is_error = True
            #
            self.__osbm.obj_dw.process_show_end()
        #
        if is_convert_flag and not is_error and pdf_path:
            self.__osbm.obj_pdfv.load_and_show_pdf_document(pdf_path)
        else:
            self.__osbm.obj_pdfv.set_empty_pdf_view()

    def current_page_to_pdf(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate IN current_page_to_pdf()")
        current = self.__lw_pages_template.currentItem()
        page = current.data(Qt.UserRole)
        self.create_and_view_current_page(page)

    def clear_pt(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate clear_pt()")
        try:
            if self.__lw_pages_template is not None:
                self.__lw_pages_template.blockSignals(True)
                self.__lw_pages_template.clear()
                self.__lw_pages_template.blockSignals(False)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in clear_pt(): {e}")

    def update_pages_template(self, template):
        """
        Обновить _lw_pages_template.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate update_pages_template(template):\ntemplate = {template}"
        )
        self.clear_pt()
        self.__lw_pages_template.blockSignals(True)
        if template:
            pages = self.__osbm.obj_prodb.get_pages_by_template(template)
            for page in pages:
                print(f"page = {page}")
                item = QListWidgetItem()
                item.setText(page.get("name_page"))
                item.setCheckState(Qt.Checked if page.get("included") else Qt.Unchecked)
                #
                typefile_page = page.get("typefile_page")
                if typefile_page == "DOCX":
                    item.setIcon(self.__icons.get("page"))
                elif typefile_page == "PDF":
                    item.setIcon(self.__icons.get("pdf"))
                #
                item.setData(Qt.UserRole, page)
                self.__lw_pages_template.addItem(item)

        self.__lw_pages_template.blockSignals(False)


# obj_lwpt = LWPagesTemplate()

``
### D:\vs_projects\auto-exec-doc\package\controllers\pdfview.py
``python
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QSizePolicy, QApplication
from PySide6.QtCore import QUrl, Qt, QObject
from PySide6.QtGui import QMouseEvent, QWheelEvent
import sys

DELTA_ZOOM = 0.1
MAX_ZOOM = 4
MIN_ZOOM = 0.1  

class PdfView(QObject):
    def __init__(self):
        super().__init__()
        self.__widget_pdf_view = None
        self.__document = None
        self.__zoom = 1
        self.__is_dragging = False
        self.__last_mouse_pos = None
        self.__last_mouse_pos_before_zoom = None 

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("PdfView setting_all_osbm()")

    def connect_pdfview(self, widget):
        self.__osbm.obj_logg.debug_logger("PdfView connect_pdfview()")
        self.__widget_pdf_view = widget
        self.__document = None
        self.config_pdf_view_in_mainwindow()
        
        # Устанавливаем обработчики событий - исправленная строка
        self.__widget_pdf_view.viewport().installEventFilter(self)
        self.__widget_pdf_view.setMouseTracking(True)

    def eventFilter(self, obj, event):
        """Обработка событий мыши для виджета PDF"""
        if obj == self.__widget_pdf_view.viewport():
            if event.type() == QMouseEvent.MouseButtonPress:
                return self.mousePressEvent(event)
            elif event.type() == QMouseEvent.MouseButtonRelease:
                return self.mouseReleaseEvent(event)
            elif event.type() == QMouseEvent.MouseMove:
                return self.mouseMoveEvent(event)
            elif event.type() == QMouseEvent.Wheel:
                return self.wheelEvent(event)
        
        return False

    def mousePressEvent(self, event):
        """Обработка нажатия кнопки мыши"""
        if event.button() == Qt.LeftButton:
            # Начало перетаскивания
            self.__is_dragging = True
            self.__last_mouse_pos = event.position()
            self.__widget_pdf_view.setCursor(Qt.ClosedHandCursor)
            return True
        
        return False

    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши"""
        if event.button() == Qt.LeftButton and self.__is_dragging:
            # Конец перетаскивания
            self.__is_dragging = False
            self.__widget_pdf_view.setCursor(Qt.ArrowCursor)
            return True
        
        return False

    def mouseMoveEvent(self, event):
        """Обработка движения мыши"""
        if self.__is_dragging and event.buttons() & Qt.LeftButton:
            # Перетаскивание документа
            current_pos = event.position()
            delta = current_pos - self.__last_mouse_pos
            
            # Получаем текущие значения скроллбаров
            h_scroll = self.__widget_pdf_view.horizontalScrollBar()
            v_scroll = self.__widget_pdf_view.verticalScrollBar()
            
            # Обновляем позицию скроллбаров
            h_scroll.setValue(h_scroll.value() - delta.x())
            v_scroll.setValue(v_scroll.value() - delta.y())
            
            self.__last_mouse_pos = current_pos
            return True
        
        return False

    def wheelEvent(self, event):
        """Обработка колесика мыши"""
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.ControlModifier:
            self.__last_mouse_pos_before_zoom = event.position()
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            return True
        return False

    def config_pdf_view_in_mainwindow(self):
        self.__osbm.obj_logg.debug_logger("PdfView config_pdf_view_in_mainwindow()")
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.__widget_pdf_view.setDocument(self.__document)

    def zoom_in(self):
        if (self.__zoom + DELTA_ZOOM) < MAX_ZOOM and self.__widget_pdf_view.zoomMode() == QPdfView.ZoomMode.Custom:
            # Сохраняем текущие позиции скроллбаров
            h_scroll = self.__widget_pdf_view.horizontalScrollBar()
            v_scroll = self.__widget_pdf_view.verticalScrollBar()
            old_h_value = h_scroll.value()
            old_v_value = v_scroll.value()
            
            # Применяем масштабирование
            old_zoom = self.__zoom
            self.__zoom += DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)
            
            # Корректируем скролл для центрирования по курсору мыши
            if self.__last_mouse_pos_before_zoom:
                zoom_ratio = self.__zoom / old_zoom
                mouse_pos = self.__last_mouse_pos_before_zoom
                
                new_h_value = (old_h_value + mouse_pos.x()) * zoom_ratio - mouse_pos.x()
                new_v_value = (old_v_value + mouse_pos.y()) * zoom_ratio - mouse_pos.y()
                
                h_scroll.setValue(int(new_h_value))
                v_scroll.setValue(int(new_v_value))
            
            self.__osbm.obj_logg.debug_logger(f"PdfView zoom_in():\nself.__zoom = {self.__zoom}")

    def zoom_out(self):
        if (self.__zoom - DELTA_ZOOM) > MIN_ZOOM and self.__widget_pdf_view.zoomMode() == QPdfView.ZoomMode.Custom:
            # Сохраняем текущие позиции скроллбаров
            h_scroll = self.__widget_pdf_view.horizontalScrollBar()
            v_scroll = self.__widget_pdf_view.verticalScrollBar()
            old_h_value = h_scroll.value()
            old_v_value = v_scroll.value()
            
            # Применяем масштабирование
            old_zoom = self.__zoom
            self.__zoom -= DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)
            
            # Корректируем скролл для центрирования по курсору мыши
            if self.__last_mouse_pos_before_zoom:
                zoom_ratio = self.__zoom / old_zoom
                mouse_pos = self.__last_mouse_pos_before_zoom
                
                new_h_value = (old_h_value + mouse_pos.x()) * zoom_ratio - mouse_pos.x()
                new_v_value = (old_v_value + mouse_pos.y()) * zoom_ratio - mouse_pos.y()
                
                h_scroll.setValue(int(new_h_value))
                v_scroll.setValue(int(new_v_value))
            
            self.__osbm.obj_logg.debug_logger(f"PdfView zoom_out():\nself.__zoom = {self.__zoom}")

    def set_zoom_to_fit_width(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.__osbm.obj_logg.debug_logger("PdfView set_zoom_to_fit_width()")

    def set_zoom_custom(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.__osbm.obj_logg.debug_logger("PdfView set_zoom_custom()")

    def set_empty_pdf_view(self):
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setDocument(self.__document)
        self.__osbm.obj_logg.debug_logger("PdfView set_empty_pdf_view()")

    def get_view_sizes(self):
        self.__osbm.obj_logg.debug_logger("PdfView get_view_sizes()")
        return (self.__widget_pdf_view.horizontalScrollBar().value(), self.__widget_pdf_view.verticalScrollBar().value())

    def set_view_sizes(self, value):
        self.__osbm.obj_logg.debug_logger(
            f"PdfView set_view_sizes({value}):\nvalue = {value}"
        )
        self.__widget_pdf_view.horizontalScrollBar().setValue(value[0])
        self.__widget_pdf_view.verticalScrollBar().setValue(value[1])

    def load_and_show_pdf_document(self, pdf_path):
        self.__osbm.obj_logg.debug_logger(
            f"PdfView load_and_show_pdf_document(pdf_path):\npdf_path = {pdf_path}"
        )

        doc_location = QUrl.fromLocalFile(pdf_path)
        if doc_location.isLocalFile():
            print(f"doc_location = {doc_location}")
            self.__document.load(doc_location.toLocalFile())
``
### D:\vs_projects\auto-exec-doc\package\controllers\statusbar.py
``python
from PySide6.QtWidgets import (
    QStatusBar,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt

import package.components.dialogwindow.convertersettingsdialogwindow as convertersettingsdialogwindow

import resources_rc


class StatusBar:
    def __init__(self):
        self.__statusbar = None
        self.__is_active = False

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("StatusBar setting_all_osbm()")

    def get_is_active(self) -> bool:
        return self.__is_active

    def connect_statusbar(self, statusbar):
        """
        Подключить статусбар.
        """
        self.__osbm.obj_logg.debug_logger("StatusBar connect_statusbar(statusbar)")
        self.__statusbar = statusbar
        self.__is_active = True
        self.__timer = QTimer()
        self.__timer_count = 0
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        #
        self.config_statusbar()
        self.set_message("Проект не открыт")
        self.update_name_app_converter()
        self.connecting_actions()

    def config_update_statusbar(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_update_statusbar()")
        status_msword = self.__osbm.obj_offp.get_status_msword()
        self.update_status_msword_label(status_msword)
        status_libreoffice = self.__osbm.obj_offp.get_status_libreoffice()
        self.update_status_libreoffice_label(status_libreoffice)

    def config_statusbar(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_statusbar()")
        # конфигурация
        self.config_msword()
        self.config_libreoffice()
        #
        self.__statusbar.layout().setSpacing(4)
        # выбранный конвертер
        self.__name_app_converter = QLabel("NONE")
        self.__name_app_converter.setAlignment(Qt.AlignCenter)
        self.__name_app_converter.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(self.__name_app_converter)
        # кнопка настройки конвертера
        self.__btn_setting_converter = QPushButton("Настройка конвертера")
        self.__btn_setting_converter.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(self.__btn_setting_converter)
        # обновить statusbar
        self.config_update_statusbar()

    def get_red_circle(self) -> QLabel:
        icon = self.__icons.get("red_circle")
        label = QLabel()
        label.setPixmap(icon)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar get_red_circle() -> QLabel:\nlabel = {label}"
        )
        return label

    def get_yellow_circle(self) -> QLabel:
        icon = self.__icons.get("yellow_circle")
        label = QLabel()
        label.setPixmap(icon)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar get_yellow_circle() -> QLabel:\nlabel = {label}"
        )
        return label

    def get_green_circle(self) -> QLabel:
        icon = self.__icons.get("green_circle")
        label = QLabel()
        label.setPixmap(icon)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar get_green_circle() -> QLabel:\nlabel = {label}"
        )
        return label

    def config_msword(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_msword()")
        layout = QHBoxLayout()
        # иконка приложения
        icon = self.__icons.get("msword")
        label = QLabel()
        label.setPixmap(icon)
        layout.addWidget(label)
        # иконка статуса
        self.__red_msword = self.get_red_circle()
        self.__yellow_msword = self.get_yellow_circle()
        self.__green_msword = self.get_green_circle()
        layout.addWidget(self.__red_msword)
        layout.addWidget(self.__yellow_msword)
        layout.addWidget(self.__green_msword)
        layout.setContentsMargins(0, 0, 0, 0)
        # главный виджет
        mw_msword = QWidget()
        mw_msword.setLayout(layout)
        mw_msword.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(mw_msword)

    def config_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_libreoffice()")
        layout = QHBoxLayout()
        # иконка приложения
        icon = self.__icons.get("libreoffice")
        label = QLabel()
        label.setPixmap(icon)
        layout.addWidget(label)
        # иконка статуса
        self.__red_libreoffice = self.get_red_circle()
        self.__yellow_libreoffice = self.get_yellow_circle()
        self.__green_libreoffice = self.get_green_circle()
        layout.addWidget(self.__red_libreoffice)
        layout.addWidget(self.__yellow_libreoffice)
        layout.addWidget(self.__green_libreoffice)
        layout.setContentsMargins(0, 0, 0, 0)
        # главный виджет
        mw_libreoffice = QWidget()
        mw_libreoffice.setLayout(layout)
        mw_libreoffice.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(mw_libreoffice)

    def set_message(self, message: str, duration: int = 3000):
        """
        Поставить сообщение в статусбар.
        """
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar set_message(message):\nmessage = {message}"
        )
        if self.__timer.isActive():
            self.__timer.stop()
            self.__timer_count += 1
        self.__statusbar.showMessage(message + " ." * self.__timer_count)
        # Устанавливаем новый таймер для очистки сообщения
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(self.clear_message)
        self.__timer.start(duration) 

    def clear_message(self):
        self.__statusbar.clearMessage()
        self.__timer_count = 0


    def update_status_msword_label(self, status_msword):
        """Обновляется при запуске app"""
        if status_msword:
            self.__red_msword.setVisible(False)
            self.__yellow_msword.setVisible(False)
            self.__green_msword.setVisible(True)
        elif status_msword is None:
            self.__red_msword.setVisible(False)
            self.__yellow_msword.setVisible(True)
            self.__green_msword.setVisible(False)
        else:
            self.__red_msword.setVisible(True)
            self.__yellow_msword.setVisible(False)
            self.__green_msword.setVisible(False)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar update_status_status_msword_label(status_msword):\nstatus_msword = {status_msword}"
        )

    def update_status_libreoffice_label(self, status_libreoffice):
        """Обновляется при запуске app"""
        if status_libreoffice:
            self.__red_libreoffice.setVisible(False)
            self.__yellow_libreoffice.setVisible(False)
            self.__green_libreoffice.setVisible(True)
        elif status_libreoffice is None:
            self.__red_libreoffice.setVisible(False)
            self.__yellow_libreoffice.setVisible(True)
            self.__green_libreoffice.setVisible(False)
        else:
            self.__red_libreoffice.setVisible(True)
            self.__yellow_libreoffice.setVisible(False)
            self.__green_libreoffice.setVisible(False)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar update_status_libreoffice_label(status_libreoffice):\nstatus_libreoffice = {status_libreoffice}"
        )

    def update_name_app_converter(self):
        app_converter = self.__osbm.obj_settings.get_app_converter()
        print(f"app_converter = {app_converter}")
        name_app_converter = "None"
        if app_converter == "MSWORD":
            name_app_converter = "MS Word"
        elif app_converter == "LIBREOFFICE":
            name_app_converter = "LibreOffice"
        print(f"name_app_converter = {name_app_converter}")
        self.__name_app_converter.setText(name_app_converter)
        self.__osbm.obj_logg.debug_logger("StatusBar update_name_app_converter()")

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("StatusBar connecting_actions()")
        self.__btn_setting_converter.clicked.connect(self.show_converter_settings)

    def show_converter_settings(self):
        self.__osbm.obj_logg.debug_logger("StatusBar show_converter_settings()")
        self.__osbm.obj_convsdw = (
            convertersettingsdialogwindow.ConverterSettingsDialogWindow(
                self.__osbm
            )
        )
        self.__osbm.obj_convsdw.exec()


# obj_stab = StatusBar()

``
### D:\vs_projects\auto-exec-doc\package\controllers\style.py
``python
from PySide6.QtWidgets import (
    QWidget
)



class Style:

    def set_style_for(self, widget):
        widget.setStyleSheet(qss)


qss = """
/*!*************************************
    VS15 Dark
****************************************
    Author: chintsu_kun, holt59, MO2 Team
    Version: 2.5.0
    Licence: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)
    Source: https://github.com/nikolay-borzov/modorganizer-themes
****************************************
*/

/* For some reason applying background-color or border fixes paddings properties */
QListWidget::item {
    border-width: 0;
}

/* Don't override install label on download widget.
     MO2 assigns color depending on download state */
#installLabel {
    color: none;
}

/* Make `background-color` work for :hover, :focus and :pressed states */
QToolButton {
    border: none;
}

* {
    font-family: Open Sans;
}

/* Main Window */
QWidget {
    background-color: #2d2d30;
    color: #f1f1f1;
}

QWidget::disabled {
    color: #656565;
}

/* Common */
/* remove outline */
* {
    outline: 0;
}

*:disabled,
QListView::item:disabled,
*::item:selected:disabled {
    color: #656565;
}

/* line heights */
/* QTreeView#fileTree::item - currently have problem with size column vertical
     text align */
#bsaList::item,
#dataTree::item,
#modList::item,
#categoriesTree::item,
#savegameList::item,
#tabConflicts QTreeWidget::item {
    padding: 0.3em 0;
}

QListView::item,
QTreeView#espList::item {
    /*
    padding: 0.3em 0;
    */
}
QListView#lw_pages_template::item {
    padding: 0.2em 0;
}

/* to enable border color */
QTreeView,
QListView,
QTextEdit,
QWebView,
QTableView {
    border-style: solid;
    border-width: 1px;
}

QAbstractItemView {
    color: #dcdcdc;
    background-color: #1e1e1e;
    alternate-background-color: #262626;
    border-color: #3f3f46;
}

QAbstractItemView::item:selected,
QAbstractItemView::item:selected:hover,
QAbstractItemView::item:alternate:selected,
QAbstractItemView::item:alternate:selected:hover {
    color: #f1f1f1;
    background-color: #3399ff;
}

QAbstractItemView[filtered=true] {
    border: 2px solid #f00 !important;
}

QAbstractItemView,
QListView,
QTreeView {
    show-decoration-selected: 1;
}

QAbstractItemView::item:hover,
QAbstractItemView::item:alternate:hover,
QAbstractItemView::item:disabled:hover,
QAbstractItemView::item:alternate:disabled:hover QListView::item:hover,
QTreeView::branch:hover,
QTreeWidget::item:hover {
    background-color: rgba(51, 153, 255, 0.3);
}

QAbstractItemView::item:selected:disabled,
QAbstractItemView::item:alternate:selected:disabled,
QListView::item:selected:disabled,
QTreeView::branch:selected:disabled,
QTreeWidget::item:selected:disabled {
    background-color: rgba(51, 153, 255, 0.3);
}

QTreeView::branch:selected,
#bsaList::branch:selected {
    background-color: #3399ff;
}

QLabel {
    background-color: transparent;
}

LinkLabel {
    qproperty-linkColor: #3399ff;
}

/* Left Pane & File Trees #QTreeView, #QListView*/
QTreeView::branch:closed:has-children {
    image: url(:/png/resources/png/branch-closed.png);
}

QTreeView::branch:open:has-children {
    image: url(:/png/resources/png/branch-open.png);
}

QListView::item {
    color: #f1f1f1;
}

/* Text areas and text fields #QTextEdit, #QLineEdit, #QWebView */
QTextEdit,
QWebView,
QLineEdit,
QAbstractSpinBox,
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button,
QComboBox {
    background-color: #333337;
    border-color: #3f3f46;
}

QLineEdit:hover,
QAbstractSpinBox:hover,
QTextEdit:hover,
QComboBox:hover,
QComboBox:editable:hover {
    border-color: #007acc;
}

QLineEdit:focus,
QAbstractSpinBox::focus,
QTextEdit:focus,
QComboBox:focus,
QComboBox:editable:focus,
QComboBox:on {
    background-color: #3f3f46;
    border-color: #3399ff;
}

QComboBox:on {
    border-bottom-color: #3f3f46;
}

QLineEdit,
QAbstractSpinBox {
    min-height: 15px;
    padding: 2px;
    border-style: solid;
    border-width: 1px;
}

QLineEdit {
    margin-top: 0;
}

/* clear button */
QLineEdit QToolButton,
QLineEdit QToolButton:hover {
    background: none;
    margin-top: 1px;
}

QLineEdit#espFilterEdit QToolButton {
    margin-top: -2px;
    margin-bottom: 1px;
}

/* Drop-downs #QComboBox*/
QComboBox {
    min-height: 20px;
    padding-left: 5px;
    margin: 3px 0 1px 0;
    border-style: solid;
    border-width: 1px;
}

QComboBox:editable {
    padding-left: 3px;
    /* to enable hover styles */
    background-color: transparent;
}

QComboBox::drop-down {
    width: 20px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border: none;
}

QComboBox::down-arrow {
    image: url(:/png/resources/png/combobox-down.png);
}

QComboBox QAbstractItemView {
    background-color: #1b1b1c;
    selection-background-color: #3f3f46;
    border-color: #3399ff;
    border-style: solid;
    border-width: 0 1px 1px 1px;
}

/* Doesn't work http://stackoverflow.com/questions/13308341/qcombobox-abstractitemviewitem */
/* QComboBox QAbstractItemView:item {
    padding: 10px;
    margin: 10px;
} */
/* Toolbar */
QToolBar {
    border: none;
}

QToolBar::separator {
    border-left-color: #222222;
    border-right-color: #46464a;
    border-width: 0 1px 0 1px;
    border-style: solid;
    width: 0;
}

QToolButton {
    padding: 4px;
}

QToolButton:hover, QToolButton:focus {
    background-color: #3e3e40;
}

QToolButton:pressed {
    background-color: #3399ff;
}

QToolButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-top: 10%;
    padding-right: 5%;
}

/* Group Boxes #QGroupBox */
QGroupBox {
    border-color: #3f3f46;
    border-style: solid;
    border-width: 1px;
    /*
    padding: 1em 0.3em 0.3em 0.3em;
    margin-top: 0.65em;
    */
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px;
    left: 10px;
}

/* LCD Count */
QLCDNumber {
    border-color: #3f3f46;
    border-style: solid;
    border-width: 1px;
}

/* Buttons #QPushButton */
QPushButton {
    background-color: #333337;
    border-color: #3f3f46;
    min-height: 18px;
    padding: 2px 5px;
    border-style: solid;
    border-width: 1px;
}

QPushButton:hover,
QPushButton:checked,
QAbstractSpinBox::up-button:hover,
QAbstractSpinBox::down-button:hover {
    background-color: #007acc;
}

QPushButton:focus {
    border-color: #007acc;
}

QPushButton:pressed,
QPushButton:checked:hover,
QAbstractSpinBox::up-button:pressed,
QAbstractSpinBox::down-button:pressed {
    background-color: #1c97ea;
}

QPushButton:disabled,
QAbstractSpinBox::up-button:disabled,
QAbstractSpinBox::down-button:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}

QPushButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 5%;
}

/* Dialog buttons */
QSlider::handle:horizontal,
QSlider::handle:vertical {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}

QSlider::handle:horizontal:hover,
QSlider::handle:vertical:hover,
QSlider::handle:horizontal:pressed,
QSlider::handle:horizontal:focus:pressed,
QSlider::handle:vertical:pressed,
QSlider::handle:vertical:focus:pressed {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}

QSlider::handle:horizontal:focus,
QSlider::handle:vertical:focus {
    background-color: #dddddd;
    border-color: #3399ff;
}


QSlider::handle:horizontal:disabled,
QSlider::handle:vertical:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}


/* Check boxes and Radio buttons common #QCheckBox, #QRadioButton */
QListView::indicator,
QGroupBox::indicator,
QTreeView::indicator,
QCheckBox::indicator,
QRadioButton::indicator {
    background-color: #2d2d30;
    border-color: #3f3f46;
    width: 13px;
    height: 13px;
    border-style: solid;
    border-width: 1px;
}
QListView::indicator:hover,
QGroupBox::indicator:hover,
QTreeView::indicator:hover,
QCheckBox::indicator:hover,
QRadioButton::indicator:hover {
    background-color: #3f3f46;
    border-color: #007acc;
}
QListView::indicator:checked,
QGroupBox::indicator:checked,
QTreeView::indicator:checked,
QCheckBox::indicator:checked {
    image: url(:/png/resources/png/checkbox-check.png);
}
QListView::indicator:checked:disabled,
QGroupBox::indicator:disabled,
QTreeView::indicator:checked:disabled,
QCheckBox::indicator:checked:disabled {
    image: url(:/png/resources/png/checkbox-check-disabled.png);
}

/* Check boxes special */
QTreeView#modList::indicator {
    width: 15px;
    height: 15px;
}

/* Radio buttons #QRadioButton */
QRadioButton::indicator {
    border-radius: 7px;
}

QRadioButton::indicator::checked {
    background-color: #B9B9BA;
    border-width: 2px;
    width: 11px;
    height: 11px;
}

QRadioButton::indicator::checked:hover {
    border-color: #3f3f46;
}

/* Spinners #QSpinBox, #QDoubleSpinBox */
QAbstractSpinBox {
    margin: 1px;
}

QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button {
    border-style: solid;
    border-width: 1px;
    subcontrol-origin: padding;
}

QAbstractSpinBox::up-button {
    subcontrol-position: top right;
}

QAbstractSpinBox::up-arrow {
    image: url(:/png/resources/png/spinner-up.png);
}

QAbstractSpinBox::down-button {
    subcontrol-position: bottom right;
}

QAbstractSpinBox::down-arrow {
    image: url(:/png/resources/png/spinner-down.png);
}

/* Sliders #QSlider */
QSlider::groove:horizontal {
    background-color: #3f3f46;
    border: none;
    height: 8px;
    margin: 2px 0;
}

QSlider::handle:horizontal {
    width: 0.5em;
    height: 2em;
    margin: -7px 0;
    subcontrol-origin: margin;
}

/* Scroll Bars #QAbstractScrollArea, #QScrollBar*/
/* assigning background still leaves not filled area*/
QAbstractScrollArea::corner {
    background-color: transparent;
}

/* Horizontal */
QScrollBar:horizontal {
    height: 18px;
    border: none;
    margin: 0 23px 0 23px;
}

QScrollBar::handle:horizontal {
    min-width: 32px;
    margin: 4px 2px;
}

QScrollBar::add-line:horizontal {
    width: 23px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    width: 23px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

/* Vertical */
QScrollBar:vertical {
    width: 20px;
    border: none;
    margin: 23px 0 23px 0;
}

QScrollBar::handle:vertical {
    min-height: 32px;
    margin: 2px 4px;
}

QScrollBar::add-line:vertical {
    height: 23px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    height: 23px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

/* Combined */
QScrollBar {
    background-color: #3e3e42;
    border: none;
}

QScrollBar::handle {
    background-color: #686868;
}

QScrollBar::add-line,
QScrollBar::sub-line {
    background-color: #3e3e42;
    border: none;
}

/* QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::add-line:vertical:hover,
QScrollBar::sub-line:vertical:hover,
QScrollBar::add-line:horizontal:pressed,
QScrollBar::sub-line:horizontal:pressed,
QScrollBar::add-line:vertical:pressed,
QScrollBar::sub-line:vertical:pressed { } */
QScrollBar::handle:hover {
    background: #9e9e9e;
}

QScrollBar::handle:pressed {
    background: #efebef;
}

QScrollBar::handle:disabled {
    background: #555558;
}

QScrollBar::add-page,
QScrollBar::sub-page {
    background: transparent;
}

QScrollBar::up-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-up.png);
}

QScrollBar::up-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-up-hover.png);
}

QScrollBar::up-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-up-disabled.png);
}

QScrollBar::right-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-right.png);
}

QScrollBar::right-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}

QScrollBar::right-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-right-disabled.png);
}

QScrollBar::down-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-down.png);
}

QScrollBar::down-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-down-hover.png);
}

QScrollBar::down-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-down-disabled.png);
}

QScrollBar::left-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-left.png);
}

QScrollBar::left-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}

QScrollBar::left-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-left-disabled.png);
}

/* Header Rows and Tables (Configure Mod Categories) #QTableView, #QHeaderView */
QTableView {
    gridline-color: #3f3f46;
    selection-background-color: #3399ff;
    selection-color: #f1f1f1;
}

QTableView QTableCornerButton::section {
    background: #252526;
    border-color: #3f3f46;
    border-style: solid;
    border-width: 0 1px 1px 0;
}

QHeaderView {
    border: none;
}

QHeaderView::section {
    background: #252526;
    border-color: #3f3f46;
    padding: 3px 5px;
    border-style: solid;
    border-width: 0 1px 1px 0;
}

QHeaderView::section:hover {
    background: #3e3e40;
    color: #f6f6f6;
}

QHeaderView::section:last {
    border-right: 0;
}

QHeaderView::up-arrow {
    image: url(:/png/resources/png/sort-asc.png);
    width: 0px;
}


QHeaderView::down-arrow {
    image: url(:/png/resources/png/sort-desc.png);
    width: 0px;
}


/* Context menus, toolbar drop-downs #QMenu    */
QMenu {
    background-color: #1a1a1c;
    border-color: #333337;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}

QMenu::item {
    background: transparent;
    padding: 4px 20px;
}

QMenu::item:selected,
QMenuBar::item:selected {
    background-color: #333334;
}

QMenu::item:disabled {
    background-color: transparent;
}

QMenu::separator {
    background-color: #333337;
    height: 1px;
    margin: 1px 0;
}

QMenu::icon {
    margin: 1px;
}

QMenu::right-arrow {
    image: url(:/png/resources/png/sub-menu-arrow.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 0.5em;
}

QMenu QPushButton {
    background-color: transparent;
    border-color: #3f3f46;
    margin: 1px 0 1px 0;
}

QMenu QCheckBox,
QMenu QRadioButton {
    background-color: transparent;
    padding: 5px 2px;
}

/* Tool tips #QToolTip, #SaveGameInfoWidget */
QToolTip,
SaveGameInfoWidget {
    background-color: #424245;
    border-color: #4d4d50;
    color: #f1f1f1;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}

QStatusBar::item {
    border: None;
}

/* Progress Bars (Downloads) #QProgressBar */
QProgressBar {
    background-color: #e6e6e6;
    color: #000;
    border-color: #bcbcbc;
    text-align: center;
    border-style: solid;
    border-width: 1px;
    margin: 0px;
}

QProgressBar::chunk {
    background: #06b025;
}

DownloadListView[downloadView=standard]::item {
    padding: 16px;
}

DownloadListView[downloadView=compact]::item {
    padding: 4px;
}

/* Right Pane and Tab Bars #QTabWidget, #QTabBar */
QTabWidget::pane {
    border-color: #3f3f46;
    border-top-color: #007acc;
    top: 0;
    border-style: solid;
    border-width: 1px;
}

QTabWidget::pane:disabled {
    border-top-color: #3f3f46;
}

QTabBar::tab {
    background-color: transparent;
    padding: 4px 1em;
    border: none;
}

QTabBar::tab:hover {
    background-color: #1c97ea;
}

QTabBar::tab:selected,
QTabBar::tab:selected:hover {
    background-color: #007acc;
}

QTabBar::tab:disabled {
    background-color: transparent;
    color: #656565;
}

QTabBar::tab:selected:disabled {
    background-color: #3f3f46;
}

/* Scrollers */
QTabBar QToolButton {
    background-color: #333337;
    border-color: #3f3f46;
    padding: 1px;
    margin: 0;
    border-style: solid;
    border-width: 1px;
}

QTabBar QToolButton:hover {
    border-color: #007acc;
    border-width: 1px;
    border-style: solid;
}

QTabBar QToolButton:disabled,
QTabBar QToolButton:pressed:hover {
    background-color: #333337;
}

QTabBar::scroller {
    width: 23px;
    background-color: red;
}

QTabBar QToolButton::right-arrow {
    image: url(:/png/resources/png/scrollbar-right.png);
}

QTabBar QToolButton::right-arrow:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}

QTabBar QToolButton::left-arrow {
    image: url(:/png/resources/png/scrollbar-left.png);
}

QTabBar QToolButton::left-arrow:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}

/* Special styles */
QWidget#tabImages QPushButton {
    background-color: transparent;
    margin: 0 0.3em;
    padding: 0;
}

/* like dialog QPushButton*/
QWidget#tabESPs QToolButton {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}

QWidget#tabESPs QToolButton:hover {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}

QWidget#tabESPs QToolButton:focus {
    background-color: #dddddd;
    border-color: #3399ff;
}

QWidget#tabESPs QToolButton:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}

QTreeWidget#categoriesList {
    /* min-width: 225px; */
}

QTreeWidget#categoriesList::item {
    background-position: center left;
    background-repeat: no-repeat;
    padding: 0.35em 10px;
}

QTreeWidget#categoriesList::item:has-children {
    background-image: url(:/png/resources/png/branch-closed.png);
}

QTreeWidget#categoriesList::item:has-children:open {
    background-image: url(:/png/resources/png/branch-open.png);
}

QDialog#QueryOverwriteDialog QPushButton {
    margin-left: 0.5em;
}

QDialog#PyCfgDialog QPushButton:hover {
    background-color: #BEE6FD;
}

QLineEdit#modFilterEdit {
    margin-top: 2px;
}

/* highlight unchecked BSAs */
QWidget#bsaTab QTreeWidget::indicator:unchecked {
    background-color: #3399ff;
}

/* increase version text field */
QLineEdit#versionEdit {
    max-width: 100px;
}

/* Dialogs width changes */
/* increase width to prevent buttons cutting */
QDialog#QueryOverwriteDialog {
    min-width: 565px;
}

QDialog#ModInfoDialog {
    min-width: 850px;
}

QLineEdit[valid-filter=false] {
    background-color: #661111 !important;
}

/* собственное решение */
QToolBar QToolButton:disabled {
    background-color: #252526;
}

QToolBar QToolButton:checked {
    background-color: #3399ff;
}

"""


from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QApplication

import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(qss)
        self.setWindowTitle("Custom with Sorting Table")


        # Основной виджет с QVBoxLayout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        # Создание таблицы
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)  # Устанавливаем количество строк
        self.tableWidget.setColumnCount(3)  # Устанавливаем количество колонок

        # Установка заголовков
        self.tableWidget.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])

        # Заполнение таблицы данными
        for row in range(5):
            for column in range(3):
                item = QTableWidgetItem(f'Item {row},{column}')
                self.tableWidget.setItem(row, column, item)

        # Включение сортировки
        self.tableWidget.setSortingEnabled(True)

        # Добавление таблицы в компоновку
        layout.addWidget(self.tableWidget)

        self.resize(400, 300)

# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())


``
### D:\vs_projects\auto-exec-doc\package\controllers\tabwinputforms.py
``python
import os
import json
from functools import partial

import package.components.widgets.customsection as customsection

import package.components.widgets.forms.formdate as formdate
import package.components.widgets.forms.formimage as formimage
import package.components.widgets.forms.formtable as formtable
import package.components.widgets.forms.formtext as formtext
import package.components.widgets.forms.formlongtext as formlongtext
import package.components.widgets.forms.formlist as formlist

from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QMenu
from PySide6.QtGui import QAction, Qt

class TabWInputForms:    
    def __init__(self):
        self.__tab_widget = None
    
    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("TabWInputForms setting_all_osbm()")

    def connect_inputforms(self, tab_widget):
        """
        Подключить tab_widget для управления вкладками
        """
        self.__osbm.obj_logg.debug_logger("TabWInputForms connect_inputforms(tab_widget)")
        self.__tab_widget = tab_widget
        self.__icons = self.__osbm.obj_icons.get_icons()        #

    def delete_all_tabs(self):  
        """
        Удаление всех вкладок в tabw_inputforms
        """
        self.__osbm.obj_logg.debug_logger("TabWInputForms delete_all_tabs()")
        self.__tab_widget.clear()

    def get_section_name(self, section_info) -> str:
        """
        Определение типа/названия секции
        """
        self.__osbm.obj_logg.debug_logger(f"TabWInputForms get_section_name(section_info):\nsection_info = {section_info}") 
        section_type = section_info.get("type")
        section_name = None
        if section_type == "page":
            page = section_info.get("page")
            section_name = f'Страница: {page.get("name_page")}'
        elif section_type == "template":
            template = section_info.get("template")
            section_name = f'Шаблон: {template.get("name_template")}'
        elif section_type == "group":
            group = section_info.get("group")
            section_name = f'Группа: {group.get("name_node")}'
        elif section_type == "project":
            project = section_info.get("project")
            section_name = project.get("name_node")
        return section_name
    

    def add_form_in_tab(self, tab_layout, pair, type_section):
        """
        Добавление формы во вкладку в зависимости от типа контента.
        НЕ ВКЛЮЧЕН В logger!!!
        """
        id_variable = pair.get("id_variable")
        current_variable = self.__osbm.obj_prodb.get_variable_by_id(id_variable)
        type_variable = current_variable.get("type_variable")
        config_variable = current_variable.get("config_variable")
        config_dict = dict()        
        if config_variable:
            config_dict = json.loads(config_variable)

        item = None
        if type_variable == "TEXT":
            item = formtext.FormText(self.__osbm, pair, current_variable)
        elif type_variable == "LONGTEXT":
            item = formlongtext.FormLongText(self.__osbm, pair, current_variable)
        elif type_variable == "DATE":
            item = formdate.FormDate(self.__osbm, pair, current_variable, config_dict)
        elif type_variable == "IMAGE":
            item = formimage.FormImage(self.__osbm, pair, current_variable, config_dict)
        elif type_variable == "TABLE":
            item = formtable.FormTable(self.__osbm, pair, current_variable, config_dict)
        elif type_variable == "LIST":
            item = formlist.FormList(self.__osbm, pair, current_variable)

        if item:
            # setSizePolicy тут нужон 
            item.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            #
            item.setContextMenuPolicy(Qt.CustomContextMenu)
            item.customContextMenuRequested.connect(
                lambda pos: self.context_menu(pos, item, current_variable, type_section)
            )
            tab_layout.addWidget(item)

    def context_menu(self, pos, item, current_variable, type_section, *args):
        """
        Меню по правой кнопки мыши (ui.treewidget_structure_execdoc)
        """
        menu = QMenu(item)
        # action_edit_variables для всех
        action_edit_variables = QAction(
            "Изменить в редакторе переменных", item
        )
        action_edit_variables.setIcon(self.__icons.get("edit_variables"))
        action_edit_variables.triggered.connect(
            lambda: self.__osbm.obj_mw.edit_menu_item("VARIABLE", "EDIT", current_variable, type_section)
        )
        menu.addAction(action_edit_variables)
        #
        menu.exec(item.mapToGlobal(pos))


    def add_sections_in_tabs(self):
        self.__osbm.obj_logg.debug_logger("TabWInputForms add_sections_in_tabs()")
        
        sections_info = self.__osbm.obj_seci.get_sections_info()

        for section_info in sections_info:
            try:
                section_name = self.get_section_name(section_info)

                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

                tab_content = QWidget()
                tab_layout = QVBoxLayout(tab_content)
                tab_layout.setSpacing(9)

                # Добавление форм в вкладку
                data_section = section_info.get("data")
                type_section = section_info.get("type")
                for pair in data_section:
                    self.add_form_in_tab(tab_layout, pair, type_section)

                # Добавление кнопки "Сбросить значения"
                reset_button = QPushButton("Сбросить все значения вкладки")
                reset_button.clicked.connect(partial(self.reset_tab_values, tab_layout))
                tab_layout.addWidget(reset_button)

                # Добавление пустого виджета
                tab_layout.addItem(
                    QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
                )
                # Добавление виджета и вкладки
                scroll_area.setWidget(tab_content)
                self.__tab_widget.addTab(scroll_area, section_name)

            except Exception as e:
                self.__osbm.obj_logg.error_logger(f"Error in add_sections_in_tabs(): {e}")

    def reset_tab_values(self, tab_layout):
        for i in range(tab_layout.count()):
            widget = tab_layout.itemAt(i).widget()
            if hasattr(widget, 'reset_value'):
                widget.reset_value()
        # TODO сделать reset_value (data_rowcol -> [""])
        # [{"id_rowcol": "4b73557866c011ef8fbfdce9947e4a05", "data_rowcol": [""]}, {"id_rowcol": "5207feeb66c011ef8450dce9947e4a05", "data_rowcol": [""]}]
        

    def update_tabs(self, page):
        self.__osbm.obj_logg.debug_logger("TabWInputForms update_tabs()")
        self.delete_all_tabs()        
        if page is not None:
            self.__osbm.obj_seci.update_sections_info(page)
            self.add_sections_in_tabs()

``
### D:\vs_projects\auto-exec-doc\package\controllers\twstructureexecdoc.py
``python
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt


class TWStructureExecDoc:
    def __init__(self):
        self.__tw = None
        self.__icons = None
        self.__nodes_to_items = dict()
        self.__expanded_states = dict()

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("TWStructureExecDoc setting_all_osbm()")

    def connect_structureexecdoc(self, tr_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        self.__osbm.obj_logg.debug_logger(
            "TWStructureExecDoc connect_structureexecdoc(tr_sed)"
        )
        self.__tw = tr_sed
        self.__icons = self.__osbm.obj_icons.get_icons()

        # Очистить при запуске
        self.clear_sed()

        self.__tw.currentItemChanged.connect(
            lambda current: current and self.current_item_changed(current)
        )
        self.__tw.itemChanged.connect(lambda item: item and self.item_changed(item))
        # раскрытие/свертывание элементов
        self.__tw.itemExpanded.connect(self.on_item_expanded)
        self.__tw.itemCollapsed.connect(self.on_item_collapsed)

    def get_current_node(self):
        self.__osbm.obj_logg.debug_logger("TWStructureExecDoc get_current_node()")
        current_item = self.__tw.currentItem()
        if current_item is None:
            return None
        else:
            return current_item.data(0, Qt.UserRole)

    def get_all_items_with_states(self):
        """Получить все items с их состояниями включения"""
        items_states = {}
        for id_node, item in self.__nodes_to_items.items():
            items_states[id_node] = item.checkState(0) == Qt.Checked
        return items_states

    def current_item_changed(self, current):
        self.__osbm.obj_logg.debug_logger(
            f"TWStructureExecDoc current_item_changed(current):\ncurrent = {current}"
        )
        node = current.data(0, Qt.UserRole)
        # обновить combobox -> страницы
        self.__osbm.obj_comt.update_combox_templates(node)

    def item_changed(self, item):
        self.__osbm.obj_logg.debug_logger(
            f"TWStructureExecDoc item_changed(item):\nitem = {item}"
        )
        if item is not None:
            self.__tw.blockSignals(True)
            node = item.data(0, Qt.UserRole)
            state = int(item.checkState(0) == Qt.Checked)
            self.set_state_included_for_child(node, item.checkState(0) == Qt.Checked)
            self.__osbm.obj_prodb.set_included_for_node(node, state)  # Сохраняем сразу в БД
            self.__tw.blockSignals(False)

    def clear_sed(self):
        """
        Очистить дерево
        """
        self.__osbm.obj_logg.debug_logger("TWStructureExecDoc clear_tr_sed()")
        if self.__tw is not None:
            self.__tw.blockSignals(True)
            self.__tw.clear()
            self.__tw.setHeaderLabels([""])
            self.__tw.blockSignals(False)

    def update_structure_exec_doc(self):
        """
        Создает структуру дерева ИД
        """
        self.__osbm.obj_logg.debug_logger(
            "TWStructureExecDoc update_structure_exec_doc()"
        )
        #
        open_node = self.get_current_node()
        self.__open_node_flag = False
        # очистка
        self.clear_sed()
        # Задать название столбца
        title = f"{self.__osbm.obj_settings.get_project_current_name()}"
        self.__tw.setHeaderLabels([title])
        # проход по вершинам
        self.dfs(self.__osbm.obj_prodb.get_project_node(), open_node)
        #
        if self.__tw.topLevelItemCount() > 0 and not self.__open_node_flag:
            self.__tw.setCurrentItem(self.__tw.topLevelItem(0))

    def dfs(self, parent_node, open_node=None):
        """
        Проход по всем вершинам.
        """
        self.__osbm.obj_logg.debug_logger(
            f"TWStructureExecDoc dfs(parent_node):\nparent_node = {parent_node}\n open_node = {open_node}"
        )
        childs = self.__osbm.obj_prodb.get_childs(parent_node)
        if childs:
            # Сортировка по order_node
            childs.sort(key=lambda node: int(node.get("order_node")))
            for child in childs:
                # действие
                self.set_item_in_nodes_to_items(child, open_node)
                # проход по дочерним вершинам
                self.dfs(child, open_node)


    def set_item_in_nodes_to_items(self, node, open_node=None):
        """
        Поставить item в nodes_to_items.
        """
        self.__osbm.obj_logg.debug_logger(
            f"TWStructureExecDoc set_item_in_nodes_to_items(node):\nnode = {node}"
        )
        self.__tw.blockSignals(True)
        # добавляем вершину
        item = self.add_item_in_tree_widget(node)
        # текст в зависимости от типа
        self.set_text_and_icon_for_item_by_node(item, node)
        # раскрытие вершины
        self.set_expanded_for_item(item, node)
        # С галочкой по умолчанию
        state = node.get("included")
        item.setCheckState(0, Qt.Checked if state else Qt.Unchecked)
        self.__nodes_to_items[node.get("id_node")] = item
        # если было до clear
        if open_node and open_node.get("id_node") == node.get("id_node"):
            self.__tw.setCurrentItem(item)
            self.__open_node_flag = True
        #
        self.__tw.blockSignals(False)

    def add_item_in_tree_widget(self, node) -> object:
        self.__osbm.obj_logg.debug_logger(
            f"TWStructureExecDoc add_item_in_tree_widget(node):\nnode = {node}"
        )
        item = None
        if node.get("id_parent") == 0:
            item = QTreeWidgetItem(self.__tw)
            item.setData(0, Qt.UserRole, node)
        else:
            item = QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])
            item.setData(0, Qt.UserRole, node)
        return item

    def set_text_and_icon_for_item_by_node(self, item, node):
        self.__osbm.obj_logg.debug_logger(
            f"TWStructureExecDoc get_text_by_node(item, node):\nitem = {item},\nnode = {node}"
        )
        # иконки
        if node.get("type_node") == "FORM":
            icon = self.__icons.get("form")
            icon = item.setIcon(0, icon)
        elif node.get("type_node") == "GROUP":
            icon = self.__icons.get("group")
            icon = item.setIcon(0, icon)
        # текст
        text = node.get("name_node")
        item.setText(0, text)

    def set_expanded_for_item(self, item, node):
        self.__osbm.obj_logg.debug_logger(
            f"TWStructureExecDoc set_expanded_for_item(item, node):\nitem = {item},\nnode = {node}"
        )
        id_node = node.get("id_node")
        value_expand = self.__expanded_states.get(id_node)
        if value_expand is not None:
            item.setExpanded(value_expand)
        else:
            self.__expanded_states["id_node"] = False
            item.setExpanded(False)

    def set_state_included_for_child(self, node, state):
        self.__osbm.obj_logg.debug_logger(
            f"""TWStructureExecDoc set_state_included_for_childs(node, state):\nid_node = {node.get("id_node")},\nstate = {state}"""
        )
        item = self.__nodes_to_items.get(node.get("id_node"))
        if item is not None:
            item.setCheckState(0, Qt.Checked if state else Qt.Unchecked)
            # Сохраняем состояние текущего узла
            self.__osbm.obj_prodb.set_included_for_node(node, state)
            
            childs = self.__osbm.obj_prodb.get_childs(node)
            if childs:
                for child in childs:
                    self.set_state_included_for_child(child, state)

    def on_item_expanded(self, item):
        """Элемент раскрыт"""
        node = item.data(0, Qt.UserRole)
        id_node = node.get("id_node")
        self.__expanded_states[id_node] = True

    def on_item_collapsed(self, item):
        """Элемент свернут"""
        node = item.data(0, Qt.UserRole)
        id_node = node.get("id_node")
        self.__expanded_states[id_node] = False


# obj_twsed = TWStructureExecDoc()
``
### D:\vs_projects\auto-exec-doc\package\controllers\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\modules\-settingsdatabase.py
``python
# import sqlite3
# import datetime
# import os

# class SettingsDatabaseObjectsManager:
#     def __init__(self, osbm):
#         self.obj_logg = osbm.obj_logg
#         self.obj_dirm = osbm.obj_dirm

# class SettingsDatabase:
#     def __init__(self):
#         pass

#     def setting_osbm(self, osbm):
#         self.__osbm = SettingsDatabaseObjectsManager(osbm)

#     def create_and_setting_db_settings(self):
#         """
#         Настройка базы данных перед использованием приложения
#         """
#         self.__osbm.obj_logg.debug_logger(
#             "SettingsDatabase create_and_setting_db_settings()"
#         )
#         if not os.path.exists(self.__osbm.obj_dirm.get_db_settings_dirpath()):
#             # создать путь
#             os.mkdir(self.__osbm.obj_dirm.get_db_settings_dirpath())
#             # Добавляем данные в пустую БД
#             self.add_tables_and_datas_to_empty_db_settings()

#     # region Методы add (tables, values)

#     def add_tables_and_datas_to_empty_db_settings(self):
#         """
#         Добавление таблиц и данных в БД программы.
#         """
#         self.__osbm.obj_logg.debug_logger(
#             "SettingsDatabase add_tables_and_datas_to_empty_db_settings()"
#         )
#         conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_settings_dirpath())
#         cursor = conn.cursor()

#         cursor.executescript("""
# BEGIN TRANSACTION;
# CREATE TABLE IF NOT EXISTS "Projects" (
# 	"id_project"	INTEGER NOT NULL UNIQUE,
# 	"name_project"	TEXT NOT NULL,
# 	"directory_project"	TEXT NOT NULL,
# 	"date_create_project"	TEXT NOT NULL,
# 	"date_last_open_project"	TEXT NOT NULL,
# 	PRIMARY KEY("id_project" AUTOINCREMENT)
# );
# CREATE TABLE IF NOT EXISTS "Settings" (
# 	"id_setting"	INTEGER NOT NULL UNIQUE,
# 	"name_setting"	TEXT NOT NULL UNIQUE,
# 	"value_setting"	TEXT,
# 	PRIMARY KEY("id_setting" AUTOINCREMENT)
# );
# INSERT INTO "Projects" VALUES (20,'gdgffdg','C:/Users/hayar/Documents/AutoExecDoc Projects/gdgffdg','2024-08-10 16:36:35','2024-08-10 16:54:21');
# INSERT INTO "Projects" VALUES (21,'dsdf','C:/Users/hayar/Documents/AutoExecDoc Projects/dsdf','2024-08-10 16:57:31','2024-08-10 21:16:56');
# INSERT INTO "Settings" VALUES (1,'app_converter','LIBREOFFICE');
# INSERT INTO "Settings" VALUES (2,'libreoffice_path','C:\Program Files\LibreOffice\program\soffice.exe');
# INSERT INTO "Settings" VALUES (3,'project_current_name',NULL);
# COMMIT;
#         """)

#         conn.commit()
#         conn.close()

#     def get_conn(self) -> object:
#         """
#         Запрос курсора.
#         """
#         self.__osbm.obj_logg.debug_logger("SettingsDatabase get_conn() -> object")
#         conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_settings_dirpath())
#         conn.row_factory = sqlite3.Row
#         return conn

#     def get_fetchall(self, cursor):
#         self.__osbm.obj_logg.debug_logger(
#             "SettingsDatabase get_fetchall(cursor, conn) -> list"
#         )
#         cursor_result = cursor.fetchall()
#         result = [dict(row) for row in cursor_result] if cursor_result else []
#         return result

#     def get_fetchone(self, cursor):
#         self.__osbm.obj_logg.debug_logger(
#             "SettingsDatabase get_fetchone(cursor, conn) -> list"
#         )
#         cursor_result = cursor.fetchone()
#         result = dict(cursor_result) if cursor_result else {}
#         return result

#     def add_new_project_to_db(self):
#         """
#         Добавление в БД новый проекта.
#         """
#         self.__osbm.obj_logg.debug_logger(
#             "SettingsDatabase add_new_project_to_db()"
#         )
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         name_project = os.path.basename(
#             self.__osbm.obj_dirm.get_project_dirpath()
#         )
#         directory_project = self.__osbm.obj_dirm.get_project_dirpath()
#         # текущее время для date_create_project и для date_last_open_project
#         current_datetime = datetime.datetime.now().replace(microsecond=0)
#         cursor.execute(
#             "INSERT INTO Projects (name_project, directory_project, date_create_project, date_last_open_project) VALUES (?, ?, ?, ?)",
#             (name_project, directory_project, current_datetime, current_datetime),
#         )

#         conn.commit()
#         conn.close()

#     def update_project_to_db(self):
#         """
#         Обновление проекта в БД.
#         """
#         self.__osbm.obj_logg.debug_logger("SettingsDatabase update_project_to_db()")

#         conn = self.get_conn()
#         cursor = conn.cursor()
#         name_project = os.path.basename(
#             self.__osbm.obj_dirm.get_project_dirpath()
#         )
#         directory_project = self.__osbm.obj_dirm.get_project_dirpath()
#         # текущее время для date_last_open_project
#         current_datetime = datetime.datetime.now().replace(microsecond=0)
#         cursor.execute(
#             "UPDATE Projects SET date_last_open_project = ? WHERE name_project = ? AND directory_project = ?",
#             (current_datetime, name_project, directory_project),
#         )
#         conn.commit()
#         conn.close()

#     def add_or_update_open_project_to_db(self):
#         """
#         Добавление или обновление открытого проекта в БД.
#         """
#         self.__osbm.obj_logg.debug_logger(
#             "SettingsDatabase add_or_update_open_project_to_db()"
#         )
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         name_project = os.path.basename(
#             self.__osbm.obj_dirm.get_project_dirpath()
#         )
#         directory_project = self.__osbm.obj_dirm.get_project_dirpath()
#         print(f"name_project = {name_project}")
#         # узнать, если проект в БД по имени и директории
#         cursor.execute(
#             "SELECT * FROM Projects WHERE name_project = ? AND directory_project = ?",
#             (name_project, directory_project),
#         )
#         result = self.get_fetchone(cursor)
#         conn.commit()
#         conn.close()
#         print(f"result = {result}")
#         if result == {}:
#             self.add_new_project_to_db()
#         else:
#             self.update_project_to_db()

#     def get_app_converter(self) -> str:
#         """
#         Запрос значения app_converter из БД.
#         """
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT value_setting FROM Settings WHERE name_setting = 'app_converter'"
#         )
#         result = self.get_fetchone(cursor)
#         conn.close()
#         self.__osbm.obj_logg.debug_logger(
#             f"SettingsDatabase get_app_converter():\nresult = {result}"
#         )
#         return result.get("value_setting")

#     def set_app_converter(self, app_converter: str):
#         """
#         Установка значения app_converter в БД.
#         """
#         self.__osbm.obj_logg.debug_logger(
#             f"SettingsDatabase set_app_converter(app_converter):\napp_converter = {app_converter}"
#         )
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE Settings SET value_setting = ? WHERE name_setting = 'app_converter'",
#             (app_converter,),
#         )
#         conn.commit()
#         conn.close()

#     def get_last_projects(self) -> list:
#         """
#         Запрос последних пяти проектов из БД.
#         """
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT * FROM Projects ORDER BY date_last_open_project DESC LIMIT 5"
#         )
#         result = self.get_fetchall(cursor)
#         conn.close()
#         self.__osbm.obj_logg.debug_logger(
#             f"SettingsDatabase get_last_projects():\nresult = {result}"
#         )
#         return result


#     def get_libreoffice_path(self) -> str:
#         """
#         Запрос значения libreoffice_path из БД.
#         """
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT value_setting FROM Settings WHERE name_setting = 'libreoffice_path'"
#         )
#         result = self.get_fetchone(cursor)
#         conn.close()
#         self.__osbm.obj_logg.debug_logger(
#             f"SettingsDatabase get_libreoffice_path():\nresult = {result}"
#         )
#         return result.get("value_setting")

#     def get_project_current_name(self):
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT value_setting FROM Settings WHERE name_setting = 'project_current_name'"
#         )
#         result = self.get_fetchone(cursor)
#         conn.close()
#         self.__osbm.obj_logg.debug_logger(
#             f"SettingsDatabase get_project_current_name():\nresult = {result}"
#         )
#         return result.get("value_setting")

#     def set_project_current_name(self, project_name):
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE Settings SET value_setting = ? WHERE name_setting = 'project_current_name'",
#             (project_name,),
#         )
#         self.__osbm.obj_logg.debug_logger(
#             f"SettingsDatabase set_project_current_name(project_name):\nproject_name = {project_name}"
#         )
#         conn.commit()
#         conn.close()

#     def delete_project_from_db(self, project):
#         self.__osbm.obj_logg.debug_logger(
#             f"SettingsDatabase delete_project_from_db(project):\nproject = {project}"
#         )
#         conn = self.get_conn()
#         cursor = conn.cursor()
#         cursor.execute(
#             "DELETE FROM Projects WHERE name_project = ? AND directory_project = ?",
#             (project.get("name_project"), project.get("directory_project")),
#         )
#         conn.commit()
#         conn.close()

# # obj_settings = SettingsDatabase()

``
### D:\vs_projects\auto-exec-doc\package\modules\converter.py
``python
import os
import json
import copy
import functools

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
# from docx.enum.text import WD_BREAK
# from docx import Document

import threading
import multiprocessing

import pythoncom
import comtypes.client
import subprocess

from PySide6.QtCore import QDate, QLocale

from pypdf import PdfWriter
import datetime

import package.modules.convertervarimage as convertervarimage


class ConverterPool:
    def __init__(self):
        self.__cashe_temp_images = dict()
        self.__is_word_active = False

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
            else:
                default_value = local_osbm.obj_com.default_value
                if default_value == "variable":
                    data_variable[str(name_variable)] = name_variable
                else:
                    data_variable[str(name_variable)] = ""
        except Exception as e:
            local_osbm.obj_logg.error_logger(f"Error in type_variable_is_text: {e}")

    def type_variable_is_list(self, local_osbm, data_variable, name_variable, value):
        local_osbm.obj_logg.debug_logger(
            f"Converter type_variable_is_list(data_variable, name_variable, value):\ndata_variable = {data_variable},\nname_variable = {name_variable},\nvalue = {value}"
        )
        try:
            if value:
                data = json.loads(value)
                data_variable[str(name_variable)] = data
            else:
                default_value = local_osbm.obj_com.default_value
                if default_value == "variable":
                    data_variable[str(name_variable)] = [name_variable]
                else:
                    data_variable[str(name_variable)] = []
        except Exception as e:
            local_osbm.obj_logg.error_logger(f"Error in type_variable_is_list: {e}")

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
            else:
                default_value = local_osbm.obj_com.default_value
                if default_value == "variable":
                    data_variable[str(name_variable)] = name_variable
                else:
                    data_variable[str(name_variable)] = ""
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
                # размер контейнера в emu
                emu_sizes = convvarimg.get_emu_width_and_height_by_unit(
                    unit, width, height
                )
                emu_width = emu_sizes[0]
                emu_height = emu_sizes[1]
                # размер контейнера в мм
                mm_sizes = convvarimg.get_mm_width_and_height_by_emu(
                    emu_width, emu_height
                )
                mm_width = mm_sizes[0]
                mm_height = mm_sizes[1]
                # проверить в словаре
                is_reimage = True
                add_dict = dict()
                cashe_dict = self.__cashe_temp_images.get(value, None)
                #
                if cashe_dict:
                    is_reimage = False
                    temp_image = cashe_dict.get("temp_image", None)
                    temp_width = cashe_dict.get("width", None)
                    temp_height = cashe_dict.get("height", None)
                else:
                    temp_image = convvarimg.get_temp_image(value)
                    add_dict["temp_image"] = temp_image
                #
                inline_image = InlineImage(docx_template, temp_image)
                if sizing_mode == "NOCHANGES":
                    pass
                elif sizing_mode == "CONTAIN":
                    # только ширину ради пропорции
                    if is_reimage:
                        scaled_mm_sizes = convvarimg.contain_sizing_mode(
                            temp_image, mm_width, mm_height
                        )
                        inline_image.width = Mm(scaled_mm_sizes[0])
                        add_dict["width"] = scaled_mm_sizes[0]
                    else:
                        inline_image.width = Mm(temp_width)
                elif sizing_mode == "COVER":
                    # только ширину ради пропорции
                    if is_reimage:
                        scaled_mm_sizes = convvarimg.cover_sizing_mode(
                            temp_image, mm_width, mm_height
                        )
                        inline_image.width = Mm(scaled_mm_sizes[0])
                        add_dict["width"] = scaled_mm_sizes[0]
                    else:
                        inline_image.width = Mm(temp_width)
                elif sizing_mode == "FILL":
                    if is_reimage:
                        inline_image.width = Mm(mm_width)
                        inline_image.height = Mm(mm_height)
                        add_dict["width"] = mm_width
                        add_dict["height"] = mm_height
                    else:
                        inline_image.width = Mm(temp_width)
                        inline_image.height = Mm(temp_height)

                # добавить новое если впервый раз
                if is_reimage:
                    self.__cashe_temp_images[value] = add_dict
                #
                data_variable[str(name_variable)] = inline_image
            else:
                default_value = local_osbm.obj_com.default_value
                if default_value == "variable":
                    data_variable[str(name_variable)] = name_variable
                else:
                    data_variable[str(name_variable)] = ""
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
            if value:
                current_variable = local_osbm.obj_prodb.get_variable_by_id(id_variable)
                config_variable = current_variable.get("config_variable")
                config_dict = dict()
                if config_variable:
                    config_dict = json.loads(config_variable)
                # config_dict: шаблон записи
                id_to_attr_dict = dict()
                object_entry = dict()
                #
                headers_table = []
                rowcols = sorted(
                    config_dict.get("ROWCOLS", []), key=lambda x: x.get("ORDER", 0)
                )
                for rowcol in rowcols:
                    attr_rowcol = rowcol.get("ATTR")
                    id_rowcol = rowcol.get("ID")
                    title_rowcol = rowcol.get("TITLE")
                    id_to_attr_dict[id_rowcol] = attr_rowcol
                    object_entry[attr_rowcol] = str()
                    headers_table.append(title_rowcol)
                # заполнять data_variable
                data = json.loads(value)
                # таблица и словрь записей
                values_table = []
                entrys = dict()
                # проходим по всем rowcol
                for rowcol in data:
                    id_rowcol = rowcol.get("id_rowcol")
                    # если есть атрибут в config_dict
                    if id_rowcol in id_to_attr_dict:
                        attr_rowcol = id_to_attr_dict.get(id_rowcol)
                        data_rowcol = rowcol.get("data_rowcol")
                        # проходим по всем значениям data_rowcol с именем attr_rowcol
                        for i, cell_value in enumerate(data_rowcol):
                            entry = entrys.get(i)
                            entry = entry if entry else copy.deepcopy(object_entry)
                            entry[attr_rowcol] = cell_value
                            entrys[i] = entry
                # проходим по записям entrys
                for object_entry in entrys.values():
                    for key, value in object_entry.items():
                        print(f"key = {key}, value = {value}")
                        object_entry[key] = self.get_cell_value(data_variable, value)
                    values_table.append(object_entry)
                #
                data_table = {"h": headers_table, "v": values_table}
                data_variable[str(name_variable)] = data_table
            else:
                default_value = local_osbm.obj_com.default_value
                if default_value == "variable":
                    data_table = {"h": ["..."], "v": ["..."]}
                    data_variable[str(name_variable)] = data_table
                else:
                    data_table = {"h": [""], "v": [""]}
                    data_variable[str(name_variable)] = data_table
        except Exception as e:
            local_osbm.obj_logg.error_logger(f"Error in type_variable_is_table: {e}")

    def get_cell_value(self, data_variable, cell_value):
        result = cell_value
        if cell_value:
            if str(cell_value).startswith("{{ ") and str(cell_value).endswith(" }}"):
                result = data_variable.get(cell_value[3:-3], cell_value)
            else:
                try:
                    json_data = json.loads(cell_value)
                    if isinstance(json_data, list) or isinstance(json_data, dict) or isinstance(json_data, str):
                        result = json_data
                except Exception as e:
                    pass
        print(f"get_cell_value: cell_value = {cell_value}, result = {result}")
        return result

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
        elif not is_rerender and type_variable == "LIST":
            self.type_variable_is_list(local_osbm, data_variable, name_variable, value)
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
        self.rerender(local_osbm, template_path, docx_path, sections_info)

    def rerender(self, local_osbm, template_path, docx_path, sections_info):
        local_osbm.obj_logg.debug_logger(
            f"Converter rerender(template_path, docx_path, sections_info):\ntemplate_path = {template_path},\ndocx_path = {docx_path},\nsections_info = {sections_info}"
        )
        current_path = template_path
        flag = 10
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
            # print(f"BEFORE SAVE data_variable = {data_variable}")
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
        app_converter = local_osbm.obj_settings.get_app_converter()
        if app_converter == "MSWORD":
            self.convert_from_docx_to_pdf_using_msword(local_osbm, docx_path, pdf_path)
        # elif app_converter == "OPENOFFICE":
        #     self.convert_from_docx_to_pdf_using_openoffice(docx_path, pdf_path)
        elif app_converter == "LIBREOFFICE":
            self.convert_from_docx_to_pdf_using_libreoffice(
                local_osbm, docx_path, pdf_path
            )

    def get_active_msword(self, local_osbm):
        local_osbm.obj_logg.debug_logger("Converter get_active_msword()")
        try:
            pythoncom.CoInitialize()
            word = comtypes.client.GetActiveObject("Word.Application")
            self.__is_word_active = True
        except Exception as e:
            local_osbm.obj_logg.error_logger(
                "Error in Converter.get_active_msword():"
            )
            self.__is_word_active = False
            # raise local_osbm.obj_com.errors.MsWordError(e)
        
    def convert_from_docx_to_pdf_using_msword(self, local_osbm, docx_path, pdf_path):
        local_osbm.obj_logg.debug_logger(
            "Converter convert_from_docx_to_pdf_using_msword(docx_path, pdf_path)"
        )
        try:
            self.__is_word_active = False
            thread = threading.Thread(target=self.get_active_msword, args=(local_osbm,))
            thread.start()
            # ждём 3 секунды
            thread.join(3)
            if thread.is_alive():
                raise local_osbm.obj_com.errors.MsWordError(
                    "Error in convert_from_docx_to_pdf_using_msword(): Timeout"
                )
            if not self.__is_word_active:
                raise local_osbm.obj_com.errors.MsWordError(
                    "Error in convert_from_docx_to_pdf_using_msword(): Word object is not available"
                )
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
            libreoffice_path = local_osbm.obj_settings.get_libreoffice_path()
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
        self.obj_settings = osbm.obj_settings
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
                    id_active_template = child.get("id_active_template")
                    if id_active_template:
                        template = {"id_template": id_active_template}
                        pages = self.__osbm.obj_prodb.get_pages_by_template(template)
                        for page in pages:
                            # если страница включена
                            if page.get("included"):
                                object = {
                                    "type": "page",
                                    "page": page,
                                    "number_page": self.__number_page,
                                }
                                # print(f"object = {object}")
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
        app_converter = self.__osbm.obj_settings.get_app_converter()
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

``
### D:\vs_projects\auto-exec-doc\package\modules\convertervarimage.py
``python
import os
from docx.shared import Length


class ConverterVarImage:
    """
    Зависимый от Converter класс.
    """

    def __init__(self, osbm):
        self.__osbm = osbm

    def get_original_image_path_by_file_name_with_png(self, file_name_with_png) -> str:
        # получить путь к изображению
        original_image_path = os.path.abspath(
            os.path.join(
                self.__osbm.obj_dirm.get_images_folder_dirpath(),
                file_name_with_png,
            )
        )
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_original_image_path_by_file_name_with_png() -> str:\n result = {original_image_path}"
        )
        return original_image_path

    def get_temp_image_path(self, file_name_with_png) -> str:
        # путь к временному файлу
        temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
        temp_file_path = os.path.join(temp_dir, file_name_with_png)
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_temp_image_path() -> str:\n result = {temp_file_path}"
        )
        return temp_file_path

    def get_temp_image(self, file_name_with_png) -> str:
        # пути
        original_image_path = self.get_original_image_path_by_file_name_with_png(
            file_name_with_png
        )
        temp_file_path = self.get_temp_image_path(file_name_with_png)
        # копирование
        self.__osbm.obj_film.copy_file(original_image_path, temp_file_path)
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_temp_image(file_name_with_png) -> str:\nfile_name_with_png = {file_name_with_png} \n result = {temp_file_path}"
        )
        #
        return temp_file_path

    def get_emu_width_and_height_by_unit(self, unit, width, height) -> tuple:
        emu_width = float()
        emu_height = float()
        #
        if unit == "MM":
            emu_width = width * Length._EMUS_PER_MM
            emu_height = height * Length._EMUS_PER_MM
        elif unit == "CM":
            emu_width = width * Length._EMUS_PER_CM
            emu_height = height * Length._EMUS_PER_CM
        elif unit == "INCH":
            emu_width = width * Length._EMUS_PER_INCH
            emu_height = height * Length._EMUS_PER_INCH
        elif unit == "PT":
            emu_width = width * Length._EMUS_PER_PT
            emu_height = height * Length._EMUS_PER_PT
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_emu_width_and_height_by_unit() -> tuple:\n result = ({emu_width}, {emu_height})"
        )
        #
        return emu_width, emu_height

    def get_mm_width_and_height_by_emu(self, emu_width, emu_height) -> tuple:
        mm_width = emu_width / float(Length._EMUS_PER_MM)
        mm_height = emu_height / float(Length._EMUS_PER_MM)
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_mm_width_and_height_by_emu() -> tuple:\n result = ({mm_width}, {mm_height})"
        )
        #
        return mm_width, mm_height

    def contain_sizing_mode(self, temp_image, mm_width, mm_height) -> tuple:
        # размеры изображения
        image_width, image_height = self.__osbm.obj_imgr.get_sizes_image(temp_image)
        # коэффициенты
        width_ratio = mm_width / image_width
        height_ratio = mm_height / image_height
        # минимальный коэффициент
        scale_factor = min(width_ratio, height_ratio)
        # новый размеры
        scaled_mm_width = image_width * scale_factor
        scaled_mm_height = image_height * scale_factor
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage contain_sizing_mode() -> tuple:\n result = ({scaled_mm_width}, {scaled_mm_height})"
        )
        #
        return scaled_mm_width, scaled_mm_height

    def cover_sizing_mode(self, temp_image, mm_width, mm_height) -> tuple:
        # размеры изображения
        image_width, image_height = self.__osbm.obj_imgr.get_sizes_image(temp_image)
        # 
        height = 1000
        width_a = (image_width / image_height) * height
        width_b = (mm_width / mm_height) * height
        # новый уменьшенный размер
        if width_a > width_b:
            new_image_width = image_height * (mm_height / mm_width)
            new_image_height = image_height
        else:
            new_image_width = image_width
            new_image_height = image_width * (mm_width / mm_height)
        #
        self.__osbm.obj_imgr.crop_image(temp_image, image_width, image_height, new_image_width, new_image_height)
        #
        self.__osbm.obj_logg.debug_logger(f"ConverterVarImage cover_sizing_mode() -> tuple:\n result = ({new_image_width}, {new_image_height})")
        #
        return mm_width, mm_height
        






        
``
### D:\vs_projects\auto-exec-doc\package\modules\dirpathsmanager.py
``python
import os
import tempfile

from PySide6.QtCore import QStandardPaths


class ObjectsManagerDirPathManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg

class DirPathManager:
    def __init__(self):
        self.__main_dirpath = ""
        self.__documents_dirpath = ""
        self.__pictures_dirpath = ""
        self.__temp_dirpath = ""
        self.__default_folder_projects_dirpath = ""
        self.__db_settings_dirpath = ""
        self.__db_original_project_dirpath = ""
        self.__project_dirpath = ""
        self.__db_project_dirpath = ""
        self.__logs_dirpath = ""
        self.__forms_folder_dirpath = ""
        self.__images_folder_dirpath = ""
        self.__global_documents_dirpath = ""
        self.__global_images_dirpath = ""


    def setting_osbm(self, osbm):
        self.__osbm = ObjectsManagerDirPathManager(osbm)
        self.__osbm.obj_logg.debug_logger(f"DirPathManager setting_osbm():\nself.__osbm = {self.__osbm}")


    def setting_paths(self, main_dirpath):
        self.__osbm.obj_logg.debug_logger("DirPathManager setting_paths()")
        # путь к main.py
        self.__main_dirpath = main_dirpath

        # путь к Документы
        self.__documents_dirpath = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
        )
        # путь к Изображения
        self.__pictures_dirpath = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.PicturesLocation
        )

        # путь к папке с Temp
        self.__temp_dirpath = tempfile.mkdtemp()

        # путь к папке с проектами по умолчанию
        self.__default_folder_projects_dirpath = os.path.join(
            self.__documents_dirpath, "AutoExecDoc Projects"
        )

        # путь к папке к базе данных
        self.__db_settings_dirpath = os.path.join(
            self.__main_dirpath, "db", "settings.db"
        )
        self.__db_original_project_dirpath = os.path.join(
            self.__main_dirpath, "db", "project.db"
        )

        # путь к директории проекта
        self.__project_dirpath = None
        # путь к project.db проекта
        self.__db_project_dirpath = None

        # путь к папке с логами
        self.__logs_dirpath = os.path.join(
            self.__main_dirpath, "logs"
        )

        # путь к папке с формами (по умолчанию проект не загружен поэтому и пусто)
        self.__forms_folder_dirpath = None
        self.__images_folder_dirpath = None
        self.__pdfs_filder_dirpath = None


    def set_new_dirpaths_for_project(self):
        self.__osbm.obj_logg.debug_logger("DirPathManager set_new_dirpaths_for_project()")
        # папка forms в проекте
        self.__forms_folder_dirpath = os.path.join(
            self.get_project_dirpath(), "forms"
        )

        # папка images в проекте
        self.__images_folder_dirpath = os.path.join(
            self.get_project_dirpath(), "images"
        )

        # папка pdfs в проекте
        self.__pdfs_filder_dirpath = os.path.join(
            self.get_project_dirpath(), "pdfs"
        )

    def get_forms_folder_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_forms_folder_dirpath() -> str: {self.__forms_folder_dirpath}"
        )
        return self.__forms_folder_dirpath

    def get_images_folder_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_image_folder_dirpath() -> str: {self.__images_folder_dirpath}"
        )
        return self.__images_folder_dirpath

    def get_pdfs_folder_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"get_pdfs_folder_dirpath() -> str: {self.__pdfs_filder_dirpath}"
        )
        return self.__pdfs_filder_dirpath

    def set_project_dirpath(self, dirpath: str):
        self.__project_dirpath = dirpath
        self.__osbm.obj_logg.debug_logger(f"DirPathManager set_project_dirpath(dirpath: str):\ndirpath = {dirpath}")

    def set_db_project_dirpath(self, dirpath: str):
        self.__db_project_dirpath = dirpath
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager set_db_project_dirpath(dirpath: str):\ndirpath = {dirpath}"
        )

    def get_main_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_main_dirpath() -> str: {self.__main_dirpath}"
        )
        return self.__main_dirpath

    def get_documents_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_documents_dirpath() -> str: {self.__documents_dirpath}"
        )
        return self.__documents_dirpath

    def get_pictures_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_pictures_dirpath() -> str: {self.__pictures_dirpath}"
        )
        return self.__pictures_dirpath

    def get_folder_in_documents_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_folder_in_documents_dirpath() -> str: {self._folder_in_documents_dirpath}"
        )
        return self._folder_in_documents_dirpath

    def get_db_settings_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_db_settings_dirpath() -> str: {self.__db_settings_dirpath}"
        )
        return self.__db_settings_dirpath

    def get_default_folder_projects_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_default_folder_projects_dirpath() -> str: {self.__default_folder_projects_dirpath}"
        )
        return self.__default_folder_projects_dirpath

    def get_logs_dirpath(self) -> str:
        # ТУТ НЕ НУЖЕН self.__osbm.obj_logg.debug_logger()
        return self.__logs_dirpath

    def get_project_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_project_dirpath() -> str: {self.__project_dirpath}"
        )
        return self.__project_dirpath

    def get_db_project_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_db_project_dirpath() -> str: {self.__db_project_dirpath}"
        )
        return self.__db_project_dirpath

    def get_db_original_project_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_db_original_project_dirpath() -> str: {self.__db_original_project_dirpath}"
        )
        return self.__db_original_project_dirpath

    def get_temp_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger("DirPathManager get_temp_dirpath() -> str:")
        return self.__temp_dirpath

    def set_new_temp_dirpath(self):
        self.__temp_dirpath = tempfile.mkdtemp()
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager set_temp_dirpath(dirpath: str):\n__temp_dirpath = {self.__temp_dirpath}"
        )


# obj_dirm = DirPathManager()
``
### D:\vs_projects\auto-exec-doc\package\modules\filefoldermanager.py
``python
import os
import shutil
import base64
import datetime
import uuid

class FileFolderManagerObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm
        self.obj_settings = osbm.obj_settings


class FileFolderManager:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = FileFolderManagerObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(f"FileFolderManager setting_osbm():\nself.__osbm = {self.__osbm}")


    def create_and_setting_files_and_folders(self):
        """
        Создание и конфигурация папок и файлов.
        """
        self.__osbm.obj_logg.debug_logger(
            "FileFolderManager create_and_setting_files_and_folders()"
        )
        if not os.path.exists(
            self.__osbm.obj_dirm.get_default_folder_projects_dirpath()
        ):
            os.mkdir(self.__osbm.obj_dirm.get_default_folder_projects_dirpath())

    def check_aed_file(self):
        """
        Создание файла aed.
        """
        self.__osbm.obj_logg.debug_logger("FileFolderManager check_aed_file()")
        # создать указатель файл
        name_aed = self.__osbm.obj_settings.get_project_current_name()
        aedfilename = f"{name_aed}.aed"
        aedfilepath = os.path.join(
            self.__osbm.obj_dirm.get_project_dirpath(), aedfilename
        )
        if not os.path.exists(aedfilepath):
            aedfile = open(aedfilepath, "a+")
            # перевести в base64
            message = f"{aedfilename} {aedfilepath} {datetime.datetime.now()}"
            message_bytes = message.encode("utf-8")
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode("utf-8")
            print(base64_message)
            # записать в файл
            aedfile.write(base64_message)
            aedfile.close()

    def create_folders_and_aed_for_project(self):
        """
        Добавление в проект папок форм.
        """
        self.__osbm.obj_logg.debug_logger(
            "FileFolderManager create_folders_and_aed_for_project()"
        )
        # файл project.aed
        self.check_aed_file()
        # папка forms в проекте
        forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()

        if not os.path.exists(forms_folder_dirpath):
            os.makedirs(forms_folder_dirpath)

        # папка images в проекте
        image_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()

        if not os.path.exists(image_folder_dirpath):
            os.makedirs(image_folder_dirpath)

        # # папка с pdfs
        pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()

        if not os.path.exists(pdfs_folder_dirpath):
            os.makedirs(pdfs_folder_dirpath)

        # Папка TEMP/AUTOEXECDOC
        if not os.path.exists(self.__osbm.obj_dirm.get_temp_dirpath()):
            os.makedirs(self.__osbm.obj_dirm.get_temp_dirpath())


    def clear_temp_folder(self, is_del_folder=False):
        """
        Очистка папки temp.
        """
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager clear_temp_folder(is_del_folder):\nis_del_folder = {is_del_folder},\ntemp_dirpath = {self.__osbm.obj_dirm.get_temp_dirpath()}"
        )
        temp_dirpath = self.__osbm.obj_dirm.get_temp_dirpath()
        try:
            shutil.rmtree(temp_dirpath)
            if not is_del_folder:
                os.mkdir(temp_dirpath)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in clear_temp_folder(): {e}")

    def move_image_from_temp_to_project(self, name_image):
        self.__osbm.obj_logg.debug_logger(
            "FileFolderManager move_image_from_temp_to_project()"
        )
        # путь к папке с шаблонами
        temp_dirpath = self.__osbm.obj_dirm.get_temp_dirpath()
        image_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()
        try:
            shutil.move(
                os.path.join(temp_dirpath, name_image),
                os.path.join(image_folder_dirpath, name_image),
            )
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def delete_image_from_project(self, image_dirpath):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager delete_image_from_project(image_dirpath):\nimage_dirpath = {image_dirpath}"
        )
        # путь к папке с шаблонами
        image_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()
        print(f"image_folder_dirpath = {image_folder_dirpath}")
        try:
            os.remove(os.path.join(image_folder_dirpath, image_dirpath))
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def copy_project_for_saveas(self, old_folder_path, new_folder_path):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager copy_project_for_saveas(old_folder_path, new_folder_path):\nold_folder_path = {old_folder_path},\nnew_folder_path = {new_folder_path}"
        )
        for f in os.listdir(old_folder_path):
            src_path = os.path.join(old_folder_path, f)
            dest_path = os.path.join(new_folder_path, f)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            elif os.path.isfile(src_path):
                if not f.endswith(".aed"):
                    shutil.copy(src_path, dest_path)

    def copy_file(self, src_path, dest_path):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager copy_file(src_path, dest_path):\nsrc_path = {src_path},\ndest_path = {dest_path}"
        )
        try:
            shutil.copy(src_path, dest_path)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def docx_from_temp_to_forms(self, temp_copy_file_path, file_name):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager docx_from_temp_to_forms(temp_copy_file_path, file_name):\ntemp_copy_file_path = {temp_copy_file_path},\nfile_name = {file_name}"
        )
        # к папке с шаблонами
        forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
        try:
            file_name_with_docx = file_name + ".docx"
            shutil.move(
                temp_copy_file_path,
                os.path.join(forms_folder_dirpath, file_name_with_docx),
            )
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def pdf_from_temp_to_pdfs(self, temp_copy_file_path, file_name):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager pdf_from_temp_to_pdfs(temp_copy_file_path, file_name):\ntemp_copy_file_path = {temp_copy_file_path},\nfile_name = {file_name}"
        )
        # к папке с pdfs
        pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
        try:
            file_name_with_docx = file_name + ".pdf"
            shutil.move(
                temp_copy_file_path,
                os.path.join(pdfs_folder_dirpath, file_name_with_docx),
            )
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def copynew_page_for_new_template(self, old_page_filename, typefile_page):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager copynew_page_for_new_template(old_page_filename, typefile_page):\nold_page_filename = {old_page_filename},\ntypefile_page = {typefile_page}"
        )
        old_page_path = str()
        new_page_path = str()
        # генерируем новый id и имя для новой страницы
        unique_id = f"{str(uuid.uuid4().hex)[:3]}-{id(old_page_path)%1000}"
        new_page_filename = f"{unique_id}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        # в зависимости от ...
        if typefile_page == "DOCX":
            forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
            old_page_path = os.path.join(forms_folder_dirpath, old_page_filename + ".docx")
            new_page_path = os.path.join(forms_folder_dirpath, new_page_filename + ".docx")
        elif typefile_page == "PDF":
            pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
            old_page_path = os.path.join(pdfs_folder_dirpath, old_page_filename + ".pdf") 
            new_page_path = os.path.join(pdfs_folder_dirpath, new_page_filename + ".pdf")       
        # копирование
        self.copy_file(old_page_path, new_page_path)       
        return new_page_filename

    def delete_page_from_project(self, page_filename, typefile_page):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager delete_page_from_project(page_filename, typefile_page):\npage_filename = {page_filename}\n typefile_page = {typefile_page}"
        )
        if typefile_page == "DOCX":
            forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
            page_path = os.path.join(forms_folder_dirpath, page_filename + ".docx")
        elif typefile_page == "PDF":
            pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
            page_path = os.path.join(pdfs_folder_dirpath, page_filename + ".pdf")
        #
        try:
            os.remove(page_path)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def get_list_of_docx_in_forms_folder(self):
        forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
        result = os.listdir(forms_folder_dirpath)
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager get_list_of_docx_in_forms_folder(): \n result = {result}"
        )
        return result
    
    def get_list_of_pdfs_in_pdfs_folder(self):
        pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
        result = os.listdir(pdfs_folder_dirpath)
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager get_list_of_pdfs_in_pdfs_folder(): \n result = {result}"
        )
        return result
    
    def get_list_of_images_in_images_folder(self):
        images_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()
        result = os.listdir(images_folder_dirpath)
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager get_list_of_images_in_images_folder(): \n result = {result}"
        )
        return result
    

# obj_film = FileFolderManager()  
``
### D:\vs_projects\auto-exec-doc\package\modules\imageresizer.py
``python
import os

from PIL import Image as PilImage
from PIL import ExifTags


class ImageResizerObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm
        self.obj_film = osbm.obj_film


class ImageResizer:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = ImageResizerObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer setting_osbm():\nself.__osbm = {self.__osbm}"
        )

    def save_image_then_selected(self, image_dirpath, file_name_with_format):
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer save_image_then_selected(image_dirpath, file_name_with_format):\nimage_dirpath = {image_dirpath} \n file_name_with_format = {file_name_with_format}"
        )
        # пути: к временной папке, к временному файлу
        temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
        temp_file_path = os.path.join(temp_dir, file_name_with_format)
        # Открыть изображение, Сохранить изображение в временный файл
        image = PilImage.open(image_dirpath)
        # Получение EXIF данных
        if hasattr(image, "_getexif"):
            exif = image._getexif()
            if exif is not None:
                orientation = None
                for tag, value in exif.items():
                    if ExifTags.TAGS.get(tag) == "Orientation":
                        orientation = value
                        break
                # Корректировка ориентации
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        # Сохранить изображение во временный файл
        image.save(temp_file_path, "PNG")

    def get_sizes_image(self, image_dirpath):
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer get_sizes_image(image_dirpath):\nimage_dirpath = {image_dirpath}"
        )
        image = PilImage.open(image_dirpath)
        width, height = image.size
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer get_sizes_image(image_dirpath) -> tuple:\n result = ({width}, {height})"
        )
        return width, height

    def crop_image(
        self, temp_image, image_width, image_height, new_image_width, new_image_height
    ):
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer crop_image(temp_image, image_width, image_height, new_image_width, new_image_height):\n"
            f"temp_image = {temp_image} \n"
            f"image_width = {image_width} \n"
            f"image_height = {image_height} \n"
            f"new_image_width = {new_image_width} \n"
            f"new_image_height = {new_image_height}"
        )
        new_image_width = int(new_image_width)
        new_image_height = int(new_image_height)
        #
        image = PilImage.open(temp_image)
        # Обрезаем изображение до размеров контейнера
        left = (image_width - new_image_width) // 2
        top = (image_height - new_image_height) // 2
        right = (image_width + new_image_width) // 2
        bottom = (image_height + new_image_height) // 2
        #
        image = image.crop((left, top, right, bottom))
        #
        image.save(temp_image)

``
### D:\vs_projects\auto-exec-doc\package\modules\log.py
``python
import logging
import datetime
import os
from concurrent.futures import ThreadPoolExecutor

class LogObjectsManager:
    def __init__(self, osbm):
        self.obj_dirm = osbm.obj_dirm

class Log:
    def __init__(self):
        self.__osbm = None
        self.__logger = logging.getLogger("Main logger")

    def setting_osbm(self, osbm):
        self.__osbm = LogObjectsManager(osbm)

    def setting_logger(self):
        log_folder = self.__osbm.obj_dirm.get_logs_dirpath()

        log_file = os.path.join(
            log_folder,
            str(datetime.datetime.now().replace(microsecond=0)).replace(":", "-")
            + ".log",
        )

        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        
        # FileHandler для записи логов в файл
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # StreamHandler для вывода логов в консоль
        console_handler = logging.StreamHandler()       
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)      

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(console_handler)
        self.__logger.setLevel(logging.DEBUG)

        self.debug_logger("Config logger")

    def debug_logger(self, message: str):
        self.__logger.debug(f"\033[34m {message}\033[00m")

    def info_logger(self, message: str):
        self.__logger.info(f"\033[32m {message}\033[00m")

    def warning_logger(self, message: str):
        self.__logger.warning(f"\033[93m {message}\033[00m")

    def error_logger(self, message: str):
        self.__logger.error(f"\033[31m {message}\033[00m")

    def critical_logger(self, message: str):
        self.__logger.critical(f"\033[95m {message}\033[00m")

    def disable_logging(self):
        """Отключение логирования, удаление всех обработчиков."""
        handlers = self.__logger.handlers[:]
        for handler in handlers:
            self.__logger.removeHandler(handler)
            # Закрываем обработчик, чтобы освободить ресурсы
            handler.close() 
``
### D:\vs_projects\auto-exec-doc\package\modules\officepackets.py
``python
from PySide6.QtCore import QThread, Signal

import traceback
import comtypes.client
import pythoncom
import os
import threading

class MsWordThread(QThread):
    # cигнал для обновления статуса (object - любые объекты, включая None)
    status_changed = Signal(object)

    def __init__(self, osbm):
        super().__init__()
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("MsWordThread __init__()")
        self.__status_msword = False

    def run(self):
        self.initialize_msword()

    def get_active_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread get_active_msword()")
        try:
            pythoncom.CoInitialize()
            self.__word = comtypes.client.GetActiveObject("Word.Application")
            self.__status_msword = True
        except Exception as e:
            self.__osbm.obj_logg.debug_logger(f"No active Word instance: {e}")
            self.__status_msword = False
            

    def initialize_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread initialize_msword()")
        try:
            pythoncom.CoInitialize()
            self.__status_msword = None
            self.status_changed.emit(self.__status_msword)
            
            thread = threading.Thread(target=self.get_active_msword)
            thread.start()
            thread.join(3)
            
            if thread.is_alive() or not self.__status_msword:
                try:
                    self.__word = comtypes.client.CreateObject("Word.Application")
                    self.__status_msword = True
                except Exception as create_error:
                    self.__osbm.obj_logg.error_logger(f"Error creating Word.Application: {create_error}")
                    self.__status_msword = False
                    
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in initialize_msword(): {e} ? {traceback.format_exc()}")
            self.__status_msword = False
        finally:
            self.status_changed.emit(self.__status_msword)

    def terminate_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread terminate_msword()")
        try:
            if hasattr(self, '_MsWordThread__word') and self.__word:
                self.__word.Quit()
                self.__status_msword = False
        except Exception as e:
            self.__status_msword = False
            self.__osbm.obj_logg.error_logger(f"Error in terminate_msword(): {e} ? {traceback.format_exc()}")
        


class OfficePackets:
    def __init__(self):
        self.__status_msword = False
        self.__status_libreoffice = False

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("OfficePackets setting_all_osbm()")

    def resetting_office_packets(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets resetting_office_packets()")
        # экземпляр QThread
        if not self.__status_msword:
            try:
                self.__msword_thread = MsWordThread(self.__osbm)
                # подключение сигнала к слоту и запуск потока
                self.__msword_thread.status_changed.connect(self.update_status_msword)
                self.__msword_thread.start()
            except Exception as e:
                self.__osbm.obj_logg.error_logger(f"Error creating MsWordThread: {e}")
                self.__status_msword = False
        else:
            print("MsWordThread is already running")
        # проверка наличия LibreOffice
        self.run_libreoffice()
            
        
    def update_status_msword(self, status):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets update_status_msword(status):\nstatus = {status}"
        )
        self.__status_msword = status
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_msword_label(self.__status_msword)

    def get_status_msword(self):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets get_status_msword():\nself.__status_msword = {self.__status_msword}"
        )
        return self.__status_msword

    def get_status_libreoffice(self):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets get_status_libreoffice():\nself.__status_libreoffice = {self.__status_libreoffice}"
        )
        return self.__status_libreoffice
    
    def run_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets run_libreoffice()")
        libreoffice_path = self.__osbm.obj_settings.get_libreoffice_path()
        if os.path.exists(libreoffice_path):
            self.__status_libreoffice = True
        else:
            self.__status_libreoffice = False
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_libreoffice_label(
                self.__status_libreoffice
            )

    def terminate_msword(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets terminate_msword()")
        try:
            if hasattr(self, '_OfficePackets__msword_thread') and self.__msword_thread:
                self.__msword_thread.terminate_msword()
                self.__msword_thread.quit()
                self.__msword_thread.wait()
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in OfficePackets.terminate_msword():\n {e}  ? {traceback.format_exc()}")
        finally:
            self.__status_msword = False

    def terminate_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets terminate_libreoffice()")
        self.__status_libreoffice = False


    def run_individual_msword(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets run_individual_msword()")
        def run_msword():
            try:
                word = comtypes.client.CreateObject("Word.Application")
            except Exception as e:
                self.__osbm.obj_logg.error_logger(
                    f"OfficePackets run_individual_msword():\nerror = {e} ? {traceback.format_exc()}"
                )
        individual_thread = threading.Thread(target=run_msword)
        individual_thread.start()

``
### D:\vs_projects\auto-exec-doc\package\modules\project.py
``python
import os
import time


class Project:
    def __init__(self):
        # по умолчанию None
        self.__current_name = None
        # по умолчанию False
        self.__status_active = False
        self.__status_save = False

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("Project setting_all_osbm()")

    def is_active_status(self) -> bool:
        self.__osbm.obj_logg.debug_logger(
            f"Project is_active_status() -> bool: {self.__status_active}"
        )
        return self.__status_active

    def is_status_save(self) -> bool:
        self.__osbm.obj_logg.debug_logger(
            f"Project is_status_save() -> bool: {self.__status_save}"
        )
        return self.__status_save

    def check_project_before_new_or_open(self) -> bool:
        """
        Проверка текущего проекта до создания или открытия нового.
        """
        self.__osbm.obj_logg.debug_logger(
            "Project check_project_before_new_or_open()"
        )
        # появление диалогового окна, когда проект активен, но не сохранен
        if self.__status_active and not self.__status_save:
            answer = self.__osbm.obj_dw.save_active_project()
            if answer == "Yes":
                self.save_project()
                return True
            elif answer == "Cancel":
                # отменяет создание проекта
                return False
        return True

    def set_project_dirpaths(self, folder_path: str):
        """
        Установка путей к папке проекта.
        Установка пути к project.db проекта.
        """
        self.__osbm.obj_logg.debug_logger(
            f"Project set_project_dirpaths(folder_path: str):\nfolder_path = {folder_path}"
        )
        # Установка пути к папке проекта
        self.__osbm.obj_dirm.set_project_dirpath(folder_path)
        # Установка пути к project.db проекта
        self.__osbm.obj_dirm.set_db_project_dirpath(
            os.path.join(self.__osbm.obj_dirm.get_project_dirpath(), "project.db")
        )

    def new_project(self):
        """
        Действие создание проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project new_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = self.__osbm.obj_dw.select_folder_for_new_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.clear_window_before_new_or_open_project()
                self.config_new_project()

    def clear_window_before_new_or_open_project(self):
        self.__osbm.obj_logg.debug_logger(
            "Project clear_window_before_new_or_open_project()"
        )
        # очистка structureexecdoc
        self.__osbm.obj_twsed.clear_sed()
        # очистка comboxts
        self.__osbm.obj_comt.clear_comboxts()
        # очистка pages_template
        self.__osbm.obj_lwpt.clear_pt()
        # очистка pdfview
        self.__osbm.obj_pdfv.set_empty_pdf_view()
        # очистка inputforms
        self.__osbm.obj_tabwif.delete_all_tabs()

    def config_new_project(self):
        """
        Конфигурация нового проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project config_new_project()")

        self.__current_name = os.path.basename(
            self.__osbm.obj_dirm.get_project_dirpath()
        )
        self.__osbm.obj_settings.set_project_current_name(self.__current_name)

        self.__osbm.obj_settings.add_new_project_to_db()
        self.__osbm.obj_prodb.create_and_config_db_project()
        # настраиваем контроллеры
        # обновляем окно
        self.__osbm.obj_mw.update_main_window()
        # пути для проекта
        self.__osbm.obj_dirm.set_new_dirpaths_for_project()
        # добавляем папки в новый проект
        self.__osbm.obj_film.create_folders_and_aed_for_project()
        # активируем проект
        self.set_true_actives_project()
        # сообщение для статусбара
        self.__osbm.obj_stab.set_message(
            f"Проект c именем {self.__current_name} создан и открыт."
        )
        # обновляем меню
        self.__osbm.obj_mw.update_menu_recent_projects()

    def save_project(self):
        """
        Сохранение проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project save_project()")
        if self.__status_active:
            # сохранить в базу данных
            self.__osbm.obj_dw.process_save_start()
            self.__osbm.obj_seci.save_data_to_database()
            if self.__osbm.obj_lwpt.is_page_template_selected():
                # получить значение высоты страницы
                saved_view_sizes = self.__osbm.obj_pdfv.get_view_sizes()
                # сохранить в pdf (обработчик ошибок внутри obj_lwpt)
                self.__osbm.obj_lwpt.current_page_to_pdf()
                # восстановить высоту страницы
                self.__osbm.obj_pdfv.set_view_sizes(saved_view_sizes)
            # настроить статус
            self.__status_save = True
            self.__osbm.obj_stab.set_message(
                f"Проект c именем {self.__current_name} сохранён."
            )
            self.__osbm.obj_dw.process_save_end()
        else:
            self.__osbm.obj_stab.set_message(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )
            self.__osbm.obj_dw.warning_message(
                "Нечего сохранять.\nЛибо проект не открыт, либо форма не выбрана.",
            )

    def saveas_project(self):
        """
        Сохранение проекта под новым именем или в новом месте.
        """
        self.__osbm.obj_logg.debug_logger("Project saveas_project()")
        if self.__status_active:
            old_folder_path = self.__osbm.obj_dirm.get_project_dirpath()
            # Запрашиваем новое имя или новую директорию для сохранения
            new_folder_path = (
                self.__osbm.obj_dw.select_folder_for_saveas_project()
            )
            if new_folder_path:
                # Установка путей к новому проекту
                self.set_project_dirpaths(new_folder_path)
                # копирование проекта
                self.__osbm.obj_film.copy_project_for_saveas(
                    old_folder_path, new_folder_path
                )
                # открытие проекта
                self.config_open_project()
            else:
                self.__osbm.obj_stab.set_message("Сохранение отменено.")
                self.__osbm.obj_dw.warning_message("Сохранение отменено.")
        else:
            self.__osbm.obj_stab.set_message(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )

    def open_project(self):
        """Открытие проекта."""
        self.__osbm.obj_logg.debug_logger("Project open_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = self.__osbm.obj_dw.select_folder_for_open_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.clear_window_before_new_or_open_project()
                self.config_open_project()

    def config_open_project(self):
        """
        Конфигурация открытого проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project config_open_project()")

        self.__current_name = os.path.basename(
            self.__osbm.obj_dirm.get_project_dirpath()
        )
        self.__osbm.obj_settings.set_project_current_name(self.__current_name)
        # настраиваем базы данных
        self.__osbm.obj_settings.add_or_update_project()
        self.__osbm.obj_prodb.create_and_config_db_project()
        # обновляем окно
        self.__osbm.obj_mw.update_main_window()
        # пути для проекта
        self.__osbm.obj_dirm.set_new_dirpaths_for_project()

        self.set_true_actives_project()
        # сообщение для статусбара
        self.__osbm.obj_stab.set_message(
            f"Проект c именем {self.__current_name} открыт."
        )
        # добавляем папки в новый проект
        self.__osbm.obj_film.create_folders_and_aed_for_project()
        # обновляем меню
        self.__osbm.obj_mw.update_menu_recent_projects()

    def open_recent_project(self, project):
        """Открытие недавнего проекта."""
        self.__osbm.obj_logg.debug_logger(
            f"Project open_recent_project(project):\nproject = {project}"
        )
        directory_project = project.get("directory_project")
        if os.path.exists(directory_project):
            self.set_project_dirpaths(directory_project)
            self.clear_window_before_new_or_open_project()
            self.config_open_project()
        else:
            self.__osbm.obj_dw.warning_message(
                f"Проект с именем {project.get('name_project')} не существует."
            )
            # удаляем проект из БД и обновляем меню
            self.__osbm.obj_settings.delete_project_from_db(project)
            self.__osbm.obj_mw.update_menu_recent_projects()

    def set_true_actives_project(self):
        """
        Задает активность проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project set_true_actives_project()")
        self.__status_active = True
        self.__status_save = True
        # активировать qactions в статусбаре
        self.__osbm.obj_mw.enable_qt_actions()
        # значение по умолчанию включить
        self.__osbm.obj_mw.config_combox_default()


    def export_to_pdf(self):
        """
        Экспорт проекта в pdf.
        """
        self.__osbm.obj_logg.debug_logger("Project export_to_pdf()")
        multipage_pdf_path = (
            self.__osbm.obj_dw.select_name_and_dirpath_export_pdf()
        )
        if multipage_pdf_path:
            self.__osbm.obj_stab.set_message("Процесс экспорта в PDF...")
            # проверка на доступность конвертера
            flag_converter = False
            app_converter = self.__osbm.obj_settings.get_app_converter()
            status_msword = self.__osbm.obj_offp.get_status_msword()
            status_libreoffice = self.__osbm.obj_offp.get_status_libreoffice()
            if app_converter == "MSWORD" and status_msword:
                flag_converter = True
            elif app_converter == "LIBREOFFICE" and status_libreoffice:
                flag_converter = True
            #
            if flag_converter:
                self.__osbm.obj_dw.process_export_start()
                start_time = time.time()
                try:
                    self.__osbm.obj_conv.export_to_pdf(multipage_pdf_path)
                    end_time = time.time()
                    self.__osbm.obj_stab.set_message(
                        f"Экспорт завершен. Файл {multipage_pdf_path} готов."
                    )
                    # открыть pdf
                    os.startfile(os.path.dirname(multipage_pdf_path))
                    self.__osbm.obj_logg.debug_logger(
                        f"Project export_to_pdf() -> time: {end_time - start_time}"
                    )
                    
                except self.__osbm.obj_com.errors.MsWordError:
                    msg = "Экспорт отменён! Выбранный конвертер перестал работать."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                    self.__osbm.obj_offp.terminate_msword()
                    self.__osbm.obj_stab.update_status_msword_label(False)

                except self.__osbm.obj_com.errors.LibreOfficeError:
                    msg = "Экспорт отменён! Выбранный конвертер перестал работать."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                    self.__osbm.obj_offp.terminate_libreoffice()
                    self.__osbm.obj_stab.update_status_libreoffice_label(False)
                #
                self.__osbm.obj_dw.process_export_end()
            else:
                msg = "Экспорт отменён! Выбранный конвертер не работает."
                self.__osbm.obj_dw.warning_message(msg)
                self.__osbm.obj_stab.set_message(msg)


# obj_proj = Project()

``
### D:\vs_projects\auto-exec-doc\package\modules\projectdatabase.py
``python
import sqlite3
import os


class ProjectDatabaseObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm


class ProjectDatabase:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = ProjectDatabaseObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase setting_osbm():\nself.__osbm = {self.__osbm}"
        )

    def create_and_config_db_project(self):
        """
        Настройка базы данных перед использованием проекта
        """
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase create_and_config_db_project()"
        )

        if not os.path.exists(self.__osbm.obj_dirm.get_db_project_dirpath()):
            # Добавляем данные в пустую БД
            self.add_tables_and_datas_to_empty_db_project()

        # set всем included = True
        # self.set_all_included_in_db_project_to_true()

    def add_tables_and_datas_to_empty_db_project(self):
        """
        Добавление таблиц и данных в БД программы при запуске.
        """
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase add_tables_and_datas_to_empty_db_project()"
        )
        conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.executescript(
            """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Project_nodes" (
	"id_node"	INTEGER NOT NULL UNIQUE,
	"name_node"	TEXT UNIQUE,
	"id_parent"	INTEGER,
	"order_node"	TEXT NOT NULL,
	"type_node"	TEXT,
	"id_active_template"	INTEGER,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_node" AUTOINCREMENT),
	UNIQUE("name_node"),
	FOREIGN KEY("id_active_template") REFERENCES "Project_templates"("id_template") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "Project_nodes_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_node"	INTEGER NOT NULL,
	"id_variable"	INTEGER NOT NULL,
	"value_pair"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_node") REFERENCES "Project_nodes"("id_node") ON DELETE CASCADE,
	FOREIGN KEY("id_variable") REFERENCES "Project_variables"("id_variable") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_pages" (
	"id_page"	INTEGER NOT NULL UNIQUE,
	"id_parent_template"	INTEGER,
	"name_page"	TEXT,
	"filename_page"	TEXT UNIQUE,
	"typefile_page"	TEXT,
	"order_page"	INTEGER NOT NULL,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_page" AUTOINCREMENT),
	FOREIGN KEY("id_parent_template") REFERENCES "Project_templates"("id_template") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_pages_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_page"	INTEGER NOT NULL,
	"id_variable"	INTEGER NOT NULL,
	"value_pair"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_page") REFERENCES "Project_pages"("id_page") ON DELETE CASCADE,
	FOREIGN KEY("id_variable") REFERENCES "Project_variables"("id_variable") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_templates" (
	"id_template"	INTEGER NOT NULL UNIQUE,
	"name_template"	TEXT,
	"id_parent_node"	INTEGER,
	PRIMARY KEY("id_template" AUTOINCREMENT),
	FOREIGN KEY("id_parent_node") REFERENCES "Project_nodes"("id_node") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_templates_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_template"	INTEGER NOT NULL,
	"id_variable"	INTEGER NOT NULL,
	"value_pair"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_template") REFERENCES "Project_templates"("id_template") ON DELETE CASCADE,
	FOREIGN KEY("id_variable") REFERENCES "Project_variables"("id_variable") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_variables" (
	"id_variable"	INTEGER NOT NULL UNIQUE,
	"name_variable"	TEXT NOT NULL UNIQUE,
	"type_variable"	TEXT NOT NULL,
	"title_variable"	TEXT,
	"order_variable"	INTEGER NOT NULL,
	"config_variable"	TEXT,
	"description_variable"	TEXT,
	"is_global"	INTEGER,
	PRIMARY KEY("id_variable" AUTOINCREMENT),
	UNIQUE("name_variable")
);
INSERT INTO "Project_nodes" VALUES (0,'Проект',NULL,'0','PROJECT',NULL,1);
COMMIT;
        """
        )
        conn.commit()
        conn.close()

    def get_conn(self) -> object:
        """
        Запрос курсора.
        """
        self.__osbm.obj_logg.debug_logger("ProjectDatabase get_conn() -> object")
        conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row
        return conn

    def get_fetchall(self, cursor):
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase get_fetchall(cursor, conn) -> list"
        )
        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        return result

    def get_fetchone(self, cursor):
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase get_fetchone(cursor, conn) -> list"
        )
        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        return result

    def get_nodes(self) -> list:
        """
        Запрос на все вершины.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes;
        """)

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_nodes() -> list:\nresult = {result}"
        )
        return result

    def get_project_node(self) -> object:
        """
        Запрос на вершину проекта.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes
        WHERE type_node = "PROJECT";
        """)

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_project_node() -> object:\nresult = {result}"
        )
        return result

    def get_group_nodes(self) -> list:
        """
        Получение вершин групп.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes
        WHERE type_node = "GROUP";
        """)

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_group_nodes() -> list:\nresult = {result}"
        )
        return result

    def get_form_nodes(self) -> list:
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes
        WHERE type_node = "FORM";
        """)

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_form_nodes() -> list:\nresult = {result}"
        )
        return result

    def get_childs(self, parent_node) -> list:
        """
        Запрос на детей вершины.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_parent = ?
        ORDER BY order_node ASC
        """,
            [parent_node.get("id_node")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_childs(parent_node) -> list: parent_node = {parent_node}\nresult = {result}"
        )
        return result

    def get_template_by_id(self, id_template) -> object:
        """
        Запрос на получение template из таблицы Project_templates.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        WHERE id_template = ?
        """,
            [id_template],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_template_by_id(id_template) -> object: id_template = {id_template}\nresult = {result}"
        )
        return result

    def get_templates_by_form(self, form) -> list:
        """
        Получение templates определенной form.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        WHERE id_parent_node = ?
        """,
            [form.get("id_node")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_templates_by_form(form) -> list: form = {form}\nresult = {result}"
        )
        return result

    def get_all_pages(self) -> list:
        """
        Запрос на получение всех pages из таблицы Project_pages.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute(
            """
        SELECT * FROM Project_pages
        """
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_all_pages() -> list:\nresult = {result}"
        )
        return result

    def get_pages_by_template(self, template) -> list:
        """
        Запрос на получение pages из таблицы Project_pages.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages
        WHERE id_parent_template = ?
        ORDER BY order_page
        """,
            [template.get("id_template")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_pages_by_template(template) -> list: template = {template}\nresult = {result}"
        )
        return result

    def insert_page(self, page) -> int:
        """
        Добавление page в таблицу Project_pages.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_page(page) -> int: page = {page}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_pages
        (id_parent_template, name_page, filename_page, typefile_page, order_page, included)
        VALUES
        (?, ?, ?, ?, ?, ?)
        """,
            [
                page.get("id_parent_template"),
                page.get("name_page"),
                page.get("filename_page"),
                page.get("typefile_page"),
                page.get("order_page"),
                page.get("included"),
            ],
        )
        conn.commit()
        primary_key = cursor.lastrowid
        conn.close()
        return primary_key

    def get_parent_template(self, page) -> object:
        """
        Определение родителя parent_template для page.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        WHERE id_template = ?
        """,
            [page.get("id_parent_template")],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_parent_template() -> object\nresult = {result}"
        )
        return result

    def get_parent_node_template(self, template) -> object:
        """
        Определение родителя parent_node для template.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [template.get("id_parent_node")],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_parent_node_template() -> object\nresult = {result}"
        )
        return result

    def get_node_parent(self, node) -> object:
        """
        Запрос на получение node_parent из таблицы Project_nodes.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [node.get("id_parent")],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_parent(node) -> object: node = {node}\nresult = {result}"
        )
        return result

    def get_node_by_id(self, id_node) -> object:
        """
        Запрос на получение node по id.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [id_node],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_by_id(id_node) -> object: id_node = {id_node}\nresult = {result}"
        )
        return result

    def get_variable_by_id(self, id_variable) -> object:
        """
        Запрос на получение variable по id.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_variables
        WHERE id_variable = ?
        """,
            [id_variable],
        )
        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_config_variable(id_variable) -> list: id_variable = {id_variable}\nresult = {result}"
        )
        return result

    def get_page_by_id(self, id_page) -> object:
        """
        Запрос на получение page по id.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages
        WHERE id_page = ?
        """,
            [id_page],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_page_by_id(id_page) -> object: id_page = {id_page}\nresult = {result}"
        )
        return result

    def update_nodes_included_states(self, nodes_states):
        """
        Массовое обновление состояний включения узлов
        nodes_states: словарь {id_node: included_state}
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_nodes_included_states(nodes_states):\nnodes_states = {nodes_states}"
        )
        
        conn = self.get_conn()
        cursor = conn.cursor()
        
        for id_node, included_state in nodes_states.items():
            cursor.execute(
                """
                UPDATE Project_nodes
                SET included = ?
                WHERE id_node = ?
                """,
                [included_state, id_node]
            )
        
        conn.commit()
        conn.close()


    def set_included_for_node(self, node, state):
        """
        Запрос на установку включенности для вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_included_for_node(node, state): node = {node}, state = {state}"
        )

        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Project_nodes
                SET included = ?
                WHERE id_node = ?
                """,
                [state, node.get("id_node")],
            )
            conn.commit()
            conn.close()
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in set_included_for_node: {e}")

    def delete_page(self, page):
        """
        Запрос на удаление страницы из Project_pages.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_page(page): page = {page}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_pages
        WHERE id_page = ?
        """,
            [page.get("id_page")],
        )
        conn.commit()
        conn.close()

    def get_page_data(self, page) -> list:
        """
        Запрос на получение данных страницы из Project_pages_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages_data
        WHERE id_page = ?
        ORDER BY (SELECT order_variable FROM Project_variables WHERE id_variable = Project_pages_data.id_variable)
        """,
            [page.get("id_page")],
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_page_data(page) -> list: page = {page}\nresult = {result}"
        )
        return result

    def get_templates(self) -> list:
        """
        Запрос на получение шаблонов из Project_templates.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        """
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_templates() -> list:\nresult = {result}"
        )
        return result

    def get_template_data(self, template) -> list:
        """
        Запрос на получение данных шаблона из Project_templates_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates_data
        WHERE id_template = ?
        ORDER BY (SELECT order_variable FROM Project_variables WHERE id_variable = Project_templates_data.id_variable)
        """,
            [template.get("id_template")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_template_data(template) -> list: template = {template}\nresult = {result}"
        )
        return result

    def get_node_data(self, node) -> object:
        """
        Запрос на получение данных вершины из Project_nodes_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes_data
        WHERE id_node = ?
        ORDER BY (SELECT order_variable FROM Project_variables WHERE id_variable = Project_nodes_data.id_variable)
        """,
            [node.get("id_node")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_data(node) -> list: node = {node}\nresult = {result}"
        )
        return result

    def update_page(self, page):
        """
        Запрос на обновление страницы в Project_pages.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_page(page): page = {page}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages
        SET name_page = ?, filename_page = ?, typefile_page = ?
        WHERE id_page = ?
        """,
            [
                page.get("name_page"),
                page.get("filename_page"),
                page.get("typefile_page"),
                page.get("id_page"),
            ],
        )
        conn.commit()
        conn.close()

    def update_page_data(self, id_pair, value_pair):
        """
        Запрос на обновление данных страницы в Project_pages_data.
        """
        print(f"update_page_data(id_pair, value_pair): id_pair = {id_pair}, value_pair = {value_pair}")
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_page_data(id_pair, value_pair): id_pair = {id_pair}, value_pair = {value_pair}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages_data
        SET value_pair = ?
        WHERE id_pair = ?
        """,
            [value_pair, id_pair],
        )
        conn.commit()
        conn.close()

    def update_template_data(self, id_pair, value_pair):
        """
        Запрос на обновление данных шаблона в Project_templates_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_template_data(id_pair, value_pair): id_pair = {id_pair}, value_pair = {value_pair}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_templates_data
        SET value_pair = ?
        WHERE id_pair = ?
        """,
            [value_pair, id_pair],
        )
        conn.commit()
        conn.close()

    def update_node_data(self, id_pair, value_pair):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_node_data(id_pair, value_pair): id_pair = {id_pair}, value_pair = {value_pair}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes_data
        SET value_pair = ?
        WHERE id_pair = ?
        """,
            [value_pair, id_pair],
        )
        conn.commit()
        conn.close()

    def get_page_value_pair_by_id_pair(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_pages_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value_pair FROM Project_pages_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_page_value_pair_by_id_pair(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def get_template_value_pair_by_id_pair(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_templates_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value_pair FROM Project_templates_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_template_value_pair_by_id_pair(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def get_node_value_pair_by_id_pair(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_nodes_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value_pair FROM Project_nodes_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_value_pair_by_id_pair(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def set_all_included_in_db_project_to_true(self):
        """
        Установка всех included = True
        """
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase set_all_included_in_db_project_to_true()"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.executescript(
            """
        UPDATE Project_pages
        SET included = 1;

        UPDATE Project_nodes
        SET included = 1;
        """
        )
        conn.commit()
        conn.close()

    def get_variables(self) -> list:
        """
        Запрос на получение переменных проекта.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_variables
        ORDER BY order_variable
        """
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_variables() -> list\nresult = {result}"
        )
        return result

    def insert_node_datas(self, node, pair_list):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_node_datas(node, pair_list):\nnode = {node}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_nodes_data
            (id_node, id_variable)
            VALUES
            (?, ?)
            """,
                [node.get("id_node"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def insert_template_data(self, template, pair):
        """
        Запрос на вставку одной строки данных вершины в Project_templates_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_template_data(template, pair):\ntemplate = {template}\npair = {pair}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_templates_data
        (id_template, id_variable, value_pair)
        VALUES
        (?, ?, ?)
        """,
            [template.get("id_template"), pair.get("id_variable"), pair.get("value_pair")],
        )
        conn.commit()
        conn.close()

    def insert_template_datas(self, template, pair_list):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_template_datas(template, pair_list):\ntemplate = {template}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_templates_data
            (id_template, id_variable)
            VALUES
            (?, ?)
            """,
                [template.get("id_template"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def insert_page_data(self, page, pair):
        """
        Запрос на вставку одной строки данных вершины в Project_pages_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_page_data(page, pair):\npage = {page}\npair = {pair}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_pages_data
        (id_page, id_variable, value_pair)
        VALUES
        (?, ?, ?)
        """,
            [page.get("id_page"), pair.get("id_variable"), pair.get("value_pair")],
        )
        conn.commit()
        conn.close()

    def insert_page_datas(self, page, pair_list):
        """
        Запрос на обновление данных страницы в Project_pages_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_page_datas(page, pair_list):\npage = {page}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_pages_data
            (id_page, id_variable)
            VALUES
            (?, ?)
            """,
                [page.get("id_page"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def delete_node_datas(self, node, pair_list):
        """
        Запрос на удаление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_node_datas(node, pair_list):\nnode = {node}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_nodes_data
            WHERE id_node = ?
            AND id_variable = ?
            """,
                [node.get("id_node"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def delete_template_datas(self, template, pair_list):
        """
        Запрос на удаление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_template_datas(template, pair_list):\ntemplate = {template}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_templates_data
            WHERE id_template = ?
            AND id_variable = ?
            """,
                [template.get("id_template"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def delete_page_datas(self, page, pair_list):
        """
        Запрос на удаление данных страницы в Project_pages_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_page_datas(page, pair_list):\npage = {page}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_pages_data
            WHERE id_page = ?
            AND id_variable = ?
            """,
                [page.get("id_page"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def insert_variable(self, variable) -> int:
        """
        Запрос на вставку данных переменной в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_variable(variable):\nvariable = {variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_variables
        (name_variable, type_variable, title_variable, order_variable, config_variable, description_variable)
        VALUES
        (?, ?, ?, ?, ?, ?)
        """,
            [
                variable.get("name_variable"),
                variable.get("type_variable"),
                variable.get("title_variable"),
                variable.get("order_variable"),
                variable.get("config_variable"),
                variable.get("description_variable"),
            ],
        )
        conn.commit()
        primary_key = cursor.lastrowid
        conn.close()
        return primary_key

    def update_variable(self, variable):
        """
        Запрос на обновление данных переменной в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_variable(variable):\nvariable = {variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_variables
        SET
        name_variable = ?,
        type_variable = ?,
        title_variable = ?,
        order_variable = ?,
        config_variable = ?,
        description_variable = ?
        WHERE id_variable = ?
        """,
            [
                variable.get("name_variable"),
                variable.get("type_variable"),
                variable.get("title_variable"),
                variable.get("order_variable"),
                variable.get("config_variable"),
                variable.get("description_variable"),
                variable.get("id_variable"),
            ],
        )
        conn.commit()
        conn.close()

    def delete_variable(self, variable):
        """
        Запрос на удаление данных переменной в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_variable(variable):\nvariable = {variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_variables
        WHERE id_variable = ?
        """,
            [variable.get("id_variable")],
        )
        conn.commit()
        conn.close()

    def get_variable_by_name(self, name_variable):
        """
        Запрос на получение переменной по имени в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_variable_by_name(name_variable):\nname_variable = {name_variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT *
        FROM Project_variables
        WHERE name_variable = ?
        """,
            [name_variable],
        )
        result = self.get_fetchone(cursor)
        conn.close()
        return result

    def get_node_by_name(self, name_node):
        """
        Запрос на получение вершины по имени в Project_nodes.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_by_name(name_node):\nname_node = {name_node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT *
        FROM Project_nodes
        WHERE name_node = ?
        """,
            [name_node],
        )
        result = self.get_fetchone(cursor)
        conn.close()
        return result

    def update_node(self, node):
        """
        Обновление данных вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_node(node): node = {node}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET name_node = ?, id_parent = ?, order_node = ?, type_node = ?, id_active_template = ?, included = ?
        WHERE id_node = ?
        """,
            [
                node.get("name_node"),
                node.get("id_parent"),
                node.get("order_node"),
                node.get("type_node"),
                node.get("id_active_template"),
                node.get("included"),
                node.get("id_node"),
            ],
        )
        conn.commit()
        conn.close()

    def add_node(self, edit_node):
        """
        Добавление вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase add_node(edit_node): edit_node = {edit_node}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_nodes (id_active_template, id_parent, included, name_node, order_node, type_node)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            [
                edit_node.get("id_active_template"),
                edit_node.get("id_parent"),
                edit_node.get("included"),
                edit_node.get("name_node"),
                edit_node.get("order_node"),
                edit_node.get("type_node"),
            ],
        )
        conn.commit()
        conn.close()

    def delete_node(self, node):
        """
        Удаление вершины по объекту node.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_node(node): node = {node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_nodes
        WHERE id_node = ?
        """,
            [node.get("id_node")],
        )
        conn.commit()
        conn.close()

    def set_new_parent_for_child_node(self, current_node, child_node):
        """
        Установка родительской вершины для дочерей группы.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_new_parent_for_child_node(current_node, child_node):\nnode = {current_node}\nchild_node = {child_node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET id_parent = ?, order_node = ?
        WHERE id_node = ?
        """,
            [
                current_node.get("id_parent"),
                current_node.get("order_node"),
                child_node.get("id_node"),
            ],
        )
        conn.commit()
        conn.close()

    def set_order_for_node(self, node, new_order):
        """
        Установка порядка для вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_order_for_node(node, new_order):\nnode = {node}\nnew_order = {new_order}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET order_node = ?
        WHERE id_node = ?
        """,
            [new_order, node.get("id_node")],
        )
        conn.commit()
        conn.close()

    def set_order_for_page(self, page, new_order):
        """
        Установка порядка для страницы.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_order_for_page(page, new_order):\npage = {page}\nnew_order = {new_order}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages
        SET order_page = ?
        WHERE id_page = ?
        """,
            [new_order, page.get("id_page")],
        )
        conn.commit()
        conn.close()

    def set_order_for_variable(self, variable, new_order):
        """
        Установка порядка для переменной.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_order_for_variable(variable, new_order):\nvariable = {variable}\nnew_order = {new_order}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_variables
        SET order_variable = ?
        WHERE id_variable = ?
        """,
            [new_order, variable.get("id_variable")],
        )
        conn.commit()
        conn.close()

    def add_template(self, name_template, form) -> int:
        """
        Добавление шаблона.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase add_template(name_template, form):\nname_template = {name_template}\nform = {form}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_templates (name_template, id_parent_node)
        VALUES (?, ?)
        """,
            [name_template, form.get("id_node")],
        )
        conn.commit()
        primary_key = cursor.lastrowid
        conn.close()
        return primary_key

    def set_new_name_for_template(self, template, name_template):
        """
        Установка нового имени шаблона.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_new_name_for_template(template, name_template):\ntemplate = {template}\nname_template = {name_template}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_templates
        SET name_template = ?
        WHERE id_template = ?
        """,
            [name_template, template.get("id_template")],
        )
        conn.commit()
        conn.close()

    def delete_template(self, template):
        """
        Удаление шаблона.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_template(template):\ntemplate = {template}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_templates
        WHERE id_template = ?
        """,
            [template.get("id_template")],
        )
        conn.commit()
        conn.close()

    def set_active_template_for_node_by_id(self, id_node, id_template):
        """
        Установка активного шаблона для вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_active_template_for_node_by_id(id_node, id_template):\nid_node = {id_node}\nid_template = {id_template}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET id_active_template = ?
        WHERE id_node = ?
        """,
            [id_template, id_node],
        )
        conn.commit()
        conn.close()

    def count_all_variable_usages(self):
        self.__osbm.obj_logg.debug_logger("ProjectDatabase count_all_variable_usages()")
        #
        conn = self.get_conn()
        cursor = conn.cursor()
        # все id_variable из Project_variables
        cursor.execute("SELECT id_variable FROM Project_variables;")
        # cursor.fetchall() а не self.get_fetchall(cursor)
        variable_ids = [row[0] for row in cursor.fetchall()]
        if not variable_ids:
            return {}
        #
        placeholders = ", ".join("?" for _ in variable_ids)
        # Объединенный запрос с подсчетом
        cursor.execute(
            f"""
        SELECT id_variable, 
            COUNT(DISTINCT id_node) AS nodes_count, 
            COUNT(DISTINCT id_page) AS pages_count,
            COUNT(DISTINCT id_template) AS templates_count
        FROM (
            SELECT id_variable, id_node, NULL AS id_page, NULL AS id_template
            FROM Project_nodes_data
            WHERE id_variable IN ({placeholders})

            UNION ALL

            SELECT id_variable, NULL AS id_node, id_page, NULL AS id_template
            FROM Project_pages_data
            WHERE id_variable IN ({placeholders})

            UNION ALL

            SELECT id_variable, NULL AS id_node, NULL AS id_page, id_template
            FROM Project_templates_data
            WHERE id_variable IN ({placeholders})
        )
        GROUP BY id_variable;
        """,
            variable_ids * 3,
        )  # утраиваем список переменных для трех фильтров
        # cursor.fetchall() а не self.get_fetchall(cursor)
        result = cursor.fetchall()
        conn.close()
        # Форматируем результат в словарь
        usage_summary = {
            id_variable: {"nodes_count": 0, "pages_count": 0, "templates_count": 0}
            for id_variable in variable_ids
        }
        for row in result:
            usage_summary[row[0]] = {
                "nodes_count": row[1],
                "pages_count": row[2],
                "templates_count": row[3],
            }

        return usage_summary
    
    def get_all_images(self) -> list:
        """
        Запрос на получение всех value_pair в таблицах _data, если type_variable равен IMAGE.
        """
        self.__osbm.obj_logg.debug_logger("ProjectDatabase get_all_images()")
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT nd.value_pair
        FROM Project_nodes_data nd
        JOIN Project_variables v ON v.id_variable = nd.id_variable
        WHERE v.type_variable = 'IMAGE'
        
        UNION ALL
        
        SELECT pd.value_pair
        FROM Project_pages_data pd
        JOIN Project_variables v ON v.id_variable = pd.id_variable
        WHERE v.type_variable = 'IMAGE'
        
        UNION ALL
        
        SELECT td.value_pair
        FROM Project_templates_data td
        JOIN Project_variables v ON v.id_variable = td.id_variable
        WHERE v.type_variable = 'IMAGE';
        """)

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_all_images() -> list:\nresult = {result}"
        )
        return result

    def set_included_for_page(self, page, new_state):
        """
        Установка включения для страницы.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_included_for_page(page, new_state):\npage = {page}\nincluded = {new_state}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages
        SET included = ?
        WHERE id_page = ?
        """,
            [new_state, page.get("id_page")],
        )
        conn.commit()
        conn.close()



# obj_prodb = ProjectDatabase()

``
### D:\vs_projects\auto-exec-doc\package\modules\sectionsinfo.py
``python
class SectionsInfoObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_prodb = osbm.obj_prodb
        self.obj_film = osbm.obj_film

class SectionsInfo:
    def __init__(self):
        self.__sections_info = []

    def setting_osbm(self, osbm):
        self.__osbm = SectionsInfoObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo setting_osbm(): \nself.__osbm = {self.__osbm}")

    def get_sections_info(self):
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo self.__sections_info = {self.__sections_info}")
        return self.__sections_info

    def update_sections_info(self, page):
        # обновить информацию, нужная для создания секций
        self.__sections_info.clear()
        self.add_page_for_sections_info(page)
        template = self.__osbm.obj_prodb.get_parent_template(page)
        self.add_template_for_sections_info(template)
        node = self.__osbm.obj_prodb.get_parent_node_template(template)
        self.add_nodes_for_sections_info(node)
    
    def add_page_for_sections_info(self, page):
        """
        Добавление секции для страницы.
        """
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_page_for_datas(page):\npage = {page}")

        data = self.__osbm.obj_prodb.get_page_data(page)
        if data:
            section = {
                "type": "page",
                "page": page,
                "data": data,
            }
            self.__sections_info.append(section)

    def add_template_for_sections_info(self, template):
        """ """
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_template_for_datas(page):\npage = {template}")
        
        data = self.__osbm.obj_prodb.get_template_data(template)
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
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_node_for_datas(node):\nnode = {node}")

        data = self.__osbm.obj_prodb.get_node_data(node)
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
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo add_nodes_for_sections_info(node):\nnode = {node}")
        parent_node = node
        flag = True
        while flag:
            self.add_node_for_datas(parent_node)
            parent_node = self.__osbm.obj_prodb.get_node_parent(parent_node)
            if not parent_node:
                flag = False


    def save_data_to_database(self):
        """
        Cохранение информации в __sections_info в БД
        """
        self.__osbm.obj_logg.debug_logger("SectionsInfo save_data_to_database()")
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
                value = pair.get("value_pair")
                old_value = self.update_data_from_pair(section_type, id_pair, value)
                id_variable = pair.get("id_variable")
                self.save_image(id_variable, old_value, value)               

    def update_data_from_pair(self, section_type, id_pair, value):
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo update_data_with_pair(section_type, pair):\nsection_type = {section_type},\nid_pair = {id_pair},\nvalue = {value}")
        old_value = None
        print(f"section_type = {section_type},\nid_pair = {id_pair},\nvalue = {value}")
        if section_type == "page":
            old_value = self.__osbm.obj_prodb.get_page_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_page_data(id_pair, value)
        elif section_type == "template":
            old_value = self.__osbm.obj_prodb.get_template_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_template_data(id_pair, value)
        elif section_type == "group":
            old_value = self.__osbm.obj_prodb.get_node_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_node_data(id_pair, value)
        elif section_type == "project":
            old_value = self.__osbm.obj_prodb.get_node_value_pair_by_id_pair(
                id_pair
            )
            self.__osbm.obj_prodb.update_node_data(id_pair, value)
        # так как old_value = {'value_pair': 'img_20240816184801.png'}
        return old_value.get("value_pair")

    def save_image(self, id_variable, old_value, value):
        self.__osbm.obj_logg.debug_logger(f"SectionsInfo save_image(id_variable, old_value, value):\nid_variable = {id_variable},\nold_value = {old_value},\nvalue = {value}")
        current_variable = self.__osbm.obj_prodb.get_variable_by_id(
            id_variable
        )
        print(f"id_variable = {id_variable}\n")
        print(f"current_variable = {current_variable}\n")
        type_variable = current_variable.get("type_variable")
        if type_variable == "IMAGE":
            self.__osbm.obj_film.delete_image_from_project(
                old_value
            )
            self.__osbm.obj_film.move_image_from_temp_to_project(
                value
            )


# obj_seci = SectionsInfo()
``
### D:\vs_projects\auto-exec-doc\package\modules\settingsmanager.py
``python
from PySide6.QtCore import QSettings
import datetime
import os

class SettingsManagerObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm

class SettingsManager:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        """Сохраняем метод setting_osbm как в оригинальном SettingsDatabase"""
        self.__osbm = SettingsManagerObjectsManager(osbm)
        self.__settings = QSettings("Constanta", "AutoExecDoc")
        self.__osbm.obj_logg.debug_logger("SettingsManager setting_osbm() completed")

    def initialize_default_settings(self):
        """Инициализация настроек по умолчанию"""
        self.__osbm.obj_logg.debug_logger("SettingsManager initialize_default_settings()")
        
        # Устанавливаем значения по умолчанию, если они еще не существуют
        if not self.__settings.contains("app_converter"):
            self.__settings.setValue("app_converter", "LIBREOFFICE")
        
        if not self.__settings.contains("libreoffice_path"):
            self.__settings.setValue("libreoffice_path", "C:\\Program Files\\LibreOffice\\program\\soffice.exe")
        
        if not self.__settings.contains("project_current_name"):
            self.__settings.setValue("project_current_name", "")
        
        # Инициализируем список проектов, если его нет
        if not self.__settings.contains("projects"):
            self.__settings.setValue("projects", [])

    # region Методы для работы с настройками

    def get_app_converter(self) -> str:
        """Получить выбранный конвертер"""
        result = self.__settings.value("app_converter", "LIBREOFFICE")
        self.__osbm.obj_logg.debug_logger(f"SettingsManager get_app_converter(): {result}")
        return result

    def set_app_converter(self, app_converter: str):
        """Установить конвертер"""
        self.__osbm.obj_logg.debug_logger(f"SettingsManager set_app_converter(): {app_converter}")
        self.__settings.setValue("app_converter", app_converter)

    def get_libreoffice_path(self) -> str:
        """Получить путь к LibreOffice"""
        result = self.__settings.value("libreoffice_path", "C:\\Program Files\\LibreOffice\\program\\soffice.exe")
        self.__osbm.obj_logg.debug_logger(f"SettingsManager get_libreoffice_path(): {result}")
        return result
    
    def set_libreoffice_path(self, path: str):
        """Установить путь к LibreOffice"""
        self.__osbm.obj_logg.debug_logger(f"SettingsManager set_libreoffice_path(): {path}")
        self.__settings.setValue("libreoffice_path", path)

    def get_project_current_name(self) -> str:
        """Получить имя текущего проекта"""
        result = self.__settings.value("project_current_name", "")
        self.__osbm.obj_logg.debug_logger(f"SettingsManager get_project_current_name(): {result}")
        return result

    def set_project_current_name(self, project_name: str):
        """Установить имя текущего проекта"""
        self.__osbm.obj_logg.debug_logger(f"SettingsManager set_project_current_name(): {project_name}")
        self.__settings.setValue("project_current_name", project_name)

    # endregion

    # region Методы для работы с проектами (совместимые с оригинальным интерфейсом)

    def add_new_project_to_db(self):
        """Совместимый метод с оригинальным SettingsDatabase"""
        self.__osbm.obj_logg.debug_logger("SettingsManager add_new_project_to_db()")
        project_dir = self.__osbm.obj_dirm.get_project_dirpath()
        self.add_or_update_project(project_dir)

    def update_project_to_db(self):
        """Совместимый метод с оригинальным SettingsDatabase"""
        self.__osbm.obj_logg.debug_logger("SettingsManager update_project_to_db()")
        project_dir = self.__osbm.obj_dirm.get_project_dirpath()
        self.add_or_update_project(project_dir)

    def add_or_update_open_project_to_db(self):
        """Совместимый метод с оригинальным SettingsDatabase - БЕЗ ПАРАМЕТРОВ"""
        self.__osbm.obj_logg.debug_logger("SettingsManager add_or_update_open_project_to_db()")
        project_dir = self.__osbm.obj_dirm.get_project_dirpath()
        self.add_or_update_project(project_dir)

    def add_or_update_project(self, project_dir: str = None):
        """Основной метод для добавления/обновления проекта"""
        if project_dir is None:
            project_dir = self.__osbm.obj_dirm.get_project_dirpath()
            
        projects = self.get_projects()
        project_name = os.path.basename(project_dir)
        current_datetime = datetime.datetime.now().replace(microsecond=0).isoformat()
        
        # Ищем существующий проект
        existing_project = None
        for i, project in enumerate(projects):
            if project.get('directory_project') == project_dir:
                existing_project = i
                break
        
        project_data = {
            'name_project': project_name,
            'directory_project': project_dir,
            'date_create_project': current_datetime if existing_project is None else 
                                 projects[existing_project]['date_create_project'],
            'date_last_open_project': current_datetime
        }
        
        if existing_project is not None:
            # Обновляем существующий проект
            projects[existing_project] = project_data
        else:
            # Добавляем новый проект
            projects.append(project_data)
        
        # Сохраняем обновленный список
        self.__settings.setValue("projects", projects)
        self.__osbm.obj_logg.debug_logger(f"SettingsManager add_or_update_project(): {project_name}")

    def get_projects(self) -> list:
        """Получить список всех проектов"""
        projects = self.__settings.value("projects", [])
        self.__osbm.obj_logg.debug_logger(f"SettingsManager get_projects(): {len(projects)} projects")
        return projects

    def get_last_projects(self, limit: int = 5) -> list:
        """Получить последние проекты"""
        projects = self.get_projects()
        # Сортируем по дате последнего открытия
        sorted_projects = sorted(projects, 
                               key=lambda x: x.get('date_last_open_project', ''), 
                               reverse=True)
        self.__osbm.obj_logg.debug_logger(f"SettingsManager get_last_projects(): {len(sorted_projects[:limit])} projects")
        return sorted_projects[:limit]

    def delete_project_from_db(self, project):
        """Совместимый метод с оригинальным SettingsDatabase"""
        self.__osbm.obj_logg.debug_logger(f"SettingsManager delete_project_from_db(): {project}")
        project_dir = project.get('directory_project')
        self.delete_project(project_dir)

    def delete_project(self, project_dir: str):
        """Удалить проект из списка"""
        projects = self.get_projects()
        projects = [p for p in projects if p.get('directory_project') != project_dir]
        self.__settings.setValue("projects", projects)
        self.__osbm.obj_logg.debug_logger(f"SettingsManager delete_project(): {project_dir}")

    # endregion

    def sync(self):
        """Синхронизировать настройки"""
        self.__settings.sync()
``
### D:\vs_projects\auto-exec-doc\package\modules\__init__.py
``python

``
### D:\vs_projects\auto-exec-doc\package\ui\convertersettingsdialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'convertersettingsdialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_ConverterSettingsDialogWindow(object):
    def setupUi(self, ConverterSettingsDialogWindow):
        if not ConverterSettingsDialogWindow.objectName():
            ConverterSettingsDialogWindow.setObjectName(u"ConverterSettingsDialogWindow")
        ConverterSettingsDialogWindow.resize(546, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConverterSettingsDialogWindow.sizePolicy().hasHeightForWidth())
        ConverterSettingsDialogWindow.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ConverterSettingsDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_converter = QWidget(ConverterSettingsDialogWindow)
        self.widget_converter.setObjectName(u"widget_converter")
        sizePolicy.setHeightForWidth(self.widget_converter.sizePolicy().hasHeightForWidth())
        self.widget_converter.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget_converter)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.converter = QLabel(self.widget_converter)
        self.converter.setObjectName(u"converter")
        self.converter.setMinimumSize(QSize(0, 0))
        self.converter.setMaximumSize(QSize(16777215, 16))
        self.converter.setStyleSheet(u"font-weight: bold;")
        self.converter.setTextFormat(Qt.AutoText)
        self.converter.setScaledContents(False)

        self.verticalLayout_2.addWidget(self.converter)

        self.radbtn_msword = QRadioButton(self.widget_converter)
        self.radbtn_msword.setObjectName(u"radbtn_msword")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/msword.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.radbtn_msword.setIcon(icon)

        self.verticalLayout_2.addWidget(self.radbtn_msword)

        self.radbtn_libreoffice = QRadioButton(self.widget_converter)
        self.radbtn_libreoffice.setObjectName(u"radbtn_libreoffice")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/libreoffice.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.radbtn_libreoffice.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.radbtn_libreoffice)


        self.horizontalLayout.addWidget(self.widget_converter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.explanation = QLabel(ConverterSettingsDialogWindow)
        self.explanation.setObjectName(u"explanation")
        self.explanation.setTextFormat(Qt.MarkdownText)
        self.explanation.setScaledContents(False)
        self.explanation.setWordWrap(False)

        self.horizontalLayout.addWidget(self.explanation)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_save = QPushButton(ConverterSettingsDialogWindow)
        self.btn_save.setObjectName(u"btn_save")
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_save.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.btn_save)

        self.btn_close = QPushButton(ConverterSettingsDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon3 = QIcon()
        icon3.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(ConverterSettingsDialogWindow)

        QMetaObject.connectSlotsByName(ConverterSettingsDialogWindow)
    # setupUi

    def retranslateUi(self, ConverterSettingsDialogWindow):
        ConverterSettingsDialogWindow.setWindowTitle(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0435\u0440\u0430", None))
        self.converter.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"<html><head/><body><p>\u041a\u043e\u043d\u0432\u0435\u0440\u0442\u0435\u0440</p></body></html>", None))
        self.radbtn_msword.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"Microsoft Word", None))
        self.radbtn_libreoffice.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"LibreOffice", None))
        self.explanation.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0443, \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043d\u0443\u044e \u043d\u0430 \u0434\u0430\u043d\u043d\u043e\u043c \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0435:\n"
" - \u0414\u043b\u044f \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430 \u0432 \u0440\u0435\u0436\u0438\u043c\u0435 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0432\u0440\u0435\u043c\u0435\u043d\u0438\n"
" - \u0414\u043b\u044f \u044d\u043a\u0441\u043f\u043e\u0440\u0442\u0430 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430 \u0432 PDF", None))
        self.btn_save.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("ConverterSettingsDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\customitemqlistwidget_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'customitemqlistwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)
import resources_rc

class Ui_CustomItemQListWidget(object):
    def setupUi(self, CustomItemQListWidget):
        if not CustomItemQListWidget.objectName():
            CustomItemQListWidget.setObjectName(u"CustomItemQListWidget")
        CustomItemQListWidget.resize(416, 28)
        CustomItemQListWidget.setMinimumSize(QSize(0, 0))
        CustomItemQListWidget.setMaximumSize(QSize(1515, 16777215))
        self.horizontalLayout = QHBoxLayout(CustomItemQListWidget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 2, 2, 2)
        self.label_text = QLabel(CustomItemQListWidget)
        self.label_text.setObjectName(u"label_text")
        self.label_text.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.label_text)

        self.btn_edit = QPushButton(CustomItemQListWidget)
        self.btn_edit.setObjectName(u"btn_edit")
        self.btn_edit.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/white-icons/resources/white-icons/pen.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_edit.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton(CustomItemQListWidget)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setMaximumSize(QSize(16777215, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/white-icons/resources/white-icons/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_delete.setIcon(icon1)

        self.horizontalLayout.addWidget(self.btn_delete)

        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(CustomItemQListWidget)

        QMetaObject.connectSlotsByName(CustomItemQListWidget)
    # setupUi

    def retranslateUi(self, CustomItemQListWidget):
        CustomItemQListWidget.setWindowTitle(QCoreApplication.translate("CustomItemQListWidget", u"Form", None))
        self.label_text.setText(QCoreApplication.translate("CustomItemQListWidget", u"224", None))
        self.btn_edit.setText("")
        self.btn_delete.setText("")
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formdate_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formdate.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_FormDateWidget(object):
    def setupUi(self, FormDateWidget):
        if not FormDateWidget.objectName():
            FormDateWidget.setObjectName(u"FormDateWidget")
        FormDateWidget.resize(439, 121)
        self.verticalLayout = QVBoxLayout(FormDateWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormDateWidget)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setScaledContents(False)
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormDateWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.hl.addWidget(self.title)

        self.label_variable = QLabel(FormDateWidget)
        self.label_variable.setObjectName(u"label_variable")

        self.hl.addWidget(self.label_variable)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.hl_date = QHBoxLayout()
        self.hl_date.setObjectName(u"hl_date")
        self.dateedit = QDateEdit(FormDateWidget)
        self.dateedit.setObjectName(u"dateedit")
        self.dateedit.setTimeSpec(Qt.UTC)

        self.hl_date.addWidget(self.dateedit)

        self.btn_set_current = QPushButton(FormDateWidget)
        self.btn_set_current.setObjectName(u"btn_set_current")

        self.hl_date.addWidget(self.btn_set_current)

        self.hl_date.setStretch(0, 1)

        self.verticalLayout.addLayout(self.hl_date)

        self.textbrowser = QTextBrowser(FormDateWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.retranslateUi(FormDateWidget)

        QMetaObject.connectSlotsByName(FormDateWidget)
    # setupUi

    def retranslateUi(self, FormDateWidget):
        FormDateWidget.setWindowTitle(QCoreApplication.translate("FormDateWidget", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormDateWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormDateWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.label_variable.setText(QCoreApplication.translate("FormDateWidget", u"<html><head/><body><p><span style=\" font-style:italic;\">variable</span></p></body></html>", None))
        self.btn_set_current.setText(QCoreApplication.translate("FormDateWidget", u"\u0412\u044b\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0443\u044e \u0434\u0430\u0442\u0443", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormDateWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formimage_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formimage.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_FormImageWidget(object):
    def setupUi(self, FormImageWidget):
        if not FormImageWidget.objectName():
            FormImageWidget.setObjectName(u"FormImageWidget")
        FormImageWidget.resize(425, 155)
        FormImageWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormImageWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormImageWidget)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormImageWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.hl.addWidget(self.title)

        self.label_variable = QLabel(FormImageWidget)
        self.label_variable.setObjectName(u"label_variable")

        self.hl.addWidget(self.label_variable)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.hl_select_clear = QHBoxLayout()
        self.hl_select_clear.setSpacing(6)
        self.hl_select_clear.setObjectName(u"hl_select_clear")
        self.select_button = QPushButton(FormImageWidget)
        self.select_button.setObjectName(u"select_button")

        self.hl_select_clear.addWidget(self.select_button)

        self.btn_reset = QPushButton(FormImageWidget)
        self.btn_reset.setObjectName(u"btn_reset")

        self.hl_select_clear.addWidget(self.btn_reset)

        self.hl_select_clear.setStretch(0, 1)

        self.verticalLayout.addLayout(self.hl_select_clear)

        self.label = QLabel(FormImageWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font-style: italic;")

        self.verticalLayout.addWidget(self.label)

        self.scale_layout = QHBoxLayout()
        self.scale_layout.setObjectName(u"scale_layout")

        self.verticalLayout.addLayout(self.scale_layout)

        self.textbrowser = QTextBrowser(FormImageWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.retranslateUi(FormImageWidget)

        QMetaObject.connectSlotsByName(FormImageWidget)
    # setupUi

    def retranslateUi(self, FormImageWidget):
        FormImageWidget.setWindowTitle(QCoreApplication.translate("FormImageWidget", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormImageWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormImageWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.label_variable.setText(QCoreApplication.translate("FormImageWidget", u"<html><head/><body><p><span style=\" font-style:italic;\">variable</span></p></body></html>", None))
        self.select_button.setText(QCoreApplication.translate("FormImageWidget", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
        self.btn_reset.setText(QCoreApplication.translate("FormImageWidget", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c", None))
        self.label.setText(QCoreApplication.translate("FormImageWidget", u"\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormImageWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formlistdialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formlistdialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_FormListDialogWindow(object):
    def setupUi(self, FormListDialogWindow):
        if not FormListDialogWindow.objectName():
            FormListDialogWindow.setObjectName(u"FormListDialogWindow")
        FormListDialogWindow.resize(500, 350)
        self.verticalLayout = QVBoxLayout(FormListDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_nametable = QLabel(FormListDialogWindow)
        self.label_nametable.setObjectName(u"label_nametable")

        self.verticalLayout.addWidget(self.label_nametable)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.add_button = QPushButton(FormListDialogWindow)
        self.add_button.setObjectName(u"add_button")

        self.buttons_layout.addWidget(self.add_button)

        self.delete_button = QPushButton(FormListDialogWindow)
        self.delete_button.setObjectName(u"delete_button")

        self.buttons_layout.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.buttons_layout)

        self.lw = QListWidget(FormListDialogWindow)
        self.lw.setObjectName(u"lw")

        self.verticalLayout.addWidget(self.lw)

        self.hl_moving = QHBoxLayout()
        self.hl_moving.setObjectName(u"hl_moving")
        self.label_move = QLabel(FormListDialogWindow)
        self.label_move.setObjectName(u"label_move")

        self.hl_moving.addWidget(self.label_move)

        self.btn_up = QPushButton(FormListDialogWindow)
        self.btn_up.setObjectName(u"btn_up")

        self.hl_moving.addWidget(self.btn_up)

        self.btn_down = QPushButton(FormListDialogWindow)
        self.btn_down.setObjectName(u"btn_down")

        self.hl_moving.addWidget(self.btn_down)

        self.hl_moving.setStretch(1, 1)
        self.hl_moving.setStretch(2, 1)

        self.verticalLayout.addLayout(self.hl_moving)

        self.line = QFrame(FormListDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_saveclose = QHBoxLayout()
        self.hl_saveclose.setObjectName(u"hl_saveclose")
        self.btn_save = QPushButton(FormListDialogWindow)
        self.btn_save.setObjectName(u"btn_save")

        self.hl_saveclose.addWidget(self.btn_save)

        self.btn_close = QPushButton(FormListDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.hl_saveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_saveclose)


        self.retranslateUi(FormListDialogWindow)

        QMetaObject.connectSlotsByName(FormListDialogWindow)
    # setupUi

    def retranslateUi(self, FormListDialogWindow):
        FormListDialogWindow.setWindowTitle(QCoreApplication.translate("FormListDialogWindow", u"Dialog", None))
        self.label_nametable.setText(QCoreApplication.translate("FormListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">TextLabel</span></p></body></html>", None))
        self.add_button.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.delete_button.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.label_move.setText(QCoreApplication.translate("FormListDialogWindow", u"\u041f\u0435\u0440\u0435\u043c\u0435\u0441\u0442\u0438\u0442\u044c", None))
        self.btn_up.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0412\u0432\u0435\u0440\u0445", None))
        self.btn_down.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0412\u043d\u0438\u0437", None))
        self.btn_save.setText(QCoreApplication.translate("FormListDialogWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("FormListDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formlist_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formlist.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_FormListWidget(object):
    def setupUi(self, FormListWidget):
        if not FormListWidget.objectName():
            FormListWidget.setObjectName(u"FormListWidget")
        FormListWidget.resize(431, 123)
        FormListWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormListWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormListWidget)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormListWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.hl.addWidget(self.title)

        self.label_variable = QLabel(FormListWidget)
        self.label_variable.setObjectName(u"label_variable")

        self.hl.addWidget(self.label_variable)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.btn_edittable = QPushButton(FormListWidget)
        self.btn_edittable.setObjectName(u"btn_edittable")

        self.verticalLayout.addWidget(self.btn_edittable)

        self.textbrowser = QTextBrowser(FormListWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textbrowser.sizePolicy().hasHeightForWidth())
        self.textbrowser.setSizePolicy(sizePolicy)
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(FormListWidget)

        QMetaObject.connectSlotsByName(FormListWidget)
    # setupUi

    def retranslateUi(self, FormListWidget):
        FormListWidget.setWindowTitle(QCoreApplication.translate("FormListWidget", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormListWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormListWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.label_variable.setText(QCoreApplication.translate("FormListWidget", u"<html><head/><body><p><span style=\" font-style:italic;\">TextLabel</span></p></body></html>", None))
        self.btn_edittable.setText(QCoreApplication.translate("FormListWidget", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormListWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formlongtext_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formlongtext.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

class Ui_FormLongText(object):
    def setupUi(self, FormLongText):
        if not FormLongText.objectName():
            FormLongText.setObjectName(u"FormLongText")
        FormLongText.resize(465, 170)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FormLongText.sizePolicy().hasHeightForWidth())
        FormLongText.setSizePolicy(sizePolicy)
        FormLongText.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormLongText)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormLongText)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormLongText)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)
        self.title.setScaledContents(False)

        self.hl.addWidget(self.title)

        self.label_variable = QLabel(FormLongText)
        self.label_variable.setObjectName(u"label_variable")

        self.hl.addWidget(self.label_variable)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.textedit = QTextEdit(FormLongText)
        self.textedit.setObjectName(u"textedit")
        self.textedit.setMaximumSize(QSize(16777215, 100))
        self.textedit.setAcceptRichText(False)

        self.verticalLayout.addWidget(self.textedit)

        self.textbrowser = QTextBrowser(FormLongText)
        self.textbrowser.setObjectName(u"textbrowser")
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.retranslateUi(FormLongText)

        QMetaObject.connectSlotsByName(FormLongText)
    # setupUi

    def retranslateUi(self, FormLongText):
        FormLongText.setWindowTitle(QCoreApplication.translate("FormLongText", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormLongText", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormLongText", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.label_variable.setText(QCoreApplication.translate("FormLongText", u"<html><head/><body><p><span style=\" font-style:italic;\">variable</span></p></body></html>", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormLongText", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formtabledialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formtabledialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_FormTableDialogWindow(object):
    def setupUi(self, FormTableDialogWindow):
        if not FormTableDialogWindow.objectName():
            FormTableDialogWindow.setObjectName(u"FormTableDialogWindow")
        FormTableDialogWindow.resize(700, 400)
        self.verticalLayout = QVBoxLayout(FormTableDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_nametable = QLabel(FormTableDialogWindow)
        self.label_nametable.setObjectName(u"label_nametable")

        self.verticalLayout.addWidget(self.label_nametable)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.add_button = QPushButton(FormTableDialogWindow)
        self.add_button.setObjectName(u"add_button")

        self.buttons_layout.addWidget(self.add_button)

        self.delete_button = QPushButton(FormTableDialogWindow)
        self.delete_button.setObjectName(u"delete_button")

        self.buttons_layout.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.buttons_layout)

        self.table = QTableWidget(FormTableDialogWindow)
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)

        self.line = QFrame(FormTableDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_saveclose = QHBoxLayout()
        self.hl_saveclose.setObjectName(u"hl_saveclose")
        self.btn_save = QPushButton(FormTableDialogWindow)
        self.btn_save.setObjectName(u"btn_save")

        self.hl_saveclose.addWidget(self.btn_save)

        self.btn_close = QPushButton(FormTableDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.hl_saveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_saveclose)


        self.retranslateUi(FormTableDialogWindow)

        QMetaObject.connectSlotsByName(FormTableDialogWindow)
    # setupUi

    def retranslateUi(self, FormTableDialogWindow):
        FormTableDialogWindow.setWindowTitle(QCoreApplication.translate("FormTableDialogWindow", u"Dialog", None))
        self.label_nametable.setText(QCoreApplication.translate("FormTableDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">TextLabel</span></p></body></html>", None))
        self.add_button.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
        self.delete_button.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
        self.btn_save.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("FormTableDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formtable_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formtable.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_FormTableWidget(object):
    def setupUi(self, FormTableWidget):
        if not FormTableWidget.objectName():
            FormTableWidget.setObjectName(u"FormTableWidget")
        FormTableWidget.resize(431, 123)
        FormTableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormTableWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormTableWidget)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormTableWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)

        self.hl.addWidget(self.title)

        self.label_variable = QLabel(FormTableWidget)
        self.label_variable.setObjectName(u"label_variable")

        self.hl.addWidget(self.label_variable)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.btn_edittable = QPushButton(FormTableWidget)
        self.btn_edittable.setObjectName(u"btn_edittable")

        self.verticalLayout.addWidget(self.btn_edittable)

        self.textbrowser = QTextBrowser(FormTableWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textbrowser.sizePolicy().hasHeightForWidth())
        self.textbrowser.setSizePolicy(sizePolicy)
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(FormTableWidget)

        QMetaObject.connectSlotsByName(FormTableWidget)
    # setupUi

    def retranslateUi(self, FormTableWidget):
        FormTableWidget.setWindowTitle(QCoreApplication.translate("FormTableWidget", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormTableWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormTableWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.label_variable.setText(QCoreApplication.translate("FormTableWidget", u"<html><head/><body><p><span style=\" font-style:italic;\">TextLabel</span></p></body></html>", None))
        self.btn_edittable.setText(QCoreApplication.translate("FormTableWidget", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443", None))
        self.textbrowser.setHtml(QCoreApplication.translate("FormTableWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\formtext_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formtext.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_FormTextWidget(object):
    def setupUi(self, FormTextWidget):
        if not FormTextWidget.objectName():
            FormTextWidget.setObjectName(u"FormTextWidget")
        FormTextWidget.resize(465, 121)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FormTextWidget.sizePolicy().hasHeightForWidth())
        FormTextWidget.setSizePolicy(sizePolicy)
        FormTextWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(FormTextWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.hl = QHBoxLayout()
        self.hl.setSpacing(9)
        self.hl.setObjectName(u"hl")
        self.label_typevariable = QLabel(FormTextWidget)
        self.label_typevariable.setObjectName(u"label_typevariable")
        self.label_typevariable.setAlignment(Qt.AlignCenter)

        self.hl.addWidget(self.label_typevariable)

        self.title = QLabel(FormTextWidget)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 16))
        self.title.setStyleSheet(u"font-weight: bold;")
        self.title.setTextFormat(Qt.AutoText)
        self.title.setScaledContents(False)

        self.hl.addWidget(self.title)

        self.label_variable = QLabel(FormTextWidget)
        self.label_variable.setObjectName(u"label_variable")

        self.hl.addWidget(self.label_variable)

        self.hl.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl)

        self.lineedit = QLineEdit(FormTextWidget)
        self.lineedit.setObjectName(u"lineedit")

        self.verticalLayout.addWidget(self.lineedit)

        self.textbrowser = QTextBrowser(FormTextWidget)
        self.textbrowser.setObjectName(u"textbrowser")
        self.textbrowser.setStyleSheet(u"background-color: #f0f0f0;\n"
"border: none")
        self.textbrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalLayout.addWidget(self.textbrowser)


        self.retranslateUi(FormTextWidget)

        QMetaObject.connectSlotsByName(FormTextWidget)
    # setupUi

    def retranslateUi(self, FormTextWidget):
        FormTextWidget.setWindowTitle(QCoreApplication.translate("FormTextWidget", u"Form", None))
        self.label_typevariable.setText(QCoreApplication.translate("FormTextWidget", u"\u0418\u041a", None))
        self.title.setText(QCoreApplication.translate("FormTextWidget", u"<html><head/><body><p>\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a</p></body></html>", None))
        self.label_variable.setText(QCoreApplication.translate("FormTextWidget", u"<html><head/><body><p><span style=\" font-style:italic;\">variable</span></p></body></html>", None))
        self.lineedit.setText("")
        self.textbrowser.setHtml(QCoreApplication.translate("FormTextWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435</p></body></html>", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\mainwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QSplitter,
    QStatusBar, QTabWidget, QToolBar, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1366, 768)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setStyleSheet(u"\n"
"/* For some reason applying background-color or border fixes paddings properties */\n"
"QListWidget::item {\n"
"    border-width: 0;\n"
"}\n"
"\n"
"/* Don't override install label on download widget.\n"
"     MO2 assigns color depending on download state */\n"
"#installLabel {\n"
"    color: none;\n"
"}\n"
"\n"
"/* Make `background-color` work for :hover, :focus and :pressed states */\n"
"QToolButton {\n"
"    border: none;\n"
"}\n"
"\n"
"* {\n"
"    font-family: Open Sans;\n"
"}\n"
"\n"
"/* Main Window */\n"
"QWidget {\n"
"    background-color: #2d2d30;\n"
"    color: #f1f1f1;\n"
"}\n"
"\n"
"QWidget::disabled {\n"
"    color: #656565;\n"
"}\n"
"\n"
"/* Common */\n"
"/* remove outline */\n"
"* {\n"
"    outline: 0;\n"
"}\n"
"\n"
"*:disabled,\n"
"QListView::item:disabled,\n"
"*::item:selected:disabled {\n"
"    color: #656565;\n"
"}\n"
"\n"
"/* line heights */\n"
"/* QTreeView#fileTree::item - currently have problem with size column vertical\n"
"     text align */\n"
"#bsaList::item,\n"
"#dataTree::item,\n"
""
                        "#modList::item,\n"
"#categoriesTree::item,\n"
"#savegameList::item,\n"
"#tabConflicts QTreeWidget::item {\n"
"    padding: 0.3em 0;\n"
"}\n"
"\n"
"QListView::item,\n"
"QTreeView#espList::item {\n"
"    /*\n"
"    padding: 0.3em 0;\n"
"    */\n"
"}\n"
"QListView#lw_pages_template::item {\n"
"    padding: 0.2em 0;\n"
"}\n"
"\n"
"/* to enable border color */\n"
"QTreeView,\n"
"QListView,\n"
"QTextEdit,\n"
"QWebView,\n"
"QTableView {\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QAbstractItemView {\n"
"    color: #dcdcdc;\n"
"    background-color: #1e1e1e;\n"
"    alternate-background-color: #262626;\n"
"    border-color: #3f3f46;\n"
"}\n"
"\n"
"QAbstractItemView::item:selected,\n"
"QAbstractItemView::item:selected:hover,\n"
"QAbstractItemView::item:alternate:selected,\n"
"QAbstractItemView::item:alternate:selected:hover {\n"
"    color: #f1f1f1;\n"
"    background-color: #3399ff;\n"
"}\n"
"\n"
"QAbstractItemView[filtered=true] {\n"
"    border: 2px solid #f00 !important;\n"
"}\n"
"\n"
"QA"
                        "bstractItemView,\n"
"QListView,\n"
"QTreeView {\n"
"    show-decoration-selected: 1;\n"
"}\n"
"\n"
"QAbstractItemView::item:hover,\n"
"QAbstractItemView::item:alternate:hover,\n"
"QAbstractItemView::item:disabled:hover,\n"
"QAbstractItemView::item:alternate:disabled:hover QListView::item:hover,\n"
"QTreeView::branch:hover,\n"
"QTreeWidget::item:hover {\n"
"    background-color: rgba(51, 153, 255, 0.3);\n"
"}\n"
"\n"
"QAbstractItemView::item:selected:disabled,\n"
"QAbstractItemView::item:alternate:selected:disabled,\n"
"QListView::item:selected:disabled,\n"
"QTreeView::branch:selected:disabled,\n"
"QTreeWidget::item:selected:disabled {\n"
"    background-color: rgba(51, 153, 255, 0.3);\n"
"}\n"
"\n"
"QTreeView::branch:selected,\n"
"#bsaList::branch:selected {\n"
"    background-color: #3399ff;\n"
"}\n"
"\n"
"QLabel {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"LinkLabel {\n"
"    qproperty-linkColor: #3399ff;\n"
"}\n"
"\n"
"/* Left Pane & File Trees #QTreeView, #QListView*/\n"
"QTreeView::branch:close"
                        "d:has-children {\n"
"    image: url(:/png/resources/png/branch-closed.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children {\n"
"    image: url(:/png/resources/png/branch-open.png);\n"
"}\n"
"\n"
"QListView::item {\n"
"    color: #f1f1f1;\n"
"}\n"
"\n"
"/* Text areas and text fields #QTextEdit, #QLineEdit, #QWebView */\n"
"QTextEdit,\n"
"QWebView,\n"
"QLineEdit,\n"
"QAbstractSpinBox,\n"
"QAbstractSpinBox::up-button,\n"
"QAbstractSpinBox::down-button,\n"
"QComboBox {\n"
"    background-color: #333337;\n"
"    border-color: #3f3f46;\n"
"}\n"
"\n"
"QLineEdit:hover,\n"
"QAbstractSpinBox:hover,\n"
"QTextEdit:hover,\n"
"QComboBox:hover,\n"
"QComboBox:editable:hover {\n"
"    border-color: #007acc;\n"
"}\n"
"\n"
"QLineEdit:focus,\n"
"QAbstractSpinBox::focus,\n"
"QTextEdit:focus,\n"
"QComboBox:focus,\n"
"QComboBox:editable:focus,\n"
"QComboBox:on {\n"
"    background-color: #3f3f46;\n"
"    border-color: #3399ff;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"    border-bottom-color: #3f3f46;\n"
"}\n"
"\n"
"QLineEdit,\n"
"QAbs"
                        "tractSpinBox {\n"
"    min-height: 15px;\n"
"    padding: 2px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    margin-top: 0;\n"
"}\n"
"\n"
"/* clear button */\n"
"QLineEdit QToolButton,\n"
"QLineEdit QToolButton:hover {\n"
"    background: none;\n"
"    margin-top: 1px;\n"
"}\n"
"\n"
"QLineEdit#espFilterEdit QToolButton {\n"
"    margin-top: -2px;\n"
"    margin-bottom: 1px;\n"
"}\n"
"\n"
"/* Drop-downs #QComboBox*/\n"
"QComboBox {\n"
"    min-height: 20px;\n"
"    padding-left: 5px;\n"
"    margin: 3px 0 1px 0;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    padding-left: 3px;\n"
"    /* to enable hover styles */\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 20px;\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/png/resources/png/combobox-down.png);\n"
"}\n"
"\n"
""
                        "QComboBox QAbstractItemView {\n"
"    background-color: #1b1b1c;\n"
"    selection-background-color: #3f3f46;\n"
"    border-color: #3399ff;\n"
"    border-style: solid;\n"
"    border-width: 0 1px 1px 1px;\n"
"}\n"
"\n"
"/* Doesn't work http://stackoverflow.com/questions/13308341/qcombobox-abstractitemviewitem */\n"
"/* QComboBox QAbstractItemView:item {\n"
"    padding: 10px;\n"
"    margin: 10px;\n"
"} */\n"
"/* Toolbar */\n"
"QToolBar {\n"
"    border: none;\n"
"}\n"
"\n"
"QToolBar::separator {\n"
"    border-left-color: #222222;\n"
"    border-right-color: #46464a;\n"
"    border-width: 0 1px 0 1px;\n"
"    border-style: solid;\n"
"    width: 0;\n"
"}\n"
"\n"
"QToolButton {\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:hover, QToolButton:focus {\n"
"    background-color: #3e3e40;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background-color: #3399ff;\n"
"}\n"
"\n"
"QToolButton::menu-indicator {\n"
"    image: url(:/png/resources/png/combobox-down.png);\n"
"    subcontrol-origin: padding;\n"
"    subcon"
                        "trol-position: center right;\n"
"    padding-top: 10%;\n"
"    padding-right: 5%;\n"
"}\n"
"\n"
"/* Group Boxes #QGroupBox */\n"
"QGroupBox {\n"
"    border-color: #3f3f46;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    /*\n"
"    padding: 1em 0.3em 0.3em 0.3em;\n"
"    margin-top: 0.65em;\n"
"    */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 2px;\n"
"    left: 10px;\n"
"}\n"
"\n"
"/* LCD Count */\n"
"QLCDNumber {\n"
"    border-color: #3f3f46;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"/* Buttons #QPushButton */\n"
"QPushButton {\n"
"    background-color: #333337;\n"
"    border-color: #3f3f46;\n"
"    min-height: 18px;\n"
"    padding: 2px 5px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QPushButton:hover,\n"
"QPushButton:checked,\n"
"QAbstractSpinBox::up-button:hover,\n"
"QAbstractSpinBox::down-button:hover {\n"
"    background-color: #007acc;\n"
"}\n"
"\n"
""
                        "QPushButton:focus {\n"
"    border-color: #007acc;\n"
"}\n"
"\n"
"QPushButton:pressed,\n"
"QPushButton:checked:hover,\n"
"QAbstractSpinBox::up-button:pressed,\n"
"QAbstractSpinBox::down-button:pressed {\n"
"    background-color: #1c97ea;\n"
"}\n"
"\n"
"QPushButton:disabled,\n"
"QAbstractSpinBox::up-button:disabled,\n"
"QAbstractSpinBox::down-button:disabled {\n"
"    background-color: #333337;\n"
"    border-color: #3f3f46;\n"
"}\n"
"\n"
"QPushButton::menu-indicator {\n"
"    image: url(:/png/resources/png/combobox-down.png);\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: center right;\n"
"    padding-right: 5%;\n"
"}\n"
"\n"
"/* Dialog buttons */\n"
"QSlider::handle:horizontal,\n"
"QSlider::handle:vertical {\n"
"    color: #000000;\n"
"    background-color: #dddddd;\n"
"    border-color: #707070;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover,\n"
"QSlider::handle:vertical:hover,\n"
"QSlider::handle:horizontal:pressed,\n"
"QSlider::hand"
                        "le:horizontal:focus:pressed,\n"
"QSlider::handle:vertical:pressed,\n"
"QSlider::handle:vertical:focus:pressed {\n"
"    background-color: #BEE6FD;\n"
"    border-color: #3c7fb1;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:focus,\n"
"QSlider::handle:vertical:focus {\n"
"    background-color: #dddddd;\n"
"    border-color: #3399ff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal:disabled,\n"
"QSlider::handle:vertical:disabled {\n"
"    background-color: #333337;\n"
"    border-color: #3f3f46;\n"
"}\n"
"\n"
"\n"
"/* Check boxes and Radio buttons common #QCheckBox, #QRadioButton */\n"
"QListView::indicator,\n"
"QGroupBox::indicator,\n"
"QTreeView::indicator,\n"
"QCheckBox::indicator,\n"
"QRadioButton::indicator {\n"
"    background-color: #2d2d30;\n"
"    border-color: #3f3f46;\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"QListView::indicator:hover,\n"
"QGroupBox::indicator:hover,\n"
"QTreeView::indicator:hover,\n"
"QCheckBox::indicator:hover,\n"
"QRadio"
                        "Button::indicator:hover {\n"
"    background-color: #3f3f46;\n"
"    border-color: #007acc;\n"
"}\n"
"QListView::indicator:checked,\n"
"QGroupBox::indicator:checked,\n"
"QTreeView::indicator:checked,\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/png/resources/png/checkbox-check.png);\n"
"}\n"
"QListView::indicator:checked:disabled,\n"
"QGroupBox::indicator:disabled,\n"
"QTreeView::indicator:checked:disabled,\n"
"QCheckBox::indicator:checked:disabled {\n"
"    image: url(:/png/resources/png/checkbox-check-disabled.png);\n"
"}\n"
"\n"
"/* Check boxes special */\n"
"QTreeView#modList::indicator {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"}\n"
"\n"
"/* Radio buttons #QRadioButton */\n"
"QRadioButton::indicator {\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"QRadioButton::indicator::checked {\n"
"    background-color: #B9B9BA;\n"
"    border-width: 2px;\n"
"    width: 11px;\n"
"    height: 11px;\n"
"}\n"
"\n"
"QRadioButton::indicator::checked:hover {\n"
"    border-color: #3f3f46;\n"
"}\n"
"\n"
"/* Spin"
                        "ners #QSpinBox, #QDoubleSpinBox */\n"
"QAbstractSpinBox {\n"
"    margin: 1px;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-button,\n"
"QAbstractSpinBox::down-button {\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    subcontrol-origin: padding;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-button {\n"
"    subcontrol-position: top right;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-arrow {\n"
"    image: url(:/png/resources/png/spinner-up.png);\n"
"}\n"
"\n"
"QAbstractSpinBox::down-button {\n"
"    subcontrol-position: bottom right;\n"
"}\n"
"\n"
"QAbstractSpinBox::down-arrow {\n"
"    image: url(:/png/resources/png/spinner-down.png);\n"
"}\n"
"\n"
"/* Sliders #QSlider */\n"
"QSlider::groove:horizontal {\n"
"    background-color: #3f3f46;\n"
"    border: none;\n"
"    height: 8px;\n"
"    margin: 2px 0;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    width: 0.5em;\n"
"    height: 2em;\n"
"    margin: -7px 0;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Scroll Bars #QAbstractScrollArea, #QScrollBar*/\n"
"/* assi"
                        "gning background still leaves not filled area*/\n"
"QAbstractScrollArea::corner {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* Horizontal */\n"
"QScrollBar:horizontal {\n"
"    height: 18px;\n"
"    border: none;\n"
"    margin: 0 23px 0 23px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    min-width: 32px;\n"
"    margin: 4px 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    width: 23px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    width: 23px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Vertical */\n"
"QScrollBar:vertical {\n"
"    width: 20px;\n"
"    border: none;\n"
"    margin: 23px 0 23px 0;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    min-height: 32px;\n"
"    margin: 2px 4px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    height: 23px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBa"
                        "r::sub-line:vertical {\n"
"    height: 23px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Combined */\n"
"QScrollBar {\n"
"    background-color: #3e3e42;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
"    background-color: #686868;\n"
"}\n"
"\n"
"QScrollBar::add-line,\n"
"QScrollBar::sub-line {\n"
"    background-color: #3e3e42;\n"
"    border: none;\n"
"}\n"
"\n"
"/* QScrollBar::add-line:horizontal:hover,\n"
"QScrollBar::sub-line:horizontal:hover,\n"
"QScrollBar::add-line:vertical:hover,\n"
"QScrollBar::sub-line:vertical:hover,\n"
"QScrollBar::add-line:horizontal:pressed,\n"
"QScrollBar::sub-line:horizontal:pressed,\n"
"QScrollBar::add-line:vertical:pressed,\n"
"QScrollBar::sub-line:vertical:pressed { } */\n"
"QScrollBar::handle:hover {\n"
"    background: #9e9e9e;\n"
"}\n"
"\n"
"QScrollBar::handle:pressed {\n"
"    background: #efebef;\n"
"}\n"
"\n"
"QScrollBar::handle:disabled {\n"
"    background: #555558;\n"
"}\n"
"\n"
"QScrollBar::add-page,\n"
"QSc"
                        "rollBar::sub-page {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical {\n"
"    image: url(:/png/resources/png/scrollbar-up.png);\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical:hover {\n"
"    image: url(:/png/resources/png/scrollbar-up-hover.png);\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical:disabled {\n"
"    image: url(:/png/resources/png/scrollbar-up-disabled.png);\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal {\n"
"    image: url(:/png/resources/png/scrollbar-right.png);\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal:hover {\n"
"    image: url(:/png/resources/png/scrollbar-right-hover.png);\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal:disabled {\n"
"    image: url(:/png/resources/png/scrollbar-right-disabled.png);\n"
"}\n"
"\n"
"QScrollBar::down-arrow:vertical {\n"
"    image: url(:/png/resources/png/scrollbar-down.png);\n"
"}\n"
"\n"
"QScrollBar::down-arrow:vertical:hover {\n"
"    image: url(:/png/resources/png/scrollbar-down-hover.png);\n"
"}\n"
"\n"
"QScrollBar::d"
                        "own-arrow:vertical:disabled {\n"
"    image: url(:/png/resources/png/scrollbar-down-disabled.png);\n"
"}\n"
"\n"
"QScrollBar::left-arrow:horizontal {\n"
"    image: url(:/png/resources/png/scrollbar-left.png);\n"
"}\n"
"\n"
"QScrollBar::left-arrow:horizontal:hover {\n"
"    image: url(:/png/resources/png/scrollbar-left-hover.png);\n"
"}\n"
"\n"
"QScrollBar::left-arrow:horizontal:disabled {\n"
"    image: url(:/png/resources/png/scrollbar-left-disabled.png);\n"
"}\n"
"\n"
"/* Header Rows and Tables (Configure Mod Categories) #QTableView, #QHeaderView */\n"
"QTableView {\n"
"    gridline-color: #3f3f46;\n"
"    selection-background-color: #3399ff;\n"
"    selection-color: #f1f1f1;\n"
"}\n"
"\n"
"QTableView QTableCornerButton::section {\n"
"    background: #252526;\n"
"    border-color: #3f3f46;\n"
"    border-style: solid;\n"
"    border-width: 0 1px 1px 0;\n"
"}\n"
"\n"
"QHeaderView {\n"
"    border: none;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background: #252526;\n"
"    border-color: #3f3f46;\n"
"    "
                        "padding: 3px 5px;\n"
"    border-style: solid;\n"
"    border-width: 0 1px 1px 0;\n"
"}\n"
"\n"
"QHeaderView::section:hover {\n"
"    background: #3e3e40;\n"
"    color: #f6f6f6;\n"
"}\n"
"\n"
"QHeaderView::section:last {\n"
"    border-right: 0;\n"
"}\n"
"\n"
"QHeaderView::up-arrow {\n"
"    image: url(:/png/resources/png/sort-asc.png);\n"
"    width: 0px;\n"
"}\n"
"\n"
"\n"
"QHeaderView::down-arrow {\n"
"    image: url(:/png/resources/png/sort-desc.png);\n"
"    width: 0px;\n"
"}\n"
"\n"
"\n"
"/* Context menus, toolbar drop-downs #QMenu    */\n"
"QMenu {\n"
"    background-color: #1a1a1c;\n"
"    border-color: #333337;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    background: transparent;\n"
"    padding: 4px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected,\n"
"QMenuBar::item:selected {\n"
"    background-color: #333334;\n"
"}\n"
"\n"
"QMenu::item:disabled {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"    backgrou"
                        "nd-color: #333337;\n"
"    height: 1px;\n"
"    margin: 1px 0;\n"
"}\n"
"\n"
"QMenu::icon {\n"
"    margin: 1px;\n"
"}\n"
"\n"
"QMenu::right-arrow {\n"
"    image: url(:/png/resources/png/sub-menu-arrow.png);\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: center right;\n"
"    padding-right: 0.5em;\n"
"}\n"
"\n"
"QMenu QPushButton {\n"
"    background-color: transparent;\n"
"    border-color: #3f3f46;\n"
"    margin: 1px 0 1px 0;\n"
"}\n"
"\n"
"QMenu QCheckBox,\n"
"QMenu QRadioButton {\n"
"    background-color: transparent;\n"
"    padding: 5px 2px;\n"
"}\n"
"\n"
"/* Tool tips #QToolTip, #SaveGameInfoWidget */\n"
"QToolTip,\n"
"SaveGameInfoWidget {\n"
"    background-color: #424245;\n"
"    border-color: #4d4d50;\n"
"    color: #f1f1f1;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QStatusBar::item {\n"
"    border: None;\n"
"}\n"
"\n"
"/* Progress Bars (Downloads) #QProgressBar */\n"
"QProgressBar {\n"
"    background-color: #e6e6e6;\n"
"    col"
                        "or: #000;\n"
"    border-color: #bcbcbc;\n"
"    text-align: center;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background: #06b025;\n"
"}\n"
"\n"
"DownloadListView[downloadView=standard]::item {\n"
"    padding: 16px;\n"
"}\n"
"\n"
"DownloadListView[downloadView=compact]::item {\n"
"    padding: 4px;\n"
"}\n"
"\n"
"/* Right Pane and Tab Bars #QTabWidget, #QTabBar */\n"
"QTabWidget::pane {\n"
"    border-color: #3f3f46;\n"
"    border-top-color: #007acc;\n"
"    top: 0;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QTabWidget::pane:disabled {\n"
"    border-top-color: #3f3f46;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: transparent;\n"
"    padding: 4px 1em;\n"
"    border: none;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #1c97ea;\n"
"}\n"
"\n"
"QTabBar::tab:selected,\n"
"QTabBar::tab:selected:hover {\n"
"    background-color: #007acc;\n"
"}\n"
"\n"
"QTabBar::tab:disabled {\n"
""
                        "    background-color: transparent;\n"
"    color: #656565;\n"
"}\n"
"\n"
"QTabBar::tab:selected:disabled {\n"
"    background-color: #3f3f46;\n"
"}\n"
"\n"
"/* Scrollers */\n"
"QTabBar QToolButton {\n"
"    background-color: #333337;\n"
"    border-color: #3f3f46;\n"
"    padding: 1px;\n"
"    margin: 0;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QTabBar QToolButton:hover {\n"
"    border-color: #007acc;\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"}\n"
"\n"
"QTabBar QToolButton:disabled,\n"
"QTabBar QToolButton:pressed:hover {\n"
"    background-color: #333337;\n"
"}\n"
"\n"
"QTabBar::scroller {\n"
"    width: 23px;\n"
"    background-color: red;\n"
"}\n"
"\n"
"QTabBar QToolButton::right-arrow {\n"
"    image: url(:/png/resources/png/scrollbar-right.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::right-arrow:hover {\n"
"    image: url(:/png/resources/png/scrollbar-right-hover.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::left-arrow {\n"
"    image: url(:/png/resources/png/scro"
                        "llbar-left.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::left-arrow:hover {\n"
"    image: url(:/png/resources/png/scrollbar-left-hover.png);\n"
"}\n"
"\n"
"/* Special styles */\n"
"QWidget#tabImages QPushButton {\n"
"    background-color: transparent;\n"
"    margin: 0 0.3em;\n"
"    padding: 0;\n"
"}\n"
"\n"
"/* like dialog QPushButton*/\n"
"QWidget#tabESPs QToolButton {\n"
"    color: #000000;\n"
"    background-color: #dddddd;\n"
"    border-color: #707070;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QWidget#tabESPs QToolButton:hover {\n"
"    background-color: #BEE6FD;\n"
"    border-color: #3c7fb1;\n"
"}\n"
"\n"
"QWidget#tabESPs QToolButton:focus {\n"
"    background-color: #dddddd;\n"
"    border-color: #3399ff;\n"
"}\n"
"\n"
"QWidget#tabESPs QToolButton:disabled {\n"
"    background-color: #333337;\n"
"    border-color: #3f3f46;\n"
"}\n"
"\n"
"QTreeWidget#categoriesList {\n"
"    /* min-width: 225px; */\n"
"}\n"
"\n"
"QTreeWidget#categoriesList::item {\n"
"    background-position"
                        ": center left;\n"
"    background-repeat: no-repeat;\n"
"    padding: 0.35em 10px;\n"
"}\n"
"\n"
"QTreeWidget#categoriesList::item:has-children {\n"
"    background-image: url(:/png/resources/png/branch-closed.png);\n"
"}\n"
"\n"
"QTreeWidget#categoriesList::item:has-children:open {\n"
"    background-image: url(:/png/resources/png/branch-open.png);\n"
"}\n"
"\n"
"QDialog#QueryOverwriteDialog QPushButton {\n"
"    margin-left: 0.5em;\n"
"}\n"
"\n"
"QDialog#PyCfgDialog QPushButton:hover {\n"
"    background-color: #BEE6FD;\n"
"}\n"
"\n"
"QLineEdit#modFilterEdit {\n"
"    margin-top: 2px;\n"
"}\n"
"\n"
"/* highlight unchecked BSAs */\n"
"QWidget#bsaTab QTreeWidget::indicator:unchecked {\n"
"    background-color: #3399ff;\n"
"}\n"
"\n"
"/* increase version text field */\n"
"QLineEdit#versionEdit {\n"
"    max-width: 100px;\n"
"}\n"
"\n"
"/* Dialogs width changes */\n"
"/* increase width to prevent buttons cutting */\n"
"QDialog#QueryOverwriteDialog {\n"
"    min-width: 565px;\n"
"}\n"
"\n"
"QDialog#ModInfoDialog "
                        "{\n"
"    min-width: 850px;\n"
"}\n"
"\n"
"QLineEdit[valid-filter=false] {\n"
"    background-color: #661111 !important;\n"
"}\n"
"\n"
"/* \u0441\u043e\u0431\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0435 \u0440\u0435\u0448\u0435\u043d\u0438\u0435 */\n"
"QToolBar QToolButton:disabled {\n"
"    background-color: #252526;\n"
"}\n"
"\n"
"QToolBar QToolButton:checked {\n"
"    background-color: #3399ff;\n"
"}\n"
"")
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        icon = QIcon()
        iconThemeName = u"document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u":/white-icons/resources/white-icons/add-file.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.action_new.setIcon(icon)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        icon1 = QIcon()
        icon1.addFile(u":/white-icons/resources/white-icons/open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_open.setIcon(icon1)
        self.action_saveas = QAction(MainWindow)
        self.action_saveas.setObjectName(u"action_saveas")
        self.action_saveas.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u":/white-icons/resources/white-icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_saveas.setIcon(icon2)
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save.setEnabled(False)
        self.action_save.setIcon(icon2)
        self.action_edit_variables = QAction(MainWindow)
        self.action_edit_variables.setObjectName(u"action_edit_variables")
        self.action_edit_variables.setEnabled(False)
        icon3 = QIcon()
        icon3.addFile(u":/white-icons/resources/white-icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_variables.setIcon(icon3)
        self.action_zoomfitpage = QAction(MainWindow)
        self.action_zoomfitpage.setObjectName(u"action_zoomfitpage")
        self.action_zoomfitpage.setCheckable(True)
        self.action_zoomfitpage.setEnabled(False)
        icon4 = QIcon()
        icon4.addFile(u":/white-icons/resources/white-icons/zoom-fit-width.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomfitpage.setIcon(icon4)
        self.action_zoomfitpage.setMenuRole(QAction.TextHeuristicRole)
        self.action_export_to_pdf = QAction(MainWindow)
        self.action_export_to_pdf.setObjectName(u"action_export_to_pdf")
        self.action_export_to_pdf.setEnabled(False)
        icon5 = QIcon()
        icon5.addFile(u":/white-icons/resources/white-icons/export.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_export_to_pdf.setIcon(icon5)
        self.action_edit_templates = QAction(MainWindow)
        self.action_edit_templates.setObjectName(u"action_edit_templates")
        self.action_edit_templates.setEnabled(False)
        icon6 = QIcon()
        icon6.addFile(u":/white-icons/resources/white-icons/template.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_templates.setIcon(icon6)
        self.action_edit_templates.setMenuRole(QAction.TextHeuristicRole)
        self.action_edit_composition = QAction(MainWindow)
        self.action_edit_composition.setObjectName(u"action_edit_composition")
        self.action_edit_composition.setEnabled(False)
        icon7 = QIcon()
        icon7.addFile(u":/white-icons/resources/white-icons/items-tree.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_composition.setIcon(icon7)
        self.action_edit_composition.setMenuRole(QAction.TextHeuristicRole)
        self.action_clear_trash = QAction(MainWindow)
        self.action_clear_trash.setObjectName(u"action_clear_trash")
        icon8 = QIcon()
        icon8.addFile(u":/white-icons/resources/white-icons/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_clear_trash.setIcon(icon8)
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        icon9 = QIcon()
        icon9.addFile(u":/white-icons/resources/white-icons/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_settings.setIcon(icon9)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(4, 0, 4, 0)
        self.centralwidget_splitter = QSplitter(self.centralwidget)
        self.centralwidget_splitter.setObjectName(u"centralwidget_splitter")
        self.centralwidget_splitter.setOrientation(Qt.Horizontal)
        self.gb_left = QGroupBox(self.centralwidget_splitter)
        self.gb_left.setObjectName(u"gb_left")
        self.verticalLayout_8 = QVBoxLayout(self.gb_left)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(4, 4, 4, 4)
        self.gb_left_splitter = QSplitter(self.gb_left)
        self.gb_left_splitter.setObjectName(u"gb_left_splitter")
        self.gb_left_splitter.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget = QWidget(self.gb_left_splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vbl_templates = QVBoxLayout(self.verticalLayoutWidget)
        self.vbl_templates.setObjectName(u"vbl_templates")
        self.vbl_templates.setContentsMargins(0, 0, 0, 0)
        self.label_structure_execdoc = QLabel(self.verticalLayoutWidget)
        self.label_structure_execdoc.setObjectName(u"label_structure_execdoc")
        self.label_structure_execdoc.setEnabled(True)

        self.vbl_templates.addWidget(self.label_structure_execdoc)

        self.treewidget_structure_execdoc = QTreeWidget(self.verticalLayoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"\u041f\u0440\u043e\u0435\u043a\u0442 \u043d\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d");
        self.treewidget_structure_execdoc.setHeaderItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treewidget_structure_execdoc)
        __qtreewidgetitem1.setCheckState(0, Qt.Checked);
        __qtreewidgetitem2 = QTreeWidgetItem(self.treewidget_structure_execdoc)
        __qtreewidgetitem2.setCheckState(0, Qt.Checked);
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3.setCheckState(0, Qt.Checked);
        self.treewidget_structure_execdoc.setObjectName(u"treewidget_structure_execdoc")
        self.treewidget_structure_execdoc.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.vbl_templates.addWidget(self.treewidget_structure_execdoc)

        self.gb_left_splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.gb_left_splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.vbl_pages = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vbl_pages.setObjectName(u"vbl_pages")
        self.vbl_pages.setContentsMargins(0, 0, 0, 0)
        self.label_current_template = QLabel(self.verticalLayoutWidget_2)
        self.label_current_template.setObjectName(u"label_current_template")

        self.vbl_pages.addWidget(self.label_current_template)

        self.combox_templates = QComboBox(self.verticalLayoutWidget_2)
        self.combox_templates.setObjectName(u"combox_templates")

        self.vbl_pages.addWidget(self.combox_templates)

        self.label_pages_template = QLabel(self.verticalLayoutWidget_2)
        self.label_pages_template.setObjectName(u"label_pages_template")

        self.vbl_pages.addWidget(self.label_pages_template)

        self.lw_pages_template = QListWidget(self.verticalLayoutWidget_2)
        __qlistwidgetitem = QListWidgetItem(self.lw_pages_template)
        __qlistwidgetitem.setCheckState(Qt.Checked);
        __qlistwidgetitem1 = QListWidgetItem(self.lw_pages_template)
        __qlistwidgetitem1.setCheckState(Qt.Checked);
        self.lw_pages_template.setObjectName(u"lw_pages_template")
        self.lw_pages_template.setStyleSheet(u"")

        self.vbl_pages.addWidget(self.lw_pages_template)

        self.gb_left_splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_8.addWidget(self.gb_left_splitter)

        self.centralwidget_splitter.addWidget(self.gb_left)
        self.gb_center = QGroupBox(self.centralwidget_splitter)
        self.gb_center.setObjectName(u"gb_center")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gb_center.sizePolicy().hasHeightForWidth())
        self.gb_center.setSizePolicy(sizePolicy1)
        self.gb_center.setMinimumSize(QSize(350, 0))
        self.gb_center.setFlat(False)
        self.gb_center.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.gb_center)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.label_realview = QLabel(self.gb_center)
        self.label_realview.setObjectName(u"label_realview")

        self.verticalLayout.addWidget(self.label_realview)

        self.widget_pdf_view = QPdfView(self.gb_center)
        self.widget_pdf_view.setObjectName(u"widget_pdf_view")
        self.widget_pdf_view.setMaximumSize(QSize(16777215, 16777215))
        self.widget_pdf_view.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.widget_pdf_view)

        self.verticalLayout.setStretch(1, 1)
        self.centralwidget_splitter.addWidget(self.gb_center)
        self.gb_right = QGroupBox(self.centralwidget_splitter)
        self.gb_right.setObjectName(u"gb_right")
        sizePolicy1.setHeightForWidth(self.gb_right.sizePolicy().hasHeightForWidth())
        self.gb_right.setSizePolicy(sizePolicy1)
        self.gb_right.setMinimumSize(QSize(400, 0))
        self.verticalLayout_4 = QVBoxLayout(self.gb_right)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.label_variables = QLabel(self.gb_right)
        self.label_variables.setObjectName(u"label_variables")

        self.verticalLayout_4.addWidget(self.label_variables)

        self.tabw_inputforms = QTabWidget(self.gb_right)
        self.tabw_inputforms.setObjectName(u"tabw_inputforms")

        self.verticalLayout_4.addWidget(self.tabw_inputforms)

        self.label_default = QLabel(self.gb_right)
        self.label_default.setObjectName(u"label_default")

        self.verticalLayout_4.addWidget(self.label_default)

        self.combox_default = QComboBox(self.gb_right)
        self.combox_default.setObjectName(u"combox_default")

        self.verticalLayout_4.addWidget(self.combox_default)

        self.centralwidget_splitter.addWidget(self.gb_right)

        self.verticalLayout_6.addWidget(self.centralwidget_splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1366, 23))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_recent_projects = QMenu(self.menu_file)
        self.menu_recent_projects.setObjectName(u"menu_recent_projects")
        self.menu_editors = QMenu(self.menu_bar)
        self.menu_editors.setObjectName(u"menu_editors")
        self.menu_scale = QMenu(self.menu_bar)
        self.menu_scale.setObjectName(u"menu_scale")
        self.menu = QMenu(self.menu_bar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menu_bar)
        self.tb_main = QToolBar(MainWindow)
        self.tb_main.setObjectName(u"tb_main")
        self.tb_main.setEnabled(True)
        self.tb_main.setMovable(True)
        self.tb_main.setAllowedAreas(Qt.AllToolBarAreas)
        self.tb_main.setOrientation(Qt.Horizontal)
        self.tb_main.setIconSize(QSize(32, 24))
        self.tb_main.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_main.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.tb_main)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        self.status_bar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_editors.menuAction())
        self.menu_bar.addAction(self.menu_scale.menuAction())
        self.menu_bar.addAction(self.menu.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.menu_recent_projects.menuAction())
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_export_to_pdf)
        self.menu_editors.addAction(self.action_edit_composition)
        self.menu_editors.addAction(self.action_edit_templates)
        self.menu_editors.addAction(self.action_edit_variables)
        self.menu_scale.addAction(self.action_zoomfitpage)
        self.menu.addAction(self.action_settings)
        self.menu.addAction(self.action_clear_trash)
        self.tb_main.addAction(self.action_new)
        self.tb_main.addAction(self.action_open)
        self.tb_main.addAction(self.action_save)
        self.tb_main.addAction(self.action_export_to_pdf)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_edit_composition)
        self.tb_main.addAction(self.action_edit_templates)
        self.tb_main.addAction(self.action_edit_variables)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_zoomfitpage)

        self.retranslateUi(MainWindow)

        self.tabw_inputforms.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0430\u0446\u0438\u044f \u0418\u0414", None))
        self.action_new.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439", None))
#if QT_CONFIG(shortcut)
        self.action_new.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.action_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_saveas.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a", None))
#if QT_CONFIG(shortcut)
        self.action_saveas.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.action_save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_variables.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
        self.action_edit_variables.setIconText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
#if QT_CONFIG(tooltip)
        self.action_edit_variables.setToolTip(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
#endif // QT_CONFIG(tooltip)
        self.action_zoomfitpage.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e \u0448\u0438\u0440\u0438\u043d\u0435", None))
        self.action_export_to_pdf.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 PDF", None))
        self.action_edit_templates.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432", None))
        self.action_edit_composition.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u043e\u0441\u0442\u0430\u0432\u0430 \u0418\u0414", None))
        self.action_clear_trash.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u043a\u0430 \u043e\u0442 \u043c\u0443\u0441\u043e\u0440\u0430", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b", None))
        self.label_structure_execdoc.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u043f\u0440\u043e\u0435\u043a\u0442\u0430</span></p></body></html>", None))

        __sortingEnabled = self.treewidget_structure_execdoc.isSortingEnabled()
        self.treewidget_structure_execdoc.setSortingEnabled(False)
        ___qtreewidgetitem = self.treewidget_structure_execdoc.topLevelItem(0)
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u0422\u0438\u0442\u0443\u043b\u044c\u043d\u044b\u0439 \u043b\u0438\u0441\u0442", None));
        ___qtreewidgetitem1 = self.treewidget_structure_execdoc.topLevelItem(1)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0441\u043f\u043e\u0440\u0442", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0422-1", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0422-2", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"\u041f\u0422-3", None));
        self.treewidget_structure_execdoc.setSortingEnabled(__sortingEnabled)

        self.label_current_template.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0448\u0430\u0431\u043b\u043e\u043d</span></p></body></html>", None))
        self.label_pages_template.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u0442\u0435\u043a\u0443\u0449\u0435\u0433\u043e \u0448\u0430\u0431\u043b\u043e\u043d\u0430</span></p></body></html>", None))

        __sortingEnabled1 = self.lw_pages_template.isSortingEnabled()
        self.lw_pages_template.setSortingEnabled(False)
        ___qlistwidgetitem = self.lw_pages_template.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 1", None));
        ___qlistwidgetitem1 = self.lw_pages_template.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442 2", None));
        self.lw_pages_template.setSortingEnabled(__sortingEnabled1)

        self.label_realview.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0432 \u0440\u0435\u0436\u0438\u043c\u0435 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0432\u0440\u0435\u043c\u0435\u043d\u0438</span></p></body></html>", None))
        self.label_variables.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0424\u043e\u0440\u043c\u0430 \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f</span></p></body></html>", None))
        self.label_default.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e</span></p></body></html>", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_recent_projects.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u0434\u0430\u0432\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u044b", None))
        self.menu_editors.setTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u044b", None))
        self.menu_scale.setTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0441\u0448\u0442\u0430\u0431", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0447\u0435\u0435", None))
        self.tb_main.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u0432", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nedcolumntabletag_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedcolumntablevariable.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_NedColumnTableVariable(object):
    def setupUi(self, NedColumnTableVariable):
        if not NedColumnTableVariable.objectName():
            NedColumnTableVariable.setObjectName(u"NedColumnTableVariable")
        NedColumnTableVariable.resize(400, 148)
        self.verticalLayout = QVBoxLayout(NedColumnTableVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.colname = QLabel(NedColumnTableVariable)
        self.colname.setObjectName(u"colname")
        self.colname.setMinimumSize(QSize(0, 0))
        self.colname.setMaximumSize(QSize(16777215, 16))
        self.colname.setStyleSheet(u"font-weight: bold;")
        self.colname.setTextFormat(Qt.AutoText)
        self.colname.setScaledContents(False)

        self.verticalLayout.addWidget(self.colname)

        self.lineedit_colname = QLineEdit(NedColumnTableVariable)
        self.lineedit_colname.setObjectName(u"lineedit_colname")
        self.lineedit_colname.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_colname)

        self.colvariable = QLabel(NedColumnTableVariable)
        self.colvariable.setObjectName(u"colvariable")
        self.colvariable.setMinimumSize(QSize(0, 0))
        self.colvariable.setMaximumSize(QSize(16777215, 16))
        self.colvariable.setStyleSheet(u"font-weight: bold;")
        self.colvariable.setTextFormat(Qt.AutoText)
        self.colvariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.colvariable)

        self.lineedit_colvariable = QLineEdit(NedColumnTableVariable)
        self.lineedit_colvariable.setObjectName(u"lineedit_colvariable")
        self.lineedit_colvariable.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_colvariable)

        self.btn_ned = QPushButton(NedColumnTableVariable)
        self.btn_ned.setObjectName(u"btn_ned")

        self.verticalLayout.addWidget(self.btn_ned)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(NedColumnTableVariable)

        QMetaObject.connectSlotsByName(NedColumnTableVariable)
    # setupUi

    def retranslateUi(self, NedColumnTableVariable):
        NedColumnTableVariable.setWindowTitle(QCoreApplication.translate("NedColumnTableVariable", u"Dialog", None))
        self.colname.setText(QCoreApplication.translate("NedColumnTableVariable", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u043e\u043b\u0431\u0446\u0430</p></body></html>", None))
        self.colvariable.setText(QCoreApplication.translate("NedColumnTableVariable", u"<html><head/><body><p>\u041f\u043e\u0434\u0442\u044d\u0433 </p></body></html>", None))
        self.btn_ned.setText(QCoreApplication.translate("NedColumnTableVariable", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u044d\u0433", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\neddatevariable_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neddatevariable.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_NedDateVariable(object):
    def setupUi(self, NedDateVariable):
        if not NedDateVariable.objectName():
            NedDateVariable.setObjectName(u"NedDateVariable")
        NedDateVariable.resize(400, 133)
        self.verticalLayout = QVBoxLayout(NedDateVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formatdate = QLabel(NedDateVariable)
        self.formatdate.setObjectName(u"formatdate")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formatdate.sizePolicy().hasHeightForWidth())
        self.formatdate.setSizePolicy(sizePolicy)
        self.formatdate.setMinimumSize(QSize(0, 0))
        self.formatdate.setMaximumSize(QSize(16777215, 16))
        self.formatdate.setStyleSheet(u"font-weight: bold;")
        self.formatdate.setTextFormat(Qt.AutoText)
        self.formatdate.setScaledContents(False)

        self.verticalLayout.addWidget(self.formatdate)

        self.lineedit_format = QLineEdit(NedDateVariable)
        self.lineedit_format.setObjectName(u"lineedit_format")
        self.lineedit_format.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineedit_format)

        self.label_language = QLabel(NedDateVariable)
        self.label_language.setObjectName(u"label_language")

        self.verticalLayout.addWidget(self.label_language)

        self.combox_language = QComboBox(NedDateVariable)
        self.combox_language.setObjectName(u"combox_language")

        self.verticalLayout.addWidget(self.combox_language)

        self.hl = QHBoxLayout()
        self.hl.setObjectName(u"hl")
        self.label_check = QLabel(NedDateVariable)
        self.label_check.setObjectName(u"label_check")

        self.hl.addWidget(self.label_check)

        self.dateedit_check = QDateEdit(NedDateVariable)
        self.dateedit_check.setObjectName(u"dateedit_check")

        self.hl.addWidget(self.dateedit_check)

        self.label_result = QLabel(NedDateVariable)
        self.label_result.setObjectName(u"label_result")

        self.hl.addWidget(self.label_result)

        self.hl.setStretch(1, 1)
        self.hl.setStretch(2, 1)

        self.verticalLayout.addLayout(self.hl)

        self.line = QFrame(NedDateVariable)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(NedDateVariable)

        QMetaObject.connectSlotsByName(NedDateVariable)
    # setupUi

    def retranslateUi(self, NedDateVariable):
        NedDateVariable.setWindowTitle(QCoreApplication.translate("NedDateVariable", u"Form", None))
        self.formatdate.setText(QCoreApplication.translate("NedDateVariable", u"<html><head/><body><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0434\u0430\u0442\u044b</p></body></html>", None))
        self.label_language.setText(QCoreApplication.translate("NedDateVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u042f\u0437\u044b\u043a </span></p></body></html>", None))
        self.label_check.setText(QCoreApplication.translate("NedDateVariable", u"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430:", None))
        self.label_result.setText("")
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\neddocxpdfdialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neddocxpdfdialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_NedDocxPdfDialogWindow(object):
    def setupUi(self, NedDocxPdfDialogWindow):
        if not NedDocxPdfDialogWindow.objectName():
            NedDocxPdfDialogWindow.setObjectName(u"NedDocxPdfDialogWindow")
        NedDocxPdfDialogWindow.resize(450, 450)
        self.verticalLayout = QVBoxLayout(NedDocxPdfDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_typefile = QLabel(NedDocxPdfDialogWindow)
        self.label_typefile.setObjectName(u"label_typefile")

        self.verticalLayout.addWidget(self.label_typefile)

        self.combox_typefile = QComboBox(NedDocxPdfDialogWindow)
        self.combox_typefile.setObjectName(u"combox_typefile")

        self.verticalLayout.addWidget(self.combox_typefile)

        self.label_document = QLabel(NedDocxPdfDialogWindow)
        self.label_document.setObjectName(u"label_document")
        self.label_document.setMinimumSize(QSize(0, 0))
        self.label_document.setMaximumSize(QSize(16777215, 16))
        self.label_document.setStyleSheet(u"font-weight: bold;")
        self.label_document.setTextFormat(Qt.AutoText)
        self.label_document.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_document)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_select = QPushButton(NedDocxPdfDialogWindow)
        self.btn_select.setObjectName(u"btn_select")

        self.horizontalLayout.addWidget(self.btn_select)

        self.btn_open_docx = QPushButton(NedDocxPdfDialogWindow)
        self.btn_open_docx.setObjectName(u"btn_open_docx")

        self.horizontalLayout.addWidget(self.btn_open_docx)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_file = QLabel(NedDocxPdfDialogWindow)
        self.label_file.setObjectName(u"label_file")
        self.label_file.setStyleSheet(u"font-style: italic;")

        self.verticalLayout.addWidget(self.label_file)

        self.label_variables = QLabel(NedDocxPdfDialogWindow)
        self.label_variables.setObjectName(u"label_variables")
        self.label_variables.setMinimumSize(QSize(0, 0))
        self.label_variables.setMaximumSize(QSize(16777215, 16))
        self.label_variables.setStyleSheet(u"font-weight: bold;")
        self.label_variables.setTextFormat(Qt.AutoText)
        self.label_variables.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_variables)

        self.tw_variables = QTableWidget(NedDocxPdfDialogWindow)
        self.tw_variables.setObjectName(u"tw_variables")

        self.verticalLayout.addWidget(self.tw_variables)

        self.btn_findvariables = QPushButton(NedDocxPdfDialogWindow)
        self.btn_findvariables.setObjectName(u"btn_findvariables")

        self.verticalLayout.addWidget(self.btn_findvariables)

        self.line = QFrame(NedDocxPdfDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nedvariable = QPushButton(NedDocxPdfDialogWindow)
        self.btn_nedvariable.setObjectName(u"btn_nedvariable")

        self.hl_addsaveclose.addWidget(self.btn_nedvariable)

        self.btn_close = QPushButton(NedDocxPdfDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedDocxPdfDialogWindow)

        QMetaObject.connectSlotsByName(NedDocxPdfDialogWindow)
    # setupUi

    def retranslateUi(self, NedDocxPdfDialogWindow):
        NedDocxPdfDialogWindow.setWindowTitle(QCoreApplication.translate("NedDocxPdfDialogWindow", u"Dialog", None))
        self.label_typefile.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0438\u043f \u0444\u0430\u0439\u043b\u0430</span></p></body></html>", None))
        self.label_document.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"<html><head/><body><p>\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442</p></body></html>", None))
        self.btn_select.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c docx", None))
        self.btn_open_docx.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0438 docx", None))
        self.label_file.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b", None))
        self.label_variables.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0439\u0434\u0435\u043d\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435</p></body></html>", None))
        self.btn_findvariables.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u041f\u043e\u0438\u0441\u043a \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445 \u0432 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u043c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0435", None))
        self.btn_nedvariable.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedDocxPdfDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nedimagevariable_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedimagevariable.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_NedImageVariable(object):
    def setupUi(self, NedImageVariable):
        if not NedImageVariable.objectName():
            NedImageVariable.setObjectName(u"NedImageVariable")
        NedImageVariable.resize(516, 173)
        self.verticalLayout = QVBoxLayout(NedImageVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title_units = QLabel(NedImageVariable)
        self.title_units.setObjectName(u"title_units")

        self.verticalLayout.addWidget(self.title_units)

        self.combox_units = QComboBox(NedImageVariable)
        self.combox_units.setObjectName(u"combox_units")

        self.verticalLayout.addWidget(self.combox_units)

        self.title_sms = QLabel(NedImageVariable)
        self.title_sms.setObjectName(u"title_sms")

        self.verticalLayout.addWidget(self.title_sms)

        self.combox_sms = QComboBox(NedImageVariable)
        self.combox_sms.setObjectName(u"combox_sms")

        self.verticalLayout.addWidget(self.combox_sms)

        self.title_wh = QLabel(NedImageVariable)
        self.title_wh.setObjectName(u"title_wh")

        self.verticalLayout.addWidget(self.title_wh)

        self.hl_width = QHBoxLayout()
        self.hl_width.setObjectName(u"hl_width")
        self.label = QLabel(NedImageVariable)
        self.label.setObjectName(u"label")

        self.hl_width.addWidget(self.label)

        self.dsb_height = QDoubleSpinBox(NedImageVariable)
        self.dsb_height.setObjectName(u"dsb_height")
        self.dsb_height.setMaximum(99999.990000000005239)

        self.hl_width.addWidget(self.dsb_height)

        self.label_2 = QLabel(NedImageVariable)
        self.label_2.setObjectName(u"label_2")

        self.hl_width.addWidget(self.label_2)

        self.dsb_width = QDoubleSpinBox(NedImageVariable)
        self.dsb_width.setObjectName(u"dsb_width")
        self.dsb_width.setMaximum(99999.990000000005239)

        self.hl_width.addWidget(self.dsb_width)

        self.hl_width.setStretch(1, 1)
        self.hl_width.setStretch(3, 1)

        self.verticalLayout.addLayout(self.hl_width)

        self.line = QFrame(NedImageVariable)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(NedImageVariable)

        QMetaObject.connectSlotsByName(NedImageVariable)
    # setupUi

    def retranslateUi(self, NedImageVariable):
        NedImageVariable.setWindowTitle(QCoreApplication.translate("NedImageVariable", u"Form", None))
        self.title_units.setText(QCoreApplication.translate("NedImageVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0415\u0434\u0438\u043d\u0438\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f</span></p></body></html>", None))
        self.title_sms.setText(QCoreApplication.translate("NedImageVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u041c\u0435\u0442\u043e\u0434 \u0440\u0435\u0441\u0430\u0439\u0437\u0430 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f</span></p></body></html>", None))
        self.title_wh.setText(QCoreApplication.translate("NedImageVariable", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0428\u0438\u0440\u0438\u043d\u0430 \u0438 \u0432\u044b\u0441\u043e\u0442\u0430</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("NedImageVariable", u"\u0428:", None))
        self.label_2.setText(QCoreApplication.translate("NedImageVariable", u"\u0412:", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nednodedialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nednodedialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_NedNodeDialogWindow(object):
    def setupUi(self, NedNodeDialogWindow):
        if not NedNodeDialogWindow.objectName():
            NedNodeDialogWindow.setObjectName(u"NedNodeDialogWindow")
        NedNodeDialogWindow.resize(700, 133)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NedNodeDialogWindow.sizePolicy().hasHeightForWidth())
        NedNodeDialogWindow.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(NedNodeDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.namenode = QLabel(NedNodeDialogWindow)
        self.namenode.setObjectName(u"namenode")
        self.namenode.setMinimumSize(QSize(0, 0))
        self.namenode.setMaximumSize(QSize(16777215, 16))
        self.namenode.setStyleSheet(u"font-weight: bold;")
        self.namenode.setTextFormat(Qt.AutoText)
        self.namenode.setScaledContents(False)

        self.verticalLayout.addWidget(self.namenode)

        self.lineedit_namenode = QLineEdit(NedNodeDialogWindow)
        self.lineedit_namenode.setObjectName(u"lineedit_namenode")

        self.verticalLayout.addWidget(self.lineedit_namenode)

        self.hl_placement = QHBoxLayout()
        self.hl_placement.setObjectName(u"hl_placement")
        self.label_placement = QLabel(NedNodeDialogWindow)
        self.label_placement.setObjectName(u"label_placement")

        self.hl_placement.addWidget(self.label_placement)

        self.combox_parent = QComboBox(NedNodeDialogWindow)
        self.combox_parent.setObjectName(u"combox_parent")

        self.hl_placement.addWidget(self.combox_parent)

        self.combox_neighboor = QComboBox(NedNodeDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_placement.addWidget(self.combox_neighboor)

        self.hl_placement.setStretch(1, 1)
        self.hl_placement.setStretch(2, 1)

        self.verticalLayout.addLayout(self.hl_placement)

        self.line = QFrame(NedNodeDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nesvariable = QPushButton(NedNodeDialogWindow)
        self.btn_nesvariable.setObjectName(u"btn_nesvariable")

        self.hl_addsaveclose.addWidget(self.btn_nesvariable)

        self.btn_close = QPushButton(NedNodeDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedNodeDialogWindow)

        QMetaObject.connectSlotsByName(NedNodeDialogWindow)
    # setupUi

    def retranslateUi(self, NedNodeDialogWindow):
        NedNodeDialogWindow.setWindowTitle(QCoreApplication.translate("NedNodeDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0432\u0435\u0440\u0448\u0438\u043d\u044b", None))
        self.namenode.setText(QCoreApplication.translate("NedNodeDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ...</p></body></html>", None))
        self.lineedit_namenode.setText("")
        self.label_placement.setText(QCoreApplication.translate("NedNodeDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u0432\u043d\u0443\u0442\u0440\u0438 ", None))
        self.btn_nesvariable.setText(QCoreApplication.translate("NedNodeDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedNodeDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nedpagedialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedpagedialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_NedPageDialogWindow(object):
    def setupUi(self, NedPageDialogWindow):
        if not NedPageDialogWindow.objectName():
            NedPageDialogWindow.setObjectName(u"NedPageDialogWindow")
        NedPageDialogWindow.resize(500, 603)
        self.verticalLayout = QVBoxLayout(NedPageDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.label_namepage = QLabel(NedPageDialogWindow)
        self.label_namepage.setObjectName(u"label_namepage")
        self.label_namepage.setMinimumSize(QSize(0, 0))
        self.label_namepage.setMaximumSize(QSize(16777215, 16))
        self.label_namepage.setStyleSheet(u"font-weight: bold;")
        self.label_namepage.setTextFormat(Qt.AutoText)
        self.label_namepage.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_namepage)

        self.lineedit_namepage = QLineEdit(NedPageDialogWindow)
        self.lineedit_namepage.setObjectName(u"lineedit_namepage")

        self.verticalLayout.addWidget(self.lineedit_namepage)

        self.hl_order = QHBoxLayout()
        self.hl_order.setObjectName(u"hl_order")
        self.label_after = QLabel(NedPageDialogWindow)
        self.label_after.setObjectName(u"label_after")

        self.hl_order.addWidget(self.label_after)

        self.combox_neighboor = QComboBox(NedPageDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_order.addWidget(self.combox_neighboor)

        self.hl_order.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_order)

        self.line_2 = QFrame(NedPageDialogWindow)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.hl_copypage = QHBoxLayout()
        self.hl_copypage.setObjectName(u"hl_copypage")
        self.label_copyfrom = QLabel(NedPageDialogWindow)
        self.label_copyfrom.setObjectName(u"label_copyfrom")

        self.hl_copypage.addWidget(self.label_copyfrom)

        self.combox_pages = QComboBox(NedPageDialogWindow)
        self.combox_pages.setObjectName(u"combox_pages")

        self.hl_copypage.addWidget(self.combox_pages)

        self.hl_copypage.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_copypage)

        self.line_3 = QFrame(NedPageDialogWindow)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.label_document = QLabel(NedPageDialogWindow)
        self.label_document.setObjectName(u"label_document")
        self.label_document.setMinimumSize(QSize(0, 0))
        self.label_document.setMaximumSize(QSize(16777215, 16))
        self.label_document.setStyleSheet(u"font-weight: bold;")
        self.label_document.setTextFormat(Qt.AutoText)
        self.label_document.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_document)

        self.hl_select_open = QHBoxLayout()
        self.hl_select_open.setObjectName(u"hl_select_open")
        self.btn_select = QPushButton(NedPageDialogWindow)
        self.btn_select.setObjectName(u"btn_select")

        self.hl_select_open.addWidget(self.btn_select)

        self.btn_open_docx = QPushButton(NedPageDialogWindow)
        self.btn_open_docx.setObjectName(u"btn_open_docx")

        self.hl_select_open.addWidget(self.btn_open_docx)


        self.verticalLayout.addLayout(self.hl_select_open)

        self.label_file = QLabel(NedPageDialogWindow)
        self.label_file.setObjectName(u"label_file")
        self.label_file.setStyleSheet(u"font-style: italic;")

        self.verticalLayout.addWidget(self.label_file)

        self.label_variables = QLabel(NedPageDialogWindow)
        self.label_variables.setObjectName(u"label_variables")
        self.label_variables.setMinimumSize(QSize(0, 0))
        self.label_variables.setMaximumSize(QSize(16777215, 16))
        self.label_variables.setStyleSheet(u"font-weight: bold;")
        self.label_variables.setTextFormat(Qt.AutoText)
        self.label_variables.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_variables)

        self.tw_variables = QTableWidget(NedPageDialogWindow)
        self.tw_variables.setObjectName(u"tw_variables")

        self.verticalLayout.addWidget(self.tw_variables)

        self.btn_findvariables = QPushButton(NedPageDialogWindow)
        self.btn_findvariables.setObjectName(u"btn_findvariables")

        self.verticalLayout.addWidget(self.btn_findvariables)

        self.line = QFrame(NedPageDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nedvariable = QPushButton(NedPageDialogWindow)
        self.btn_nedvariable.setObjectName(u"btn_nedvariable")

        self.hl_addsaveclose.addWidget(self.btn_nedvariable)

        self.btn_close = QPushButton(NedPageDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedPageDialogWindow)

        QMetaObject.connectSlotsByName(NedPageDialogWindow)
    # setupUi

    def retranslateUi(self, NedPageDialogWindow):
        NedPageDialogWindow.setWindowTitle(QCoreApplication.translate("NedPageDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b", None))
        self.label_namepage.setText(QCoreApplication.translate("NedPageDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b</p></body></html>", None))
        self.lineedit_namepage.setText("")
        self.label_after.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435 ", None))
        self.label_copyfrom.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u0441 ", None))
        self.label_document.setText(QCoreApplication.translate("NedPageDialogWindow", u"<html><head/><body><p>\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442 (docx \u0438\u043b\u0438 pdf)</p></body></html>", None))
        self.btn_select.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.btn_open_docx.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0438 docx", None))
        self.label_file.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u0424\u0430\u0439\u043b \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d", None))
        self.label_variables.setText(QCoreApplication.translate("NedPageDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0439\u0434\u0435\u043d\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435 (\u0434\u043b\u044f docx)</p></body></html>", None))
        self.btn_findvariables.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u041f\u043e\u0438\u0441\u043a \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445 \u0432 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u043c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0435", None))
        self.btn_nedvariable.setText(QCoreApplication.translate("NedPageDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedPageDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nedrowcoldialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedrowcoldialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_NedRowcolDialogWindow(object):
    def setupUi(self, NedRowcolDialogWindow):
        if not NedRowcolDialogWindow.objectName():
            NedRowcolDialogWindow.setObjectName(u"NedRowcolDialogWindow")
        NedRowcolDialogWindow.resize(500, 183)
        NedRowcolDialogWindow.setMaximumSize(QSize(16777215, 183))
        self.verticalLayout = QVBoxLayout(NedRowcolDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.label_attr = QLabel(NedRowcolDialogWindow)
        self.label_attr.setObjectName(u"label_attr")

        self.verticalLayout.addWidget(self.label_attr)

        self.lineedit_attr = QLineEdit(NedRowcolDialogWindow)
        self.lineedit_attr.setObjectName(u"lineedit_attr")

        self.verticalLayout.addWidget(self.lineedit_attr)

        self.label_rowcol = QLabel(NedRowcolDialogWindow)
        self.label_rowcol.setObjectName(u"label_rowcol")
        self.label_rowcol.setMinimumSize(QSize(0, 0))
        self.label_rowcol.setMaximumSize(QSize(16777215, 16))
        self.label_rowcol.setStyleSheet(u"font-weight: bold;")
        self.label_rowcol.setTextFormat(Qt.AutoText)
        self.label_rowcol.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_rowcol)

        self.lineedit_rowcoltitle = QLineEdit(NedRowcolDialogWindow)
        self.lineedit_rowcoltitle.setObjectName(u"lineedit_rowcoltitle")

        self.verticalLayout.addWidget(self.lineedit_rowcoltitle)

        self.hl_placement = QHBoxLayout()
        self.hl_placement.setObjectName(u"hl_placement")
        self.label_placement = QLabel(NedRowcolDialogWindow)
        self.label_placement.setObjectName(u"label_placement")

        self.hl_placement.addWidget(self.label_placement)

        self.combox_neighboor = QComboBox(NedRowcolDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_placement.addWidget(self.combox_neighboor)

        self.hl_placement.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_placement)

        self.line = QFrame(NedRowcolDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nesvariable = QPushButton(NedRowcolDialogWindow)
        self.btn_nesvariable.setObjectName(u"btn_nesvariable")

        self.hl_addsaveclose.addWidget(self.btn_nesvariable)

        self.btn_close = QPushButton(NedRowcolDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedRowcolDialogWindow)

        QMetaObject.connectSlotsByName(NedRowcolDialogWindow)
    # setupUi

    def retranslateUi(self, NedRowcolDialogWindow):
        NedRowcolDialogWindow.setWindowTitle(QCoreApplication.translate("NedRowcolDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u0442\u0440\u043e\u043a\u0438/\u0441\u0442\u043e\u043b\u0431\u0446\u0430 \u0442\u0430\u0431\u043b\u0438\u0446\u044b", None))
        self.label_attr.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0410\u0442\u0440\u0438\u0431\u0443\u0442 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439</span></p></body></html>", None))
        self.label_rowcol.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ...</p></body></html>", None))
        self.lineedit_rowcoltitle.setText("")
        self.label_placement.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435 ", None))
        self.btn_nesvariable.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedRowcolDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nedtablevariable_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedtablevariable.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_NedTableVariable(object):
    def setupUi(self, NedTableVariable):
        if not NedTableVariable.objectName():
            NedTableVariable.setObjectName(u"NedTableVariable")
        NedTableVariable.resize(512, 254)
        self.verticalLayout = QVBoxLayout(NedTableVariable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_rowcol = QLabel(NedTableVariable)
        self.label_rowcol.setObjectName(u"label_rowcol")
        self.label_rowcol.setMinimumSize(QSize(0, 0))
        self.label_rowcol.setMaximumSize(QSize(16777215, 16))
        self.label_rowcol.setStyleSheet(u"font-weight: bold;")
        self.label_rowcol.setTextFormat(Qt.AutoText)
        self.label_rowcol.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_rowcol)

        self.lw_attrs = QListWidget(NedTableVariable)
        self.lw_attrs.setObjectName(u"lw_attrs")

        self.verticalLayout.addWidget(self.lw_attrs)

        self.btn_addrowcol = QPushButton(NedTableVariable)
        self.btn_addrowcol.setObjectName(u"btn_addrowcol")

        self.verticalLayout.addWidget(self.btn_addrowcol)

        self.line = QFrame(NedTableVariable)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)


        self.retranslateUi(NedTableVariable)

        QMetaObject.connectSlotsByName(NedTableVariable)
    # setupUi

    def retranslateUi(self, NedTableVariable):
        NedTableVariable.setWindowTitle(QCoreApplication.translate("NedTableVariable", u"Form", None))
        self.label_rowcol.setText(QCoreApplication.translate("NedTableVariable", u"<html><head/><body><p>\u0421\u0442\u0440\u043e\u043a\u0438/\u0441\u0442\u043e\u043b\u0431\u0446\u044b</p></body></html>", None))
        self.btn_addrowcol.setText(QCoreApplication.translate("NedTableVariable", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443/\u0441\u0442\u043e\u043b\u0431\u0435\u0446", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nedtemplatedialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedtemplatedialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_NedTemplateDialogWindow(object):
    def setupUi(self, NedTemplateDialogWindow):
        if not NedTemplateDialogWindow.objectName():
            NedTemplateDialogWindow.setObjectName(u"NedTemplateDialogWindow")
        NedTemplateDialogWindow.resize(500, 168)
        self.verticalLayout = QVBoxLayout(NedTemplateDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.label_nametemplate = QLabel(NedTemplateDialogWindow)
        self.label_nametemplate.setObjectName(u"label_nametemplate")
        self.label_nametemplate.setMinimumSize(QSize(0, 0))
        self.label_nametemplate.setMaximumSize(QSize(16777215, 16))
        self.label_nametemplate.setStyleSheet(u"font-weight: bold;")
        self.label_nametemplate.setTextFormat(Qt.AutoText)
        self.label_nametemplate.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_nametemplate)

        self.lineedit_nametemplate = QLineEdit(NedTemplateDialogWindow)
        self.lineedit_nametemplate.setObjectName(u"lineedit_nametemplate")

        self.verticalLayout.addWidget(self.lineedit_nametemplate)

        self.line_2 = QFrame(NedTemplateDialogWindow)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.hl_copytemplate = QHBoxLayout()
        self.hl_copytemplate.setObjectName(u"hl_copytemplate")
        self.label_copyfrom = QLabel(NedTemplateDialogWindow)
        self.label_copyfrom.setObjectName(u"label_copyfrom")

        self.hl_copytemplate.addWidget(self.label_copyfrom)

        self.combox_templates = QComboBox(NedTemplateDialogWindow)
        self.combox_templates.setObjectName(u"combox_templates")

        self.hl_copytemplate.addWidget(self.combox_templates)

        self.hl_copytemplate.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_copytemplate)

        self.checkbox_is_active = QCheckBox(NedTemplateDialogWindow)
        self.checkbox_is_active.setObjectName(u"checkbox_is_active")

        self.verticalLayout.addWidget(self.checkbox_is_active)

        self.line = QFrame(NedTemplateDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nesvariable = QPushButton(NedTemplateDialogWindow)
        self.btn_nesvariable.setObjectName(u"btn_nesvariable")

        self.hl_addsaveclose.addWidget(self.btn_nesvariable)

        self.btn_close = QPushButton(NedTemplateDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)


        self.retranslateUi(NedTemplateDialogWindow)

        QMetaObject.connectSlotsByName(NedTemplateDialogWindow)
    # setupUi

    def retranslateUi(self, NedTemplateDialogWindow):
        NedTemplateDialogWindow.setWindowTitle(QCoreApplication.translate("NedTemplateDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u0430", None))
        self.label_nametemplate.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ...</p></body></html>", None))
        self.lineedit_nametemplate.setText("")
        self.label_copyfrom.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u0441 ", None))
        self.checkbox_is_active.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u043c \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u043c \u0444\u043e\u0440\u043c\u044b", None))
        self.btn_nesvariable.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"...", None))
        self.btn_close.setText(QCoreApplication.translate("NedTemplateDialogWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nedvariabledialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nedvariabledialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_NedVariableDialogWindow(object):
    def setupUi(self, NedVariableDialogWindow):
        if not NedVariableDialogWindow.objectName():
            NedVariableDialogWindow.setObjectName(u"NedVariableDialogWindow")
        NedVariableDialogWindow.resize(500, 289)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NedVariableDialogWindow.sizePolicy().hasHeightForWidth())
        NedVariableDialogWindow.setSizePolicy(sizePolicy)
        NedVariableDialogWindow.setBaseSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(NedVariableDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.namevariable = QLabel(NedVariableDialogWindow)
        self.namevariable.setObjectName(u"namevariable")
        self.namevariable.setMinimumSize(QSize(0, 0))
        self.namevariable.setMaximumSize(QSize(16777215, 16))
        self.namevariable.setStyleSheet(u"font-weight: bold;")
        self.namevariable.setTextFormat(Qt.AutoText)
        self.namevariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.namevariable)

        self.lineedit_namevariable = QLineEdit(NedVariableDialogWindow)
        self.lineedit_namevariable.setObjectName(u"lineedit_namevariable")

        self.verticalLayout.addWidget(self.lineedit_namevariable)

        self.titlevariable = QLabel(NedVariableDialogWindow)
        self.titlevariable.setObjectName(u"titlevariable")
        self.titlevariable.setMinimumSize(QSize(0, 0))
        self.titlevariable.setMaximumSize(QSize(16777215, 16))
        self.titlevariable.setStyleSheet(u"font-weight: bold;")
        self.titlevariable.setTextFormat(Qt.AutoText)
        self.titlevariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.titlevariable)

        self.lineedit_titlevariable = QLineEdit(NedVariableDialogWindow)
        self.lineedit_titlevariable.setObjectName(u"lineedit_titlevariable")

        self.verticalLayout.addWidget(self.lineedit_titlevariable)

        self.hl_placement = QHBoxLayout()
        self.hl_placement.setObjectName(u"hl_placement")
        self.label_placement = QLabel(NedVariableDialogWindow)
        self.label_placement.setObjectName(u"label_placement")

        self.hl_placement.addWidget(self.label_placement)

        self.combox_neighboor = QComboBox(NedVariableDialogWindow)
        self.combox_neighboor.setObjectName(u"combox_neighboor")

        self.hl_placement.addWidget(self.combox_neighboor)

        self.hl_placement.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_placement)

        self.line_2 = QFrame(NedVariableDialogWindow)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.hl_copyvariable = QHBoxLayout()
        self.hl_copyvariable.setObjectName(u"hl_copyvariable")
        self.label_copyfrom = QLabel(NedVariableDialogWindow)
        self.label_copyfrom.setObjectName(u"label_copyfrom")

        self.hl_copyvariable.addWidget(self.label_copyfrom)

        self.combox_copyvariables = QComboBox(NedVariableDialogWindow)
        self.combox_copyvariables.setObjectName(u"combox_copyvariables")

        self.hl_copyvariable.addWidget(self.combox_copyvariables)

        self.hl_copyvariable.setStretch(1, 1)

        self.verticalLayout.addLayout(self.hl_copyvariable)

        self.line_3 = QFrame(NedVariableDialogWindow)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.typevariable = QLabel(NedVariableDialogWindow)
        self.typevariable.setObjectName(u"typevariable")
        self.typevariable.setMinimumSize(QSize(0, 0))
        self.typevariable.setMaximumSize(QSize(16777215, 16))
        self.typevariable.setStyleSheet(u"font-weight: bold;")
        self.typevariable.setTextFormat(Qt.AutoText)
        self.typevariable.setScaledContents(False)

        self.verticalLayout.addWidget(self.typevariable)

        self.combox_typevariable = QComboBox(NedVariableDialogWindow)
        self.combox_typevariable.setObjectName(u"combox_typevariable")

        self.verticalLayout.addWidget(self.combox_typevariable)

        self.line = QFrame(NedVariableDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.vbl_additional_info = QVBoxLayout()
        self.vbl_additional_info.setSpacing(0)
        self.vbl_additional_info.setObjectName(u"vbl_additional_info")

        self.verticalLayout.addLayout(self.vbl_additional_info)

        self.hl_addsaveclose = QHBoxLayout()
        self.hl_addsaveclose.setObjectName(u"hl_addsaveclose")
        self.btn_nesvariable = QPushButton(NedVariableDialogWindow)
        self.btn_nesvariable.setObjectName(u"btn_nesvariable")

        self.hl_addsaveclose.addWidget(self.btn_nesvariable)

        self.btn_close = QPushButton(NedVariableDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_addsaveclose.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.hl_addsaveclose)

        self.verticalLayout.setStretch(11, 1)

        self.retranslateUi(NedVariableDialogWindow)

        QMetaObject.connectSlotsByName(NedVariableDialogWindow)
    # setupUi

    def retranslateUi(self, NedVariableDialogWindow):
        NedVariableDialogWindow.setWindowTitle(QCoreApplication.translate("NedVariableDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439", None))
        self.namevariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"<html><head/><body><p>\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f</p></body></html>", None))
        self.lineedit_namevariable.setText("")
        self.titlevariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439</p></body></html>", None))
        self.lineedit_titlevariable.setText("")
        self.label_placement.setText(QCoreApplication.translate("NedVariableDialogWindow", u"\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435", None))
        self.label_copyfrom.setText(QCoreApplication.translate("NedVariableDialogWindow", u"\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u0441 ", None))
        self.typevariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"<html><head/><body><p>\u0422\u0438\u043f \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439</p></body></html>", None))
        self.btn_nesvariable.setText(QCoreApplication.translate("NedVariableDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e", None))
        self.btn_close.setText(QCoreApplication.translate("NedVariableDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\nodeseditordialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nodeseditordialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QHeaderView, QPushButton, QSizePolicy, QSpacerItem,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_NodesEditorDialogWindow(object):
    def setupUi(self, NodesEditorDialogWindow):
        if not NodesEditorDialogWindow.objectName():
            NodesEditorDialogWindow.setObjectName(u"NodesEditorDialogWindow")
        NodesEditorDialogWindow.resize(700, 500)
        self.verticalLayout_2 = QVBoxLayout(NodesEditorDialogWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.hl_main = QHBoxLayout()
        self.hl_main.setObjectName(u"hl_main")
        self.tw_nodes = QTreeWidget(NodesEditorDialogWindow)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_nodes.setHeaderItem(__qtreewidgetitem)
        self.tw_nodes.setObjectName(u"tw_nodes")

        self.hl_main.addWidget(self.tw_nodes)

        self.vl_buttons = QVBoxLayout()
        self.vl_buttons.setObjectName(u"vl_buttons")
        self.btn_add_form = QPushButton(NodesEditorDialogWindow)
        self.btn_add_form.setObjectName(u"btn_add_form")

        self.vl_buttons.addWidget(self.btn_add_form)

        self.btn_add_group = QPushButton(NodesEditorDialogWindow)
        self.btn_add_group.setObjectName(u"btn_add_group")

        self.vl_buttons.addWidget(self.btn_add_group)

        self.btn_edit = QPushButton(NodesEditorDialogWindow)
        self.btn_edit.setObjectName(u"btn_edit")

        self.vl_buttons.addWidget(self.btn_edit)

        self.btn_delete_item = QPushButton(NodesEditorDialogWindow)
        self.btn_delete_item.setObjectName(u"btn_delete_item")

        self.vl_buttons.addWidget(self.btn_delete_item)

        self.vert_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vl_buttons.addItem(self.vert_spacer)


        self.hl_main.addLayout(self.vl_buttons)


        self.verticalLayout_2.addLayout(self.hl_main)

        self.line = QFrame(NodesEditorDialogWindow)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.hl_saveclose = QHBoxLayout()
        self.hl_saveclose.setObjectName(u"hl_saveclose")
        self.btn_close = QPushButton(NodesEditorDialogWindow)
        self.btn_close.setObjectName(u"btn_close")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon)

        self.hl_saveclose.addWidget(self.btn_close)


        self.verticalLayout_2.addLayout(self.hl_saveclose)


        self.retranslateUi(NodesEditorDialogWindow)

        QMetaObject.connectSlotsByName(NodesEditorDialogWindow)
    # setupUi

    def retranslateUi(self, NodesEditorDialogWindow):
        NodesEditorDialogWindow.setWindowTitle(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u043e\u0441\u0442\u0430\u0432\u0430 \u0418\u0414", None))
        self.btn_add_form.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0444\u043e\u0440\u043c\u0443", None))
        self.btn_add_group.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0433\u0440\u0443\u043f\u043f\u0443", None))
        self.btn_edit.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.btn_delete_item.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None))
        self.btn_close.setText(QCoreApplication.translate("NodesEditorDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\pdfwidget_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pdfwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QWidget)

class Ui_PdfWidget(object):
    def setupUi(self, PdfWidget):
        if not PdfWidget.objectName():
            PdfWidget.setObjectName(u"PdfWidget")
        PdfWidget.resize(300, 240)
        self.horizontalLayout = QHBoxLayout(PdfWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pdf_view = QPdfView(PdfWidget)
        self.pdf_view.setObjectName(u"pdf_view")

        self.horizontalLayout.addWidget(self.pdf_view)


        self.retranslateUi(PdfWidget)

        QMetaObject.connectSlotsByName(PdfWidget)
    # setupUi

    def retranslateUi(self, PdfWidget):
        PdfWidget.setWindowTitle(QCoreApplication.translate("PdfWidget", u"Form", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\templateslistsialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'templateslistsialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget)
import resources_rc

class Ui_TemplatesListDialogWindow(object):
    def setupUi(self, TemplatesListDialogWindow):
        if not TemplatesListDialogWindow.objectName():
            TemplatesListDialogWindow.setObjectName(u"TemplatesListDialogWindow")
        TemplatesListDialogWindow.resize(700, 383)
        TemplatesListDialogWindow.setMinimumSize(QSize(500, 0))
        TemplatesListDialogWindow.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(TemplatesListDialogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_form = QLabel(TemplatesListDialogWindow)
        self.label_form.setObjectName(u"label_form")

        self.verticalLayout.addWidget(self.label_form)

        self.combox_forms = QComboBox(TemplatesListDialogWindow)
        self.combox_forms.setObjectName(u"combox_forms")

        self.verticalLayout.addWidget(self.combox_forms)

        self.splitter = QSplitter(TemplatesListDialogWindow)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vl_templates = QVBoxLayout(self.verticalLayoutWidget)
        self.vl_templates.setObjectName(u"vl_templates")
        self.vl_templates.setContentsMargins(0, 0, 0, 0)
        self.label_template = QLabel(self.verticalLayoutWidget)
        self.label_template.setObjectName(u"label_template")

        self.vl_templates.addWidget(self.label_template)

        self.lw_templates = QListWidget(self.verticalLayoutWidget)
        self.lw_templates.setObjectName(u"lw_templates")

        self.vl_templates.addWidget(self.lw_templates)

        self.btn_add_template = QPushButton(self.verticalLayoutWidget)
        self.btn_add_template.setObjectName(u"btn_add_template")

        self.vl_templates.addWidget(self.btn_add_template)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.vl_pages = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vl_pages.setObjectName(u"vl_pages")
        self.vl_pages.setContentsMargins(0, 0, 0, 0)
        self.label_pages = QLabel(self.verticalLayoutWidget_2)
        self.label_pages.setObjectName(u"label_pages")

        self.vl_pages.addWidget(self.label_pages)

        self.lw_pages = QListWidget(self.verticalLayoutWidget_2)
        self.lw_pages.setObjectName(u"lw_pages")

        self.vl_pages.addWidget(self.lw_pages)

        self.btn_add_page = QPushButton(self.verticalLayoutWidget_2)
        self.btn_add_page.setObjectName(u"btn_add_page")

        self.vl_pages.addWidget(self.btn_add_page)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout.addWidget(self.splitter)

        self.line = QFrame(TemplatesListDialogWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.btn_close = QPushButton(TemplatesListDialogWindow)
        self.btn_close.setObjectName(u"btn_close")

        self.verticalLayout.addWidget(self.btn_close)

        self.verticalLayout.setStretch(2, 3)

        self.retranslateUi(TemplatesListDialogWindow)

        QMetaObject.connectSlotsByName(TemplatesListDialogWindow)
    # setupUi

    def retranslateUi(self, TemplatesListDialogWindow):
        TemplatesListDialogWindow.setWindowTitle(QCoreApplication.translate("TemplatesListDialogWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432", None))
        self.label_form.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0424\u043e\u0440\u043c\u0430</span></p></body></html>", None))
        self.label_template.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0428\u0430\u0431\u043b\u043e\u043d\u044b</span></p></body></html>", None))
        self.btn_add_template.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d", None))
        self.label_pages.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b</span></p></body></html>", None))
        self.btn_add_page.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443", None))
        self.btn_close.setText(QCoreApplication.translate("TemplatesListDialogWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\variableslistdialogwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'variableslistdialogwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QHeaderView, QLayout, QPushButton, QSizePolicy,
    QSplitter, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_VariablesListDialog(object):
    def setupUi(self, VariablesListDialog):
        if not VariablesListDialog.objectName():
            VariablesListDialog.setObjectName(u"VariablesListDialog")
        VariablesListDialog.setWindowModality(Qt.ApplicationModal)
        VariablesListDialog.resize(1250, 720)
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        VariablesListDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(VariablesListDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabwidget = QTabWidget(VariablesListDialog)
        self.tabwidget.setObjectName(u"tabwidget")
        self.tab_project = QWidget()
        self.tab_project.setObjectName(u"tab_project")
        self.verticalLayout_4 = QVBoxLayout(self.tab_project)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_create_variable = QPushButton(self.tab_project)
        self.btn_create_variable.setObjectName(u"btn_create_variable")

        self.verticalLayout_4.addWidget(self.btn_create_variable)

        self.splitter_project = QSplitter(self.tab_project)
        self.splitter_project.setObjectName(u"splitter_project")
        self.splitter_project.setOrientation(Qt.Horizontal)
        self.table_editor_project_variables = QTableWidget(self.splitter_project)
        self.table_editor_project_variables.setObjectName(u"table_editor_project_variables")
        self.splitter_project.addWidget(self.table_editor_project_variables)
        self.table_project_variables = QTableWidget(self.splitter_project)
        self.table_project_variables.setObjectName(u"table_project_variables")
        self.splitter_project.addWidget(self.table_project_variables)

        self.verticalLayout_4.addWidget(self.splitter_project)

        self.verticalLayout_4.setStretch(1, 1)
        self.tabwidget.addTab(self.tab_project, "")
        self.tab_group = QWidget()
        self.tab_group.setObjectName(u"tab_group")
        self.verticalLayout_3 = QVBoxLayout(self.tab_group)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.combox_groups = QComboBox(self.tab_group)
        self.combox_groups.setObjectName(u"combox_groups")

        self.verticalLayout_3.addWidget(self.combox_groups)

        self.splitter_group = QSplitter(self.tab_group)
        self.splitter_group.setObjectName(u"splitter_group")
        self.splitter_group.setMidLineWidth(0)
        self.splitter_group.setOrientation(Qt.Horizontal)
        self.table_editor_group_variables = QTableWidget(self.splitter_group)
        self.table_editor_group_variables.setObjectName(u"table_editor_group_variables")
        self.splitter_group.addWidget(self.table_editor_group_variables)
        self.table_group_variables = QTableWidget(self.splitter_group)
        self.table_group_variables.setObjectName(u"table_group_variables")
        self.splitter_group.addWidget(self.table_group_variables)

        self.verticalLayout_3.addWidget(self.splitter_group)

        self.tabwidget.addTab(self.tab_group, "")
        self.tab_form_template_page = QWidget()
        self.tab_form_template_page.setObjectName(u"tab_form_template_page")
        self.verticalLayout_5 = QVBoxLayout(self.tab_form_template_page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.hl_combox = QHBoxLayout()
        self.hl_combox.setObjectName(u"hl_combox")
        self.hl_combox.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.combox_forms = QComboBox(self.tab_form_template_page)
        self.combox_forms.setObjectName(u"combox_forms")

        self.hl_combox.addWidget(self.combox_forms)

        self.combox_templates = QComboBox(self.tab_form_template_page)
        self.combox_templates.setObjectName(u"combox_templates")

        self.hl_combox.addWidget(self.combox_templates)

        self.combox_pages = QComboBox(self.tab_form_template_page)
        self.combox_pages.setObjectName(u"combox_pages")

        self.hl_combox.addWidget(self.combox_pages)


        self.verticalLayout_5.addLayout(self.hl_combox)

        self.splitter_ftp = QSplitter(self.tab_form_template_page)
        self.splitter_ftp.setObjectName(u"splitter_ftp")
        self.splitter_ftp.setOrientation(Qt.Horizontal)
        self.table_editor_ftp_variables = QTableWidget(self.splitter_ftp)
        self.table_editor_ftp_variables.setObjectName(u"table_editor_ftp_variables")
        self.splitter_ftp.addWidget(self.table_editor_ftp_variables)
        self.table_ftp_variables = QTableWidget(self.splitter_ftp)
        self.table_ftp_variables.setObjectName(u"table_ftp_variables")
        self.splitter_ftp.addWidget(self.table_ftp_variables)

        self.verticalLayout_5.addWidget(self.splitter_ftp)

        self.verticalLayout_5.setStretch(1, 1)
        self.tabwidget.addTab(self.tab_form_template_page, "")

        self.verticalLayout_2.addWidget(self.tabwidget)

        self.hl_buttons = QHBoxLayout()
        self.hl_buttons.setObjectName(u"hl_buttons")
        self.btn_save = QPushButton(VariablesListDialog)
        self.btn_save.setObjectName(u"btn_save")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_save.setIcon(icon1)

        self.hl_buttons.addWidget(self.btn_save)

        self.btn_close = QPushButton(VariablesListDialog)
        self.btn_close.setObjectName(u"btn_close")
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)

        self.hl_buttons.addWidget(self.btn_close)


        self.verticalLayout_2.addLayout(self.hl_buttons)


        self.retranslateUi(VariablesListDialog)

        self.tabwidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(VariablesListDialog)
    # setupUi

    def retranslateUi(self, VariablesListDialog):
        VariablesListDialog.setWindowTitle(QCoreApplication.translate("VariablesListDialog", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445 \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None))
        self.btn_create_variable.setText(QCoreApplication.translate("VariablesListDialog", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_project), QCoreApplication.translate("VariablesListDialog", u"\u041f\u0440\u043e\u0435\u043a\u0442", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_group), QCoreApplication.translate("VariablesListDialog", u"\u0413\u0440\u0443\u043f\u043f\u0430", None))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.tab_form_template_page), QCoreApplication.translate("VariablesListDialog", u"\u0424\u043e\u0440\u043c\u0430/\u0428\u0430\u0431\u043b\u043e\u043d/\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.btn_save.setText(QCoreApplication.translate("VariablesListDialog", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_close.setText(QCoreApplication.translate("VariablesListDialog", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi


``
### D:\vs_projects\auto-exec-doc\package\ui\__init__.py
``python

``
