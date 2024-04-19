from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

import package.modules.log as log

import package.modules.projectdatabase as projectdatabase
import package.controllers.scrollareainput as scrollareainput


class MyListWidgetItem(QListWidgetItem):
    """
    Кастомный QListWidgetItem с полем page.
    """

    def __init__(self, page):
        super().__init__()
        self.page = page

    def get_page(self):
        return self.page


class PagesTemplate:
    __listwidget_pages_template = None
    __title_pt = None

    def __init__(self):
        pass

    @staticmethod
    def connect_pages_template(lw_pt, title_pt):
        """
        Подключить _listwidget_pages_template.
        """
        log.Log.debug_logger("IN connect_pages_template(lw_pt)")
        PagesTemplate.__listwidget_pages_template = lw_pt
        PagesTemplate.__title_pt = title_pt
        PagesTemplate.clear_pt()

        # Подключение сигналов
        PagesTemplate.__listwidget_pages_template.itemClicked.connect(
            lambda current: scrollareainput.ScroolAreaInput.update_scrollarea(
                current.get_page()
            )
        )

    @staticmethod
    def clear_pt():
        PagesTemplate.__listwidget_pages_template.clear()
        PagesTemplate.__title_pt.setText("Форма не выбрана")

    @staticmethod
    def create_pages_template():
        """
        Создание _listwidget_pages_template.
        """
        log.Log.debug_logger("IN create_pages_template()")

        PagesTemplate.clear_pt()
        PagesTemplate.__title_pt.setText("Форма не выбрана")

    @staticmethod
    def update_pages_template(node):
        """
        Обновить _listwidget_pages_template.
        """
        log.Log.debug_logger(f"IN update_pages_template(node) : node = {node}")

        PagesTemplate.clear_pt()

        PagesTemplate.__title_pt.setText(node.get("name_node"))

        pages = projectdatabase.Database.get_pages(node)
        for page in pages:
            item = MyListWidgetItem(page)
            item.setText(page.get("name_page"))
            PagesTemplate.__listwidget_pages_template.addItem(item)

