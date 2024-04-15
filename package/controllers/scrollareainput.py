import package.modules.log as log
import package.components.customsection as customsection


from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton


class ScroolAreaInput:
    _scrollarea_input = None
    _scrollarea_input_layout = None

    def __init__(self):
        pass

    @staticmethod
    def set_sa(sa_i, sa_il):
        ScroolAreaInput._scrollarea_input = sa_i
        ScroolAreaInput._scrollarea_input_layout = sa_il
        sa_i.setWidget(sa_il)
        log.Log.debug_logger("set_sa()")

    @staticmethod
    def get_sa_i() -> object:
        log.Log.debug_logger("get_sa_i() -> object")
        return ScroolAreaInput._scrollarea_input

    @staticmethod
    def get_sa_il() -> object:
        log.Log.debug_logger("get_sa_il() -> object")
        return ScroolAreaInput._scrollarea_input_layout

    @staticmethod
    def connect_pagestemplate(sa_i, sa_il):
        """
        Подключить _scrollarea_input и _scrollarea_input_contents
        """
        log.Log.debug_logger("IN connect_pagestemplate(sa_i, sa_il)")
        ScroolAreaInput.set_sa(sa_i, sa_il)

        # TODO
        # ScroolAreaInput.add_widget_in_sa(QLabel("Пока нет ни одного шаблона"))
        # ScroolAreaInput.add_widget_in_sa(QLabel("Нет ни одного шаблона"))
        # ScroolAreaInput.add_widget_in_sa(QLabel("Точно нет ни одного шаблона"))

        # ScroolAreaInput.delete_all_widgets_in_sa()

        section = customsection.Section("Section")
        anyLayout = QVBoxLayout()
        anyLayout.addWidget(QLabel("Some Text in Section", section))
        anyLayout.addWidget(QPushButton("Button in Section", section))
        section.setContentLayout(anyLayout)

        ScroolAreaInput.add_widget_in_sa(section)



    @staticmethod
    def add_widget_in_sa(widget):
        """
        Добавление виджета в ScroolAreaInput
        """

        log.Log.debug_logger("IN add_widget(widget)")
        ScroolAreaInput.get_sa_il().layout().addWidget(widget)

    @staticmethod
    def delete_all_widgets_in_sa():
        """
        Удаление всех виджетов в ScroolAreaInput
        """
        log.Log.debug_logger("IN delete_all_widgets_in_sa()")

        log.Log.debug_logger("clear_sa()")
        layout = ScroolAreaInput.get_sa_il().layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                del item
