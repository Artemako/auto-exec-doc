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

    def save_image_then_selected(self, image_dirpath, file_name_with_png):
        self.__osbm.obj_logg.debug_logger(
            f"ImageResizer save_image_then_selected(image_dirpath, file_name_with_png):\nimage_dirpath = {image_dirpath} \n file_name_with_png = {file_name_with_png}"
        )
        # пути: к временной папке, к временному файлу
        temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
        temp_file_path = os.path.join(temp_dir, file_name_with_png)
        # Открыть изображение, Сохранить изображение в временный файл
        image = PilImage.open(image_dirpath)
        # Получение EXIF данных
        if hasattr(image, '_getexif'):
            exif = image._getexif()
            if exif is not None:
                for tag, value in exif.items():
                    if ExifTags.TAGS.get(tag) == 'Orientation':
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

