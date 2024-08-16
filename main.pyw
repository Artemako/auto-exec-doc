import package.app as app
import os
import sys

# TODO Полный экран для QDialog
def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()

# setShortcut("Ctrl+S")
# setShortcut("Ctrl+Q")
# self.__obs_manager.obj_sb.set_message(f"{self.windowTitle()}: добавление прошло успешно!")
# self.__obs_manager.obj_sb.set_message(f"{self.windowTitle()}: сохранение прошло успешно!")