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
        self.__obs_manager.obj_l.debug_logger("PagesTemplate __init__()")
        self.__listwidget_pages_template = None
        self.__title_pt = None

    def is_page_template_selected(self):
        self.__obs_manager.obj_l.debug_logger("PagesTemplate get_listwidget_pages_template()")
        return self.__listwidget_pages_template.currentItem()

    def get_page_by_current_item(self):
        self.__obs_manager.obj_l.debug_logger("PagesTemplate get_page_by_current_item()")
        current = self.__listwidget_pages_template.currentItem()
        if current is None:
            return None
        return current.get_page()


    def connect_pages_template(self, lw_pt, title_pt):
        """
        Подключить _listwidget_pages_template.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"PagesTemplate connect_pages_template(lw_pt, title_pt):\nlw_pt = {lw_pt},\ntitle_pt = {title_pt}"
        )
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
        self.__obs_manager.obj_l.debug_logger(
            f"PagesTemplate item_page_updated(current):\ncurrent = {current}"
        )
        page = current.get_page()
        # Обновить ScroolAreaInput
        self.__obs_manager.obj_sai.update_scrollarea(page)
        # открыть pdf форму для текущей страницы
        self.__obs_manager.obj_c.create_and_view_page_pdf(page)

    def current_page_to_pdf(self):
        self.__obs_manager.obj_l.debug_logger("PagesTemplate IN current_page_to_pdf()")
        current = self.__listwidget_pages_template.currentItem()
        page = current.get_page()
        self.__obs_manager.obj_c.create_and_view_page_pdf(page)

    def clear_pt(self):
        self.__obs_manager.obj_l.debug_logger("PagesTemplate IN clear_pt()")
        self.__listwidget_pages_template.clear()
        self.__title_pt.setText("Форма не выбрана")

    def update_pages_template(self, node):
        """
        Обновить _listwidget_pages_template.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"PagesTemplate update_pages_template(node):\nnode = {node}"
        )

        self.clear_pt()

        self.__title_pt.setText(node.get("name_node"))

        id_active_template = node.get("id_active_template")
        template = self.__obs_manager.obj_pd.get_template_by_id(id_active_template)
        pages = self.__obs_manager.obj_pd.get_pages_by_template(template)
        for page in pages:
            print(f"page = {page}")
            item = MyListWidgetItem(page)
            item.setText(page.get("name_page"))
            self.__listwidget_pages_template.addItem(item)


# obj_pt = PagesTemplate()
