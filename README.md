# Проект "Simple votings"

### Цель
Предоставить пользователю сервис с простым и понятным оформлением, предназначенный для создания опросов пользователей, касательного некоторого вопроса.

### Технологический стек:
- Python 3.9
- Django 
- SQLite 

### Инструкция по настройке проекта:
1. Установить в виртуальное окружение необходимые пакеты: 
   ```bash
   pip install -r requirements.txt
   ```

2. Создать уникальный ключ приложения.  
   Генерация делается в консоли Python при помощи команд:
   ```bash
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; get_random_secret_key()"
   ```
   Далее полученное значение подставляется в соответствующую переменную.
   Внимание! Без выполнения этого пункта никакие команды далее не запустятся.

3. Синхронизировать структуру базы данных с моделями: 
   ```bash
   python manage.py migrate
   ```

4. Создать суперпользователя
   ```bash
   python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
   ```
