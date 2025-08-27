from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator, QValidator
import re


class ZoomValidator(QValidator):
    """Валидатор для полей масштабирования PDF.
    Разрешает только числа от 0.01 до 10.0 с двумя цифрами после запятой."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Регулярное выражение для проверки формата: число от 0.01 до 10.0 с двумя знаками после запятой
        self.pattern = re.compile(r'^(0\.0[1-9]|0\.[1-9]\d|0\.\d[0-9]|[1-9]\.\d{2}|10\.00)$')
    
    def validate(self, input_str, pos):
        """Валидация введенного текста"""
        if not input_str:
            return QValidator.Acceptable, input_str, pos
        
        # Проверяем, что введены только цифры, точка и запятая
        if not re.match(r'^[\d.,]*$', input_str):
            return QValidator.Invalid, input_str, pos
        
        # Заменяем запятую на точку для единообразия
        normalized_input = input_str.replace(',', '.')
        
        # Проверяем, что точка только одна
        if normalized_input.count('.') > 1:
            return QValidator.Invalid, input_str, pos
        
        # Если введена только точка или точка в конце, разрешаем
        if normalized_input == '.' or normalized_input.endswith('.'):
            return QValidator.Intermediate, input_str, pos
        
        # Если введены цифры после точки, но меньше двух, разрешаем
        if '.' in normalized_input:
            decimal_part = normalized_input.split('.')[1]
            if len(decimal_part) < 2:
                return QValidator.Intermediate, input_str, pos
        
        # Проверяем, что число в допустимом диапазоне
        try:
            value = float(normalized_input)
            if 0.01 <= value <= 10.0:
                # Проверяем формат с двумя знаками после запятой
                if self.pattern.match(normalized_input):
                    return QValidator.Acceptable, input_str, pos
                else:
                    return QValidator.Intermediate, input_str, pos
            else:
                return QValidator.Invalid, input_str, pos
        except ValueError:
            return QValidator.Invalid, input_str, pos


class PdfZoomSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(PdfZoomSettingsWidget, self).__init__(parent)
        self.config_ui()

    def config_ui(self):
        """Настройка пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы для соответствия стилю
        main_layout.setSpacing(0)
        
        # Группа настроек масштабирования PDF
        zoom_group = QGroupBox("Настройки масштабирования PDF")
        group_layout = QVBoxLayout()
        group_layout.setContentsMargins(10, 10, 10, 10)  # Стандартные отступы
        group_layout.setSpacing(10)
        
        # Минимальный масштаб
        min_zoom_layout = QHBoxLayout()
        min_zoom_label = QLabel("Мин. масштаб:")
        min_zoom_label.setFixedWidth(100)
        min_zoom_layout.addWidget(min_zoom_label)
        self.min_zoom_edit = QLineEdit()
        self.min_zoom_edit.setPlaceholderText("0.10")
        self.min_zoom_edit.setToolTip("Минимальный масштаб для PDF документа (0.01 - 10.00)")
        self.min_zoom_edit.setFixedWidth(80)
        self.min_zoom_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Устанавливаем кастомный валидатор
        self.min_zoom_edit.setValidator(ZoomValidator())
        min_zoom_layout.addWidget(self.min_zoom_edit)
        min_zoom_layout.addStretch()
        self.min_zoom_reset_btn = QPushButton("Сброс")
        self.min_zoom_reset_btn.setToolTip("Сбросить к значению по умолчанию (0.10)")
        self.min_zoom_reset_btn.setFixedWidth(60)
        min_zoom_layout.addWidget(self.min_zoom_reset_btn)
        group_layout.addLayout(min_zoom_layout)
        
        # Максимальный масштаб
        max_zoom_layout = QHBoxLayout()
        max_zoom_label = QLabel("Макс. масштаб:")
        max_zoom_label.setFixedWidth(100)
        max_zoom_layout.addWidget(max_zoom_label)
        self.max_zoom_edit = QLineEdit()
        self.max_zoom_edit.setPlaceholderText("4.00")
        self.max_zoom_edit.setToolTip("Максимальный масштаб для PDF документа (0.01 - 10.00)")
        self.max_zoom_edit.setFixedWidth(80)
        self.max_zoom_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Устанавливаем кастомный валидатор
        self.max_zoom_edit.setValidator(ZoomValidator())
        max_zoom_layout.addWidget(self.max_zoom_edit)
        max_zoom_layout.addStretch()
        self.max_zoom_reset_btn = QPushButton("Сброс")
        self.max_zoom_reset_btn.setToolTip("Сбросить к значению по умолчанию (4.00)")
        self.max_zoom_reset_btn.setFixedWidth(60)
        max_zoom_layout.addWidget(self.max_zoom_reset_btn)
        group_layout.addLayout(max_zoom_layout)
        
        # Шаг изменения масштаба
        delta_zoom_layout = QHBoxLayout()
        delta_zoom_label = QLabel("Шаг масштаба:")
        delta_zoom_label.setFixedWidth(100)
        delta_zoom_layout.addWidget(delta_zoom_label)
        self.delta_zoom_edit = QLineEdit()
        self.delta_zoom_edit.setPlaceholderText("0.10")
        self.delta_zoom_edit.setToolTip("Шаг изменения масштаба при увеличении/уменьшении (0.01 - 10.00)")
        self.delta_zoom_edit.setFixedWidth(80)
        self.delta_zoom_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Устанавливаем кастомный валидатор
        self.delta_zoom_edit.setValidator(ZoomValidator())
        delta_zoom_layout.addWidget(self.delta_zoom_edit)
        delta_zoom_layout.addStretch()
        self.delta_zoom_reset_btn = QPushButton("Сброс")
        self.delta_zoom_reset_btn.setToolTip("Сбросить к значению по умолчанию (0.10)")
        self.delta_zoom_reset_btn.setFixedWidth(60)
        delta_zoom_layout.addWidget(self.delta_zoom_reset_btn)
        group_layout.addLayout(delta_zoom_layout)
        
        zoom_group.setLayout(group_layout)
        main_layout.addWidget(zoom_group)
        
        # Подключение обработчиков событий
        self.min_zoom_reset_btn.clicked.connect(self.reset_min_zoom)
        self.max_zoom_reset_btn.clicked.connect(self.reset_max_zoom)
        self.delta_zoom_reset_btn.clicked.connect(self.reset_delta_zoom)

    def reset_min_zoom(self):
        """Сброс минимального масштаба к значению по умолчанию"""
        self.min_zoom_edit.setText("0.10")

    def reset_max_zoom(self):
        """Сброс максимального масштаба к значению по умолчанию"""
        self.max_zoom_edit.setText("4.00")

    def reset_delta_zoom(self):
        """Сброс шага изменения масштаба к значению по умолчанию"""
        self.delta_zoom_edit.setText("0.10")

    def reset_to_defaults(self):
        """Сброс всех настроек PDF к значениям по умолчанию (для вызова из внешнего кода)"""
        self.min_zoom_edit.setText("0.10")
        self.max_zoom_edit.setText("4.00")
        self.delta_zoom_edit.setText("0.10")

    def load_settings(self, settings_manager):
        """Загрузка настроек из менеджера настроек"""
        self.min_zoom_edit.setText(f"{settings_manager.get_pdf_min_zoom():.2f}")
        self.max_zoom_edit.setText(f"{settings_manager.get_pdf_max_zoom():.2f}")
        self.delta_zoom_edit.setText(f"{settings_manager.get_pdf_delta_zoom():.2f}")

    def save_settings(self, settings_manager):
        """Сохранение настроек в менеджер настроек"""
        try:
            min_zoom = float(self.min_zoom_edit.text())
            max_zoom = float(self.max_zoom_edit.text())
            delta_zoom = float(self.delta_zoom_edit.text())
            
            # Валидация значений
            if min_zoom <= 0 or max_zoom <= 0 or delta_zoom <= 0:
                raise ValueError("Все значения должны быть положительными числами")
            
            if min_zoom >= max_zoom:
                raise ValueError("Минимальный масштаб должен быть меньше максимального")
            
            if delta_zoom > (max_zoom - min_zoom):
                raise ValueError("Шаг изменения должен быть меньше разности максимального и минимального масштаба")
            
            settings_manager.set_pdf_min_zoom(min_zoom)
            settings_manager.set_pdf_max_zoom(max_zoom)
            settings_manager.set_pdf_delta_zoom(delta_zoom)
            
            return True
            
        except ValueError as e:
            # Возвращаем False в случае ошибки валидации
            return False
        except Exception as e:
            # Возвращаем False в случае других ошибок
            return False

    def validate_input(self):
        """Валидация введенных значений"""
        try:
            min_zoom = float(self.min_zoom_edit.text())
            max_zoom = float(self.max_zoom_edit.text())
            delta_zoom = float(self.delta_zoom_edit.text())
            
            if min_zoom <= 0 or max_zoom <= 0 or delta_zoom <= 0:
                return False, "Все значения должны быть положительными числами"
            
            if min_zoom >= max_zoom:
                return False, "Минимальный масштаб должен быть меньше максимального"
            
            if delta_zoom > (max_zoom - min_zoom):
                return False, "Шаг изменения должен быть меньше разности максимального и минимального масштаба"
            
            return True, ""
            
        except ValueError:
            return False, "Все значения должны быть числами"
        except Exception:
            return False, "Произошла ошибка при валидации"