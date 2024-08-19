# Ошибки
class Errors:
    class MsWordError(Exception):
        pass

    class LibreOfficeError(Exception):
        pass

    def __init__(self):
        self.MsWordError = Errors.MsWordError
        self.LibreOfficeError = Errors.LibreOfficeError


# ТЭГИ
class TagType:
    def __init__(self, index, name_type_tag, type_tag, icon):
        self.index = index
        self.name_type_tag = name_type_tag
        self.type_tag = type_tag
        self.icon = icon


class TagTypes:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.__tag_types = [
            TagType(0, "Текст", "TEXT", self.__icons.get("text")),
            TagType(1, "Дата", "DATE", self.__icons.get("date")),
            TagType(2, "Таблица", "TABLE", self.__icons.get("table")),
            TagType(3, "Изображение", "IMAGE", self.__icons.get("image")),
        ]

    def get_tag_types(self):
        self.__osbm.obj_logg.debug_logger("NedTagDialogWindow get_tag_types()")
        return self.__tag_types
    

class Common:

    def __init__(self):
        self.__osbm = None
        # без __osbm
        self.errors = None
        # с __osbm
        self.tag_types = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("Common setting_all_osbm()")
        
    def run(self):
        self.__osbm.obj_logg.debug_logger("Common run()")
        # без __osbm
        self.errors = Errors()
        # с __osbm
        self.tag_types = TagTypes(self.__osbm)
