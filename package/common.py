# Ошибки
class Errors:
    class MsWordError(Exception):
        pass

    class LibreOfficeError(Exception):
        pass

    def __init__(self):
        self.MsWordError = Errors.MsWordError
        self.LibreOfficeError = Errors.LibreOfficeError

#
# 
#

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
        self.__osbm.obj_logg.debug_logger("TagTypes get_tag_types()")
        return self.__tag_types
    
    def get_index_by_type_tag(self, type_tag):
        result = None
        for tag in self.__tag_types:
            if tag.type_tag == type_tag:
                result = tag.index
                break
        self.__osbm.obj_logg.debug_logger(
            f"TagTypes get_index_by_type_tag(type_tag):\ntype_tag = {type_tag}\n result = {result}"
        )
        return result
    
#
# 
#

class Unit:
    def __init__(self, index, name_unit, data_unit):
        self.index = index
        self.name_unit = name_unit
        self.data_unit = data_unit

class Units:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__units = [
            Unit(0, "Миллиметр (Millimeter)", "MM"),
            Unit(1, "Сантиметр (Centimeter)", "CM"),
            Unit(2, "Дюйм (Inch)", "INCH"),
            Unit(3, "Пункт (Point)", "PIXEL")
        ]

    def get_units(self):
        self.__osbm.obj_logg.debug_logger("Units get_units()")
        return self.__units
    
    def get_unit_by_data_unit(self, data_unit):
        result = None
        for unit in self.__units:
            if unit.data_unit == data_unit:
                result = unit
                break
        self.__osbm.obj_logg.debug_logger(
            f"Units get_unit_by_data_unit(data_unit):\ndata_unit = {data_unit}\n result = {result}"
        )
        return result

#
# 
#

class SizingMode:
    def __init__(self, index, name_sizing_mode, data_sizing_mode, is_wh):
        self.index = index
        self.name_sizing_mode = name_sizing_mode
        self.data_sizing_mode = data_sizing_mode
        self.is_wh = is_wh

class SizingModes:
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__sizing_modes = [
            SizingMode(0, "Без изменений", "NOCHANGES", False),
            SizingMode(1, "Вместить без изменения пропорций", "CONTAIN", True),
            SizingMode(2, "Заполнить без изменения пропорций", "COVER", True),
            SizingMode(3, "Растянуть с изменением пропорций", "FILL", True)
        ]

    def get_sizing_modes(self):
        self.__osbm.obj_logg.debug_logger("SizingModes get_sizing_modes()")
        return self.__sizing_modes

    def get_sizing_mode_by_data_sizing_mode(self, data_sizing_mode):
        result = None
        for sizing_mode in self.__sizing_modes:
            if sizing_mode.data_sizing_mode == data_sizing_mode:
                result = sizing_mode
                break
        self.__osbm.obj_logg.debug_logger(
            f"SizingModes get_sizing_mode_by_data_sizing_mode(data_sizing_mode):\ndata_sizing_mode = {data_sizing_mode}\n result = {result}"
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


class Common:

    def __init__(self):
        self.__osbm = None
        # без __osbm
        self.errors = None
        # с __osbm
        self.tag_types = None
        self.sizing_modes = None
        self.units = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("Common setting_all_osbm()")
        
    def run(self):
        self.__osbm.obj_logg.debug_logger("Common run()")
        # без __osbm
        self.errors = Errors()
        # с __osbm
        self.tag_types = TagTypes(self.__osbm)
        self.sizing_modes = SizingModes(self.__osbm)
        self.units = Units(self.__osbm)
