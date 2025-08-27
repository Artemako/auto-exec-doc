from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QSizePolicy, QApplication
from PySide6.QtCore import QUrl, Qt, QObject
from PySide6.QtGui import QMouseEvent, QWheelEvent
import sys

DELTA_ZOOM = 0.1
MAX_ZOOM = 4
MIN_ZOOM = 0.1


class PdfView(QObject):
    def __init__(self):
        super().__init__()
        self.__widget_pdf_view = None
        self.__document = None
        self.__zoom = 1
        self.__is_dragging = False
        self.__last_mouse_pos = None
        self.__last_mouse_pos_before_zoom = None

    def __del__(self):
        """Деструктор для правильного удаления eventFilter"""
        try:
            if (self.__widget_pdf_view and 
                self.__widget_pdf_view.viewport()):
                self.__widget_pdf_view.viewport().removeEventFilter(self)
        except (RuntimeError, AttributeError):
            # Объекты уже удалены - это нормально
            pass
        except Exception as e:
            # Логируем другие ошибки, если logger доступен
            try:
                if hasattr(self, '_PdfView__osbm') and self.__osbm and hasattr(self.__osbm, 'obj_logg') and self.__osbm.obj_logg:
                    self.__osbm.obj_logg.error_logger(f"Error in PdfView __del__: {e}")
            except:
                pass

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("PdfView setting_all_osbm()")

    def connect_pdfview(self, widget):
        self.__osbm.obj_logg.debug_logger("PdfView connect_pdfview()")
        self.__widget_pdf_view = widget
        self.__document = None
        self.config_pdf_view_in_mainwindow()

        # Устанавливаем обработчики событий - исправленная строка
        self.__widget_pdf_view.viewport().installEventFilter(self)
        self.__widget_pdf_view.setMouseTracking(True)

    def eventFilter(self, obj, event):
        try:
            # Проверяем, что объекты еще существуют
            if (
                not self.__widget_pdf_view
                or not self.__widget_pdf_view.viewport()
                or not self.__document
            ):
                return False

            if obj == self.__widget_pdf_view.viewport():
                if event.type() == QMouseEvent.MouseButtonPress:
                    return self.mousePressEvent(event)
                elif event.type() == QMouseEvent.MouseButtonRelease:
                    return self.mouseReleaseEvent(event)
                elif event.type() == QMouseEvent.MouseMove:
                    return self.mouseMoveEvent(event)
                elif event.type() == QMouseEvent.Wheel:
                    return self.wheelEvent(event)
                # Если событие не обработано, передаем его дальше
                return False

        except RuntimeError as e:
            # Объект уже удален - игнорируем ошибку
            if "already deleted" in str(e):
                return False
            raise
        
        # Если объект не совпадает с viewport, передаем событие дальше
        return False

    def mousePressEvent(self, event):
        """Обработка нажатия кнопки мыши"""
        if event.button() == Qt.LeftButton:
            # Начало перетаскивания
            self.__is_dragging = True
            self.__last_mouse_pos = event.position()
            self.__widget_pdf_view.setCursor(Qt.ClosedHandCursor)
            return True

        return False

    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши"""
        if event.button() == Qt.LeftButton and self.__is_dragging:
            # Конец перетаскивания
            self.__is_dragging = False
            self.__widget_pdf_view.setCursor(Qt.ArrowCursor)
            return True

        return False

    def mouseMoveEvent(self, event):
        """Обработка движения мыши"""
        if self.__is_dragging and event.buttons() & Qt.LeftButton:
            # Перетаскивание документа
            current_pos = event.position()
            delta = current_pos - self.__last_mouse_pos

            # Получаем текущие значения скроллбаров
            h_scroll = self.__widget_pdf_view.horizontalScrollBar()
            v_scroll = self.__widget_pdf_view.verticalScrollBar()

            # Обновляем позицию скроллбаров
            h_scroll.setValue(h_scroll.value() - delta.x())
            v_scroll.setValue(v_scroll.value() - delta.y())

            self.__last_mouse_pos = current_pos
            return True

        return False

    def wheelEvent(self, event):
        """Обработка колесика мыши"""
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.ControlModifier:
            self.__last_mouse_pos_before_zoom = event.position()
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            return True
        return False

    def config_pdf_view_in_mainwindow(self):
        self.__osbm.obj_logg.debug_logger("PdfView config_pdf_view_in_mainwindow()")
        self.__document = QPdfDocument()
        self.__widget_pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.__widget_pdf_view.setDocument(self.__document)

    def zoom_in(self):
        if (
            self.__zoom + DELTA_ZOOM
        ) < MAX_ZOOM and self.__widget_pdf_view.zoomMode() == QPdfView.ZoomMode.Custom:
            # Сохраняем текущие позиции скроллбаров
            h_scroll = self.__widget_pdf_view.horizontalScrollBar()
            v_scroll = self.__widget_pdf_view.verticalScrollBar()
            old_h_value = h_scroll.value()
            old_v_value = v_scroll.value()

            # Применяем масштабирование
            old_zoom = self.__zoom
            self.__zoom += DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)

            # Корректируем скролл для центрирования по курсору мыши
            if self.__last_mouse_pos_before_zoom:
                zoom_ratio = self.__zoom / old_zoom
                mouse_pos = self.__last_mouse_pos_before_zoom

                new_h_value = (old_h_value + mouse_pos.x()) * zoom_ratio - mouse_pos.x()
                new_v_value = (old_v_value + mouse_pos.y()) * zoom_ratio - mouse_pos.y()

                h_scroll.setValue(int(new_h_value))
                v_scroll.setValue(int(new_v_value))

            self.__osbm.obj_logg.debug_logger(
                f"PdfView zoom_in():\nself.__zoom = {self.__zoom}"
            )

    def zoom_out(self):
        if (
            self.__zoom - DELTA_ZOOM
        ) > MIN_ZOOM and self.__widget_pdf_view.zoomMode() == QPdfView.ZoomMode.Custom:
            # Сохраняем текущие позиции скроллбаров
            h_scroll = self.__widget_pdf_view.horizontalScrollBar()
            v_scroll = self.__widget_pdf_view.verticalScrollBar()
            old_h_value = h_scroll.value()
            old_v_value = v_scroll.value()

            # Применяем масштабирование
            old_zoom = self.__zoom
            self.__zoom -= DELTA_ZOOM
            self.__widget_pdf_view.setZoomFactor(self.__zoom)

            # Корректируем скролл для центрирования по курсору мыши
            if self.__last_mouse_pos_before_zoom:
                zoom_ratio = self.__zoom / old_zoom
                mouse_pos = self.__last_mouse_pos_before_zoom

                new_h_value = (old_h_value + mouse_pos.x()) * zoom_ratio - mouse_pos.x()
                new_v_value = (old_v_value + mouse_pos.y()) * zoom_ratio - mouse_pos.y()

                h_scroll.setValue(int(new_h_value))
                v_scroll.setValue(int(new_v_value))

            self.__osbm.obj_logg.debug_logger(
                f"PdfView zoom_out():\nself.__zoom = {self.__zoom}"
            )

    def set_zoom_to_fit_width(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.__osbm.obj_logg.debug_logger("PdfView set_zoom_to_fit_width()")

    def set_zoom_custom(self):
        self.__widget_pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.__osbm.obj_logg.debug_logger("PdfView set_zoom_custom()")

    def set_empty_pdf_view(self):
        # Проверяем, что logger доступен
        if hasattr(self, '_PdfView__osbm') and self.__osbm and hasattr(self.__osbm, 'obj_logg') and self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger("PdfView set_empty_pdf_view()")
        
        try:
            # Отключаем event filter перед очисткой
            if (self.__widget_pdf_view and 
                self.__widget_pdf_view.viewport()):
                self.__widget_pdf_view.viewport().removeEventFilter(self)

            # Очищаем документ
            if self.__document:
                self.__document.close()
                self.__document = None

            # Создаем новый пустой документ
            if self.__widget_pdf_view:
                self.__document = QPdfDocument(self.__widget_pdf_view)
                self.__widget_pdf_view.setDocument(self.__document)

                # Снова устанавливаем event filter
                if self.__widget_pdf_view.viewport():
                    self.__widget_pdf_view.viewport().installEventFilter(self)

        except (RuntimeError, AttributeError) as e:
            if "already deleted" in str(e):
                # Объекты уже удалены - это нормально при закрытии
                pass
            else:
                if hasattr(self, '_PdfView__osbm') and self.__osbm and hasattr(self.__osbm, 'obj_logg') and self.__osbm.obj_logg:
                    self.__osbm.obj_logg.error_logger(f"Error in set_empty_pdf_view(): {e}")
        except Exception as e:
            if hasattr(self, '_PdfView__osbm') and self.__osbm and hasattr(self.__osbm, 'obj_logg') and self.__osbm.obj_logg:
                self.__osbm.obj_logg.error_logger(f"Unexpected error in set_empty_pdf_view(): {e}")

    def get_view_sizes(self):
        self.__osbm.obj_logg.debug_logger("PdfView get_view_sizes()")
        return (
            self.__widget_pdf_view.horizontalScrollBar().value(),
            self.__widget_pdf_view.verticalScrollBar().value(),
        )

    def set_view_sizes(self, value):
        self.__osbm.obj_logg.debug_logger(
            f"PdfView set_view_sizes({value}):\nvalue = {value}"
        )
        self.__widget_pdf_view.horizontalScrollBar().setValue(value[0])
        self.__widget_pdf_view.verticalScrollBar().setValue(value[1])

    def load_and_show_pdf_document(self, pdf_path):
        self.__osbm.obj_logg.debug_logger(
            f"PdfView load_and_show_pdf_document(pdf_path):\npdf_path = {pdf_path}"
        )

        doc_location = QUrl.fromLocalFile(pdf_path)
        if doc_location.isLocalFile():
            print(f"doc_location = {doc_location}")
            self.__document.load(doc_location.toLocalFile())
