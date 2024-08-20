import os
import datetime
from PIL import Image

from PySide6.QtWidgets import QWidget

import package.ui.formimage_ui as formimage_ui


class FormImage(QWidget):
    def __init__(self, osbm, pair, current_tag, config_dict):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_tag = current_tag
        self.__config_dict = config_dict
        self.__osbm.obj_logg.debug_logger(
            f"FormImage __init__(self, pair, current_tag, config_dict):\npair = {pair},\ncurrent_tag = {current_tag},\nconfig_dict = {config_dict}"
        )
        super(FormImage, self).__init__()
        self.ui = formimage_ui.Ui_FormImageWidget()
        self.ui.setupUi(self)
        # ИКОНКИ
        self.__icons = self.__osbm.obj_icons.get_icons()
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.config()

    def config(self):
        self.__osbm.obj_logg.debug_logger("FormImage config()")
        # тип тега
        key_icon = self.__osbm.obj_icons.get_key_icon_by_type_tag(self.__current_tag.get("type_tag"))
        qicon_type_tag = self.__icons.get(key_icon)
        self.ui.label_typetag.setPixmap(qicon_type_tag)
        # заголовок
        self.ui.title.setText(self.__current_tag.get("title_tag"))
        # поле ввода
        self.ui.label.setText(
            "Изображение успешно выбрано"
            if self.__pair.get("value_pair")
            else "Выберите изображение"
        )
        # масштаб
        if True:
            for i in range(self.ui.scale_layout.count()):
                widget = self.ui.scale_layout.itemAt(i).widget()
                if widget is not None:
                    widget.hide()

        # описание
        description_tag = self.__current_tag.get("description_tag")
        if description_tag:
            self.ui.textbrowser.setHtml(description_tag)
        else:
            self.ui.textbrowser.hide()

        # CONFIG IMAGE
        # TODO Сделать масштаб изображения

        # connect
        self.ui.select_button.clicked.connect(lambda: self.set_new_value_in_pair())

    def set_new_value_in_pair(self):
        self.__osbm.obj_logg.debug_logger("FormImage set_new_value_in_pair()")
        image_dirpath = (
            self.__osbm.obj_dw.select_image_for_formimage_in_project()
        )
        if image_dirpath:
            # текст выбранного изображения
            self.ui.label.setText(os.path.basename(image_dirpath))
            # имя нового изображения
            file_name = f"img_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            file_name_with_png = f"{file_name}.png"

            # путь к временной папке
            temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
            # Путь к временному файлу
            temp_file_path = os.path.join(temp_dir, file_name_with_png)
            # Открыть изображение
            image = Image.open(image_dirpath)
            # Сохранить изображение в временный файл
            image.save(temp_file_path, "PNG")
            # Вывести путь к временному файлу
            print("Изображение сохранено в временную папку:", temp_file_path)
            self.__pair["value_pair"] = file_name_with_png
