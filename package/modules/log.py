from loggerpy import Logger, Level
import datetime
import os


import package.modules.dirpathsmanager as dirpathsmanager


class Log:
    __logger = Logger()

    def __init__(self):
        pass


    @staticmethod
    def config_logger():
        Log.__logger.configure(
            name="Main logger",
            log_folder=os.path.join(
                dirpathsmanager.DirPathManager.get_logs_dirpath(),
                str(datetime.datetime.now().replace(microsecond=0)).replace(":", "-"),
            ),
            print_level=Level.DEBUG,
            save_level=Level.DEBUG,
        )
        Log.debug_logger("Config logger")

    @staticmethod
    def debug_logger(message: str):
        Log.__logger.debug(message)

    @staticmethod
    def info_logger(message: str):
        Log.__logger.info(message)

    @staticmethod
    def warning_logger(message: str):
        Log.__logger.warning(message)

    @staticmethod
    def error_logger(message: str):
        Log.__logger.error(message)

    @staticmethod
    def critical_logger(message: str):
        Log.__logger.critical(message)

    # TODO Действие очистить логи
