from loggerpy import Logger, Level
import datetime
import os


import package.modules.dirpathsmanager as dirpathsmanager


class Log:
    _logger = Logger()

    def __init__(self):
        pass

    @staticmethod
    def get_logger():
        return Log._logger

    @staticmethod
    def config_logger():
        Log.get_logger().configure(
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
        Log.get_logger().debug(message)

    @staticmethod
    def info_logger(message: str):
        Log.get_logger().info(message)

    @staticmethod
    def warning_logger(message: str):
        Log.get_logger().warning(message)

    @staticmethod
    def error_logger(message: str):
        Log.get_logger().error(message)

    @staticmethod
    def critical_logger(message: str):
        Log.get_logger().critical(message)
