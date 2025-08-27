from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QComboBox, QCheckBox
from PySide6.QtCore import Qt

class SettingsDialogWindow(QDialog):
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("SettingsDialogWindow __init__()")
        super(SettingsDialogWindow, self).__init__()
        
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        self.setWindowTitle("Настройки приложения")
        
        # Конфигурация
        self.config_ui()
        self.load_settings()
        self.connecting_actions()
        
        # Свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def config_ui(self):
        """Настройка пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Тема приложения
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Тема приложения:"))
        self.theme_combo = QComboBox()
        # Используем русские названия тем
        self.theme_combo.addItems(["Темная", "Светлая"])
        theme_layout.addWidget(self.theme_combo)
        main_layout.addLayout(theme_layout)
        
        # Путь к LibreOffice
        libreoffice_layout = QHBoxLayout()
        libreoffice_layout.addWidget(QLabel("Путь к LibreOffice:"))
        self.libreoffice_path_edit = QLineEdit()
        libreoffice_layout.addWidget(self.libreoffice_path_edit)
        self.browse_libreoffice_btn = QPushButton("Обзор...")
        libreoffice_layout.addWidget(self.browse_libreoffice_btn)
        main_layout.addLayout(libreoffice_layout)
        
        # Отображение тега названия переменной
        self.show_variable_name_tag_checkbox = QCheckBox("Отображать тег названия переменной в формах ввода")
        main_layout.addWidget(self.show_variable_name_tag_checkbox)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        self.resize(500, 180)

    def connecting_actions(self):
        """Подключение обработчиков событий"""
        self.browse_libreoffice_btn.clicked.connect(self.browse_libreoffice)
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Горячие клавиши
        self.save_btn.setShortcut("Ctrl+S")
        self.cancel_btn.setShortcut("Ctrl+Q")

    def browse_libreoffice(self):
        """Выбор пути к LibreOffice"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите исполняемый файл LibreOffice",
            self.libreoffice_path_edit.text(),
            "Исполняемые файлы (*.exe)"
        )
        
        if file_path:
            self.libreoffice_path_edit.setText(file_path)

    def load_settings(self):
        """Загрузка текущих настроек"""
        # Загрузка темы (получаем русское название)
        theme_display = self.__osbm.obj_settings.get_theme_display_name()
        self.theme_combo.setCurrentText(theme_display)
        
        # Загрузка пути к LibreOffice
        libreoffice_path = self.__osbm.obj_settings.get_libreoffice_path()
        self.libreoffice_path_edit.setText(libreoffice_path)
        
        # Загрузка настройки отображения тега названия переменной
        self.__original_show_variable_name_tag = self.__osbm.obj_settings.get_show_variable_name_tag()
        self.show_variable_name_tag_checkbox.setChecked(self.__original_show_variable_name_tag)

    def save_settings(self):
        """Сохранение настроек"""
        try:
            # Сохранение темы (используем русское название для установки)
            theme_display = self.theme_combo.currentText()
            self.__osbm.obj_settings.set_theme_by_display_name(theme_display)
            
            # Применение новой темы
            theme_english = self.__osbm.obj_settings.get_theme()
            self.__osbm.obj_style.apply_theme_to_all_windows(theme_english)
            
            # Сохранение пути к LibreOffice
            libreoffice_path = self.libreoffice_path_edit.text().strip()
            
            # Проверка валидности пути
            if libreoffice_path and not libreoffice_path.endswith("soffice.exe"):
                QMessageBox.warning(
                    self,
                    "Предупреждение",
                    "Путь должен указывать на исполняемый файл soffice.exe"
                )
                return
            
            self.__osbm.obj_settings.set_libreoffice_path(libreoffice_path)
            
            # Сохранение настройки отображения тега названия переменной
            show_variable_name_tag = self.show_variable_name_tag_checkbox.isChecked()
            self.__osbm.obj_settings.set_show_variable_name_tag(show_variable_name_tag)
            
            self.__osbm.obj_settings.sync()
            
            # Обновление статуса LibreOffice в главном окне
            self.__osbm.obj_offp.resetting_office_packets()
            if self.__osbm.obj_stab.get_is_active():
                self.__osbm.obj_stab.update_status_libreoffice_label(
                    self.__osbm.obj_offp.get_status_libreoffice()
                )
            
            # Обновление отображения тегов названий переменных в формах ввода только если настройка изменилась
            if show_variable_name_tag != self.__original_show_variable_name_tag:
                self.__osbm.obj_tabwif.update_variable_name_tags()
            
            self.accept()
            
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error saving settings: {e}")
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при сохранении настроек: {str(e)}"
            )