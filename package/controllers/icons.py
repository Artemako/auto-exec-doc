from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import resources_rc

class Icons:
    def __init__(self):
        self.__icons_cache = dict()

    def setting_all_obs_manager(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(f"Icons setting_obs_manager():\nself.__obs_manager = {self.__obs_manager}")

    def get_icons(self, size = 16) -> dict:
        self.__obs_manager.obj_l.debug_logger(f"Icons get_icons(size):\nsize = {size}")
        result = self.__icons_cache.get(size)
        if result:
            return result
        else:
            icons = dict()
            # типы тэгов
            icons["text"] = QIcon(":/icons/resources/icons/text.svg")
            icons["date"] = QIcon(":/icons/resources/icons/calendar.svg")
            icons["table"] = QIcon(":/icons/resources/icons/table.svg")
            icons["image"] = QIcon(":/icons/resources/icons/picture.svg")
            # прочее
            icons["save"] = QIcon(":/icons/resources/icons/save.svg")
            icons["close"] = QIcon(":/icons/resources/icons/close.svg")
            icons["add"] = QIcon(":/icons/resources/icons/plus.svg")
            # круги 
            icons["red_circle"] = QIcon(":/icons/resources/icons/red-circle.svg")
            icons["yellow_circle"] = QIcon(":/icons/resources/icons/yellow-circle.svg")
            icons["green_circle"] = QIcon(":/icons/resources/icons/green-circle.svg")
            # word, libreoffice
            icons["libreoffice"] = QIcon(":/icons/resources/icons/libreoffice.svg")
            icons["msword"] = QIcon(":/icons/resources/icons/msword.svg")
            # ручка и корзина
            icons["pen"] = QIcon(":/icons/resources/icons/pen.svg")
            icons["trash"] = QIcon(":/icons/resources/icons/trash.svg")
            # группа и форма
            icons["form"] = QIcon(":/icons/resources/icons/file-text.svg")
            icons["group"] = QIcon(":/icons/resources/icons/folder.svg")
            # страница
            icons["page"] = QIcon(":/icons/resources/icons/page.svg")
            #
            for key, elem in icons.items():
                icons[key] = elem.pixmap(QSize(size, size))
            self.__icons_cache[key] = icons
            return icons