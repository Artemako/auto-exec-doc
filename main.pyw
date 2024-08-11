import package.app as app
import os
import sys


def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()

lol = """
from PySide6.QtCore import QKeySequence
setShortcut(QKeySequence("Ctrl+S"))

self.__obs_manager.obj_sb.set_message(f"{self.windowTitle()}: сохранение прошло успешно!")
"""