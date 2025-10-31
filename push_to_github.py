import subprocess
import sys
import os


def run_command(command, check=True):
    """Выполняет команду и возвращает результат"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if result.returncode != 0 and check:
            print(f"Ошибка: {result.stderr}")
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        print(f"Исключение при выполнении команды: {e}")
        return False, str(e)


def check_git_config():
    """Проверяет настройки Git"""
    print("\n" + "="*60)
    print("Проверка настроек Git...")
    print("="*60)
    
    # Проверяем user.name
    success, output = run_command("git config user.name", check=False)
    if not success or not output.strip():
        print("⚠ Имя пользователя Git не настроено")
        name = input("Введите ваше имя для Git: ").strip()
        if name:
            run_command(f'git config --global user.name "{name}"')
    else:
        print(f"✓ Имя пользователя: {output.strip()}")
    
    # Проверяем user.email
    success, output = run_command("git config user.email", check=False)
    if not success or not output.strip():
        print("⚠ Email пользователя Git не настроен")
        email = input("Введите ваш email для Git: ").strip()
        if email:
            run_command(f'git config --global user.email "{email}"')
    else:
        print(f"✓ Email: {output.strip()}")


def check_git_repo():
    """Проверяет, является ли текущая директория git репозиторием"""
    success, _ = run_command("git rev-parse --git-dir", check=False)
    return success


def get_repository_info():
    """Запрашивает информацию о репозитории"""
    print("\n" + "="*60)
    print("Информация о репозитории GitHub")
    print("="*60)
    
    username = input("Введите ваш GitHub username: ").strip()
    if not username:
        print("❌ Username обязателен!")
        sys.exit(1)
    
    repo_name = input("Введите название репозитория: ").strip()
    if not repo_name:
        print("❌ Название репозитория обязательно!")
        sys.exit(1)
    
    # Убираем .git из названия, если есть
    repo_name = repo_name.replace('.git', '')
    
    use_ssh = input("Использовать SSH? (y/n, по умолчанию n): ").strip().lower()
    use_ssh = use_ssh == 'y' or use_ssh == 'yes'
    
    return username, repo_name, use_ssh


def setup_remote(username, repo_name, use_ssh):
    """Настраивает remote репозиторий"""
    if use_ssh:
        remote_url = f"git@github.com:{username}/{repo_name}.git"
    else:
        remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"\n🔗 Настройка remote: {remote_url}")
    
    # Проверяем, есть ли уже remote origin
    success, output = run_command("git remote get-url origin", check=False)
    if success:
        current_url = output.strip()
        print(f"⚠ Remote 'origin' уже настроен: {current_url}")
        
        # Проверяем, правильно ли настроен URL
        if current_url != remote_url:
            print(f"⚠ URL отличается от ожидаемого!")
            print(f"   Текущий: {current_url}")
            print(f"   Ожидается: {remote_url}")
            change = input("Изменить на правильный? (y/n): ").strip().lower()
            if change == 'y' or change == '':
                success, _ = run_command(f'git remote set-url origin {remote_url}')
                if success:
                    print("✓ URL обновлен")
                else:
                    print("❌ Не удалось обновить URL")
            else:
                print("⚠ Используется существующий URL")
        else:
            print("✓ Remote URL настроен правильно")
    else:
        # Добавляем новый remote
        print("➕ Добавление нового remote...")
        success, _ = run_command(f'git remote add origin {remote_url}')
        if not success:
            print("⚠ Не удалось добавить remote, возможно он уже существует")
            change = input("Попробовать изменить существующий? (y/n): ").strip().lower()
            if change == 'y' or change == '':
                run_command(f'git remote set-url origin {remote_url}')
            else:
                return False
    
    # Проверяем финальный URL
    success, output = run_command("git remote get-url origin", check=False)
    if success:
        print(f"✓ Remote настроен: {output.strip()}")
    
    return True


def commit_and_push():
    """Выполняет коммит и пуш"""
    print("\n" + "="*60)
    print("Коммит и загрузка на GitHub")
    print("="*60)
    
    # Проверяем статус
    print("\n📋 Текущий статус:")
    run_command("git status")
    
    # Проверяем, есть ли изменения для коммита
    success, output = run_command("git diff --cached --name-only", check=False)
    has_staged = success and output.strip()
    
    if not has_staged:
        print("\n⚠ Нет файлов для коммита. Добавляем все файлы...")
        run_command("git add .")
    
    # Проверяем, есть ли коммиты
    success, output = run_command("git log --oneline -1", check=False)
    has_commits = success and output.strip()
    
    if not has_commits:
        message = input("\nВведите сообщение для первого коммита (или Enter для значения по умолчанию): ").strip()
        if not message:
            message = "Initial commit: Document Image Extractor & OCR Tool"
        
        print(f"\n💾 Создание коммита: {message}")
        success, _ = run_command(f'git commit -m "{message}"')
        if not success:
            print("❌ Ошибка при создании коммита")
            return False
    
    # Переименовываем ветку в main, если нужно
    success, output = run_command("git branch --show-current", check=False)
    current_branch = output.strip() if success else "master"
    
    if current_branch != "main":
        print(f"\n🔄 Переименование ветки {current_branch} -> main")
        run_command("git branch -M main")
    
    # Push
    print("\n🚀 Загрузка на GitHub...")
    success, output = run_command("git push -u origin main", check=False)
    
    if success:
        print("\n" + "="*60)
        print("✅ Успешно! Код загружен на GitHub")
        print("="*60)
        return True
    else:
        print("\n" + "="*60)
        print("❌ Ошибка при загрузке")
        print("="*60)
        print(f"\nДетали ошибки:\n{output}")
        
        # Проверяем тип ошибки
        if "not found" in output.lower() or "repository" in output.lower():
            print("\n⚠ Репозиторий не найден на GitHub!")
            print("📝 Действия:")
            print("1. Откройте https://github.com/new")
            print("2. Создайте новый репозиторий с названием: document-image-extractor")
            print("3. НЕ добавляйте README, .gitignore или license")
            print("4. Запустите скрипт снова")
        elif "authentication" in output.lower() or "denied" in output.lower() or "permission" in output.lower():
            print("\n⚠ Проблема с аутентификацией!")
            print("📝 Для HTTPS нужен Personal Access Token вместо пароля:")
            print("1. Откройте https://github.com/settings/tokens")
            print("2. Generate new token (classic)")
            print("3. Выберите права: repo (все)")
            print("4. Используйте токен вместо пароля при запросе")
        elif "could not read" in output.lower():
            print("\n⚠ Проблема с доступом к репозиторию!")
            print("Проверьте, что репозиторий создан и у вас есть права доступа")
        else:
            print("\nВозможные причины:")
            print("1. Репозиторий не создан на GitHub - создайте его сначала")
            print("2. Неверные учетные данные - проверьте username и название репозитория")
            print("3. Проблемы с доступом - проверьте права доступа к репозиторию")
        
        return False


def main():
    """Главная функция"""
    print("="*60)
    print("🚀 Автоматическая загрузка проекта на GitHub")
    print("="*60)
    
    # Проверяем настройки Git
    check_git_config()
    
    # Проверяем, что мы в git репозитории
    if not check_git_repo():
        print("\n⚠ Текущая директория не является git репозиторием")
        init = input("Инициализировать git репозиторий? (y/n): ").strip().lower()
        if init == 'y':
            run_command("git init")
            print("✓ Git репозиторий инициализирован")
        else:
            print("❌ Прерывание операции")
            sys.exit(1)
    
    # Получаем информацию о репозитории
    username, repo_name, use_ssh = get_repository_info()
    
    # Настраиваем remote
    setup_remote(username, repo_name, use_ssh)
    
    # Коммитим и пушим
    if commit_and_push():
        print(f"\n🌐 Ваш репозиторий: https://github.com/{username}/{repo_name}")
    else:
        print("\n💡 Попробуйте выполнить команды вручную или проверьте настройки")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Операция прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1)

