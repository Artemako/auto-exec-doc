from PySide2.QtWidgets import QMainWindow
from PySide2.QtPdf import QPdfDocument
from PySide2.QtPdfWidgets import QPdfView

import package.ui.mainwindow_ui as mainwindow_ui
import package.modules.project as project
import package.modules.log as log

import package.controllers.structureexecdoc as structureexecdoc
import package.controllers.pagestemplate as pagestemplate
import package.controllers.scrollareainput as scrollareainput
import package.controllers.statusbar as statusbar
import package.controllers.pdfview as pdfview
import package.modules.filefoldermanager as filefoldermanager


class MainWindow(QMainWindow):
    def __init__(self):
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
        log.Log.debug_logger("IN config_controllers()")
        # настройка статус бара
        statusbar.StatusBar.connect_statusbar(self.ui.status_bar)
        # настройка structureexecdoc
        structureexecdoc.StructureExecDoc.connect_structureexecdoc(
            self.ui.treewidget_structure_execdoc, self.ui.title_structure_execdoc
        )
        # настройка pagestemplate
        pagestemplate.PagesTemplate.connect_pages_template(
            self.ui.listwidget_pages_template, self.ui.title_pages_template
        )
        # настройка inputforms
        scrollareainput.ScroolAreaInput.connect_inputforms(
            self.ui.scrollarea_inputforms, self.ui.scrollarea_inputforms_layout
        )
        # ПОДКЛЮЧИТЬ PDF
        pdfview.PdfView.connect_pdfview(self.ui.widget_pdf_view, self.m_document)

    def closeEvent(self, event):
        log.Log.debug_logger(f"IN closeEvent(self, event): event = {event}")
        filefoldermanager.FileFolderManager.clear_temp_folder(True)

    def connecting_actions(self):
        """
        Method to connect to various actions on the UI.
        """
        log.Log.debug_logger("IN connecting_actions()")
        self.ui.action_new.triggered.connect(lambda: project.Project.new_project())
        self.ui.action_open.triggered.connect(lambda: project.Project.open_project())
        # TODO Добавить активности для сохранения
        self.ui.action_save.triggered.connect(lambda: project.Project.save_project())
        # self.ui.action_saveas.triggered.connect()
        self.ui.action_export_to_pdf.triggered.connect(
            lambda: project.Project.export_to_pdf()
        )
        self.ui.action_zoomin.triggered.connect(lambda: pdfview.PdfView.zoom_in())
        self.ui.action_zoomout.triggered.connect(lambda: pdfview.PdfView.zoom_out())
        self.ui.action_zoomfitpage.triggered.connect(
            lambda checked: pdfview.PdfView.set_zoom_to_fit_width()
            if checked
            else pdfview.PdfView.set_zoom_custom()
        )



