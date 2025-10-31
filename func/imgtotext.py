import os
from PIL import Image
import pytesseract
import glob


def get_image_folders(base_folder='done'):
    """
    Получает список всех папок с изображениями в указанной директории
    
    Args:
        base_folder: базовая папка для поиска
    
    Returns:
        список путей к папкам
    """
    if not os.path.exists(base_folder):
        return []
    
    folders = []
    for item in os.listdir(base_folder):
        item_path = os.path.join(base_folder, item)
        if os.path.isdir(item_path):
            folders.append(item_path)
    
    return folders


def extract_text_from_images(folder_path):
    """
    Извлекает текст из всех изображений в папке с помощью OCR
    Поддерживает русский и английский языки
    
    Args:
        folder_path: путь к папке с изображениями
    
    Returns:
        путь к созданному текстовому файлу
    """
    # Поддерживаемые форматы изображений
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.gif']
    
    # Собираем все изображения из папки
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not image_files:
        print(f"В папке {folder_path} не найдено изображений")
        return None
    
    # Извлекаем имя папки для имени файла
    folder_name = os.path.basename(folder_path)
    output_file = os.path.join(folder_path, f'{folder_name}.txt')
    
    # OCR с поддержкой русского и английского
    all_text = []
    
    print(f"Обработка {len(image_files)} изображений...")
    for i, image_path in enumerate(sorted(image_files), 1):
        print(f"Обработка изображения {i}/{len(image_files)}: {os.path.basename(image_path)}")
        
        try:
            image = Image.open(image_path)
            
            # Извлекаем текст с русским и английским языками
            text = pytesseract.image_to_string(image, lang='rus+eng')
            
            if text.strip():
                all_text.append(f"\n{'='*50}\n")
                all_text.append(f"Изображение: {os.path.basename(image_path)}\n")
                all_text.append(f"{'='*50}\n\n")
                all_text.append(text)
                all_text.append("\n\n")
                
        except Exception as e:
            print(f"Ошибка при обработке {image_path}: {e}")
            continue
    
    # Сохраняем результат
    if all_text:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(all_text))
        print(f"\nТекст сохранен в: {output_file}")
        return output_file
    else:
        print("Текст не был извлечен из изображений")
        return None

