import os

from PIL import Image as PilImage
from PIL import ExifTags


class ImageResizerObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm
        self.obj_film = osbm.obj_film


class ImageResizer:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = ImageResizerObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer setting_osbm():\nself.__osbm = {self.__osbm}"
        )

    def save_image_then_selected(self, image_dirpath, file_name_with_format):
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer save_image_then_selected(image_dirpath, file_name_with_format):\nimage_dirpath = {image_dirpath} \n file_name_with_format = {file_name_with_format}"
        )
        # пути: к временной папке, к временному файлу
        temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
        temp_file_path = os.path.join(temp_dir, file_name_with_format)
        # Открыть изображение, Сохранить изображение в временный файл
        image = PilImage.open(image_dirpath)
        # Получение EXIF данных
        if hasattr(image, "_getexif"):
            exif = image._getexif()
            if exif is not None:
                for tag, value in exif.items():
                    if ExifTags.TAGS.get(tag) == "Orientation":
                        orientation = value
                        break
                # Корректировка ориентации
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        # Сохранить изображение во временный файл
        image.save(temp_file_path, "PNG")

    def get_sizes_image(self, image_dirpath):
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer get_sizes_image(image_dirpath):\nimage_dirpath = {image_dirpath}"
        )
        image = PilImage.open(image_dirpath)
        width, height = image.size
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer get_sizes_image(image_dirpath) -> tuple:\n result = ({width}, {height})"
        )
        return width, height

    def crop_image(
        self, temp_image, new_width, new_height, container_width, container_height
    ):

        # TODO
        image = PilImage.open(temp_image)
        # Изменяем размер с последующим обрезанием
        image = image.resize((new_width, new_height), PilImage.LANCZOS)
        # Обрезаем изображение до размеров контейнера
        left = (new_width - container_width) // 2
        top = (new_height - container_height) // 2
        right = (new_width + container_width) // 2
        bottom = (new_height + container_height) // 2
        #
        image = image.crop((left, top, right, bottom))
        #
        image.save(temp_image)
