
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

import resources_rc

class Icons:
    def __init__(self):
        self.__icons_cache = dict()
        self.__type_variable_to_key_icon = {
            "TEXT": "text",
            "DATE": "date",
            "TABLE": "table",
            "IMAGE": "image"
        }

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(f"Icons setting_osbm():\nself.__osbm = {self.__osbm}")

    def get_key_icon_by_type_variable(self, type_variable):
        """
        БЕЗ logger
        """
        return self.__type_variable_to_key_icon.get(type_variable)
        
    def get_icons(self, size = 16) -> dict:
        self.__osbm.obj_logg.debug_logger(f"Icons get_icons(size):\nsize = {size}")
        result = self.__icons_cache.get(size)
        if result:
            return result
        else:
            icons = dict()
            # типы переменных
            icons["text"] = QIcon(":/white-icons/resources/white-icons/text.svg")
            icons["date"] = QIcon(":/white-icons/resources/white-icons/calendar.svg")
            icons["table"] = QIcon(":/white-icons/resources/white-icons/table.svg")
            icons["image"] = QIcon(":/white-icons/resources/white-icons/picture.svg")
            # прочее
            icons["save"] = QIcon(":/white-icons/resources/white-icons/save.svg")
            icons["close"] = QIcon(":/white-icons/resources/white-icons/close.svg")
            icons["add"] = QIcon(":/white-icons/resources/white-icons/plus.svg")
            # круги 
            icons["red_circle"] = QIcon(":/color-icons/resources/color-icons/red-circle.svg")
            icons["yellow_circle"] = QIcon(":/color-icons/resources/color-icons/yellow-circle.svg")
            icons["green_circle"] = QIcon(":/color-icons/resources/color-icons/green-circle.svg")
            # word, libreoffice
            icons["libreoffice"] = QIcon(":/color-icons/resources/color-icons/libreoffice.svg")
            icons["msword"] = QIcon(":/color-icons/resources/color-icons/msword.svg")
            # ручка и корзина
            icons["pen"] = QIcon(":/white-icons/resources/white-icons/pen.svg")
            icons["trash"] = QIcon(":/white-icons/resources/white-icons/trash.svg")
            # группа и форма
            icons["form"] = QIcon(":/white-icons/resources/white-icons/page.svg")
            icons["group"] = QIcon(":/white-icons/resources/white-icons/folder.svg")
            # страница
            icons["page"] = QIcon(":/white-icons/resources/white-icons/file-text.svg")
            # pdf
            icons["pdf"] = QIcon(":/white-icons/resources/white-icons/pdf.svg")
            #
            for key, elem in icons.items():
                if key in ["red_circle", "yellow_circle", "green_circle"]:
                    icons[key] = icons[key].pixmap(QSize(size / 2, size / 2))
                else:
                    icons[key] = elem.pixmap(QSize(size, size))
            self.__icons_cache[size] = icons
            return icons