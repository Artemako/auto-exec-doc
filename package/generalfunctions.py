from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import resources_rc

class GeneralFunctions:
    def __init__(self):
        self.__obs_manager = None
        self.__icons_cache = dict()

    def setting(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("GeneralFunctions setting(obs_manager)")

    def get_icons(self, size = 16) -> dict:
        self.__obs_manager.obj_l.debug_logger(f"GeneralFunctions get_icons(size):\nsize = {size}")
        result = self.__icons_cache.get(size)
        if result:
            return result
        else:
            icons = dict()
            # типы тэгов
            icons["qicon_text"] = QIcon(":/icons/resources/icons/text.svg")
            icons["qicon_date"] = QIcon(":/icons/resources/icons/calendar.svg")
            icons["qicon_table"] = QIcon(":/icons/resources/icons/table.svg")
            icons["qicon_image"] = QIcon(":/icons/resources/icons/picture.svg")
            # прочее
            icons["qicon_save"] = QIcon(":/icons/resources/icons/save.svg")
            icons["qicon_close"] = QIcon(":/icons/resources/icons/close.svg")
            icons["qicon_add"] = QIcon(":/icons/resources/icons/plus.svg")
            # круги 
            icons["qicon_red_circle"] = QIcon(":/icons/resources/icons/red-circle.svg")
            icons["qicon_yellow_circle"] = QIcon(":/icons/resources/icons/yellow-circle.svg")
            icons["qicon_green_circle"] = QIcon(":/icons/resources/icons/green-circle.svg")
            # word, libreoffice
            icons["qicon_libreoffice"] = QIcon(":/icons/resources/icons/libreoffice.svg")
            icons["qicon_msword"] = QIcon(":/icons/resources/icons/msword.svg")
            # ручка и корзина
            icons["qicon_pen"] = QIcon(":/icons/resources/icons/pen.svg")
            icons["qicon_trash"] = QIcon(":/icons/resources/icons/trash.svg")

            #
            for key, elem in icons.items():
                icons[key] = elem.pixmap(QSize(size, size))
            self.__icons_cache[key] = icons
            return icons
        

    def print_array(self, array):
        for i, elem in enumerate(array):
            print(f"""i = {i} elem = {elem}""")