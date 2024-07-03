from loggerpy import Logger, Level
import datetime
import os

class Log:

    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__logger = Logger()

    def config_logger(self):
        self.__logger.configure(
            name="Main logger",
            log_folder=os.path.join(
                self.__obs_manager.obj_dpm.get_logs_dirpath(),
                str(datetime.datetime.now().replace(microsecond=0)).replace(":", "-"),
            ),
            print_level=Level.DEBUG,
            save_level=Level.DEBUG,
        )
        self.debug_logger("Config logger")

    def debug_logger(self, message: str):
        self.__logger.debug(message)

    def info_logger(self, message: str):
        self.__logger.info(message)

    def warning_logger(self, message: str):
        self.__logger.warning(message)

    def error_logger(self, message: str):
        self.__logger.error(message)

    def critical_logger(self, message: str):
        self.__logger.critical(message)

    # TODO Действие очистить логи


# obj_l = Log()
