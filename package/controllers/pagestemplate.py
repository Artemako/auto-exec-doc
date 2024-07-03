from PySide6.QtWidgets import QListWidgetItem

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

    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__listwidget_pages_template = None
        self.__title_pt = None


    def is_page_template_selected(self):
        self.__obs_manager.obj_l.debug_logger("get_listwidget_pages_template()")
        return self.__listwidget_pages_template.currentItem()


    def connect_pages_template(self, lw_pt, title_pt):
        """
        Подключить _listwidget_pages_template.
        """
        self.__obs_manager.obj_l.debug_logger("IN connect_pages_template(lw_pt)")
        self.__listwidget_pages_template = lw_pt
        self.__title_pt = title_pt
        self.clear_pt()

        # Подключение сигналов
        self.__listwidget_pages_template.itemClicked.connect(
            lambda current: self.item_page_updated(current)
        )


    def item_page_updated(self, current):
        """
        Слот для сигнала itemClicked.
        """
        self.__obs_manager.obj_l.debug_logger(f"IN item_page_updated(current): current = {current}")
        page = current.get_page()
        # добыть информация для SectionInfo
        self.__obs_manager.obj_si.update_sections_info(page)
        # Обновить ScroolAreaInput после SectionInfo
        self.__obs_manager.obj_sai.update_scrollarea(page)
        # открыть pdf форму для текущей страницы
        self.__obs_manager.obj_c.create_and_view_page_pdf(page)
        

    def current_page_to_pdf(self):
        self.__obs_manager.obj_l.debug_logger("IN current_page_to_pdf()")
        current = self.__listwidget_pages_template.currentItem()
        page = current.get_page()
        self.__obs_manager.obj_c.create_and_view_page_pdf(page)


    def clear_pt(self):
        self.__listwidget_pages_template.clear()
        self.__title_pt.setText("Форма не выбрана")

    def create_pages_template(self):
        """
        Создание _listwidget_pages_template.
        """
        self.__obs_manager.obj_l.debug_logger("IN create_pages_template()")

        self.clear_pt()
        self.__title_pt.setText("Форма не выбрана")

    def update_pages_template(self, node):
        """
        Обновить _listwidget_pages_template.
        """
        self.__obs_manager.obj_l.debug_logger(f"IN update_pages_template(node) : node = {node}")

        self.clear_pt()

        self.__title_pt.setText(node.get("name_node"))

        pages = self.__obs_manager.obj_pd.get_pages_by_node(node)
        for page in pages:
            print(f"page = {page}")
            item = MyListWidgetItem(page)
            item.setText(page.get("page_name"))
            self.__listwidget_pages_template.addItem(item)




# obj_pt = PagesTemplate()