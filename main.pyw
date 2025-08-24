import package.app as app
import os
import sys

def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()

# self.__osbm.obj_stab.set_message(f"{self.windowTitle()}: добавление прошло успешно!")
# # self.__osbm.obj_stab.set_message(f"{self.windowTitle()}: сохранение прошло успешно!")

# 2025-05-26 10:30:47,716 - ERROR -  Error in OfficePackets.terminate_msword():
#  'MsWordThread' object has no attribute '_MsWordThread__word'  ? Traceback (most recent call last):
#   File "d:\projects\auto-exec-doc\package\modules\officepackets.py", line 121, in terminate_msword
#     self.__msword_thread.terminate_msword()
#   File "d:\projects\auto-exec-doc\package\modules\officepackets.py", line 59, in terminate_msword
#     raise e
#   File "d:\projects\auto-exec-doc\package\modules\officepackets.py", line 56, in terminate_msword
#     self.__word.Quit()
# AttributeError: 'MsWordThread' object has no attribute '_MsWordThread__word'