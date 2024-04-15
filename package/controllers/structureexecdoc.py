import package.modules.log as log


class StructureExecdoc:
    _treewidget_structure_execdoc = None

    def __init__(self):
        pass

    @staticmethod
    def set_tr_sed(tr_sed):
        log.Log.get_logger().debug("set_tr_sed()")
        StructureExecdoc._treewidget_structure_execdoc = tr_sed

    @staticmethod
    def get_tr_sed() -> object:
        log.Log.get_logger().debug("get_tr_sed() -> object")
        return StructureExecdoc._treewidget_structure_execdoc

    @staticmethod
    def connect_structureexecdoc(tr_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        log.Log.get_logger().debug("IN connect_structureexecdoc()")
        StructureExecdoc.set_tr_sed(tr_sed)

        # TODO

    @staticmethod
    def clear_tr_sed():
        log.Log.get_logger().debug("clear_tr_sed()")
        StructureExecdoc.get_tr_sed().clear()
