

import resources_rc

class ComboxTemplates:
    def __init__(self):
        self.__combox_templates = None

    def setting_all_obs_manager(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("ComboxTemplates setting_all_obs_manager()")

    def connect_combox_templates(self, combox_templates):
        self.__obs_manager.obj_l.debug_logger(f"ComboxTemplates connect_combox_templates(combox_templates):\ncombox_templates = {combox_templates}")
        self.__combox_templates = combox_templates
        # Очистить при запуске
        self.clear_comboxts()
        # Подключение сигналов
        self.__combox_templates.currentIndexChanged.connect(lambda index: self.combox_templates_changed(index))

    def combox_templates_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(f"ComboxTemplates combox_templates_changed(index):\nindex = {index}")
        template = self.__combox_templates.itemData(index)
        # сохранить активный шаблон для БД вершины 
        id_parent_node = template.get("id_parent_node")
        id_template = template.get("id_template")
        self.__obs_manager.obj_pd.set_active_template_for_node_by_id(id_parent_node, id_template)
        # обновить cтраницы
        self.__obs_manager.obj_lwpt.update_pages_template(template)

    def clear_comboxts(self):
        self.__combox_templates.blockSignals(True)
        self.__combox_templates.clear()
        self.__combox_templates.blockSignals(False)

    def update_combox_templates(self, node):
        self.clear_comboxts()
        self.__combox_templates.blockSignals(True)
        id_node = node.get("id_node")
        id_active_template = node.get("id_active_template")
        wrap_node = {
            "id_node": id_node
        }
        templates = self.__obs_manager.obj_pd.get_templates_by_form(wrap_node)
        index = 0
        for i, template in enumerate(templates):
            if template.get("id_template") == id_active_template:
                index = i
            self.__combox_templates.addItem(template.get("name_template"), template)
        self.__combox_templates.setCurrentIndex(index)
        # обновить cтраницы
        current_template = self.__combox_templates.itemData(index)
        self.__obs_manager.obj_lwpt.update_pages_template(current_template)
        self.__combox_templates.blockSignals(False)  
