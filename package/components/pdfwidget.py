import os

from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget


import package.ui.pdfwidget_ui as pdfwidget_ui
import package.app as app
import package.modules.dirpathsmanager as dirpathsmanager


class PdfWidget(QWidget):
    def __init__(self, parent=None):
        super(PdfWidget, self).__init__()
        self.zoom = 1
        self.document = None
        self.ui = pdfwidget_ui.Ui_PdfWidget()
        self.ui.setupUi(self)
        self.view_pdf()

    # region: Масштабирование
    def zoom_in(self):
        self.zoom += 0.1
        self.ui.view.setZoomFactor(self.zoom)
        print("zoom_in", self.zoom)

    def zoom_out(self):
        if self.zoom >= 0:
            self.zoom -= 0.1
        self.ui.view.setZoomFactor(self.zoom)
        print("zoom_out", self.zoom)

    def set_zoom_to_fit_width(self):
        self.ui.view.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def set_zoom_to_fit_view(self):
        self.ui.view.setZoomMode(QPdfView.ZoomMode.FitInView)

    def set_zoom_custom(self):
        self.ui.view.setZoomMode(QPdfView.ZoomMode.Custom)

    # endregion

    # скроллинг по горизонтали работает с нажатой клавишей Alt

    def load_pdf_for_view(self, file_path):
        """
        Load a PDF file for viewing.
        """
        self.document = QPdfDocument()
        self.document.load(file_path)
        self.ui.view.setDocument(self.document)

    def view_pdf(self):
        file_path = os.path.abspath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_documents_dirpath(), "test.pdf"
            )
        )
        self.load_pdf_for_view(file_path)
