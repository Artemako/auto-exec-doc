from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QTextEdit, QListWidget, QPushButton, QLabel,
    QSplitter, QWidget, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

import os
import json


class StorageDialogWindow(QDialog):
    """
    Диалоговое окно хранилища с двумя вкладками: Текст и Изображения
    """
    def __init__(self, osbm):
        super(StorageDialogWindow, self).__init__()
        self.__osbm = osbm
        self.storage_file = os.path.join(self.__osbm.obj_dirm.get_app_data_dir(), "storage.json")
        self.images_dir = os.path.join(self.__osbm.obj_dirm.get_app_data_dir(), "storage_images")
        
        # Создаем директорию для изображений если её нет
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
            
        self.init_ui()
        self.load_storage_data()
        
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Хранилище")
        self.setModal(True)
        self.resize(800, 600)
        
        # Основной layout
        main_layout = QVBoxLayout()
        
        # Создаем TabWidget
        self.tab_widget = QTabWidget()
        
        # Вкладка "Текст"
        self.text_tab = self.create_text_tab()
        self.tab_widget.addTab(self.text_tab, "Текст")
        
        # Вкладка "Изображения"
        self.images_tab = self.create_images_tab()
        self.tab_widget.addTab(self.images_tab, "Изображения")
        
        main_layout.addWidget(self.tab_widget)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
    def create_text_tab(self):
        """Создание вкладки для текста"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Splitter для разделения списка и редактора
        splitter = QSplitter(Qt.Horizontal)
        
        # Левая панель - список текстовых элементов
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        left_layout.addWidget(QLabel("Сохраненные тексты:"))
        
        self.text_list = QListWidget()
        self.text_list.itemClicked.connect(self.on_text_item_clicked)
        left_layout.addWidget(self.text_list)
        
        # Кнопки для текста
        text_buttons_layout = QHBoxLayout()
        self.add_text_button = QPushButton("Добавить")
        self.add_text_button.clicked.connect(self.add_text_item)
        self.delete_text_button = QPushButton("Удалить")
        self.delete_text_button.clicked.connect(self.delete_text_item)
        
        text_buttons_layout.addWidget(self.add_text_button)
        text_buttons_layout.addWidget(self.delete_text_button)
        left_layout.addLayout(text_buttons_layout)
        
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)
        
        # Правая панель - редактор текста
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("Редактор текста:"))
        
        self.text_editor = QTextEdit()
        self.text_editor.textChanged.connect(self.on_text_changed)
        right_layout.addWidget(self.text_editor)
        
        # Кнопки для редактора
        editor_buttons_layout = QHBoxLayout()
        self.save_text_button = QPushButton("Сохранить")
        self.save_text_button.clicked.connect(self.save_text_item)
        self.copy_text_button = QPushButton("Копировать")
        self.copy_text_button.clicked.connect(self.copy_text_to_clipboard)
        
        editor_buttons_layout.addWidget(self.save_text_button)
        editor_buttons_layout.addWidget(self.copy_text_button)
        right_layout.addLayout(editor_buttons_layout)
        
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        
        # Устанавливаем пропорции splitter
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter)
        widget.setLayout(layout)
        
        return widget
        
    def create_images_tab(self):
        """Создание вкладки для изображений"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Splitter для разделения списка и просмотра
        splitter = QSplitter(Qt.Horizontal)
        
        # Левая панель - список изображений
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        left_layout.addWidget(QLabel("Сохраненные изображения:"))
        
        self.images_list = QListWidget()
        self.images_list.itemClicked.connect(self.on_image_item_clicked)
        left_layout.addWidget(self.images_list)
        
        # Кнопки для изображений
        images_buttons_layout = QHBoxLayout()
        self.add_image_button = QPushButton("Добавить")
        self.add_image_button.clicked.connect(self.add_image_item)
        self.delete_image_button = QPushButton("Удалить")
        self.delete_image_button.clicked.connect(self.delete_image_item)
        
        images_buttons_layout.addWidget(self.add_image_button)
        images_buttons_layout.addWidget(self.delete_image_button)
        left_layout.addLayout(images_buttons_layout)
        
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)
        
        # Правая панель - просмотр изображения
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("Просмотр изображения:"))
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        right_layout.addWidget(self.image_label)
        
        # Информация об изображении
        self.image_info_label = QLabel("Выберите изображение для просмотра")
        right_layout.addWidget(self.image_info_label)
        
        # Кнопки для изображения
        image_buttons_layout = QHBoxLayout()
        self.copy_image_path_button = QPushButton("Копировать путь")
        self.copy_image_path_button.clicked.connect(self.copy_image_path_to_clipboard)
        
        image_buttons_layout.addWidget(self.copy_image_path_button)
        right_layout.addLayout(image_buttons_layout)
        
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        
        # Устанавливаем пропорции splitter
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter)
        widget.setLayout(layout)
        
        return widget
        
    def load_storage_data(self):
        """Загрузка данных хранилища"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Загружаем тексты
                self.text_items = data.get('texts', {})
                for title in self.text_items.keys():
                    self.text_list.addItem(title)
                    
                # Загружаем изображения
                self.image_items = data.get('images', {})
                for title in self.image_items.keys():
                    self.images_list.addItem(title)
            else:
                self.text_items = {}
                self.image_items = {}
                
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Ошибка загрузки хранилища: {e}")
            self.text_items = {}
            self.image_items = {}
            
    def save_storage_data(self):
        """Сохранение данных хранилища"""
        try:
            data = {
                'texts': self.text_items,
                'images': self.image_items
            }
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Ошибка сохранения хранилища: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные: {e}")
            
    def add_text_item(self):
        """Добавление нового текстового элемента"""
        from PySide6.QtWidgets import QInputDialog
        
        title, ok = QInputDialog.getText(self, "Добавить текст", "Введите название:")
        if ok and title:
            if title in self.text_items:
                QMessageBox.warning(self, "Ошибка", "Элемент с таким названием уже существует!")
                return
                
            self.text_items[title] = ""
            self.text_list.addItem(title)
            self.save_storage_data()
            
    def delete_text_item(self):
        """Удаление текстового элемента"""
        current_item = self.text_list.currentItem()
        if not current_item:
            return
            
        title = current_item.text()
        reply = QMessageBox.question(self, "Подтверждение", 
                                   f"Удалить элемент '{title}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            del self.text_items[title]
            self.text_list.takeItem(self.text_list.row(current_item))
            self.text_editor.clear()
            self.save_storage_data()
            
    def on_text_item_clicked(self, item):
        """Обработка клика по текстовому элементу"""
        title = item.text()
        if title in self.text_items:
            self.text_editor.setPlainText(self.text_items[title])
            
    def on_text_changed(self):
        """Обработка изменения текста в редакторе"""
        current_item = self.text_list.currentItem()
        if current_item:
            title = current_item.text()
            self.text_items[title] = self.text_editor.toPlainText()
            
    def save_text_item(self):
        """Сохранение текстового элемента"""
        current_item = self.text_list.currentItem()
        if current_item:
            title = current_item.text()
            self.text_items[title] = self.text_editor.toPlainText()
            self.save_storage_data()
            QMessageBox.information(self, "Успех", "Текст сохранен!")
            
    def copy_text_to_clipboard(self):
        """Копирование текста в буфер обмена"""
        text = self.text_editor.toPlainText()
        if text:
            clipboard = self.__osbm.obj_comwith.get_clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Успех", "Текст скопирован в буфер обмена!")
            
    def add_image_item(self):
        """Добавление нового изображения"""
        from PySide6.QtWidgets import QInputDialog
        
        # Сначала выбираем файл
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if not file_path:
            return
            
        # Затем вводим название
        title, ok = QInputDialog.getText(self, "Добавить изображение", "Введите название:")
        if ok and title:
            if title in self.image_items:
                QMessageBox.warning(self, "Ошибка", "Элемент с таким названием уже существует!")
                return
                
            # Копируем файл в папку хранилища
            import shutil
            file_ext = os.path.splitext(file_path)[1]
            new_file_name = f"{title}{file_ext}"
            new_file_path = os.path.join(self.images_dir, new_file_name)
            
            try:
                shutil.copy2(file_path, new_file_path)
                self.image_items[title] = new_file_path
                self.images_list.addItem(title)
                self.save_storage_data()
                QMessageBox.information(self, "Успех", "Изображение добавлено!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить изображение: {e}")
                
    def delete_image_item(self):
        """Удаление изображения"""
        current_item = self.images_list.currentItem()
        if not current_item:
            return
            
        title = current_item.text()
        reply = QMessageBox.question(self, "Подтверждение", 
                                   f"Удалить изображение '{title}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Удаляем файл
            if title in self.image_items:
                try:
                    os.remove(self.image_items[title])
                except:
                    pass  # Игнорируем ошибки при удалении файла
                    
            del self.image_items[title]
            self.images_list.takeItem(self.images_list.row(current_item))
            self.image_label.clear()
            self.image_info_label.setText("Выберите изображение для просмотра")
            self.save_storage_data()
            
    def on_image_item_clicked(self, item):
        """Обработка клика по изображению"""
        title = item.text()
        if title in self.image_items:
            file_path = self.image_items[title]
            if os.path.exists(file_path):
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    # Масштабируем изображение для отображения
                    scaled_pixmap = pixmap.scaled(
                        self.image_label.size(), 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                    self.image_label.setPixmap(scaled_pixmap)
                    
                    # Показываем информацию
                    file_size = os.path.getsize(file_path)
                    file_size_kb = file_size / 1024
                    self.image_info_label.setText(
                        f"Название: {title}\n"
                        f"Путь: {file_path}\n"
                        f"Размер: {file_size_kb:.1f} КБ\n"
                        f"Размеры: {pixmap.width()}x{pixmap.height()}"
                    )
                else:
                    self.image_label.setText("Ошибка загрузки изображения")
                    self.image_info_label.setText("Не удалось загрузить изображение")
            else:
                self.image_label.setText("Файл не найден")
                self.image_info_label.setText("Файл изображения не найден")
                
    def copy_image_path_to_clipboard(self):
        """Копирование пути к изображению в буфер обмена"""
        current_item = self.images_list.currentItem()
        if current_item:
            title = current_item.text()
            if title in self.image_items:
                file_path = self.image_items[title]
                clipboard = self.__osbm.obj_comwith.get_clipboard()
                clipboard.setText(file_path)
                QMessageBox.information(self, "Успех", "Путь к изображению скопирован в буфер обмена!")
                
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.save_storage_data()
        event.accept()
