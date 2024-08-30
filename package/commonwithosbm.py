from PySide6.QtWidgets import QSizePolicy


class VariableType:
    def __init__(self, index, name, data, icon, is_block):
        self.index = index
        self.name = name
        self.data = data
        self.icon = icon
        self.is_block = is_block


class VariableTypes:
    def __init__(self, osbm, icons):
        self.__osbm = osbm
        self.__icons = icons
        self.__variable_types = [
            VariableType(0, "Текст", "TEXT", self.__icons.get("text"), False),
            VariableType(
                1, "Длинный текст", "LONGTEXT", self.__icons.get("longtext"), False
            ),
            VariableType(2, "Дата", "DATE", self.__icons.get("date"), False),
            VariableType(3, "Таблица", "TABLE", self.__icons.get("table-columns"), True),
            VariableType(4, "Изображение", "IMAGE", self.__icons.get("image"), False),
        ]
    
    def get_icon_by_type_variable(self, type_variable):
        result = None
        for variable in self.__variable_types:
            if variable.data == type_variable:
                result = variable.icon
                break
        self.__osbm.obj_logg.debug_logger(f"VariableTypes get_icon_by_type_variable(type_variable):\ntype_variable = {type_variable}\n result = {result}")
        return result

    def get_variable_types(self):
        self.__osbm.obj_logg.debug_logger("VariableTypes get_variable_types()")
        return self.__variable_types

    def get_data_by_index(self, index):
        result = None
        for variable in self.__variable_types:
            if variable.index == index:
                result = variable.data
                break
        self.__osbm.obj_logg.debug_logger(
            f"VariableTypes get_data_by_index(index):\nindex = {index}\n result = {result}"
        )
        return result

    def get_index_by_data(self, data):
        result = None
        for variable in self.__variable_types:
            if variable.data == data:
                result = variable.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"VariableTypes get_index_by_data(data):\ntype_variable = {data}\n result = {result}"
        )
        return result


#
#
#


class Unit:
    def __init__(self, index, name, data):
        self.index = index
        self.name = name
        self.data = data


class Units:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__units = [
            Unit(0, "Миллиметр (Millimeter)", "MM"),
            Unit(1, "Сантиметр (Centimeter)", "CM"),
            Unit(2, "Дюйм (Inch)", "INCH"),
            Unit(3, "Пункт (Point)", "PT"),
        ]

    def get_units(self):
        self.__osbm.obj_logg.debug_logger("Units get_units()")
        return self.__units

    def get_index_unit_by_data(self, data):
        result = 0
        for unit in self.__units:
            if unit.data == data:
                result = unit.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"Units get_index_unit_by_data(data):\ndata_unit = {data}\n result = {result}"
        )
        return result


#
#
#


class SizingMode:
    def __init__(self, index, name, data, is_wh):
        self.index = index
        self.name = name
        self.data = data
        self.is_wh = is_wh


class SizingModes:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__sizing_modes = [
            SizingMode(0, "Без изменений", "NOCHANGES", False),
            SizingMode(1, "Вместить без изменения пропорций", "CONTAIN", True),
            SizingMode(2, "Заполнить без изменения пропорций", "COVER", True),
            SizingMode(3, "Растянуть с изменением пропорций", "FILL", True),
        ]

    def get_sizing_modes(self):
        self.__osbm.obj_logg.debug_logger("SizingModes get_sizing_modes()")
        return self.__sizing_modes

    def get_index_sizing_mode_by_data(self, data):
        result = 0
        for sizing_mode in self.__sizing_modes:
            if sizing_mode.data == data:
                result = sizing_mode.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"SizingModes get_index_sizing_mode_by_data(data):\ndata_sizing_mode = {data}\n result = {result}"
        )
        return result

    def get_is_wh_by_index(self, index):
        sizing_mode = self.__sizing_modes[index]
        result = sizing_mode.is_wh
        self.__osbm.obj_logg.debug_logger(
            f"SizingModes get_is_wh_by_index(index):\nindex = {index}\n result = {result}"
        )
        return result


#
#
#


class TableType:
    def __init__(self, index, name, data, icon, is_edit_rowcols):
        self.index = index
        self.name = name
        self.data = data
        self.icon = icon
        self.is_edit_rowcols = is_edit_rowcols


