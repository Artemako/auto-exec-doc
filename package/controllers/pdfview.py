from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import QUrl
import sys


import package.modules.log as log


class PdfView:
    __widget_pdf_view = None
    __document = None
    __zoom = 1    

    def __init__(self):
        pass

    @staticmethod
    def connect_pdfview(widget, m_document):
        PdfView.__widget_pdf_view = widget
        PdfView.__document = m_document

    @staticmethod
    def zoom_in():
        PdfView.__zoom += 0.1
        PdfView.__widget_pdf_view.setZoomFactor(PdfView.__zoom)
        log.Log.debug_logger(f"zoom_in(): PdfView.__zoom = {PdfView.__zoom}")

    @staticmethod
    def zoom_out():
        if PdfView.__zoom >= 0:
            PdfView.__zoom -= 0.1
        PdfView.__widget_pdf_view.setZoomFactor(PdfView.__zoom)
        log.Log.debug_logger(f"zoom_out(): PdfView.__zoom = {PdfView.__zoom}")

    @staticmethod
    def set_zoom_to_fit_width():
        PdfView.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        log.Log.debug_logger("set_zoom_to_fit_width()")

    @staticmethod
    def set_zoom_to_fit_view():
        PdfView.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        log.Log.debug_logger("set_zoom_to_fit_view()")

    @staticmethod
    def set_zoom_custom():
        PdfView.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        log.Log.debug_logger("set_zoom_custom()")

    @staticmethod
    def set_empty_pdf_view():
        PdfView.__document = QPdfDocument()
        PdfView.__widget_pdf_view.setDocument(PdfView.__document)
        log.Log.debug_logger("set_empty_pdf_view()")

    @staticmethod
    def load_and_show_pdf_document(pdf_path):

        log.Log.debug_logger(f"load_and_show_pdf_document(pdf_path): pdf_path = {pdf_path}")

        doc_location = QUrl.fromLocalFile(pdf_path)
        if doc_location.isLocalFile():
            PdfView.__document.load(doc_location.toLocalFile())

    # скроллинг по горизонтали работает с нажатой клавишей Alt