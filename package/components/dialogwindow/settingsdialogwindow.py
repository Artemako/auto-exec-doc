from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QComboBox, QCheckBox, QGroupBox, QSizePolicy, QScrollArea, QWidget
from PySide6.QtCore import Qt
import package.components.widgets.pdfzoomsettingswidget as pdfzoomsettingswidget

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
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Создаем прокручиваемую область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Создаем виджет для содержимого
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        # Тема приложения
        theme_group = QGroupBox("Тема приложения")
        theme_layout = QHBoxLayout()
        theme_layout.setContentsMargins(10, 10, 10, 10)
        theme_layout.setSpacing(10)
        
        theme_label = QLabel("Тема:")
        theme_label.setMinimumWidth(60)
        theme_label.setMaximumWidth(60)
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        # Используем русские названия тем
        self.theme_combo.addItems(["Темная", "Светлая"])
        self.theme_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        theme_layout.addWidget(self.theme_combo)
        
        self.theme_reset_btn = QPushButton("Сброс")
        self.theme_reset_btn.setToolTip("Сбросить к значению по умолчанию")
        self.theme_reset_btn.setFixedWidth(60)
        theme_layout.addWidget(self.theme_reset_btn)
        
        theme_group.setLayout(theme_layout)
        content_layout.addWidget(theme_group)
        
        # Путь к LibreOffice
        libreoffice_group = QGroupBox("Путь к LibreOffice")
        libreoffice_layout = QHBoxLayout()
        libreoffice_layout.setContentsMargins(10, 10, 10, 10)
        libreoffice_layout.setSpacing(10)
        
        libreoffice_label = QLabel("Путь:")
        libreoffice_label.setMinimumWidth(60)
        libreoffice_label.setMaximumWidth(60)
        libreoffice_layout.addWidget(libreoffice_label)
        
        self.libreoffice_path_edit = QLineEdit()
        self.libreoffice_path_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        libreoffice_layout.addWidget(self.libreoffice_path_edit)
        
        self.browse_libreoffice_btn = QPushButton("Обзор...")
        self.browse_libreoffice_btn.setFixedWidth(80)
        libreoffice_layout.addWidget(self.browse_libreoffice_btn)
        
        self.libreoffice_reset_btn = QPushButton("Сброс")
        self.libreoffice_reset_btn.setToolTip("Сбросить к значению по умолчанию")
        self.libreoffice_reset_btn.setFixedWidth(60)
        libreoffice_layout.addWidget(self.libreoffice_reset_btn)
        
        libreoffice_group.setLayout(libreoffice_layout)
        content_layout.addWidget(libreoffice_group)
        
        # Отображение тега названия переменной
        variable_tag_group = QGroupBox("Отображение тега названия переменной")
        variable_tag_layout = QHBoxLayout()
        variable_tag_layout.setContentsMargins(10, 10, 10, 10)
        variable_tag_layout.setSpacing(10)
        
        self.show_variable_name_tag_checkbox = QCheckBox("Отображать тег названия переменной в формах ввода")
        self.show_variable_name_tag_checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        variable_tag_layout.addWidget(self.show_variable_name_tag_checkbox)
        
        self.variable_tag_reset_btn = QPushButton("Сброс")
        self.variable_tag_reset_btn.setToolTip("Сбросить к значению по умолчанию")
        self.variable_tag_reset_btn.setFixedWidth(60)
        variable_tag_layout.addWidget(self.variable_tag_reset_btn)
        
        variable_tag_group.setLayout(variable_tag_layout)
        content_layout.addWidget(variable_tag_group)
        
        # Настройки масштабирования PDF
        self.pdf_zoom_widget = pdfzoomsettingswidget.PdfZoomSettingsWidget()
        content_layout.addWidget(self.pdf_zoom_widget)
        
        # Общий сброс всех настроек
        reset_all_group = QGroupBox("Сброс всех настроек")
        reset_all_layout = QHBoxLayout()
        reset_all_layout.setContentsMargins(10, 10, 10, 10)
        
        self.reset_all_btn = QPushButton("Сбросить все настройки к значениям по умолчанию")
        self.reset_all_btn.setToolTip("Сбросить все настройки к значениям по умолчанию")
        self.reset_all_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        reset_all_layout.addWidget(self.reset_all_btn)
        
        reset_all_group.setLayout(reset_all_layout)
        content_layout.addWidget(reset_all_group)
        
        # Устанавливаем виджет в прокручиваемую область
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(10)
        
        buttons_layout.addStretch()
        
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        self.resize(700, 500)
        
        # Устанавливаем политику изменения размера
        self.setMinimumSize(650, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def connecting_actions(self):
        """Подключение обработчиков событий"""
        self.browse_libreoffice_btn.clicked.connect(self.browse_libreoffice)
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Кнопки сброса отдельных параметров
        self.theme_reset_btn.clicked.connect(self.reset_theme)
        self.libreoffice_reset_btn.clicked.connect(self.reset_libreoffice_path)
        self.variable_tag_reset_btn.clicked.connect(self.reset_variable_name_tag)
        
        # Кнопка общего сброса
        self.reset_all_btn.clicked.connect(self.reset_all_settings)
        
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

    def reset_theme(self):
        """Сброс темы к значению по умолчанию"""
        self.theme_combo.setCurrentText("Темная")

    def reset_libreoffice_path(self):
        """Сброс пути к LibreOffice к значению по умолчанию"""
        default_path = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        self.libreoffice_path_edit.setText(default_path)

    def reset_variable_name_tag(self):
        """Сброс настройки отображения тега названия переменной к значению по умолчанию"""
        self.show_variable_name_tag_checkbox.setChecked(True)

    def reset_all_settings(self):
        """Сброс всех настроек к значениям по умолчанию"""
        # Сброс темы
        self.theme_combo.setCurrentText("Темная")
        
        # Сброс пути к LibreOffice
        default_path = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        self.libreoffice_path_edit.setText(default_path)
        
        # Сброс настройки отображения тега названия переменной
        self.show_variable_name_tag_checkbox.setChecked(True)
        
        # Сброс настроек масштабирования PDF
        self.pdf_zoom_widget.reset_to_defaults()

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
        
        # Загрузка настроек масштабирования PDF
        self.pdf_zoom_widget.load_settings(self.__osbm.obj_settings)

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
            
            # Сохранение настроек масштабирования PDF
            if not self.pdf_zoom_widget.save_settings(self.__osbm.obj_settings):
                QMessageBox.warning(
                    self,
                    "Предупреждение",
                    "Некорректные значения настроек масштабирования PDF. Проверьте введенные данные."
                )
                return
            
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