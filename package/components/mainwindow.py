from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QShortcut, QKeySequence, QAction
from PySide6.QtCore import QTimer

import package.ui.mainwindow_ui as mainwindow_ui

import package.components.tagslistdialogwindow as tagslistdialogwindow
import package.components.nodeseditordialogwindow as nodeseditordialogwindow

from functools import partial


class MainWindow(QMainWindow):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        # config
        self.config()
        # настройка контроллеров
        self.config_controllers()
        # Подключаем действия
        self.connecting_actions()

    def config(self):
        self.__obs_manager.obj_l.debug_logger("IN config()")
        self.ui.centralwidget_splitter.setSizes([280, 460, 626])
        self.start_qt_actions()
        self.update_menu_recent_projects()

    def config_controllers(self):
        """
        Method to configure controllers.
        """
        self.__obs_manager.obj_l.debug_logger("IN config_controllers()")
        # настройка статус бара
        self.__obs_manager.obj_sb.connect_statusbar(self.ui.status_bar)
        # настройка structureexecdoc
        self.__obs_manager.obj_sed.connect_structureexecdoc(
            self.ui.treewidget_structure_execdoc, self.ui.title_structure_execdoc
        )
        # настройка pagestemplate
        self.__obs_manager.obj_pt.connect_pages_template(
            self.ui.listwidget_pages_template, self.ui.title_pages_template
        )
        # настройка inputforms
        self.__obs_manager.obj_sai.connect_inputforms(
            self.ui.scrollarea_inputforms, self.ui.scrollarea_inputforms_layout
        )
        # ПОДКЛЮЧИТЬ PDF
        self.__obs_manager.obj_pv.connect_pdfview(self.ui.widget_pdf_view)

    def clear_before_end(self):
        self.__obs_manager.obj_l.debug_logger("IN clear_before_end()")
        # удаление pdf из виджета pdfview
        self.__obs_manager.obj_pv.set_empty_pdf_view()
        # очистка временных файлов
        self.__obs_manager.obj_ffm.clear_temp_folder(True)

    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        self.__obs_manager.obj_l.debug_logger("IN connecting_actions()")
        self.ui.action_new.triggered.connect(
            lambda: self.__obs_manager.obj_p.new_project()
        )
        self.ui.action_open.triggered.connect(
            lambda: self.__obs_manager.obj_p.open_project()
        )
        self.ui.action_save.triggered.connect(
            lambda: self.__obs_manager.obj_p.save_project()
        )
        self.ui.action_saveas.triggered.connect(
            lambda: self.__obs_manager.obj_p.saveas_project()
        )
        self.ui.action_export_to_pdf.triggered.connect(
            lambda: self.__obs_manager.obj_p.export_to_pdf()
        )
        self.ui.action_zoomin.triggered.connect(
            lambda: self.__obs_manager.obj_pv.zoom_in()
        )
        self.ui.action_zoomout.triggered.connect(
            lambda: self.__obs_manager.obj_pv.zoom_out()
        )
        self.ui.action_zoomfitpage.triggered.connect(
            lambda checked: self.__obs_manager.obj_pv.set_zoom_to_fit_width()
            if checked
            else self.__obs_manager.obj_pv.set_zoom_custom()
        )

        # TODO Добавить активности для редактирования
        self.ui.action_edit_tags.triggered.connect(lambda: self.edit_tags())
        # self.ui.action_edit_templates.triggered.connect(lambda: self.__obs_manager.obj_p.edit_templates())
        self.ui.action_edit_composition.triggered.connect(
            lambda: self.edit_composition()
        )

        # shortcut = QShortcut(QKeySequence("R"), self)
        # shortcut.activated.connect(lambda: self.__obs_manager.obj_pdf_view.set_empty_pdf_view())

    def start_qt_actions(self):
        self.ui.action_new.setEnabled(True)
        self.ui.action_open.setEnabled(True)
        self.ui.action_save.setEnabled(False)
        self.ui.action_saveas.setEnabled(False)
        self.ui.action_export_to_pdf.setEnabled(False)
        self.ui.action_edit_tags.setEnabled(False)
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
        self.ui.action_edit_tags.setEnabled(True)
        self.ui.action_edit_composition.setEnabled(True)
        self.ui.action_zoomfitpage.setEnabled(True)
        self.ui.action_export_to_pdf.setEnabled(True)
        self.ui.action_edit_templates.setEnabled(True)

    def get_view_height(self):
        return self.ui.widget_pdf_view.verticalScrollBar().value()

    def set_view_height(self, value):
        self.ui.widget_pdf_view.verticalScrollBar().setValue(value)

    def edit_tags(self):
        """Редактирование тегов."""
        self.__obs_manager.obj_l.debug_logger("IN edit_tags()")
        self.__obs_manager.obj_tldw = tagslistdialogwindow.TagsListDialogWindow(
            self.__obs_manager
        )
        self.__obs_manager.obj_tldw.exec()
        # обновить скроллвью после изменения тегов
        page = self.__obs_manager.obj_pt.get_page_by_current_item()
        if page is not None:
            self.__obs_manager.obj_sai.update_scrollarea(page)

    def edit_composition(self):
        """Редактирование композиции."""
        self.__obs_manager.obj_l.debug_logger("IN edit_composition()")
        self.__obs_manager.obj_tcdw = nodeseditordialogwindow.NodesEditorDialogWindow(
            self.__obs_manager
        )
        self.__obs_manager.obj_tcdw.exec()
        # TODO ??? обновить treewidget_structure_execdoc
        self.__obs_manager.obj_sed.update_structure_exec_doc()

    def update_menu_recent_projects(self):
        self.__obs_manager.obj_l.debug_logger("IN update_menu_recent_projects()")
        self.ui.menu_recent_projects.clear()
        last_projects = self.__obs_manager.obj_sd.get_last_projects()
        for project in last_projects:
            name_project = project.get("name_project")
            action = self.ui.menu_recent_projects.addAction(name_project)
            action.setData(project)
            action.triggered.connect(partial(self.menu_recent_projects_action, action))

    def menu_recent_projects_action(self, item):
        self.__obs_manager.obj_l.debug_logger(
            f"IN menu_recent_projects_action(item):\nitem = {item}"
        )
        project = item.data()
        self.__obs_manager.obj_p.open_recent_project(project)
