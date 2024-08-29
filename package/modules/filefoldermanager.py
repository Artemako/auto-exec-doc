import os
import shutil
import base64
import datetime
import uuid

class FileFolderManagerObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm
        self.obj_setdb = osbm.obj_setdb


class FileFolderManager:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = FileFolderManagerObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(f"FileFolderManager setting_osbm():\nself.__osbm = {self.__osbm}")


    def create_and_setting_files_and_folders(self):
        """
        Создание и конфигурация папок и файлов.
        """
        self.__osbm.obj_logg.debug_logger(
            "FileFolderManager create_and_setting_files_and_folders()"
        )
        if not os.path.exists(
            self.__osbm.obj_dirm.get_default_folder_projects_dirpath()
        ):
            os.mkdir(self.__osbm.obj_dirm.get_default_folder_projects_dirpath())

    def check_aed_file(self):
        """
        Создание файла aed.
        """
        self.__osbm.obj_logg.debug_logger("FileFolderManager check_aed_file()")
        # создать указатель файл
        name_aed = self.__osbm.obj_setdb.get_project_current_name()
        aedfilename = f"{name_aed}.aed"
        aedfilepath = os.path.join(
            self.__osbm.obj_dirm.get_project_dirpath(), aedfilename
        )
        if not os.path.exists(aedfilepath):
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

    def create_folders_and_aed_for_project(self):
        """
        Добавление в проект папок форм.
        """
        self.__osbm.obj_logg.debug_logger(
            "FileFolderManager create_folders_and_aed_for_project()"
        )
        # файл project.aed
        self.check_aed_file()
        # папка forms в проекте
        forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()

        if not os.path.exists(forms_folder_dirpath):
            os.makedirs(forms_folder_dirpath)

        # папка images в проекте
        image_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()

        if not os.path.exists(image_folder_dirpath):
            os.makedirs(image_folder_dirpath)

        # # папка с pdfs
        pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()

        if not os.path.exists(pdfs_folder_dirpath):
            os.makedirs(pdfs_folder_dirpath)

        # Папка TEMP/AUTOEXECDOC
        if not os.path.exists(self.__osbm.obj_dirm.get_temp_dirpath()):
            os.makedirs(self.__osbm.obj_dirm.get_temp_dirpath())


    def clear_temp_folder(self, is_del_folder=False):
        """
        Очистка папки temp.
        """
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager clear_temp_folder(is_del_folder):\nis_del_folder = {is_del_folder},\ntemp_dirpath = {self.__osbm.obj_dirm.get_temp_dirpath()}"
        )
        temp_dirpath = self.__osbm.obj_dirm.get_temp_dirpath()
        try:
            shutil.rmtree(temp_dirpath)
            if not is_del_folder:
                os.mkdir(temp_dirpath)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def move_image_from_temp_to_project(self, name_image):
        self.__osbm.obj_logg.debug_logger(
            "FileFolderManager move_image_from_temp_to_project()"
        )
        # путь к папке с шаблонами
        temp_dirpath = self.__osbm.obj_dirm.get_temp_dirpath()
        image_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()
        try:
            shutil.move(
                os.path.join(temp_dirpath, name_image),
                os.path.join(image_folder_dirpath, name_image),
            )
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def delete_image_from_project(self, image_dirpath):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager delete_image_from_project(image_dirpath):\nimage_dirpath = {image_dirpath}"
        )
        # путь к папке с шаблонами
        image_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()
        print(f"image_folder_dirpath = {image_folder_dirpath}")
        try:
            os.remove(os.path.join(image_folder_dirpath, image_dirpath))
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def copy_project_for_saveas(self, old_folder_path, new_folder_path):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager copy_project_for_saveas(old_folder_path, new_folder_path):\nold_folder_path = {old_folder_path},\nnew_folder_path = {new_folder_path}"
        )
        for f in os.listdir(old_folder_path):
            src_path = os.path.join(old_folder_path, f)
            dest_path = os.path.join(new_folder_path, f)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            elif os.path.isfile(src_path):
                if not f.endswith(".aed"):
                    shutil.copy(src_path, dest_path)

    def copy_file(self, src_path, dest_path):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager copy_file(src_path, dest_path):\nsrc_path = {src_path},\ndest_path = {dest_path}"
        )
        try:
            shutil.copy(src_path, dest_path)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def docx_from_temp_to_forms(self, temp_copy_file_path, file_name):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager docx_from_temp_to_forms(temp_copy_file_path, file_name):\ntemp_copy_file_path = {temp_copy_file_path},\nfile_name = {file_name}"
        )
        # к папке с шаблонами
        forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
        try:
            file_name_with_docx = file_name + ".docx"
            shutil.move(
                temp_copy_file_path,
                os.path.join(forms_folder_dirpath, file_name_with_docx),
            )
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def pdf_from_temp_to_pdfs(self, temp_copy_file_path, file_name):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager pdf_from_temp_to_pdfs(temp_copy_file_path, file_name):\ntemp_copy_file_path = {temp_copy_file_path},\nfile_name = {file_name}"
        )
        # к папке с pdfs
        pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
        try:
            file_name_with_docx = file_name + ".pdf"
            shutil.move(
                temp_copy_file_path,
                os.path.join(pdfs_folder_dirpath, file_name_with_docx),
            )
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def copynew_page_for_new_template(self, old_page_filename, typefile_page):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager copynew_page_for_new_template(old_page_filename, typefile_page):\nold_page_filename = {old_page_filename},\ntypefile_page = {typefile_page}"
        )
        old_page_path = str()
        new_page_path = str()
        # генерируем новый id и имя для новой страницы
        unique_id = f"{str(uuid.uuid4().hex)[:3]}-{id(old_page_path)%1000}"
        new_page_filename = f"{unique_id}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        # в зависимости от ...
        if typefile_page == "DOCX":
            forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
            old_page_path = os.path.join(forms_folder_dirpath, old_page_filename + ".docx")
            new_page_path = os.path.join(forms_folder_dirpath, new_page_filename + ".docx")
        elif typefile_page == "PDF":
            pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
            old_page_path = os.path.join(pdfs_folder_dirpath, old_page_filename + ".pdf") 
            new_page_path = os.path.join(pdfs_folder_dirpath, new_page_filename + ".pdf")       
        # копирование
        self.copy_file(old_page_path, new_page_path)       
        return new_page_filename

    def delete_page_from_project(self, page_filename, typefile_page):
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager delete_page_from_project(page_filename, typefile_page):\npage_filename = {page_filename}\n typefile_page = {typefile_page}"
        )
        if typefile_page == "DOCX":
            forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
            page_path = os.path.join(forms_folder_dirpath, page_filename + ".docx")
        elif typefile_page == "PDF":
            pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
            page_path = os.path.join(pdfs_folder_dirpath, page_filename + ".pdf")
        #
        try:
            os.remove(page_path)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)

    def get_list_of_docx_in_forms_folder(self):
        forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
        result = os.listdir(forms_folder_dirpath)
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager get_list_of_docx_in_forms_folder(): \n result = {result}"
        )
        return result
    
    def get_list_of_pdfs_in_pdfs_folder(self):
        pdfs_folder_dirpath = self.__osbm.obj_dirm.get_pdfs_folder_dirpath()
        result = os.listdir(pdfs_folder_dirpath)
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager get_list_of_pdfs_in_pdfs_folder(): \n result = {result}"
        )
        return result
    
    def get_list_of_images_in_images_folder(self):
        images_folder_dirpath = self.__osbm.obj_dirm.get_images_folder_dirpath()
        result = os.listdir(images_folder_dirpath)
        self.__osbm.obj_logg.debug_logger(
            f"FileFolderManager get_list_of_images_in_images_folder(): \n result = {result}"
        )
        return result
    

# obj_film = FileFolderManager()  