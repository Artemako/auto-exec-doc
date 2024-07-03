import os
import shutil
import base64
import datetime


class FileFolderManager:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager

    def create_and_config_files_and_folders(self):
        """
        Создание и конфигурация папок и файлов.
        """
        self.__obs_manager.obj_l.debug_logger("IN create_and_config_files_and_folders()")
        if not os.path.exists(
            self.__obs_manager.obj_dpm.get_default_folder_projects_dirpath()
        ):
            os.mkdir(
                self.__obs_manager.obj_dpm.get_default_folder_projects_dirpath()
            )

    def create_folders_for_new_project(self):
        """
        Добавление в проект папок форм.
        """
        self.__obs_manager.obj_l.debug_logger("IN add_forms_folders_to_new_project()")

        # создать указатель файл
        aedfilename = f"{self.__obs_manager.obj_p.get_current_name()}.aed"
        aedfilepath = os.path.join(
            self.__obs_manager.obj_dpm.get_project_dirpath(), aedfilename
        )
        aedfile = open(aedfilepath, "a+")
        # перевести в base64
        message = f"{aedfilename} {aedfilepath} {datetime.datetime.now()}"
        message_bytes = message.encode("utf-8")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("utf-8")
        print(base64_message)
        # записать в файл
        aedfile.write(base64_message)
        aedfile.close()

        # папка forms в проекте
        forms_folder_dirpath = self.__obs_manager.obj_dpm.get_forms_folder_dirpath()

        if not os.path.exists(forms_folder_dirpath):
            os.makedirs(forms_folder_dirpath)

        # папка images в проекте
        image_folder_dirpath = (
            self.__obs_manager.obj_dpm.get_images_folder_dirpath()
        )

        if not os.path.exists(image_folder_dirpath):
            os.makedirs(image_folder_dirpath)

        # # папка с pdfs
        # pdfs_folder_dirpath = dirpathsmanager.obj_dpm.get_pdfs_folder_dirpath()

        # if not os.path.exists(pdfs_folder_dirpath):
        #     os.makedirs(pdfs_folder_dirpath)

        # Папка TEMP/AUTOEXECDOC
        if not os.path.exists(self.__obs_manager.obj_dpm.get_temp_dirpath()):
            os.makedirs(self.__obs_manager.obj_dpm.get_temp_dirpath())

    def copy_templates_to_forms_folder(self):
        """
        Копирование шаблонов в папку forms.
        """
        self.__obs_manager.obj_l.debug_logger("IN copy_templates_to_forms_folder()")

        templates_main_dirpath = (
            self.__obs_manager.obj_dpm.get_templates_main_dirpath()
        )
        forms_folder_dirpath = self.__obs_manager.obj_dpm.get_forms_folder_dirpath()

        # копирование шаблонов в папку проекта forms
        for f in os.listdir(templates_main_dirpath):
            shutil.copy(
                os.path.join(templates_main_dirpath, f),
                os.path.join(forms_folder_dirpath, f),
            )

    def clear_temp_folder(self, is_del_folder=False):
        """
        Очистка папки temp.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"IN clear_temp_folder(is_del_folder): is_del_folder = {is_del_folder}, temp_dirpath = {self.__obs_manager.obj_dpm.get_temp_dirpath()}"
        )
        temp_dirpath = self.__obs_manager.obj_dpm.get_temp_dirpath()
        try:
            shutil.rmtree(temp_dirpath)
            if not is_del_folder:
                os.mkdir(temp_dirpath)
        except Exception as e:
            self.__obs_manager.obj_l.error_logger(e)

    def move_image_from_temp_to_project(self, name_image):
        self.__obs_manager.obj_l.debug_logger("IN move_image_from_temp_to_project()")
        # путь к папке с шаблонами
        temp_dirpath = self.__obs_manager.obj_dpm.get_temp_dirpath()
        image_folder_dirpath = os.path.join(
            self.__obs_manager.obj_dpm.get_project_dirpath(), "images"
        )
        try:
            shutil.move(
                os.path.join(temp_dirpath, name_image),
                os.path.join(image_folder_dirpath, name_image),
            )
        except Exception as e:
            self.__obs_manager.obj_l.error_logger(e)

    def delete_image_from_project(self, image_dirpath):
        self.__obs_manager.obj_l.debug_logger("IN delete_image_from_project()")
        # путь к папке с шаблонами
        image_folder_dirpath = os.path.join(
            self.__obs_manager.obj_dpm.get_project_dirpath(), "images"
        )
        try:
            os.remove(os.path.join(image_folder_dirpath, image_dirpath))
        except Exception as e:
            self.__obs_manager.obj_l.error_logger(e)


# obj_ffm = FileFolderManager()
