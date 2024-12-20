from PySide6.QtCore import QThread, Signal

import traceback
import comtypes.client
import pythoncom
import os
import threading

class MsWordThread(QThread):
    # cигнал для обновления статуса (object - любые объекты, включая None)
    status_changed = Signal(object)

    def __init__(self, osbm):
        super().__init__()
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("MsWordThread __init__()")
        self.__status_msword = False

    def run(self):
        self.initialize_msword()

    def get_active_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread get_active_msword()")
        try:
            pythoncom.CoInitialize()
            self.__word = comtypes.client.GetActiveObject("Word.Application")
            self.__status_msword = True
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in get_active_msword(): {e} ? {traceback.format_exc()}")
        

    def initialize_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread initialize_msword()")
        try:
            pythoncom.CoInitialize()
            self.__status_msword = None
            self.status_changed.emit(self.__status_msword)
            #
            thread = threading.Thread(target=self.get_active_msword)
            thread.start()
            # ждём 3 секунды
            thread.join(3)
            if thread.is_alive() or not self.__status_msword:
                self.__word = comtypes.client.CreateObject("Word.Application")
                # TODO dynamic=True
                self.__status_msword = True
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in initialize_msword(): {e} ? {traceback.format_exc()}")
            self.__status_msword = False
        self.status_changed.emit(self.__status_msword)


    def terminate_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread terminate_msword()")
        try:
            self.__word.Quit()
        except Exception as e:
            self.__status_msword = False
            raise e
        


class OfficePackets:
    def __init__(self):
        self.__status_msword = False
        self.__status_libreoffice = False

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("OfficePackets setting_all_osbm()")

    def resetting_office_packets(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets resetting_office_packets()")
        # экземпляр QThread
        if not self.__status_msword:
            self.__msword_thread = MsWordThread(self.__osbm)
            # подключение сигнала к слоту и запуск потока
            self.__msword_thread.status_changed.connect(self.update_status_msword)
            self.__msword_thread.start()
        else:
            print("MsWordThread is already running")
        # проверка наличия LibreOffice
        self.run_libreoffice()
        
        
    def update_status_msword(self, status):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets update_status_msword(status):\nstatus = {status}"
        )
        self.__status_msword = status
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_msword_label(self.__status_msword)

    def get_status_msword(self):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets get_status_msword():\nself.__status_msword = {self.__status_msword}"
        )
        return self.__status_msword

    def get_status_libreoffice(self):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets get_status_libreoffice():\nself.__status_libreoffice = {self.__status_libreoffice}"
        )
        return self.__status_libreoffice
    
    def run_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets run_libreoffice()")
        libreoffice_path = self.__osbm.obj_setdb.get_libreoffice_path()
        if os.path.exists(libreoffice_path):
            self.__status_libreoffice = True
        else:
            self.__status_libreoffice = False
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_libreoffice_label(
                self.__status_libreoffice
            )

    def terminate_msword(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets terminate_msword()")
        try:
            self.__msword_thread.terminate_msword()
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in OfficePackets.terminate_msword():\n {e}  ? {traceback.format_exc()}")
        self.__msword_thread.quit()
        self.__msword_thread.wait()
        self.__status_msword = False

    def terminate_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets terminate_libreoffice()")
        self.__status_libreoffice = False


    def run_individual_msword(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets run_individual_msword()")
        def run_msword():
            try:
                word = comtypes.client.CreateObject("Word.Application")
            except Exception as e:
                self.__osbm.obj_logg.error_logger(
                    f"OfficePackets run_individual_msword():\nerror = {e} ? {traceback.format_exc()}"
                )
        individual_thread = threading.Thread(target=run_msword)
        individual_thread.start()
