import os
from docx.shared import Length


class ConverterVarImage:
    """
    Зависимый от Converter класс.
    """

    def __init__(self, osbm):
        self.__osbm = osbm

    def get_original_image_path_by_file_name_with_png(self, file_name_with_png) -> str:
        # получить путь к изображению
        original_image_path = os.path.abspath(
            os.path.join(
                self.__osbm.obj_dirm.get_images_folder_dirpath(),
                file_name_with_png,
            )
        )
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_original_image_path_by_file_name_with_png() -> str:\n result = {original_image_path}"
        )
        return original_image_path

    def get_temp_image_path(self, file_name_with_png) -> str:
        # путь к временному файлу
        temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
        temp_file_path = os.path.join(temp_dir, file_name_with_png)
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_temp_image_path() -> str:\n result = {temp_file_path}"
        )
        return temp_file_path

    def get_temp_image(self, file_name_with_png) -> str:
        # пути
        original_image_path = self.get_original_image_path_by_file_name_with_png(
            file_name_with_png
        )
        temp_file_path = self.get_temp_image_path(file_name_with_png)
        # копирование
        self.__osbm.obj_film.copy_file(original_image_path, temp_file_path)
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_temp_image(file_name_with_png) -> str:\nfile_name_with_png = {file_name_with_png} \n result = {temp_file_path}"
        )
        #
        return temp_file_path

    def get_emu_width_and_height_by_unit(self, unit, width, height) -> tuple:
        emu_width = float()
        emu_height = float()
        #
        if unit == "MM":
            emu_width = width * Length._EMUS_PER_MM
            emu_height = height * Length._EMUS_PER_MM
        elif unit == "CM":
            emu_width = width * Length._EMUS_PER_CM
            emu_height = height * Length._EMUS_PER_CM
        elif unit == "INCH":
            emu_width = width * Length._EMUS_PER_INCH
            emu_height = height * Length._EMUS_PER_INCH
        elif unit == "PT":
            emu_width = width * Length._EMUS_PER_PT
            emu_height = height * Length._EMUS_PER_PT
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_emu_width_and_height_by_unit() -> tuple:\n result = ({emu_width}, {emu_height})"
        )
        #
        return emu_width, emu_height

    def get_mm_width_and_height_by_emu(self, emu_width, emu_height) -> tuple:
        mm_width = emu_width / float(Length._EMUS_PER_MM)
        mm_height = emu_height / float(Length._EMUS_PER_MM)
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage get_mm_width_and_height_by_emu() -> tuple:\n result = ({mm_width}, {mm_height})"
        )
        #
        return mm_width, mm_height

    def contain_sizing_mode(self, temp_image, mm_width, mm_height) -> tuple:
        # размеры изображения
        image_width, image_height = self.__osbm.obj_imgr.get_sizes_image(temp_image)
        # коэффициенты
        width_ratio = mm_width / image_width
        height_ratio = mm_height / image_height
        # минимальный коэффициент
        scale_factor = min(width_ratio, height_ratio)
        # новый размеры
        scaled_mm_width = image_width * scale_factor
        scaled_mm_height = image_height * scale_factor
        #
        self.__osbm.obj_logg.debug_logger(
            f"ConverterVarImage contain_sizing_mode() -> tuple:\n result = ({scaled_mm_width}, {scaled_mm_height})"
        )
        #
        return scaled_mm_width, scaled_mm_height

    def cover_sizing_mode(self, temp_image, mm_width, mm_height) -> tuple:
        # размеры изображения
        image_width, image_height = self.__osbm.obj_imgr.get_sizes_image(temp_image)
        # 
        height = 1000
        width_a = (image_width / image_height) * height
        width_b = (mm_width / mm_height) * height
        # новый уменьшенный размер
        if width_a > width_b:
            new_image_width = image_height * (mm_height / mm_width)
            new_image_height = image_height
        else:
            new_image_width = image_width
            new_image_height = image_width * (mm_width / mm_height)
        #
        self.__osbm.obj_imgr.crop_image(temp_image, image_width, image_height, new_image_width, new_image_height)
        #
        self.__osbm.obj_logg.debug_logger(f"ConverterVarImage cover_sizing_mode() -> tuple:\n result = ({new_image_width}, {new_image_height})")
        #
        return mm_width, mm_height
        






        