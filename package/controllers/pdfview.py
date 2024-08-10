from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import QUrl
import sys

DELTA_ZOOM = 0.1
MAX_ZOOM = 4
MIN_ZOOM = 0.1  

class PdfView:
    def __init__(self):
        self.__widget_pdf_view = None
        self.__document = None
        self.__zoom = 1

    def setting_all_obs_manager(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("PdfView setting_all_obs_manager()")

    def connect_pdfview(self, widget):
        self.__obs_manager.obj_l.debug_logger("PdfView connect_pdfview()")
        self.__widget_pdf_view = widget
        self.__document = None
        self.config_pdf_view_in_mainwindow()

    def config_pdf_view_in_mainwindow(self):
        self.__obs_manager.obj_l.debug_logger("PdfView config_pdf_view_in_mainwindow()")
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setDocument(self.__document)

    def zoom_in(self):
        if (self.__zoom + DELTA_ZOOM) < MAX_ZOOM:
            self.__zoom += DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)
            self.__obs_manager.obj_l.debug_logger(f"PdfView zoom_in():\nself.__zoom = {self.__zoom}")

    def zoom_out(self):
        if (self.__zoom - DELTA_ZOOM) > MIN_ZOOM:
            self.__zoom -= DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)
            self.__obs_manager.obj_l.debug_logger(f"PdfView zoom_out():\nself.__zoom = {self.__zoom}")

    def set_zoom_to_fit_width(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.__obs_manager.obj_l.debug_logger("PdfView set_zoom_to_fit_width()")

    def set_zoom_to_fit_view(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.__obs_manager.obj_l.debug_logger("PdfView set_zoom_to_fit_view()")

    def set_zoom_custom(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.__obs_manager.obj_l.debug_logger("PdfView set_zoom_custom()")

    def set_empty_pdf_view(self):
        self.__document = None
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setDocument(self.__document)
        self.__obs_manager.obj_l.debug_logger("PdfView set_empty_pdf_view()")

    def load_and_show_pdf_document(self, pdf_path):
        self.__obs_manager.obj_l.debug_logger(
            f"PdfView load_and_show_pdf_document(pdf_path):\npdf_path = {pdf_path}"
        )

        doc_location = QUrl.fromLocalFile(pdf_path)
        if doc_location.isLocalFile():
            print(f"doc_location = {doc_location}")
            self.__document.load(doc_location.toLocalFile())

    # скроллинг по горизонтали работает с нажатой клавишей Alt


# obj_pv = PdfView()
