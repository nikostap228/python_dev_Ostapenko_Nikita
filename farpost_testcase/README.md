# Python Developer Test Task

Проект для аналитики действий пользователей в блоге. Реализованы две SQLite базы данных и REST API для получения статистики.

## Технологии
- Python 3.11+
- Django 5.2
- Django REST Framework 3.16
- SQLite (две отдельные базы данных)
- python-dotenv


## Установка и запуск

### Клонирование репозитория и запуск проекта
```bash
git clone https://github.com/nikostap228/python_dev_Ostapenko_Nikita.git
cd python_dev_Ostapenko_Nikita

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Скопируйте файл с примером переменных
copy .env.example .env      # Windows

cp .env.example .env        # Linux/Mac

# Первая база данных (авторы, блоги, посты)
python manage.py migrate --database=default

# Вторая база данных (логи)
python manage.py migrate --database=logs_db

# Заполнение типов пространств (global, blog, post) и событий (login, logout, comment)
python manage.py seed_logs

# Заполнение авторов, блогов и постов
python manage.py seed_authors

# Запуск сервера
python manage.py runserver 
