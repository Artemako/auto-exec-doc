from PySide6.QtCore import QThread, Signal

import comtypes.client
import pythoncom
import os

class MsWordThread(QThread):
    # cигнал для обновления статуса (object - любые объекты, включая None)
    status_changed = Signal(object)

    def __init__(self, obs_manager):
        super().__init__()
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("MsWordThread __init__()")
        self.__status_msword = False

    def run(self):
        self.initialize_msword()

    def initialize_msword(self):
        self.__obs_manager.obj_l.debug_logger("MsWordThread initialize_msword()")
        try:
            pythoncom.CoInitialize()
            self.__status_msword = None
            self.status_changed.emit(self.__status_msword)
            try:
                self.__word = comtypes.client.GetActiveObject("Word.Application")
                self.__status_msword = True
            except Exception as e:
                print(f"Error in initialize_msword(): {e}")
                self.__word = comtypes.client.CreateObject("Word.Application")
                self.__status_msword = True
        except Exception as e:
            print(f"Error in initialize_msword(): {e}")
            self.__status_msword = False
        self.status_changed.emit(self.__status_msword)

    def terminate_msword(self):
        self.__obs_manager.obj_l.debug_logger("MsWordThread terminate_msword()")
        try:
            self.__word.Quit()
        except Exception as e:
            self.__status_msword = False
            raise e
        


class OfficePackets:
    def __init__(self):
        self.__status_msword = False
        self.__status_libreoffice = False

    def setting_all_obs_manager(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("OfficePackets setting_all_obs_manager()")

    def resetting_office_packets(self):
        self.__obs_manager.obj_l.debug_logger("OfficePackets resetting_office_packets()")
        # экземпляр QThread
        if not self.__status_msword:
            self.__msword_thread = MsWordThread(self.__obs_manager)
            # подключение сигнала к слоту и запуск потока
            self.__msword_thread.status_changed.connect(self.update_status_msword)
            self.__msword_thread.start()
        else:
            print("MsWordThread is already running")
        # проверка наличия LibreOffice
        self.run_libreoffice()
        
        
    def update_status_msword(self, status):
        self.__obs_manager.obj_l.debug_logger(
            f"OfficePackets update_status_msword(status):\nstatus = {status}"
        )
        self.__status_msword = status
        if self.__obs_manager.obj_sb.get_is_active():
            self.__obs_manager.obj_sb.update_status_msword_label(self.__status_msword)

    def get_status_msword(self):
        self.__obs_manager.obj_l.debug_logger(
            f"OfficePackets get_status_msword():\nself.__status_msword = {self.__status_msword}"
        )
        return self.__status_msword

    def get_status_libreoffice(self):
        self.__obs_manager.obj_l.debug_logger(
            f"OfficePackets get_status_libreoffice():\nself.__status_libreoffice = {self.__status_libreoffice}"
        )
        return self.__status_libreoffice
    
    def run_libreoffice(self):
        self.__obs_manager.obj_l.debug_logger("OfficePackets run_libreoffice()")
        libreoffice_path = self.__obs_manager.obj_sd.get_libreoffice_path()
        if os.path.exists(libreoffice_path):
            self.__status_libreoffice = True
        else:
            self.__status_libreoffice = False
        if self.__obs_manager.obj_sb.get_is_active():
            self.__obs_manager.obj_sb.update_status_libreoffice_label(
                self.__status_libreoffice
            )

    def terminate_msword(self):
        self.__obs_manager.obj_l.debug_logger("OfficePackets terminate_msword()")
        try:
            self.__msword_thread.terminate_msword()
        except Exception as e:
            self.__obs_manager.obj_l.error_logger("Error in OfficePackets.terminate_msword():\n" + str(e))
        self.__msword_thread.quit()
        self.__msword_thread.wait()
        self.__status_msword = False

    def terminate_libreoffice(self):
        self.__obs_manager.obj_l.debug_logger("OfficePackets terminate_libreoffice()")
        self.__status_libreoffice = False