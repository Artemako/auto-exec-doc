from PySide6.QtWidgets import (
    QStatusBar,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt

import package.components.dialogwindow.convertersettingsdialogwindow as convertersettingsdialogwindow

import resources_rc


class StatusBar:
    def __init__(self):
        self.__statusbar = None
        self.__is_active = False

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("StatusBar setting_all_osbm()")

    def get_is_active(self) -> bool:
        return self.__is_active

    def connect_statusbar(self, statusbar):
        """
        Подключить статусбар.
        """
        self.__osbm.obj_logg.debug_logger("StatusBar connect_statusbar(statusbar)")
        self.__statusbar = statusbar
        self.__is_active = True
        self.__timer = QTimer()
        self.__timer_count = 0
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        #
        self.config_statusbar()
        self.set_message("Проект не открыт")
        self.update_name_app_converter()
        self.connecting_actions()

    def config_update_statusbar(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_update_statusbar()")
        status_msword = self.__osbm.obj_offp.get_status_msword()
        self.update_status_msword_label(status_msword)
        status_libreoffice = self.__osbm.obj_offp.get_status_libreoffice()
        self.update_status_libreoffice_label(status_libreoffice)

    def config_statusbar(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_statusbar()")
        # конфигурация
        self.config_msword()
        self.config_libreoffice()
        #
        self.__statusbar.layout().setSpacing(4)
        # выбранный конвертер
        self.__name_app_converter = QLabel("NONE")
        self.__name_app_converter.setAlignment(Qt.AlignCenter)
        self.__name_app_converter.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(self.__name_app_converter)
        # кнопка настройки конвертера
        self.__btn_setting_converter = QPushButton("Настройка конвертера")
        self.__btn_setting_converter.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(self.__btn_setting_converter)
        # обновить statusbar
        self.config_update_statusbar()

    def get_red_circle(self) -> QLabel:
        icon = self.__icons.get("red_circle")
        label = QLabel()
        label.setPixmap(icon)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar get_red_circle() -> QLabel:\nlabel = {label}"
        )
        return label

    def get_yellow_circle(self) -> QLabel:
        icon = self.__icons.get("yellow_circle")
        label = QLabel()
        label.setPixmap(icon)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar get_yellow_circle() -> QLabel:\nlabel = {label}"
        )
        return label

    def get_green_circle(self) -> QLabel:
        icon = self.__icons.get("green_circle")
        label = QLabel()
        label.setPixmap(icon)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar get_green_circle() -> QLabel:\nlabel = {label}"
        )
        return label

    def config_msword(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_msword()")
        layout = QHBoxLayout()
        # иконка приложения
        icon = self.__icons.get("msword")
        label = QLabel()
        label.setPixmap(icon)
        layout.addWidget(label)
        # иконка статуса
        self.__red_msword = self.get_red_circle()
        self.__yellow_msword = self.get_yellow_circle()
        self.__green_msword = self.get_green_circle()
        layout.addWidget(self.__red_msword)
        layout.addWidget(self.__yellow_msword)
        layout.addWidget(self.__green_msword)
        layout.setContentsMargins(0, 0, 0, 0)
        # главный виджет
        mw_msword = QWidget()
        mw_msword.setLayout(layout)
        mw_msword.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(mw_msword)

    def config_libreoffice(self):
        self.__osbm.obj_logg.debug_logger("StatusBar config_libreoffice()")
        layout = QHBoxLayout()
        # иконка приложения
        icon = self.__icons.get("libreoffice")
        label = QLabel()
        label.setPixmap(icon)
        layout.addWidget(label)
        # иконка статуса
        self.__red_libreoffice = self.get_red_circle()
        self.__yellow_libreoffice = self.get_yellow_circle()
        self.__green_libreoffice = self.get_green_circle()
        layout.addWidget(self.__red_libreoffice)
        layout.addWidget(self.__yellow_libreoffice)
        layout.addWidget(self.__green_libreoffice)
        layout.setContentsMargins(0, 0, 0, 0)
        # главный виджет
        mw_libreoffice = QWidget()
        mw_libreoffice.setLayout(layout)
        mw_libreoffice.setContentsMargins(4, 0, 4, 0)
        self.__statusbar.addPermanentWidget(mw_libreoffice)

    def set_message(self, message: str, duration: int = 3000):
        """
        Поставить сообщение в статусбар.
        """
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar set_message(message):\nmessage = {message}"
        )
        if self.__timer.isActive():
            self.__timer.stop()
            self.__timer_count += 1
        self.__statusbar.showMessage(message + " ." * self.__timer_count)
        # Устанавливаем новый таймер для очистки сообщения
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(self.clear_message)
        self.__timer.start(duration) 

    def clear_message(self):
        self.__statusbar.clearMessage()
        self.__timer_count = 0


    def update_status_msword_label(self, status_msword):
        """Обновляется при запуске app"""
        if status_msword:
            self.__red_msword.setVisible(False)
            self.__yellow_msword.setVisible(False)
            self.__green_msword.setVisible(True)
        elif status_msword is None:
            self.__red_msword.setVisible(False)
            self.__yellow_msword.setVisible(True)
            self.__green_msword.setVisible(False)
        else:
            self.__red_msword.setVisible(True)
            self.__yellow_msword.setVisible(False)
            self.__green_msword.setVisible(False)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar update_status_status_msword_label(status_msword):\nstatus_msword = {status_msword}"
        )

    def update_status_libreoffice_label(self, status_libreoffice):
        """Обновляется при запуске app"""
        if status_libreoffice:
            self.__red_libreoffice.setVisible(False)
            self.__yellow_libreoffice.setVisible(False)
            self.__green_libreoffice.setVisible(True)
        elif status_libreoffice is None:
            self.__red_libreoffice.setVisible(False)
            self.__yellow_libreoffice.setVisible(True)
            self.__green_libreoffice.setVisible(False)
        else:
            self.__red_libreoffice.setVisible(True)
            self.__yellow_libreoffice.setVisible(False)
            self.__green_libreoffice.setVisible(False)
        self.__osbm.obj_logg.debug_logger(
            f"StatusBar update_status_libreoffice_label(status_libreoffice):\nstatus_libreoffice = {status_libreoffice}"
        )

    def update_name_app_converter(self):
        app_converter = self.__osbm.obj_settings.get_app_converter()
        print(f"app_converter = {app_converter}")
        name_app_converter = "None"
        if app_converter == "MSWORD":
            name_app_converter = "MS Word"
        elif app_converter == "LIBREOFFICE":
            name_app_converter = "LibreOffice"
        print(f"name_app_converter = {name_app_converter}")
        self.__name_app_converter.setText(name_app_converter)
        self.__osbm.obj_logg.debug_logger("StatusBar update_name_app_converter()")

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("StatusBar connecting_actions()")
        self.__btn_setting_converter.clicked.connect(self.show_converter_settings)
        # Добавляем кнопку для переинициализации конвертеров
        self.__btn_reinitialize_converters = QPushButton("🔄")
        self.__btn_reinitialize_converters.setToolTip("Переинициализировать конвертеры")
        self.__btn_reinitialize_converters.setMaximumWidth(30)
        self.__btn_reinitialize_converters.clicked.connect(self.reinitialize_converters)
        self.__statusbar.addPermanentWidget(self.__btn_reinitialize_converters)

    def show_converter_settings(self):
        self.__osbm.obj_logg.debug_logger("StatusBar show_converter_settings()")
        self.__osbm.obj_convsdw = (
            convertersettingsdialogwindow.ConverterSettingsDialogWindow(
                self.__osbm
            )
        )
        self.__osbm.obj_convsdw.exec()

    def reinitialize_converters(self):
        """Переинициализация конвертеров"""
        self.__osbm.obj_logg.debug_logger("StatusBar reinitialize_converters()")
        self.__osbm.obj_offp.force_reinitialize_converters()
        self.__osbm.obj_stab.set_message("Конвертеры переинициализированы")


# obj_stab = StatusBar()
