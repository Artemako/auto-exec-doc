import logging
import datetime
import os

import package.modules.dirpathsmanager as dirpathsmanager


class Log:
    # TODO Посмотреть библиотеку loggerpy
    logger = None

    def __init__(self):
        pass

    @staticmethod
    def create_and_config_logging():
        # название файла для логирования
        name_log = "log_" + str(datetime.datetime.now().replace(microsecond=0)).replace(
            " ", "_"
        )
        directory_log = dirpathsmanager.DirPathManager.get_logs_dirpath()

        Log.logger = logging.getLogger()
        Log.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(
            filename=os.path.join(directory_log, name_log)
        )
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        Log.logger.addHandler(file_handler)

    @staticmethod
    def debug(message):
        Log.logger.debug(message)

    @staticmethod
    def info(message):
        Log.logger.info(message)

    @staticmethod
    def warning(message):
        Log.logger.warning(message)

    @staticmethod
    def error(message):
        Log.logger.error(message)

    @staticmethod
    def critical(message):
        Log.logger.critical(message)
