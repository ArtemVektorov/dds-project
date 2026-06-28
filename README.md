# 💰 Веб-сервис ДДС (Движение Денежных Средств)

Приложение для учёта доходов и расходов с удобным интерфейсом.

## Возможности

- Создание, редактирование и удаление записей ДДС
- Фильтры по дате, статусу, типу, категории и подкатегории
- Динамические выпадающие списки (Тип → Категория → Подкатегория)
- Полное управление справочниками (Типы, Статусы, Категории, Подкатегории)
- Красивый и удобный интерфейс

## Технологии

- Backend: Python + Django
- Frontend: Bootstrap 5 + JavaScript
- База данных: SQLite

## Как запустить
1. Создайте виртуальное окружение

   python -m venv venv # Windows/Linux/Mac

   venv\Scripts\activate    # Windows

   source venv/bin/activate  # Linux/Mac

1. Клонируйте репозиторий
   
   git clone https://github.com/ArtemVektorov/dds-project.git

2. Установите зависимости
   
   pip install -r requirements.txt

3. Примените миграции

   python manage.py migrate

4. Запустите сервер

   python manage.py runserver


Откройте в браузере: http://127.0.0.1:8000/core