class TableTypes:
    def __init__(self, osbm, icons):
        self.__osbm = osbm
        self.__icons = icons
        self.__table_types = [
            # TableType(0, "Произвольный", "FULL", False),
            TableType(0, "Настройка столбцов таблицы", "COL", self.__icons.get("table-columns"), True),
            TableType(1, "Настройка строк таблицы", "ROW", self.__icons.get("table-rows"), True),
        ]
        self.__text_btns = {
            # "0": ("Строки/Столбцы", "Добавить строку/столбец"),
            "0": ("Столбцы", "Добавить столбец"),
            "1": ("Строки", "Добавить строку"),
        }

    def get_table_types(self):
        self.__osbm.obj_logg.debug_logger("TableTypes get_table_types()")
        return self.__table_types

    def get_is_edit_rowcols_by_index(self, index):
        table_type = self.__table_types[index]
        result = table_type.is_edit_rowcols
        self.__osbm.obj_logg.debug_logger(
            f"TableTypes get_is_edit_rowcols_by_index(index):\nindex = {index}\n result = {result}"
        )
        return result

    def get_text_btns_by_index(self, index):
        result = 0
        for key, value in self.__text_btns.items():
            if int(key) == index:
                result = value
                break
        self.__osbm.obj_logg.debug_logger(
            f"TableTypes get_text_btns_by_data(data):\index = {index}\n result = {result}"
        )
        return result

    def get_index_by_data(self, data):
        result = 0
        for table_type in self.__table_types:
            if table_type.data == data:
                result = table_type.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"TableTypes get_index_by_data(data):\ndata = {data}\n result = {result}"
        )
        return result


#
#
#


class PageType:
    def __init__(self, index, name, data, icon):
        self.index = index
        self.name = name
        self.data = data
        self.icon = icon


class PageTypes:
    def __init__(self, osbm, icons):
        self.__osbm = osbm
        self.__icons = icons
        self.__page_types = [
            PageType(0, "Файл DOCX", "DOCX", self.__icons.get("page")),
            PageType(1, "Файл PDF", "PDF", self.__icons.get("pdf")),
        ]

    def get_page_types(self):
        self.__osbm.obj_logg.debug_logger("PageTypes get_page_types()")
        return self.__page_types

    def get_index_by_data(self, data):
        result = 0
        for page_type in self.__page_types:
            if page_type.data == data:
                result = page_type.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"PageTypes get_index_by_data(data):\ndata = {data}\n result = {result}"
        )
        return result


#
#
#


class language:
    def __init__(self, index, name, data, emoji):
        self.index = index
        self.name = name
        self.data = data
        self.emoji = emoji


class Languages:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__languages = [
            language(0, "Русский", "ru_RU", "🇷🇺"),
            language(1, "English", "en_US", "🇬🇧"),  # ,
            # language(2, "Chinese", "zh_CN", "🇨🇳"),
            # language(3, "French", "fr_FR", "🇫🇷"),
            # language(4, "German", "de_DE", "🇩🇪"),
            # language(5, "Spanish", "es_ES", "🇪🇸"),
            # language(6, "Portuguese", "pt_BR", "🇵🇹"),
            # language(7, "Italian", "it_IT", "🇮🇹"),
            # language(8, "Japanese", "ja_JP", "🇯🇵"),
            # language(9, "Korean", "ko_KR", "🇰🇷"),
        ]

    def get_languages(self):
        self.__osbm.obj_logg.debug_logger("Languages get_languages()")
        return self.__languages


#
#
#


class ResizeQt:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("ResizeQt __init__(osbm)")

    def set_temp_max_height(self, widget):
        width = widget.width()
        widget.setMaximumSize(width, 5000)
        widget.setMinimumWidth(width)
        widget.adjustSize()
        widget.setMaximumSize(5000, widget.height())
        self.__osbm.obj_logg.debug_logger("ResizeQt set_resize(widget)")


class CommonWithOsmb:
    def __init__(self):
        self.__osbm = None
        self.__icons = None
        #
        self.variable_types = None
        self.sizing_modes = None
        self.units = None
        self.table_types = None
        self.page_types = None
        self.languages = None
        self.resizeqt = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("CommonWithOsmb setting_all_osbm()")

    def run(self):
        self.__osbm.obj_logg.debug_logger("CommonWithOsmb run()")
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        #
        self.variable_types = VariableTypes(self.__osbm, self.__icons)
        self.sizing_modes = SizingModes(self.__osbm)
        self.units = Units(self.__osbm)
        self.table_types = TableTypes(self.__osbm, self.__icons)
        self.page_types = PageTypes(self.__osbm, self.__icons)
        self.languages = Languages(self.__osbm)
        self.resizeqt = ResizeQt(self.__osbm)
