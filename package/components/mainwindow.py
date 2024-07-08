from PySide6.QtWidgets import QMainWindow
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QShortcut, QKeySequence

import package.ui.mainwindow_ui as mainwindow_ui

class MainWindow(QMainWindow):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # настройка pdfViewer
        self.config_pdf_view_in_mainwindow()
        # настройка контроллеров
        self.config_controllers()
        # Подключаем действия
        self.connecting_actions()

    def config_pdf_view_in_mainwindow(self):
        self.m_document = QPdfDocument(self)
        self.ui.widget_pdf_view.setDocument(self.m_document)
          
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
        self.__obs_manager.obj_pv.connect_pdfview(self.ui.widget_pdf_view, self.m_document)

    def closeEvent(self, event):
        self.__obs_manager.obj_l.debug_logger(f"IN closeEvent(self, event): event = {event}")
        # удаление pdf из виджета pdfview
        self.__obs_manager.obj_pv.set_empty_pdf_view()
        # очистка временных файлов
        self.__obs_manager.obj_ffm.clear_temp_folder(True)

    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        self.__obs_manager.obj_l.debug_logger("IN connecting_actions()")
        self.ui.action_new.triggered.connect(lambda: self.__obs_manager.obj_p.new_project())
        self.ui.action_open.triggered.connect(lambda: self.__obs_manager.obj_p.open_project())
        # TODO Добавить активности для сохранения
        self.ui.action_save.triggered.connect(lambda: self.__obs_manager.obj_p.save_project())
        # self.ui.action_saveas.triggered.connect()
        self.ui.action_export_to_pdf.triggered.connect(
            lambda: self.__obs_manager.obj_p.export_to_pdf()
        )
        self.ui.action_zoomin.triggered.connect(lambda: self.__obs_manager.obj_pv.zoom_in())
        self.ui.action_zoomout.triggered.connect(lambda: self.__obs_manager.obj_pv.zoom_out())
        self.ui.action_zoomfitpage.triggered.connect(
            lambda checked: self.__obs_manager.obj_pv.set_zoom_to_fit_width()
            if checked
            else self.__obs_manager.obj_pv.set_zoom_custom()
        )

        # TODO Добавить активности для редактирования
        self.ui.action_edit_tags.triggered.connect(lambda: self.__obs_manager.obj_p.edit_tags())
        #self.ui.action_edit_templates.triggered.connect(lambda: self.__obs_manager.obj_p.edit_templates())

        # shortcut = QShortcut(QKeySequence("R"), self)
        # shortcut.activated.connect(lambda: self.__obs_manager.obj_pdf_view.set_empty_pdf_view())

    def enable_qt_actions(self):
        """
        Активирует кнопки в статусбаре при открытии проекта
        """
        self.ui.action_save.setEnabled(True)
        self.ui.action_zoomin.setEnabled(True)
        self.ui.action_zoomout.setEnabled(True)
        self.ui.action_edit_tags.setEnabled(True)
        self.ui.action_zoomfitpage.setEnabled(True)
        self.ui.action_export_to_pdf.setEnabled(True)
        self.ui.action_edit_templates.setEnabled(True)
        
    
    def get_view_height(self):
        return self.ui.widget_pdf_view.verticalScrollBar().value()
    
    def set_view_height(self, value):
        self.ui.widget_pdf_view.verticalScrollBar().setValue(value)

