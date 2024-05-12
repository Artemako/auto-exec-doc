from loggerpy import Logger, Level
import datetime
import os


import package.modules.dirpathsmanager as dirpathsmanager


class Log:
    def __init__(self):
        self.__logger = Logger()

    def config_logger(self):
        obj_l.__logger.configure(
            name="Main logger",
            log_folder=os.path.join(
                dirpathsmanager.obj_dpm.get_logs_dirpath(),
                str(datetime.datetime.now().replace(microsecond=0)).replace(":", "-"),
            ),
            print_level=Level.DEBUG,
            save_level=Level.DEBUG,
        )
        obj_l.debug_logger("Config logger")

    def debug_logger(self, message: str):
        obj_l.__logger.debug(message)

    def info_logger(self, message: str):
        obj_l.__logger.info(message)

    def warning_logger(self, message: str):
        obj_l.__logger.warning(message)

    def error_logger(self, message: str):
        obj_l.__logger.error(message)

    def critical_logger(self, message: str):
        obj_l.__logger.critical(message)

    # TODO Действие очистить логи


obj_l = Log()
