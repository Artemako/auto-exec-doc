import os

from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QSizePolicy


import package.app as app
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.converter as converter

import package.modules.log as log


class PdfView:
    __widget_pdf_view = None
    __zoom = 1
    __document = None

    def __init__(self):
        pass

    @staticmethod
    def connect_pdfview(widget):
        PdfView.__widget_pdf_view = widget
        PdfView.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)

        # PdfView.view_test_pdf()

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

    # endregion

    # скроллинг по горизонтали работает с нажатой клавишей Alt

    @staticmethod
    def open_pdf_file_for_page(page):
        log.Log.debug_logger(f"IN open_pdf_file_for_page(page): page = {page}")
        # имя файла для открытия
        pdf_name = page.get("template_name") + ".pdf"
        # путь файла для открытия
        page_pdf_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_pdfs_folder_dirpath(), pdf_name
            )
        )

        if not os.path.exists(page_pdf_path):
            converter.Converter.create_page_pdf(page)
            pass

        PdfView.load_pdf_for_view(page_pdf_path)

    @staticmethod
    def load_pdf_for_view(file_path):
        """
        Load a PDF file for viewing.
        """
        log.Log.debug_logger(
            f"IN load_pdf_for_view(file_path): file_path = {file_path}"
        )
        PdfView.__document = QPdfDocument()
        PdfView.__document.load(file_path)
        PdfView.__widget_pdf_view.setDocument(PdfView.__document)
