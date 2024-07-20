from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import QUrl
import sys



class PdfView:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__widget_pdf_view = None
        self.__document = None
        self.__zoom = 1

    def connect_pdfview(self, widget):
        self.__widget_pdf_view = widget
        self.__document = None
        self.config_pdf_view_in_mainwindow()

    def config_pdf_view_in_mainwindow(self):
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setDocument(self.__document)

    def zoom_in(self):
        self.__zoom += 0.1
        self.__widget_pdf_view.setZoomFactor(self.__zoom)
        self.__obs_manager.obj_l.debug_logger(f"zoom_in():\nself.__zoom = {self.__zoom}")

    def zoom_out(self):
        if self.__zoom >= 0:
            self.__zoom -= 0.1
        self.__widget_pdf_view.setZoomFactor(self.__zoom)
        self.__obs_manager.obj_l.debug_logger(f"zoom_out():\nself.__zoom = {self.__zoom}")

    def set_zoom_to_fit_width(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.__obs_manager.obj_l.debug_logger("set_zoom_to_fit_width()")

    def set_zoom_to_fit_view(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.__obs_manager.obj_l.debug_logger("set_zoom_to_fit_view()")

    def set_zoom_custom(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.__obs_manager.obj_l.debug_logger("set_zoom_custom()")

    def set_empty_pdf_view(self):
        self.__document = None
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setDocument(self.__document)
        self.__obs_manager.obj_l.debug_logger("set_empty_pdf_view()")

    def load_and_show_pdf_document(self, pdf_path):
        self.__obs_manager.obj_l.debug_logger(
            f"IN load_and_show_pdf_document(pdf_path):\npdf_path = {pdf_path}"
        )

        doc_location = QUrl.fromLocalFile(pdf_path)
        if doc_location.isLocalFile():
            print(f"doc_location = {doc_location}")
            self.__document.load(doc_location.toLocalFile())

    # скроллинг по горизонтали работает с нажатой клавишей Alt


# obj_pv = PdfView()
