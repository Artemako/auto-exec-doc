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

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("PdfView setting_all_osbm()")

    def connect_pdfview(self, widget):
        self.__osbm.obj_logg.debug_logger("PdfView connect_pdfview()")
        self.__widget_pdf_view = widget
        self.__document = None
        self.config_pdf_view_in_mainwindow()

    def config_pdf_view_in_mainwindow(self):
        self.__osbm.obj_logg.debug_logger("PdfView config_pdf_view_in_mainwindow()")
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.__widget_pdf_view.setDocument(self.__document)

    def zoom_in(self):
        if (self.__zoom + DELTA_ZOOM) < MAX_ZOOM:
            self.__zoom += DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)
            self.__osbm.obj_logg.debug_logger(f"PdfView zoom_in():\nself.__zoom = {self.__zoom}")

    def zoom_out(self):
        if (self.__zoom - DELTA_ZOOM) > MIN_ZOOM:
            self.__zoom -= DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)
            self.__osbm.obj_logg.debug_logger(f"PdfView zoom_out():\nself.__zoom = {self.__zoom}")

    def set_zoom_to_fit_width(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.__osbm.obj_logg.debug_logger("PdfView set_zoom_to_fit_width()")

    def set_zoom_to_fit_view(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.__osbm.obj_logg.debug_logger("PdfView set_zoom_to_fit_view()")

    def set_zoom_custom(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.__osbm.obj_logg.debug_logger("PdfView set_zoom_custom()")

    def set_empty_pdf_view(self):
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setDocument(self.__document)
        self.__osbm.obj_logg.debug_logger("PdfView set_empty_pdf_view()")

    def get_view_height(self):
        self.__osbm.obj_logg.debug_logger("PdfView get_view_height()")
        return self.__widget_pdf_view.verticalScrollBar().value()

    def set_view_height(self, value):
        self.__osbm.obj_logg.debug_logger(
            f"PdfView set_view_height({value}):\nvalue = {value}"
        )
        self.__widget_pdf_view.verticalScrollBar().setValue(value)

    def load_and_show_pdf_document(self, pdf_path):
        self.__osbm.obj_logg.debug_logger(
            f"PdfView load_and_show_pdf_document(pdf_path):\npdf_path = {pdf_path}"
        )

        doc_location = QUrl.fromLocalFile(pdf_path)
        if doc_location.isLocalFile():
            print(f"doc_location = {doc_location}")
            self.__document.load(doc_location.toLocalFile())

    # скроллинг по горизонтали работает с нажатой клавишей Alt


# obj_pdfv = PdfView()
