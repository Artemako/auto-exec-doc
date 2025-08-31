# Асинхронная инициализация MS Word

## Проблема

При запуске программы происходила задержка в 1-3 секунды из-за блокирующей проверки доступности конвертера MS Word. Главное окно не отображалось до завершения проверки.

## Решение

Реализована асинхронная инициализация MS Word, которая позволяет:
- Мгновенно открывать главное окно программы
- Проверять доступность MS Word в фоновом режиме
- Отображать статус проверки в реальном времени

## Изменения в коде

### 1. Файл `package/app.py`

#### Метод `check_before_run()`
- **Было**: `self.osbm.obj_offp.resetting_office_packets()` - блокирующая проверка
- **Стало**: `self.osbm.obj_offp.initialize_libreoffice_only()` - только быстрая проверка LibreOffice

#### Метод `start_app()`
- **Добавлено**: `self.osbm.obj_offp.initialize_msword_async()` - асинхронная инициализация MS Word после показа окна

### 2. Файл `package/modules/officepackets.py`

#### Новые методы:

**`initialize_libreoffice_only()`**
```python
def initialize_libreoffice_only(self):
    """Быстрая инициализация только LibreOffice"""
    self.__osbm.obj_logg.debug_logger("OfficePackets initialize_libreoffice_only()")
    self.run_libreoffice()
```

**`initialize_msword_async()`**
```python
def initialize_msword_async(self):
    """Асинхронная инициализация MS Word"""
    self.__osbm.obj_logg.debug_logger("OfficePackets initialize_msword_async()")
    if not self.__status_msword:
        # Устанавливаем состояние "проверяется" (None)
        self.__status_msword = None
        if self.__osbm.obj_stab.get_is_active():
            self.__osbm.obj_stab.update_status_msword_label(self.__status_msword)
        
        try:
            self.__msword_thread = MsWordThread(self.__osbm)
            self.__msword_thread.status_changed.connect(self.update_status_msword)
            self.__msword_thread.start()
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error creating MsWordThread: {e}")
            self.__status_msword = False
            if self.__osbm.obj_stab.get_is_active():
                self.__osbm.obj_stab.update_status_msword_label(self.__status_msword)
    else:
        self.__osbm.obj_logg.debug_logger("MsWordThread is already running")
```

## Логика работы

### Последовательность запуска:

1. **Инициализация базовых компонентов** (быстро)
   - Настройка путей
   - Создание папок
   - Инициализация БД
   - Проверка LibreOffice

2. **Создание и показ главного окна** (мгновенно)
   - Настройка шрифтов
   - Создание MainWindow
   - Отображение окна

3. **Асинхронная проверка MS Word** (в фоне)
   - Установка статуса "проверяется" (желтый индикатор)
   - Поиск активного экземпляра Word (3 сек таймаут)
   - Создание нового экземпляра при необходимости
   - Обновление статуса (зеленый/красный индикатор)

### Состояния индикатора MS Word:

- **Красный** (`False`) - MS Word недоступен
- **Желтый** (`None`) - MS Word проверяется
- **Зеленый** (`True`) - MS Word доступен

## Преимущества

1. **Быстрый запуск** - главное окно открывается мгновенно
2. **Отзывчивый интерфейс** - пользователь видит прогресс проверки
3. **Сохранение функционала** - вся логика проверки осталась без изменений
4. **Обратная совместимость** - существующий код продолжает работать

## Тестирование

Для проверки работы создан тестовый скрипт `test_async_init.py`, который демонстрирует:
- Временные характеристики инициализации
- Корректность обновления статусов
- Обработку ошибок

## Совместимость

Изменения полностью совместимы с существующим кодом:
- Метод `resetting_office_packets()` сохранен для обратной совместимости
- Все сигналы и слоты работают как прежде
- Статусная строка корректно отображает все состояния
