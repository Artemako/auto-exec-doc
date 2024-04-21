from PySide6.QtWidgets import QWidget, QTableWidgetItem

import package.modules.log as log

import package.ui.formtable_ui as formtable_ui

import package.controllers.scrollareainput as scrollareainput


class FormTable(QWidget):
    def __init__(self, section_index, config_content, config_table, value):
        log.Log.debug_logger(
            f"FormTable(self, section_index, config_content, config_table, value): section_index = {section_index}, config_content = {config_content}, config_table = {config_table}, value = {value}"
        )

        super(FormTable, self).__init__()
        self.ui = formtable_ui.Ui_FormTableWidget()
        self.ui.setupUi(self)

        # self к этим section_index, config_content, config_table, value
        self.section_index = section_index
        self.config_content = config_content
        self.config_table = config_table
        self.value = value

        self.labels = []
        # self.content = []

        # заголовок
        self.ui.title.setText(self.config_content["title_content"])

        # описание
        description_content = self.config_content["description_content"]
        if description_content:
            self.ui.textbrowser.setHtml(description_content)
        else:
            self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из self.config_table        
        for config in self.config_table:
            type_config = config.get("type_config")
            value_config = config.get("value_config")
            if type_config == "HEADER":
                self.labels.append(value_config)
            # elif type_config == "CONTENT":
            #     self.content.append(value_config)


        self.ui.table.setColumnCount(len(self.labels))
        self.ui.table.setHorizontalHeaderLabels(self.labels)

        # поставить значения из таблицы
        self.create_table_from_json_data()
        
        # connect
        self.ui.add_button.clicked.connect(self.add_row)
        self.ui.delete_button.clicked.connect(self.delete_row)
        self.ui.table.cellChanged.connect(lambda: self.set_value_in_sections_info())

    def add_row(self):
        row_count = self.ui.table.rowCount()
        self.ui.table.insertRow(row_count)
        for column in range(self.ui.table.columnCount()):
            item = QTableWidgetItem()
            self.ui.table.setItem(row_count, column, item)

    def delete_row(self):
        current_row = self.ui.table.currentRow()
        if current_row >= 0:
            self.ui.table.removeRow(current_row)

    # def update_cell(self, row, column):
    #     item = self.ui.table.item(row, column)
    #     if item:
    #         print(f"Cell ({row}, {column}) changed to {item.text()}")
        
    def to_json(self) -> list:
        log.Log.debug_logger("IN to_json(self) -> list:" )
        data = []
        for row in range(self.ui.table.rowCount()):
            row_data = []
            for column in range(self.ui.table.columnCount()):
                item = self.ui.table.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        print(f"data = {data}")
        return data


    def create_table_from_json_data(self):
        log.Log.debug_logger(
            "IN create_table_from_json_data(self):"
        )
        if self.value:
            self.ui.table.setRowCount(len(self.value))
            self.ui.table.setColumnCount(len(self.value[0]))
            for row, row_data in enumerate(self.value):
                for column, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    self.ui.table.setItem(row, column, item)


    def set_value_in_sections_info(self):
        log.Log.debug_logger(
            "set_value_in_sections_info(self):"
        )
        
        sections_info = scrollareainput.ScroolAreaInput.get_sections_info()
        section_info = sections_info[self.section_index]
        section_data = section_info.get("data")
        section_data[self.config_content.get("name_content")] = self.to_json()