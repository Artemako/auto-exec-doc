from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

import package.modules.log as log

import package.modules.projectdatabase as projectdatabase
import package.controllers.scrollareainput as scrollareainput


class MyListWidgetItem(QListWidgetItem):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def get_page(self):
        return self.page


class PagesTemplate:
    _listwidget_pages_template = None
    _title_pt = None

    def __init__(self):
        pass

    @staticmethod
    def set_lw_pt(lw_pt):
        log.Log.debug_logger("set_lw_pt()")
        PagesTemplate._listwidget_pages_template = lw_pt

    @staticmethod
    def get_lw_pt() -> object:
        log.Log.debug_logger("get_lw_pt()")
        return PagesTemplate._listwidget_pages_template

    @staticmethod
    def set_title_pt(title):
        log.Log.debug_logger("set_title_pt()")
        PagesTemplate._title_pt = title

    @staticmethod
    def get_title_pt() -> object:
        log.Log.debug_logger("get_title_pt()")
        return PagesTemplate._title_pt

    @staticmethod
    def connect_pages_template(lw_pt, title_pt):
        """
        Подключить _listwidget_pages_template.
        """
        log.Log.debug_logger("IN connect_pages_template(lw_pt)")
        PagesTemplate.set_lw_pt(lw_pt)
        PagesTemplate.set_title_pt(title_pt)
        PagesTemplate.clear_pt()

        # Подключение сигналов
        PagesTemplate.get_lw_pt().itemClicked.connect(
            lambda current: scrollareainput.ScroolAreaInput.update_scrollarea(
                current.get_page()
            )
        )

    @staticmethod
    def clear_pt():
        PagesTemplate.get_lw_pt().clear()
        PagesTemplate.get_title_pt().setText("Форма не выбрана")

    @staticmethod
    def create_pages_template():
        """
        Создание _listwidget_pages_template.
        """
        log.Log.debug_logger("IN create_pages_template()")
        
        PagesTemplate.clear_pt()
        PagesTemplate.get_title_pt().setText("Форма не выбрана")
    
    @staticmethod
    def update_pages_template(node):
        """
        Обновить _listwidget_pages_template.
        """
        log.Log.debug_logger(f"IN update_pages_template(node) : node = {node}")

        PagesTemplate.clear_pt()

        PagesTemplate.get_title_pt().setText(node.get("name_node"))

        pages = projectdatabase.Database.get_pages(node)
        for page in pages:
            item = MyListWidgetItem(page)
            item.setText(page.get("name_page"))
            item.setCheckState(Qt.Checked)
            PagesTemplate.get_lw_pt().addItem(item)
