# TeamFinder

Платформа для поиска единомышленников для совместной работы над pet-проектами.

## Возможности

- Регистрация и авторизация по email
- Создание, редактирование и завершение проектов
- Отклик на участие в проектах
- Управление необходимыми навыками для проектов
- Фильтрация проектов по навыкам
- Постраничная пагинация (12 элементов на страницу)
- Генерация аватара по умолчанию

## Стек технологий

- Python 3.9+
- Django 4.2
- PostgreSQL 15
- Docker / Docker Compose
- HTML, CSS, JavaScript

## Установка и запуск

```bash
git clone [https://github.com/sofitrutnewa/team-finder-ad.git](https://github.com/sofitrutnewa/team-finder-ad.git)
cd team-finder-ad
cp .env_example .env
docker-compose up -d
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## .env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5436
TASK_VERSION=3

## Был выполнен 3 вариант задания
