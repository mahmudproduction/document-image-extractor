# Инструкция по загрузке проекта на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Откройте [GitHub.com](https://github.com) и войдите в свой аккаунт
2. Нажмите кнопку **"+"** в правом верхнем углу и выберите **"New repository"**
3. Заполните форму:
   - **Repository name**: например `document-image-extractor` или `pdf-image-ocr`
   - **Description**: "Утилита для извлечения изображений из документов и распознавания текста"
   - Выберите **Public** или **Private**
   - **НЕ** добавляйте README, .gitignore или license (мы уже создали их)
4. Нажмите **"Create repository"**

## Шаг 2: Подключите локальный репозиторий к GitHub

После создания репозитория GitHub покажет вам команды. Выполните следующие команды:

```bash
# Замените YOUR_USERNAME на ваш GitHub username и REPOSITORY_NAME на название репозитория
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

Или если вы используете SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

## Альтернативный способ через GitHub CLI

Если у вас установлен GitHub CLI:

```bash
gh repo create REPOSITORY_NAME --public --source=. --remote=origin --push
```

## Шаг 3: Проверьте результат

Откройте ваш репозиторий на GitHub и убедитесь, что все файлы загружены:
- ✅ convert.py
- ✅ func/ (папка с функциями)
- ✅ README.md
- ✅ .gitignore

## Полезные команды Git

```bash
# Проверить статус
git status

# Добавить изменения
git add .

# Сделать коммит
git commit -m "Описание изменений"

# Отправить изменения на GitHub
git push

# Получить изменения с GitHub
git pull
```

## Настройка Git (если еще не настроено)

Если это первый раз когда вы используете Git, выполните:

```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш@email.com"
```

