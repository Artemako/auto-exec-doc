import package.modules.log as log
import package.components.customsection as customsection


from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton


class ScroolAreaInput:
    _scrollarea_input = None
    _scrollarea_input_layout = None

    def __init__(self):
        pass

    @staticmethod
    def set_sa(sa_if, sa_ifl):
        ScroolAreaInput._scrollarea_input = sa_if
        ScroolAreaInput._scrollarea_input_layout = sa_ifl
        sa_if.setWidget(sa_ifl)
        log.Log.debug_logger("set_sa()")

    @staticmethod
    def get_sa_if() -> object:
        log.Log.debug_logger("get_sa_if() -> object")
        return ScroolAreaInput._scrollarea_input

    @staticmethod
    def get_sa_ifl() -> object:
        log.Log.debug_logger("get_sa_ifl() -> object")
        return ScroolAreaInput._scrollarea_input_layout

    @staticmethod
    def connect_inputforms(sa_if, sa_ifl):
        """
        Подключить _scrollarea_input и _scrollarea_input_contents
        """
        log.Log.debug_logger("IN connect_pages_template(sa_if, sa_ifl)")
        ScroolAreaInput.set_sa(sa_if, sa_ifl)

        # TODO Шаблон-черновик
        #ScroolAreaInput.add_widget_in_sa(QLabel("Пока нет ни одного шаблона"))
        #ScroolAreaInput.add_widget_in_sa(QLabel("Нет ни одного шаблона"))
        #ScroolAreaInput.add_widget_in_sa(QLabel("Точно нет ни одного шаблона"))

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
        ScroolAreaInput.get_sa_ifl().layout().addWidget(widget)

    @staticmethod
    def delete_all_widgets_in_sa():
        """
        Удаление всех виджетов в ScroolAreaInput
        """
        log.Log.debug_logger("IN delete_all_widgets_in_sa()")

        log.Log.debug_logger("clear_sa()")
        layout = ScroolAreaInput.get_sa_ifl().layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                del item
