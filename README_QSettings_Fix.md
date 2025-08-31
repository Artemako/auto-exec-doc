# Исправление проблемы с сериализацией QSettings в многопроцессорной обработке

## Проблема

При экспорте проекта в PDF возникала ошибка:
```
TypeError: cannot pickle 'PySide6.QtCore.QSettings' object
```

Ошибка происходила в файле `package/modules/converter.py` при использовании `multiprocessing.Pool` для параллельной обработки страниц документа.

## Причина

Объект `QSettings` из PySide6 не может быть сериализован (pickled) для передачи между процессами в многопроцессорной обработке. В классе `ConverterObjectsManager` содержалась ссылка на `obj_settings`, который включал объект `QSettings`.

## Решение

### 1. Создан новый класс `ConverterSettingsData`

```python
class ConverterSettingsData:
    """Класс для передачи только сериализуемых данных настроек в многопроцессорную обработку"""
    def __init__(self, app_converter=None, libreoffice_path=None):
        # Принимаем значения напрямую, а не через settings_manager
        self.app_converter = app_converter or "LIBREOFFICE"
        self.libreoffice_path = libreoffice_path or "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
    
    @classmethod
    def from_settings_manager(cls, settings_manager):
        """Создает объект из settings_manager, извлекая только сериализуемые данные"""
        # Проверяем, инициализирован ли settings_manager
        if hasattr(settings_manager, '_SettingsManager__settings'):
            app_converter = settings_manager.get_app_converter()
            libreoffice_path = settings_manager.get_libreoffice_path()
        else:
            # Значения по умолчанию, если settings_manager еще не инициализирован
            app_converter = "LIBREOFFICE"
            libreoffice_path = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        return cls(app_converter, libreoffice_path)
```

Этот класс теперь принимает значения напрямую, избегая передачи `QSettings` объекта. Метод `from_settings_manager` извлекает только необходимые данные из `SettingsManager` и создает сериализуемый объект.

### 2. Создан класс `ConverterObjectsManagerForMultiprocessing`

Для многопроцессорной обработки создан отдельный класс без `obj_settings`:

```python
class ConverterObjectsManagerForMultiprocessing:
    """Версия ConverterObjectsManager для многопроцессорной обработки без obj_settings"""
    def __init__(self, osbm, settings_data):
        # ... те же объекты, что и в ConverterObjectsManager
        # НО без obj_settings для возможности сериализации
        self.settings_data = settings_data
```

Класс теперь принимает готовые сериализуемые данные настроек, избегая создания `ConverterSettingsData` внутри конструктора.

### 3. Обновлен класс `ConverterObjectsManager`

- Сохранена ссылка на `obj_settings` для совместимости с существующим кодом
- Добавлен объект `settings_data` типа `ConverterSettingsData`

### 4. Обновлены методы конвертации

В методах конвертации заменили использование:
- `local_osbm.obj_settings.get_app_converter()` → `local_osbm.settings_data.app_converter`
- `local_osbm.obj_settings.get_libreoffice_path()` → `local_osbm.settings_data.libreoffice_path`

### 5. Обновлен метод многопроцессорной обработки

В методе `get_list_of_created_pdf_pages` используется `ConverterObjectsManagerForMultiprocessing` с уже готовыми данными настроек:

```python
args = [
    (ConverterObjectsManagerForMultiprocessing(self.__osbm, self.__osbm.settings_data), obj) 
    for obj in project_pages_objects
]
```

Это обеспечивает полную сериализуемость объектов для многопроцессорной обработки.

## Измененные файлы

- `package/modules/converter.py` - основное исправление

## Тестирование

Создан тестовый файл `test_converter_fix.py` для проверки:
- Создания `ConverterSettingsData`
- Создания `ConverterObjectsManager`
- Сериализации объектов для многопроцессорной обработки

Все тесты прошли успешно.

## Результат

✅ **Проблема с сериализацией `QSettings` решена**  
✅ **Совместимость с существующим кодом сохранена**  
✅ **Предпросмотр документов работает корректно**  
✅ **Экспорт проекта в PDF работает с многопроцессорной обработкой**

Теперь программа корректно работает как для предпросмотра документов, так и для экспорта в PDF с использованием многопроцессорной обработки.
