import logging
import datetime
import os
from concurrent.futures import ThreadPoolExecutor

class LogObjectsManager:
    def __init__(self, osbm):
        self.obj_dirm = osbm.obj_dirm

class Log:
    def __init__(self):
        self.__osbm = None
        self.__logger = logging.getLogger("Main logger")
        self.__executor = ThreadPoolExecutor(max_workers=2)

    def setting_osbm(self, osbm):
        self.__osbm = LogObjectsManager(osbm)

    def setting_logger(self):
        log_folder = self.__osbm.obj_dirm.get_logs_dirpath()

        log_file = os.path.join(
            log_folder,
            str(datetime.datetime.now().replace(microsecond=0)).replace(":", "-")
            + ".log",
        )

        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        
        # FileHandler для записи логов в файл
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # StreamHandler для вывода логов в консоль
        console_handler = logging.StreamHandler()       
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)      

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(console_handler)
        self.__logger.setLevel(logging.DEBUG)

        self.debug_logger("Config logger")

    def debug_logger(self, message: str):
        self.__executor.submit(self.__logger.debug, f"\033[34m {message}\033[00m")

    def info_logger(self, message: str):
        self.__executor.submit(self.__logger.info, f"\033[32m {message}\033[00m")

    def warning_logger(self, message: str):
        self.__executor.submit(self.__logger.warning, f"\033[93m {message}\033[00m")

    def error_logger(self, message: str):
        self.__executor.submit(self.__logger.error, f"\033[31m {message}\033[00m")

    def critical_logger(self, message: str):
        self.__executor.submit(self.__logger.critical, f"\033[95m {message}\033[00m")

    def disable_logging(self):
        """Отключение логирования, удаление всех обработчиков."""
        handlers = self.__logger.handlers[:]
        for handler in handlers:
            self.__logger.removeHandler(handler)
            # Закрываем обработчик, чтобы освободить ресурсы
            handler.close() 