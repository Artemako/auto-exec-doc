from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

import package.modules.log as log

import package.modules.projectdatabase as projectdatabase

class MyListWidgetItem(QListWidgetItem):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def get_page(self):
        return self.page


class PagesTemplate:
    _listwidget_pages_template = None

    def __init__(self):
        pass

    @staticmethod
    def set_lw_pt(lw_pt):
        log.Log.debug_logger("set_lw_pt()")
        PagesTemplate._listwidget_pages_template = lw_pt

    @staticmethod
    def get_lw_pt() -> object:
        log.Log.debug_logger("get_lw_pt() -> object")
        return PagesTemplate._listwidget_pages_template

    @staticmethod
    def connect_pages_template(lw_pt):
        """
        Подключить _listwidget_pages_template.
        """
        log.Log.debug_logger("IN connect_pages_template(lw_pt)")
        PagesTemplate.set_lw_pt(lw_pt)

    
    @staticmethod
    def create_pages_template():
        """
        Создать _listwidget_pages_template.
        """
        log.Log.debug_logger("IN create_pages_template()")
        PagesTemplate.get_lw_pt().clear()

    @staticmethod
    def update_pages_template(node):
        """
        Обновить _listwidget_pages_template.
        """
        log.Log.debug_logger(f"IN update_pages_template(node) : node = {node}")

        PagesTemplate.get_lw_pt().clear()

        pages = projectdatabase.Database.get_pages(node)
        for page in pages:
            item = MyListWidgetItem(page)
            item.setText(page.get("name_page"))
            # TODO state in SQL + отображение форм
            item.setCheckState(Qt.Checked)
            PagesTemplate.get_lw_pt().addItem(item)


        

    

        

