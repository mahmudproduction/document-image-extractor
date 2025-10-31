import os
import zipfile


def extract_images_from_docx(docx_path, output_folder):
    """
    Извлекает изображения из DOCX файла (DOCX - это ZIP архив)
    
    Args:
        docx_path: путь к DOCX файлу
        output_folder: папка для сохранения изображений
    
    Returns:
        список путей к сохраненным изображениям
    """
    saved_images = []
    
    try:
        # DOCX файлы - это ZIP архивы
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            # Извлекаем все файлы из папки word/media/ (там хранятся изображения)
            image_files = [f for f in zip_ref.namelist() if f.startswith('word/media/')]
            
            for image_file in image_files:
                try:
                    # Извлекаем файл
                    file_data = zip_ref.read(image_file)
                    
                    # Получаем имя файла
                    filename = os.path.basename(image_file)
                    
                    # Сохраняем изображение
                    image_path = os.path.join(output_folder, filename)
                    
                    # Если файл уже существует, добавляем префикс
                    if os.path.exists(image_path):
                        name, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(image_path):
                            image_path = os.path.join(output_folder, f"{name}_{counter}{ext}")
                            counter += 1
                    
                    with open(image_path, 'wb') as f:
                        f.write(file_data)
                    
                    saved_images.append(image_path)
                    
                except Exception as e:
                    print(f"Ошибка при извлечении {image_file}: {e}")
                    continue
                    
    except Exception as e:
        print(f"Ошибка при открытии DOCX файла: {e}")
    
    return saved_images


def extract_images_from_doc_old(doc_path, output_folder):
    """
    Извлекает изображения из DOC файла (старый формат OLE2)
    
    Args:
        doc_path: путь к DOC файлу
        output_folder: папка для сохранения изображений
    
    Returns:
        список путей к сохраненным изображениям
    """
    saved_images = []
    
    try:
        # DOC файлы - это OLE2 файлы (более сложный формат)
        # Используем библиотеку olefile для работы с DOC
        import olefile
        
        if not olefile.isOleFile(doc_path):
            print("Файл не является корректным DOC файлом")
            return []
        
        with olefile.OleFileIO(doc_path) as ole:
            # В DOC файлах изображения хранятся в разных местах
            # Пробуем найти изображения в потоках
            
            stream_names = ole.listdir()
            
            # Пробуем найти все потоки и искать в них изображения по сигнатурам
            for stream_name in stream_names:
                try:
                    stream_path = '/'.join(stream_name) if isinstance(stream_name, tuple) else stream_name
                    stream_data = ole.openstream(stream_path).read()
                    
                    # Проверяем сигнатуры изображений
                    if stream_data.startswith(b'\xff\xd8\xff'):  # JPEG
                        ext = '.jpg'
                    elif stream_data.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
                        ext = '.png'
                    elif stream_data.startswith(b'GIF87a') or stream_data.startswith(b'GIF89a'):  # GIF
                        ext = '.gif'
                    elif stream_data.startswith(b'BM'):  # BMP
                        ext = '.bmp'
                    else:
                        continue
                    
                    # Сохраняем изображение
                    filename = f"image_{stream_path.replace('/', '_')}{ext}"
                    image_path = os.path.join(output_folder, filename)
                    
                    # Если файл уже существует, добавляем префикс
                    if os.path.exists(image_path):
                        name, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(image_path):
                            image_path = os.path.join(output_folder, f"{name}_{counter}{ext}")
                            counter += 1
                    
                    with open(image_path, 'wb') as f:
                        f.write(stream_data)
                    
                    saved_images.append(image_path)
                    
                except Exception:
                    continue
                    
    except ImportError:
        print("Для работы с DOC файлами необходима библиотека olefile")
        print("Установите: pip install olefile")
        return []
    except Exception as e:
        print(f"Ошибка при извлечении изображений из DOC файла: {e}")
    
    return saved_images


def extract_images_from_doc(doc_path, output_folder):
    """
    Извлекает изображения из DOC/DOCX файла и сохраняет их в указанную папку
    
    Args:
        doc_path: путь к DOC/DOCX файлу
        output_folder: папка для сохранения изображений
    
    Returns:
        список путей к сохраненным изображениям
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Определяем тип файла по расширению
    file_ext = os.path.splitext(doc_path)[1].lower()
    
    if file_ext == '.docx':
        return extract_images_from_docx(doc_path, output_folder)
    elif file_ext == '.doc':
        return extract_images_from_doc_old(doc_path, output_folder)
    else:
        print(f"Неподдерживаемый формат файла: {file_ext}")
        return []

