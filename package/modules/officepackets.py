from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QTimer

import traceback
import comtypes.client
import pythoncom
import os
import threading
import time

class MsWordThread(QThread):
    # cигнал для обновления статуса (object - любые объекты, включая None)
    status_changed = Signal(object)

    def __init__(self, osbm):
        super().__init__()
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("MsWordThread __init__()")
        self.__status_msword = False
        self.__word = None

    def run(self):
        self.initialize_msword()

    def get_active_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread get_active_msword()")
        try:
            pythoncom.CoInitialize()
            self.__word = comtypes.client.GetActiveObject("Word.Application")
            self.__status_msword = True
        except Exception as e:
            self.__osbm.obj_logg.debug_logger(f"No active Word instance: {e}")
            self.__status_msword = False
            

    def initialize_msword(self):
        self.__osbm.obj_logg.debug_logger("MsWordThread initialize_msword()")
        try:
            pythoncom.CoInitialize()
            self.__status_msword = None
            self.status_changed.emit(self.__status_msword)
            
            thread = threading.Thread(target=self.get_active_msword)
            thread.start()
            thread.join(3)
            
            if thread.is_alive() or not self.__status_msword:
                try:
                    self.__word = comtypes.client.CreateObject("Word.Application")
                    self.__status_msword = True
                except Exception as create_error:
                    self.__osbm.obj_logg.error_logger(f"Error creating Word.Application: {create_error}")
                    self.__status_msword = False
                    
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in initialize_msword(): {e} ? {traceback.format_exc()}")
            self.__status_msword = False
        finally:
            self.status_changed.emit(self.__status_msword)

    def test_word_connection(self):
        """Проверяет, работает ли соединение с Word"""
        try:
            if self.__word:
                _ = self.__word.Version
                return True
        except Exception:
            self.__word = None
            self.__status_msword = False
        return False

    def terminate_msword(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets terminate_msword()")
        try:
            if self.__word:
                try:
                    _ = self.__word.Version
                    self.__word.Quit()
                    self.__word = None
                except Exception:
                    self.__word = None
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in terminate_msword(): {e}")
        finally:
            self.__status_msword = False
            self.status_changed.emit(False)
            


class OfficePackets:
    def __init__(self):
        self.__status_msword = False
        self.__status_libreoffice = False
        self.__msword_thread = None
        self.__init_attempts = 0
        self.__max_init_attempts = 3
        self.__init_timer = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("OfficePackets setting_all_osbm()")

    def resetting_office_packets(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets resetting_office_packets()")
        self.__init_attempts = 0
        self._try_initialize_msword()
        # проверка наличия LibreOffice
        self.run_libreoffice()

    def _try_initialize_msword(self):
        """Попытка инициализации MS Word с повторными попытками"""
        if self.__init_attempts >= self.__max_init_attempts:
            self.__osbm.obj_logg.debug_logger("Max MS Word initialization attempts reached")
            self.__status_msword = False
            if self.__osbm.obj_stab.get_is_active():
                self.__osbm.obj_stab.update_status_msword_label(False)
            return

        self.__init_attempts += 1
        self.__osbm.obj_logg.debug_logger(f"MS Word initialization attempt {self.__init_attempts}/{self.__max_init_attempts}")
        
        try:
            if self.__msword_thread:
                self.__msword_thread.quit()
                self.__msword_thread.wait()
            
            self.__msword_thread = MsWordThread(self.__osbm)
            self.__msword_thread.status_changed.connect(self.update_status_msword)
            self.__msword_thread.start()
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error creating MsWordThread: {e}")
            self.__status_msword = False
            if self.__osbm.obj_stab.get_is_active():
                self.__osbm.obj_stab.update_status_msword_label(False)
            
            # Планируем повторную попытку через 2 секунды
            if self.__init_attempts < self.__max_init_attempts:
                if not self.__init_timer:
                    self.__init_timer = QTimer()
                    self.__init_timer.setSingleShot(True)
                    self.__init_timer.timeout.connect(self._try_initialize_msword)
                self.__init_timer.start(2000)
            
        
    def update_status_msword(self, status):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets update_status_msword(status):\nstatus = {status}"
        )
        self.__status_msword = status
        
        # Если инициализация не удалась, пробуем еще раз
        if status is False and self.__init_attempts < self.__max_init_attempts:
            self.__osbm.obj_logg.debug_logger("MS Word initialization failed, retrying...")
            if not self.__init_timer:
                self.__init_timer = QTimer()
                self.__init_timer.setSingleShot(True)
                self.__init_timer.timeout.connect(self._try_initialize_msword)
            self.__init_timer.start(2000)
        
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_msword_label(self.__status_msword)


    def get_status_msword(self):
        """Проверяет, доступен ли Word"""
        try:
            # Проверяем реальное состояние через поток
            if self.__msword_thread and self.__msword_thread.test_word_connection():
                return True
            else:
                # Если реальная проверка не прошла, обновляем статус
                if self.__status_msword:
                    self.__status_msword = False
                    if self.__osbm.obj_stab.get_is_active():
                        self.__osbm.obj_stab.update_status_msword_label(False)
                return False
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in get_status_msword: {e}")
            return False

    def get_status_libreoffice(self):
        self.__osbm.obj_logg.debug_logger(
            f"OfficePackets get_status_libreoffice():\nself.__status_libreoffice = {self.__status_libreoffice}"
        )
        return self.__status_libreoffice
    
    def run_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets run_libreoffice()")
        libreoffice_path = self.__osbm.obj_settings.get_libreoffice_path()
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
            if self.__msword_thread:
                self.__msword_thread.terminate_msword()
                self.__msword_thread.quit()
                self.__msword_thread.wait()
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in OfficePackets.terminate_msword():\n {e}  ? {traceback.format_exc()}")
        finally:
            self.__status_msword = False

    def terminate_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("OfficePackets terminate_libreoffice()")
        self.__status_libreoffice = False

    def force_reinitialize_converters(self):
        """Принудительная переинициализация конвертеров"""
        self.__osbm.obj_logg.debug_logger("OfficePackets force_reinitialize_converters()")
        self.__init_attempts = 0
        self._try_initialize_msword()
        self.run_libreoffice()

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
