import os
import sys
import glob
import subprocess


def check_dependencies():
    """Проверяет наличие всех необходимых библиотек и зависимостей"""
    missing_deps = []
    
    # Проверка pypdf
    try:
        import pypdf
    except ImportError:
        missing_deps.append("pypdf - для работы с PDF файлами")
    
    # Проверка Pillow (PIL)
    try:
        import PIL
        from PIL import Image
    except ImportError:
        missing_deps.append("Pillow (PIL) - для работы с изображениями")
    
    # Проверка olefile (для DOC файлов, опционально)
    olefile_available = False
    try:
        import olefile
        olefile_available = True
    except ImportError:
        # olefile не критичен, но рекомендуется для работы с DOC файлами
        pass
    
    # Проверка pytesseract
    pytesseract_available = False
    try:
        import pytesseract
        pytesseract_available = True
    except ImportError:
        missing_deps.append("pytesseract - для OCR (извлечения текста из изображений)")
    
    # Проверка Tesseract OCR (системная утилита) только если pytesseract установлен
    if pytesseract_available:
        tesseract_found = False
        tesseract_path = None
        
        try:
            # Пробуем получить версию через pytesseract (проверяет PATH и стандартные пути)
            try:
                pytesseract.get_tesseract_version()
                tesseract_found = True
            except Exception as e:
                # Пробуем через subprocess с разными вариантами команды
                commands = ['tesseract', 'tesseract.exe']
                for cmd in commands:
                    try:
                        result = subprocess.run([cmd, '--version'], 
                                              capture_output=True, 
                                              text=True,
                                              timeout=5)
                        if result.returncode == 0:
                            tesseract_found = True
                            tesseract_path = cmd
                            break
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        continue
                
                # Если не нашли в PATH, проверяем стандартные пути Windows
                if not tesseract_found and os.name == 'nt':
                    windows_paths = [
                        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                        r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
                        r'C:\Tesseract-OCR\tesseract.exe',
                    ]
                    
                    for path in windows_paths:
                        if os.path.exists(path):
                            try:
                                result = subprocess.run([path, '--version'], 
                                                      capture_output=True, 
                                                      text=True,
                                                      timeout=5)
                                if result.returncode == 0:
                                    tesseract_found = True
                                    tesseract_path = path
                                    # Устанавливаем путь для pytesseract
                                    import pytesseract
                                    pytesseract.pytesseract.tesseract_cmd = path
                                    break
                            except Exception:
                                continue
                
                # Если все еще не нашли, пробуем найти через where (Windows) или which (Linux/Mac)
                if not tesseract_found:
                    if os.name == 'nt':
                        find_cmd = ['where', 'tesseract']
                    else:
                        find_cmd = ['which', 'tesseract']
                    
                    try:
                        result = subprocess.run(find_cmd, 
                                              capture_output=True, 
                                              text=True,
                                              timeout=5)
                        if result.returncode == 0 and result.stdout.strip():
                            found_path = result.stdout.strip().split('\n')[0]
                            if os.path.exists(found_path):
                                tesseract_found = True
                                tesseract_path = found_path
                                import pytesseract
                                pytesseract.pytesseract.tesseract_cmd = found_path
                    except Exception:
                        pass
                        
        except Exception:
            pass
        
        # Если Tesseract найден, устанавливаем путь глобально для pytesseract
        if tesseract_found and tesseract_path:
            try:
                import pytesseract
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            except Exception:
                pass
        elif not tesseract_found:
            missing_deps.append("Tesseract OCR - системная утилита для распознавания текста (нужно установить отдельно)")
    
    # Если есть отсутствующие зависимости
    if missing_deps:
        print("=" * 60)
        print("ОТСУТСТВУЮТ НЕОБХОДИМЫЕ ЗАВИСИМОСТИ!")
        print("=" * 60)
        print("\nДля работы программы необходимо установить:\n")
        for i, dep in enumerate(missing_deps, 1):
            print(f"{i}. {dep}")
        
        print("\n" + "=" * 60)
        print("ИНСТРУКЦИЯ ПО УСТАНОВКЕ:")
        print("=" * 60)
        
        if "pypdf" in str(missing_deps):
            print("\n• pypdf:  pip install pypdf")
        if "Pillow" in str(missing_deps):
            print("\n• Pillow: pip install Pillow")
        if "pytesseract" in str(missing_deps):
            print("\n• pytesseract: pip install pytesseract")
        
        # Предупреждение об olefile (не критично, но рекомендуется)
        if not olefile_available:
            print("\n• olefile (рекомендуется для работы с DOC файлами): pip install olefile")
        
        if "Tesseract OCR" in str(missing_deps):
            print("\n• Tesseract OCR:")
            print("  Windows: скачайте с https://github.com/UB-Mannheim/tesseract/wiki")
            print("           или используйте: choco install tesseract")
            print("  Linux:   sudo apt-get install tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng")
            print("  macOS:   brew install tesseract")
            print("\n  После установки Tesseract добавьте языковые пакеты:")
            print("  - Русский: tesseract-ocr-rus или tesseract-lang-rus")
            print("  - Английский: обычно включен по умолчанию")
        
        print("\n" + "=" * 60)
        print("После установки всех зависимостей запустите программу снова.")
        print("=" * 60)
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    # Если все зависимости есть, продолжаем импорт
    if not missing_deps:
        print("✓ Все зависимости установлены. Запуск программы...\n")
    return len(missing_deps) == 0


