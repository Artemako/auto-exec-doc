from PySide6.QtWidgets import QDialog, QSizePolicy

import package.ui.nednodedialogwindow_ui as nednodedialogwindow_ui

class NedNodeDialogWindow(QDialog):
    def __init__(self, osbm, type_window, type_node, nodes, node=None):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow __init__(osbm, type_window, type_node, nodes, node):\ntype_window = {type_window}\ntype_node = {type_node}\nnodes = {nodes}\nnode = {node}"
        )
        self.__type_window = type_window
        self.__type_node = type_node
        self.__nodes = nodes
        self.__node = node
        super(NedNodeDialogWindow, self).__init__()
        self.ui = nednodedialogwindow_ui.Ui_NedNodeDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__osbm.obj_comwith.resizeqt.set_temp_max_height(self)
        #
        self.__data = []
        # одноразовые действия
        self.config_maindata()
        self.config_placementdata()
        self.connecting_actions()


    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def get_project_and_group_nodes(self) -> list:
        nodes = []
        for node in self.__nodes:
            if node.get("type_node") == "PROJECT" or node.get("type_node") == "GROUP":
                nodes.append(node)
        # сортирока
        nodes.sort(key=lambda node: int(node.get("order_node")))
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_project_and_group_nodes nodes = {nodes}"
        )
        return nodes


    def config_maindata(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow config_maindata()")
        if self.__type_window == "create":
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название новой формы")
                self.ui.btn_nesvariable.setText("Добавить форму")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название новой группы")
                self.ui.btn_nesvariable.setText("Добавить группу")
        elif self.__type_window == "edit":
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название формы")
                self.ui.btn_nesvariable.setText("Сохранить форму")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название группы")
                self.ui.btn_nesvariable.setText("Сохранить группу")
            # заполняем форму
            self.ui.lineedit_namenode.setText(self.__node.get("name_node"))

    def config_placementdata(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow config_placementdata()")
        # заполняем combobox'ы
        self.fill_combox_parent()
        self.fill_combox_neighboor()

    def fill_combox_parent(self):
        self.__osbm.obj_logg.debug_logger(
            "NedNodeDialogWindow fill_combox_parent()"
        )
        combobox = self.ui.combox_parent
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        index = 0
        project_and_group_nodes = self.get_project_and_group_nodes()
        for prgr_node in project_and_group_nodes:
            # проверка на одинаковые вершины
            if self.__type_window == "create":
                combobox.addItem(prgr_node.get("name_node"), prgr_node)
            else:
                # поиск соседа
                if prgr_node.get("id_node") == self.__node.get("id_parent"):
                    current_index = index
                # проверка на одинаковые вершины
                if prgr_node.get("id_node") != self.__node.get("id_node"):
                    combobox.addItem(prgr_node.get("name_node"), prgr_node)
                    index += 1
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def get_childs(self, parent_node):
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_childs(parent_node):\nparent_node = {parent_node}"
        )
        # сортировка была сделана при получении данных с БД
        childs = list(
            filter(
                lambda node: node.get("id_parent") == parent_node.get("id_node"),
                self.__nodes,
            )
        )
        # сортировка тут нужна из-за reconfig()
        childs.sort(key=lambda node: int(node.get("order_node")))

        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_childs(parent_node):\nparent_node = {parent_node}\nchilds = {childs}"
        )
        return childs

    def fill_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow combox_neighboor()")
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        parent_node = self.ui.combox_parent.currentData()
        if parent_node:
            combobox.addItem("- В начало -", "START")
            childs_nodes = self.get_childs(parent_node)
            if self.__type_window == "create":
                for index, child_node in enumerate(childs_nodes):
                    combobox.addItem("После: " + child_node.get("name_node"), child_node)
            else:
                for index, child_node in enumerate(childs_nodes):
                    if self.__node.get("id_node") != child_node.get("id_node"):
                        combobox.addItem("После: " + child_node.get("name_node"), child_node)
                    else:
                        current_index = index
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def connecting_actions(self):
        self.ui.btn_nesvariable.clicked.connect(self.action_nesvariable)
        self.ui.btn_nesvariable.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.combox_parent.currentIndexChanged.connect(self.fill_combox_neighboor)
        
    def action_nesvariable(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow action_nesvariable()")
        name_node = self.ui.lineedit_namenode.text()
        if len(name_node) > 0:
            node_by_name = self.__osbm.obj_prodb.get_node_by_name(name_node)
            print(f"node_by_name = {node_by_name}")
            if self.__type_window == "create":
                if not node_by_name:
                    self.add_new_node()
                    self.accept()
                else:
                    msg = "Другая вершина с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)
                
            elif self.__type_window == "edit":
                if not node_by_name:
                    self.save_edit_node()
                    self.accept()
                elif self.__node.get("name_node") == name_node:
                    # ↑ если имя переменной не изменилось
                    self.save_edit_node()
                    self.accept()
                else:
                    msg = "Другая вершина с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)
        else:
            msg = "Заполните поле названия!"
            self.__osbm.obj_dw.warning_message(msg)

    def save_edit_node(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow save_edit_node()")
        self.__data = []
        self.edit_data(True)

    def get_edit_old_nodes_when_is_edit(self, id_old_parent_node) -> list:
        self.__osbm.obj_logg.debug_logger(
            f"NedNodeDialogWindow get_edit_old_nodes_when_is_edit(id_old_parent_node):\nid_old_parent_node = {id_old_parent_node}"
        )
        edit_old_nodes = []
        # обертка для функции
        old_parent_wrap_node = {
            "id_node": id_old_parent_node
        }
        old_childs_nodes = self.get_childs(old_parent_wrap_node)
        # цикл по старой группе
        index = 0
        for child_node in old_childs_nodes:
            if child_node.get("id_node") != self.__node.get("id_node"):
                child_node["order_node"] = index
                edit_old_nodes.append(child_node)
                index += 1
            else:
                # заменить пустышкой для childs_nodes.insert()
                edit_old_nodes.append("WRAPPER")
        return edit_old_nodes

    def edit_data(self, is_edit = True): 
        self.__osbm.obj_logg.debug_logger(f"NedNodeDialogWindow edit_data(is_edit):\nis_edit = {is_edit}")
        #
        id_old_parent_node = self.__node.get("id_parent")
        edit_old_nodes = []
        # для edit
        if is_edit:
            edit_old_nodes = self.get_edit_old_nodes_when_is_edit(id_old_parent_node)
        # для create
        new_parent_node = self.ui.combox_parent.currentData()
        if new_parent_node:
            id_new_parent_node = new_parent_node.get("id_node")
            # проверка на одинаковых родитилей
            childs_nodes = []
            if id_new_parent_node == id_old_parent_node:
                childs_nodes = edit_old_nodes
            else:
                # не забудем про изменения в старой группе
                for node in edit_old_nodes:
                    self.__data.append(node)
                # новая группа
                childs_nodes = self.get_childs(new_parent_node)
            # сосед в новой группе
            neighboor_node = self.ui.combox_neighboor.currentData()
            if neighboor_node:
                # вставка вершины в группу
                self.__node["name_node"] = self.ui.lineedit_namenode.text()
                self.__node["id_parent"] = new_parent_node.get("id_node")
                if neighboor_node == "START":
                    # вставить в самое начало
                    childs_nodes.insert(0, self.__node)
                else:
                    # вставить после соседа
                    neighboor_index = int(neighboor_node.get("order_node")) + 1
                    childs_nodes.insert(neighboor_index, self.__node)
                # цикл по новой группе
                index = 0
                for child_node in childs_nodes:
                    if child_node != "WRAPPER":
                        child_node["order_node"] = index
                        self.__data.append(child_node)
                        index += 1
        

    def add_new_node(self):
        self.__osbm.obj_logg.debug_logger("NedNodeDialogWindow add_new_node()")
        # подготовка данных
        self.__node = {
            "id_active_template": None,
            "id_node": -111,
            "id_parent": None,
            "included": 1,
            "name_node": None,
            "order_node": None,
            "type_node": self.__type_node,
        }
        # 
        self.__data = []
        self.edit_data(False)
