# 'Хакатон Лента х Практикум сентябрь’23. Команда 20'

## Описание

### Технологии
 - ![](https://img.shields.io/badge/Python-3.11-blue)
 - ![](https://img.shields.io/badge/Django-3.2-blue)
 - ![](https://img.shields.io/badge/Django_REST_Framework-3.14-blue)
 - ![](https://img.shields.io/badge/Djoser-blue)
 - ![](https://img.shields.io/badge/Postgresql-blue)
 - ![](https://img.shields.io/badge/Docker-blue)
 - ![](https://img.shields.io/badge/Docker-compose-blue)


### Установка

1. Клонировать репозиторий (открыть терминал в нужной папке, вставить эту строчку,
   и нажать "ENTER", в директории появится папка с названием проекта):

   ```python
   git clone https://github.com/msavilov/lenta_hackathon.git
   ```
2. Перейти в ветку develop:

   ```python
   cd lenta_hackathon && git checkout develop
   ```

3. Установить виртуальное окружение для проекта (там же набираешь одну из этих команд
   и нажимаешь "ENTER", в директории появится папка env):

   ```python
   # для OS Lunix и MacOS
   python3 -m venv venv

   # для OS Windows и MacOS
   python -m venv venv
   ```

4. Активировать виртуальное окружение для проекта (там же набираешь одну из этих команд
   и нажимаешь "ENTER", в терминал слева появится (venv)):

   ```python
   # для OS Lunix и MacOS
   source venv/bin/activate

   # для OS Windows
   source venv/Scripts/activate
   ```

5. Установить зависимости:

      ```python
   # для OS Lunix и MacOS
   python3 -m pip install --upgrade pip && pip install -r requirements.txt

   # для OS Windows
   python -m pip install --upgrade pip && pip install -r requirements.txt
   ```

6. Cоздайте файл `.env` в директории `/backend/`:

   ```python
   cd backend && nano .env

   В открывшийся редактор вставьте ключи ниже и после закройте командой "Ctrl + X"

   SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
   DEBUG=''
   ALLOWED_HOSTS='*' (или,ваши,хосты,через,запятые,без,пробелов)
   ```

7. Выполнить миграции на уровне проекта из директории `/backend/`
   (если не вы перешли на нее предыдущей комнаде cd backend,
   то выполните команду cd backend):

   ```python
   # для OS Lunix и MacOS
   python3 manage.py makemigrations users
   python3 manage.py makemigrations sales
   python3 manage.py migrate

   # для OS Windows
   python manage.py makemigrations users
   python manage.py makemigrations sales
   python manage.py migrate
   ```
8. Создание суперпользователя: ввести команду 'python manage.py createsuperuser'

   ```python
   # для OS Lunix и MacOS
   python3 manage.py createsuperuser

   # для OS Windows
   python manage.py createsuperuser
   ```
9. Запустить проект локально:

   ```python
   # для OS Lunix и MacOS
   python3 manage.py runserver

   # для OS Windows
   python manage.py runserver
   ```

### Вход в админку
- [Admin](http://127.0.0.1:8000/admin) со своим почтой и паролем

### Работа с документацией и Postman после запуска проекта
- [Swagger](http://127.0.0.1:8000/swagger/)
