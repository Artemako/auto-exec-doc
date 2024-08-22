from multiprocessing import Pool
from PIL import Image
from PIL import ExifTags
import os

def process_image(file_path):
    image = Image.open(file_path)

    # Получение EXIF данных
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if exif is not None:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == 'Orientation':
                    orientation = value
                    break
            
            # Корректировка ориентации
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)

    # Пример обработки: изменение размера
    image = image.resize((100, 100))
    
    # Сохранение обработанного изображения
    output_path = os.path.join('output', os.path.basename(file_path))
    image.save(output_path)

def main():
    # Получение списка файлов изображений
    image_folder = 'images'
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('JPG', 'JPEG', 'PNG'))]

    # Создание папки для сохранения обработанных изображений, если она не существует
    os.makedirs('output', exist_ok=True)

    # Использование Pool для обработки изображений
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_image, image_files)

if __name__ == '__main__':
    main()
