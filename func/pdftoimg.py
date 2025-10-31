import os
from pypdf import PdfReader
from PIL import Image
import io


def extract_images_from_pdf(pdf_path, output_folder):
    """
    Извлекает изображения из PDF файла и сохраняет их в указанную папку
    
    Args:
        pdf_path: путь к PDF файлу
        output_folder: папка для сохранения изображений
    
    Returns:
        список путей к сохраненным изображениям
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    saved_images = []
    reader = PdfReader(pdf_path)
    
    for page_num, page in enumerate(reader.pages):
        try:
            resources = page.get('/Resources', {})
            if not resources:
                continue
            
            xObject = resources.get('/XObject')
            if not xObject:
                continue
            
            xObject_dict = xObject.get_object() if hasattr(xObject, 'get_object') else xObject
            
            for obj_name in xObject_dict:
                try:
                    obj = xObject_dict[obj_name]
                    if hasattr(obj, 'get_object'):
                        obj = obj.get_object()
                    
                    if not isinstance(obj, dict):
                        continue
                    
                    if obj.get('/Subtype') == '/Image':
                        try:
                            data = obj.get_data()
                            
                            # Определяем расширение файла
                            filter_type = obj.get('/Filter')
                            if isinstance(filter_type, list):
                                filter_type = filter_type[0]
                            
                            # JPEG изображения
                            if filter_type == '/DCTDecode':
                                ext = '.jpg'
                            # PNG изображения  
                            elif filter_type == '/FlateDecode':
                                ext = '.png'
                            # CCITTFaxDecode (обычно TIFF)
                            elif filter_type == '/CCITTFaxDecode':
                                ext = '.tiff'
                            # Другие форматы
                            else:
                                ext = '.png'
                            
                            # Сохраняем изображение
                            clean_name = obj_name.replace('/', '_').replace(' ', '_')
                            image_path = os.path.join(output_folder, f'image_page{page_num + 1}_{clean_name}{ext}')
                            
                            with open(image_path, 'wb') as img_file:
                                img_file.write(data)
                            
                            saved_images.append(image_path)
                            
                        except Exception as e:
                            print(f"Ошибка при извлечении изображения {obj_name}: {e}")
                            continue
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Ошибка при обработке страницы {page_num + 1}: {e}")
            continue
    
    return saved_images

