import package.modules.log as log


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
    def connect_pagestemplate(lw_pt):
        """
        Подключить _listwidget_pages_template.
        """
        log.Log.debug_logger("IN connect_pagestemplate(lw_pt)")
        PagesTemplate.set_lw_pt(lw_pt)

        # TODO
