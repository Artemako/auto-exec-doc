from PySide6.QtWidgets import QListWidgetItem

import package.modules.log as log

import package.modules.projectdatabase as projectdatabase
import package.controllers.scrollareainput as scrollareainput
import package.modules.sectionsinfo as sectionsinfo
import package.modules.converter as converter

import package.controllers.pdfview as pdfview


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
    def is_page_template_selected():
        log.Log.debug_logger("get_listwidget_pages_template()")
        return PagesTemplate.__listwidget_pages_template.currentItem()

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
            lambda current: PagesTemplate.item_page_updated(current)
        )

    @staticmethod
    def item_page_updated(current):
        """
        Слот для сигнала itemClicked.
        """
        log.Log.debug_logger(f"IN item_page_updated(current): current = {current}")
        page = current.get_page()
        # добыть информация для SectionInfo
        sectionsinfo.SectionsInfoGlobal.update_sections_info(page)
        # Обновить ScroolAreaInput после SectionInfo
        scrollareainput.ScroolAreaInput.update_scrollarea(page)
        # открыть pdf форму для текущей страницы
        converter.Converter.create_and_open_one_page_pdf(page)
        
    @staticmethod
    def current_page_to_pdf():
        log.Log.debug_logger("IN current_page_to_pdf()")
        current = PagesTemplate.__listwidget_pages_template.currentItem()
        page = current.get_page()
        converter.Converter.create_and_open_one_page_pdf(page)



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

        pages = projectdatabase.Database.get_pages_by_node(node)
        for page in pages:
            print(f"page = {page}")
            item = MyListWidgetItem(page)
            item.setText(page.get("page_name"))
            PagesTemplate.__listwidget_pages_template.addItem(item)