# Проверяем зависимости перед импортом функций
if check_dependencies():
    from func.pdftoimg import extract_images_from_pdf
    from func.doctoimg import extract_images_from_doc
    from func.imgtotext import get_image_folders, extract_text_from_images


def clear_screen():
    """Очищает экран"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_documents():
    """Получает список документов (PDF, DOC, DOCX) в текущей директории"""
    documents = []
    
    # Ищем PDF файлы
    pdf_files = glob.glob('*.pdf')
    documents.extend([(f, 'pdf') for f in pdf_files])
    
    # Ищем DOC файлы
    doc_files = glob.glob('*.doc')
    documents.extend([(f, 'doc') for f in doc_files])
    
    # Ищем DOCX файлы
    docx_files = glob.glob('*.docx')
    documents.extend([(f, 'docx') for f in docx_files])
    
    return documents


def extract_images_menu():
    """Меню для извлечения изображений из документов"""
    while True:
        clear_screen()
        print("|Вытащить из документа изображения|")
        print()
        
        documents = get_documents()
        
        if not documents:
            print("Документы не найдены в текущей директории")
            print("\n0 Назад в главное меню")
            choice = input("\n===============> ")
            if choice == '0':
                return
            continue
        
        # Показываем список документов
        for i, (filename, filetype) in enumerate(documents, 1):
            print(f"{i} {filename}")
        
        print("0 Назад в главное меню")
        choice = input("\n===============> ")
        
        if choice == '0':
            return
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(documents):
                selected_file, file_type = documents[choice_num - 1]
                
                # Создаем папку для изображений
                file_name_without_ext = os.path.splitext(selected_file)[0]
                output_folder = os.path.join('done', file_name_without_ext)
                
                print(f"\nИзвлечение изображений из {selected_file}...")
                
                # Извлекаем изображения в зависимости от типа файла
                if file_type == 'pdf':
                    saved_images = extract_images_from_pdf(selected_file, output_folder)
                    if saved_images:
                        print(f"Извлечено {len(saved_images)} изображений в папку: {output_folder}")
                    else:
                        print("Изображения не найдены в документе")
                elif file_type in ['doc', 'docx']:
                    saved_images = extract_images_from_doc(selected_file, output_folder)
                    if saved_images:
                        print(f"Извлечено {len(saved_images)} изображений в папку: {output_folder}")
                    else:
                        print("Изображения не найдены в документе")
                
                input("\nНажмите Enter для продолжения...")
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")
        except ValueError:
            print("Неверный ввод!")
            input("Нажмите Enter для продолжения...")
        except Exception as e:
            print(f"Ошибка: {e}")
            input("Нажмите Enter для продолжения...")


def extract_text_menu():
    """Меню для извлечения текста из изображений"""
    while True:
        clear_screen()
        print("|папки с изображениями|")
        print()
        
        folders = get_image_folders('done')
        
        if not folders:
            print("Папки с изображениями не найдены в папке 'done'")
            print("\n0 Назад в главное меню")
            choice = input("\n===============> ")
            if choice == '0':
                return
            continue
        
        # Показываем список папок
        for i, folder_path in enumerate(folders, 1):
            folder_name = os.path.basename(folder_path)
            print(f"{i} {folder_name}")
        
        print("0 Назад в главное меню")
        choice = input("\n===============> ")
        
        if choice == '0':
            return
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(folders):
                selected_folder = folders[choice_num - 1]
                
                print(f"\nОбработка папки: {os.path.basename(selected_folder)}...")
                result_file = extract_text_from_images(selected_folder)
                
                if result_file:
                    print(f"Готово! Файл сохранен: {result_file}")
                else:
                    print("Не удалось извлечь текст")
                
                input("\nНажмите Enter для продолжения...")
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")
        except ValueError:
            print("Неверный ввод!")
            input("Нажмите Enter для продолжения...")
        except Exception as e:
            print(f"Ошибка: {e}")
            input("Нажмите Enter для продолжения...")


def main_menu():
    """Главное меню программы"""
    while True:
        clear_screen()
        print("|Меню|")
        print()
        print("1   Вытащить из документа изображения")
        print("2  Извлечь из изображений текст")
        print("0  Выход")
        print()
        choice = input("===============> ")
        
        if choice == '1':
            extract_images_menu()
        elif choice == '2':
            extract_text_menu()
        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")
            input("Нажмите Enter для продолжения...")


if __name__ == "__main__":
    main_menu()

