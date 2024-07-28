import os
import datetime
from PIL import Image

from PySide6.QtWidgets import QWidget

import package.ui.formimage_ui as formimage_ui


class FormImage(QWidget):
    def __init__(self, obs_manager, pair, config_tag, config_image):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            f"FormImage __init__(self, pair, config_tag, config_image):\npair = {pair},\nconfig_tag = {config_tag},\nconfig_image = {config_image}"
        )

        super(FormImage, self).__init__()
        self.ui = formimage_ui.Ui_FormImageWidget()
        self.ui.setupUi(self)

        # заголовок
        self.ui.title.setText(config_tag["title_tag"])
        # поле ввода
        self.ui.label.setText(
            "Изображение успешно выбрано" if pair.get("value") else "Выберите изображение"
        )
        # масштаб
        # TODO Сделать масштаб изображения
        if True:
            for i in range(self.ui.scale_layout.count()):
                widget = self.ui.scale_layout.itemAt(i).widget()
                if widget is not None:
                    widget.hide()

        # описание
        description_tag = config_tag["description_tag"]
        if description_tag:
            self.ui.textbrowser.setHtml(description_tag)
        else:
            self.ui.textbrowser.hide()

        # CONFIG IMAGE

        # connect
        self.ui.select_button.clicked.connect(lambda: self.set_new_value_in_pair(pair))

    def set_new_value_in_pair(self, pair):
        self.__obs_manager.obj_l.debug_logger(f"FormImage set_new_value_in_pair(self, pair): pair = {pair}")
        image_dirpath = self.__obs_manager.obj_dw.select_image_for_formimage_in_project()
        # TODO Сделать удаление предыдущего изображения (при сохранении)
        if image_dirpath:
            # текст выбранного изображения
            self.ui.label.setText(os.path.basename(image_dirpath))  
            # имя нового изображения
            file_name = f"img_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            file_name_with_png = f"{file_name}.png"       

            # путь к временной папке
            temp_dir = self.__obs_manager.obj_dpm.get_temp_dirpath()
            # Путь к временному файлу
            temp_file_path = os.path.join(temp_dir, file_name_with_png)
            # Открыть изображение
            image = Image.open(image_dirpath)
            # Сохранить изображение в временный файл
            image.save(temp_file_path, "PNG")
            # Вывести путь к временному файлу
            print("Изображение сохранено в временную папку:", temp_file_path)
            pair["value"] = file_name_with_png
