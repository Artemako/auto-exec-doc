from PySide6.QtCore import QSettings
import datetime
import os


class SettingsManagerObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm


class SettingsManager:
    def __init__(self):
        # Словарь для преобразования английских названий в русские
        self.__theme_display_names = {
            "dark": "Тёмная",
            "light": "Светлая"
        }
        self.__theme_keys_by_display = {v: k for k, v in self.__theme_display_names.items()}

    def setting_osbm(self, osbm):
        """Сохраняем метод setting_osbm как в оригинальном SettingsDatabase"""
        self.__osbm = SettingsManagerObjectsManager(osbm)
        self.__settings = QSettings("Constanta", "AutoExecDoc")
        self.__osbm.obj_logg.debug_logger("SettingsManager setting_osbm() completed")

    def initialize_default_settings(self):
        """Инициализация настроек по умолчанию"""
        self.__osbm.obj_logg.debug_logger(
            "SettingsManager initialize_default_settings()"
        )

        # Устанавливаем значения по умолчанию, если они еще не существуют
        if not self.__settings.contains("app_converter"):
            self.__settings.setValue("app_converter", "LIBREOFFICE")

        if not self.__settings.contains("libreoffice_path"):
            self.__settings.setValue(
                "libreoffice_path",
                "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
            )

        if not self.__settings.contains("project_current_name"):
            self.__settings.setValue("project_current_name", "")

        # иниц. список проектов, если его нет
        if not self.__settings.contains("projects"):
            self.__settings.setValue("projects", [])

        # настройка темы (сохраняем английское название)
        if not self.__settings.contains("theme"):
            self.__settings.setValue("theme", "dark")

    # region Методы для работы с темой

    def get_theme(self) -> str:
        """Возвращает внутренний ключ темы (dark/light)"""
        result = self.__settings.value("theme", "dark")
        self.__osbm.obj_logg.debug_logger(f"SettingsManager get_theme(): {result}")
        return result

    def get_theme_display_name(self) -> str:
        """Возвращает русское название текущей темы"""
        theme_key = self.get_theme()
        return self.__theme_display_names.get(theme_key, "Тёмная")

    def set_theme_by_display_name(self, display_name: str):
        """Устанавливает тему по русскому названию, сохраняет английский ключ"""
        theme_key = self.__theme_keys_by_display.get(display_name, "dark")
        self.set_theme(theme_key)

    def set_theme(self, theme: str):
        """Сохраняет тему как 'dark' или 'light'"""
        self.__osbm.obj_logg.debug_logger(f"SettingsManager set_theme(): {theme}")
        self.__settings.setValue("theme", theme)

    # endregion

    # region Методы для работы с настройками

    def get_app_converter(self) -> str:
        """Получить выбранный конвертер"""
        result = self.__settings.value("app_converter", "LIBREOFFICE")
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager get_app_converter(): {result}"
        )
        return result

    def set_app_converter(self, app_converter: str):
        """Установить конвертер"""
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager set_app_converter(): {app_converter}"
        )
        self.__settings.setValue("app_converter", app_converter)

    def get_libreoffice_path(self) -> str:
        """Получить путь к LibreOffice"""
        result = self.__settings.value(
            "libreoffice_path", "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        )
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager get_libreoffice_path(): {result}"
        )
        return result

    def set_libreoffice_path(self, path: str):
        """Установить путь к LibreOffice"""
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager set_libreoffice_path(): {path}"
        )
        self.__settings.setValue("libreoffice_path", path)

    def get_project_current_name(self) -> str:
        """Получить имя текущего проекта"""
        result = self.__settings.value("project_current_name", "")
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager get_project_current_name(): {result}"
        )
        return result

    def set_project_current_name(self, project_name: str):
        """Установить имя текущего проекта"""
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager set_project_current_name(): {project_name}"
        )
        self.__settings.setValue("project_current_name", project_name)

    # endregion

    # region Методы для работы с проектами (совместимые с оригинальным интерфейсом)

    def add_new_project_to_db(self):
        """Совместимый метод с оригинальным SettingsDatabase"""
        self.__osbm.obj_logg.debug_logger("SettingsManager add_new_project_to_db()")
        project_dir = self.__osbm.obj_dirm.get_project_dirpath()
        self.add_or_update_project(project_dir)

    def update_project_to_db(self):
        """Совместимый метод с оригинальным SettingsDatabase"""
        self.__osbm.obj_logg.debug_logger("SettingsManager update_project_to_db()")
        project_dir = self.__osbm.obj_dirm.get_project_dirpath()
        self.add_or_update_project(project_dir)

    def add_or_update_open_project_to_db(self):
        """Совместимый метод с оригинальным SettingsDatabase - БЕЗ ПАРАМЕТРОВ"""
        self.__osbm.obj_logg.debug_logger(
            "SettingsManager add_or_update_open_project_to_db()"
        )
        project_dir = self.__osbm.obj_dirm.get_project_dirpath()
        self.add_or_update_project(project_dir)

    def add_or_update_project(self, project_dir: str = None):
        """Основной метод для добавления/обновления проекта"""
        if project_dir is None:
            project_dir = self.__osbm.obj_dirm.get_project_dirpath()

        projects = self.get_projects()
        project_name = os.path.basename(project_dir)
        current_datetime = datetime.datetime.now().replace(microsecond=0).isoformat()

        # Ищем существующий проект
        existing_project = None
        for i, project in enumerate(projects):
            if project.get("directory_project") == project_dir:
                existing_project = i
                break

        project_data = {
            "name_project": project_name,
            "directory_project": project_dir,
            "date_create_project": current_datetime
            if existing_project is None
            else projects[existing_project]["date_create_project"],
            "date_last_open_project": current_datetime,
        }

        if existing_project is not None:
            # Обновляем существующий проект
            projects[existing_project] = project_data
        else:
            # Добавляем новый проект
            projects.append(project_data)

        # Сохраняем обновленный список
        self.__settings.setValue("projects", projects)
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager add_or_update_project(): {project_name}"
        )

    def get_projects(self) -> list:
        """Получить список всех проектов"""
        projects = self.__settings.value("projects", [])
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager get_projects(): {len(projects)} projects"
        )
        return projects

    def get_last_projects(self, limit: int = 5) -> list:
        """Получить последние проекты"""
        projects = self.get_projects()
        # Сортируем по дате последнего открытия
        sorted_projects = sorted(
            projects, key=lambda x: x.get("date_last_open_project", ""), reverse=True
        )
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager get_last_projects(): {len(sorted_projects[:limit])} projects"
        )
        return sorted_projects[:limit]

    def delete_project_from_db(self, project):
        """Совместимый метод с оригинальным SettingsDatabase"""
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager delete_project_from_db(): {project}"
        )
        project_dir = project.get("directory_project")
        self.delete_project(project_dir)

    def delete_project(self, project_dir: str):
        """Удалить проект из списка"""
        projects = self.get_projects()
        projects = [p for p in projects if p.get("directory_project") != project_dir]
        self.__settings.setValue("projects", projects)
        self.__osbm.obj_logg.debug_logger(
            f"SettingsManager delete_project(): {project_dir}"
        )

    # endregion

    def sync(self):
        """Синхронизировать настройки"""
        self.__settings.sync()