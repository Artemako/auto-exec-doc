from PySide6.QtWidgets import (
    QWidget
)
from PySide6.QtCore import QTimer, QSize

import package.ui.nedtabletag_ui as nedtabletag_ui

# TODO !!! РАБОТА С ТАБЛИЦАМИ
class NedTableTag(QWidget):
    def __init__(self, obs_manager, type_window, tag = None):
        self.__obs_manager = obs_manager
        self.__type_window = type_window
        self.__tag = tag
        self.__obs_manager.obj_l.debug_logger("NedTableTag __init__(obs_manager, type_window)")
        super(NedTableTag, self).__init__()
        self.ui = nedtabletag_ui.Ui_NedTableTag()
        self.ui.setupUi(self)
        #
        self.__data = {
            "type_table": None,
            "rowcol": None
        }
        #
        self.config_combox_typetable()
        self.config_tw_attrs()
        #
        self.connecting_actions()

    def get_data(self):
        self.__obs_manager.obj_l.debug_logger("NedTableTag get_data()")
        return self.__data

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger("NedTableTag connecting_actions()")
        self.ui.combox_typetable.currentIndexChanged.connect(self.config_tw_attrs)
        self.ui.btn_addrowcol.clicked.connect(self.btn_addrowcol_clicked)

    def btn_addrowcol_clicked(self):
        # TODO btn_addrowcol_clicked 
        ...
    
    def config_combox_typetable(self):
        self.__obs_manager.obj_l.debug_logger("NedTableTag config_combox_typetable()")
        combobox = self.ui.combox_typetable
        combobox.blockSignals(True)
        combobox.clear()
        combobox.addItem("Произвольный", "FULL")
        combobox.addItem("По строкам", "ROW")
        combobox.addItem("По столбцам", "COL")
        index = 0
        if self.__type_window == "edit":
           typetable_config = self.__obs_manager.obj_pd.get_typetable_configs_table_by_tag(self.__tag)
           typetable = typetable_config.get("type_config")
           if typetable == "FULL":
               index = 0
           elif typetable == "ROW":
               index = 1
           elif typetable == "COL":
               index = 2
        combobox.setCurrentIndex(index)
        combobox.blockSignals(False)

    def config_tw_attrs(self):
        self.__obs_manager.obj_l.debug_logger("NedTableTag config_tw_attrs()")
        typetable = self.ui.combox_typetable.currentData()
        if typetable == "FULL":
            self.ui.label_rowcol.setEnabled(False)
            self.ui.tw_attrs.setEnabled(False)
            self.ui.btn_addrowcol.setEnabled(False)
        elif typetable == "ROW":
            self.ui.label_rowcol.setEnabled(True)
            self.ui.tw_attrs.setEnabled(True)
            self.ui.btn_addrowcol.setEnabled(True)
            self.ui.label_rowcol.setText("Строки")
            self.ui.btn_addrowcol.setText("Добавить строку")
            self.config_data_table()
        elif typetable == "COL":
            self.ui.label_rowcol.setEnabled(True)
            self.ui.tw_attrs.setEnabled(True)
            self.ui.btn_addrowcol.setEnabled(True)
            self.ui.label_rowcol.setText("Столбцы")
            self.ui.btn_addrowcol.setText("Добавить столбцец")
            self.config_data_table()

    def config_data_table(self):
        self.__obs_manager.obj_l.debug_logger("NedTableTag config_data_table()")
        table_widget = self.ui.tw_attrs
        table_widget.blockSignals(True)
        table_widget.clear()
        rowcol_configs = self.__obs_manager.obj_pd.get_rowcol_configs_table_by_tag(self.__tag)
        table_widget.setRowCount(len(rowcol_configs))
        for rowcol_config in rowcol_configs:
            value_config = rowcol_config.get("value_config")
            # TODO config_data_table

        table_widget.blockSignals(False)
            

