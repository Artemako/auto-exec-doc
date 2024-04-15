import package.modules.log as log


class ScroolAreaInput:
    _scrollarea_input = None
    _scrollarea_input_contents = None

    def __init__(self):
        pass

    @staticmethod
    def set_sa_i(sa_i):
        log.Log.debug_logger("set_sa_i()")
        ScroolAreaInput._scrollarea_input = sa_i

    @staticmethod
    def set_sa_ic(sa_ic):
        log.Log.debug_logger("set_sa_ic()")
        ScroolAreaInput._scrollarea_input_contents = sa_ic

    @staticmethod
    def get_sa_i() -> object:
        log.Log.debug_logger("get_sa_i() -> object")
        return ScroolAreaInput._scrollarea_input

    @staticmethod
    def get_sa_ic() -> object:
        log.Log.debug_logger("get_sa_ic() -> object")
        return ScroolAreaInput._scrollarea_input_contents

    @staticmethod
    def connect_pagestemplate(sa_i, sa_ic):
        """
        Подключить _scrollarea_input и _scrollarea_input_contents
        """
        log.Log.debug_logger("IN connect_pagestemplate(sa_i, sa_ic)")
        ScroolAreaInput.set_sa_i(sa_i)
        ScroolAreaInput.set_sa_ic(sa_ic)

        # TODO
