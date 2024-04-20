import os

from PySide6.QtWidgets import QWidget

import package.modules.log as log

import package.ui.formimage_ui as formimage_ui

import package.controllers.scrollareainput as scrollareainput

import package.components.dialogwindows as dialogwindows


class FormImage(QWidget):
    def __init__(self, section_index, config_content, config_image, value):
        log.Log.debug_logger(
            f"FormImage(self, section_index, config_content, config_image, value): section_index = {section_index}, config_content = {config_content}, config_image = {config_image}, value = {value}"
        )

        super(FormImage, self).__init__()
        self.ui = formimage_ui.Ui_FormImageWidget()
        self.ui.setupUi(self)

        self.section_index = section_index

        # заголовок
        self.ui.title.setText(config_content["title_content"])
        # поле ввода
        self.ui.label.setText(
            "Изображение выбрано" if value else "Выберите изображение"
        )
        # масштаб
        # TODO
        if True:
            for i in range(self.ui.scale_layout.count()):
                widget = self.ui.scale_layout.itemAt(i).widget()
                if widget is not None:
                    widget.hide()

        # описание
        description_content = config_content["description_content"]
        if description_content:
            self.ui.textbrowser.setHtml(description_content)
        else:
            self.ui.textbrowser.hide()

        # CONFIG IMAGE

        # connect
        self.ui.select_button.clicked.connect(lambda: self.select_image(config_content))

    def select_image(self, config_content):
        log.Log.debug_logger(
            f"select_image(self, config_content): config_content = {config_content}"
        )
        image_dirpath = (
            dialogwindows.DialogWindows.select_image_for_formimage_in_project()
        )
        if image_dirpath:
            self.ui.label.setText(os.path.basename(image_dirpath))
            # TODO Загрузить изображение сразу

            sections_info = scrollareainput.ScroolAreaInput.get_sections_info()
            section_info = sections_info[self.section_index]
            section_data = section_info.get("data")
            section_data[config_content.get("name_content")] = True
