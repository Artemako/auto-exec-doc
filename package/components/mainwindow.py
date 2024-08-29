from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QShortcut, QKeySequence, QAction, Qt
from PySide6.QtCore import QTimer

import package.ui.mainwindow_ui as mainwindow_ui

import package.components.dialogwindow.variableslistdialogwindow as variableslistdialogwindow
import package.components.dialogwindow.nodeseditordialogwindow as nodeseditordialogwindow
import package.components.dialogwindow.templateslistsialogwindow as templateslistsialogwindow

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
        self.__osbm.obj_saif.connect_inputforms(
            self.ui.scrollarea_inputforms, self.ui.scrollarea_inputforms_layout
        )
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

    def edit_menu_item(self, type_edit, type_item):
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
        self.ui.action_zoomin.triggered.connect(lambda: self.__osbm.obj_pdfv.zoom_in())
        self.ui.action_zoomout.triggered.connect(
            lambda: self.__osbm.obj_pdfv.zoom_out()
        )
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
        self.ui.action_clear_trash.triggered.connect(lambda: self.clear_trash())

    def start_qt_actions(self):
        self.ui.action_new.setEnabled(True)
        self.ui.action_open.setEnabled(True)
        self.ui.action_save.setEnabled(False)
        self.ui.action_saveas.setEnabled(False)
        self.ui.action_export_to_pdf.setEnabled(False)
        self.ui.action_edit_variables.setEnabled(False)
        self.ui.action_edit_composition.setEnabled(False)
        self.ui.action_edit_templates.setEnabled(False)
        self.ui.action_zoomin.setEnabled(False)
        self.ui.action_zoomout.setEnabled(False)
        self.ui.action_zoomfitpage.setEnabled(False)
        self.ui.action_clear_trash.setEnabled(False)

    def enable_qt_actions(self):
        """
        Активирует кнопки в статусбаре при открытии проекта
        """
        self.ui.action_save.setEnabled(True)
        self.ui.action_saveas.setEnabled(True)
        self.ui.action_zoomin.setEnabled(True)
        self.ui.action_zoomout.setEnabled(True)
        self.ui.action_edit_variables.setEnabled(True)
        self.ui.action_edit_composition.setEnabled(True)
        self.ui.action_zoomfitpage.setEnabled(True)
        self.ui.action_export_to_pdf.setEnabled(True)
        self.ui.action_edit_templates.setEnabled(True)
        self.ui.action_clear_trash.setEnabled(True)

    def edit_variables(self, open_node=None, open_template=None, open_page=None):
        """Редактирование переменных."""
        self.__osbm.obj_logg.debug_logger("MainWindow edit_variables()")
        self.__osbm.obj_variablesldw = (
            variableslistdialogwindow.VariablesListDialogWindow(
                self.__osbm, open_node, open_template, open_page
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
        self.__osbm.obj_saif.update_scrollarea(page)

    def update_menu_recent_projects(self):
        self.__osbm.obj_logg.debug_logger("MainWindow update_menu_recent_projects()")
        self.ui.menu_recent_projects.clear()
        last_projects = self.__osbm.obj_setdb.get_last_projects()
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

    def clear_trash(self):
        self.__osbm.obj_logg.debug_logger("MainWindow clear_trash()")
        #
        self.__osbm.obj_dw.process_delete_trash_start()
        try:
            # временные файлы в temp
            self.__osbm.obj_film.clear_temp_folder(False)
            # временные файлы в проекте
            list_of_pages = self.__osbm.obj_prodb.get_all_pages()
            list_of_images = self.__osbm.obj_prodb.get_all_images()
            #
            list_of_docx_in_forms = self.__osbm.obj_film.get_list_of_docx_in_forms_folder()
            list_of_pdfs_in_pdfs = self.__osbm.obj_film.get_list_of_pdfs_in_pdfs_folder()
            list_of_images_in_images = self.__osbm.obj_film.get_list_of_images_in_images_folder()
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
            for image in list_of_images_in_images:
                if not active_images.get(image):
                    self.__osbm.obj_film.delete_image_from_project(
                        image
                    )
                    
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)
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
