from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QShortcut, QKeySequence, QAction
from PySide6.QtCore import QTimer

import package.ui.mainwindow_ui as mainwindow_ui

import package.components.dialogwindow.variableslistdialogwindow as variableslistdialogwindow
import package.components.dialogwindow.nodeseditordialogwindow as nodeseditordialogwindow
import package.components.dialogwindow.templateslistsialogwindow as templateslistsialogwindow

from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, osbm):
        self.__osbm = osbm
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        # config
        self.config()
        # настройка контроллеров
        self.config_controllers()
        # Подключаем действия
        self.connecting_actions()
        # Запускаем Common после инициализации QGuiApplication
        self.__osbm.obj_comwith.run()

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
        self.__osbm.obj_lwpt.connect_pages_template(
            self.ui.lw_pages_template
        )
        # настройка comboboxtemplates
        self.__osbm.obj_comt.connect_combox_templates(
            self.ui.combox_templates
        )
        # настройка inputforms
        self.__osbm.obj_saif.connect_inputforms(
            self.ui.scrollarea_inputforms, self.ui.scrollarea_inputforms_layout
        )
        # ПОДКЛЮЧИТЬ PDF
        self.__osbm.obj_pdfv.connect_pdfview(self.ui.widget_pdf_view)

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
        self.ui.action_new.triggered.connect(
            lambda: self.__osbm.obj_proj.new_project()
        )
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
        self.ui.action_zoomin.triggered.connect(
            lambda: self.__osbm.obj_pdfv.zoom_in()
        )
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

    def edit_variables(self):
        """Редактирование переменных."""
        self.__osbm.obj_logg.debug_logger("MainWindow edit_variables()")
        self.__osbm.obj_variablesldw = variableslistdialogwindow.VariablesListDialogWindow(
            self.__osbm
        )
        self.__osbm.obj_variablesldw.exec()
        self.update_main_window()

    def edit_templates(self):
        """Редактирование шаблонов."""
        self.__osbm.obj_logg.debug_logger("MainWindow edit_templates()")
        # TODO Закрыть документ, а иначе конфертер выдает ошибку
        self.__osbm.obj_templdw = templateslistsialogwindow.TemplatesListDialogWindow(
            self.__osbm
        )
        self.__osbm.obj_templdw.exec()
        self.update_main_window()

    def edit_structure_nodes(self):
        """Редактирование структуры узлов."""
        self.__osbm.obj_logg.debug_logger("MainWindow edit_structure_nodes()")
        self.__osbm.obj_nedw = nodeseditordialogwindow.NodesEditorDialogWindow(
            self.__osbm
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
        # self.__osbm.obj_pdfv.set_empty_pdf_view()
        # scrollarea_inputforms
        page = self.__osbm.obj_lwpt.get_page_by_current_item()
        self.__osbm.obj_saif.update_scrollarea(page)
        
        

    def update_menu_recent_projects(self):
        self.__osbm.obj_logg.debug_logger(
            "MainWindow update_menu_recent_projects()"
        )
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
