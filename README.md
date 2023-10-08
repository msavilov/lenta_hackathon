# lenta_hackathon

## Описание

### Технологии
 - _[Python 3.11.5](https://docs.python.org/3/)_
 - _[Django 4.2.4](https://docs.djangoproject.com/en/4.1/releases/3.2.16/)_
 - _[Django REST framework 3.12.4](https://www.django-rest-framework.org/)_
 - _[Djoser 2.2.0](https://djoser.readthedocs.io/en/latest/)_
 - _[SQLite3](https://www3.sqlite.org/index.html)_


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
   и нажимаешь "ENTER", в терминал слева появится (venv) - значит ты в виртуально окружении)):

   ```python
   # для OS Lunix и MacOS
   source venv/bin/activate

   # для OS Windows
   source venv/Scripts/activate
   ```

5. Установить зависимости (так же в той же директории):

      ```python
   # для OS Lunix и MacOS
   python3 -m pip install --upgrade pip && pip install -r requirements.txt

   # для OS Windows
   python -m pip install --upgrade pip && pip install -r requirements.txt
   ```

6. Cоздайте файл `.env` в директории `/backend/` (вставить отправленный):


   ```python
   cd backend && nano .env

   В открывшийся редактор вставьте ключи ниже и после закройте командой "Ctrl + X"

   SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
   DEBUG=''
   ALLOWED_HOSTS='*' (или,ваши,хосты,через,запятые,без,пробелов)
   ```

7. Выполнить миграции на уровне проекта из директории `/backend/`
   (если не вы перешли на нее предыдущей комнадно cd backend,
   то выполните команду cd backend):

   ```python
   # для OS Lunix и MacOS
   python3 manage.py makemigrations && python3 manage.py migrate

   # для OS Windows
   python manage.py makemigrations && python manage.py migrate
   ```
8. Создание суперпользователя
    ввести команду 'python manage.py createsuperuser', там придумаешь почту и пароль

   ```python
   # для OS Lunix и MacOS
   python3 manage.py createsuperuser

   # для OS Windows
   python manage.py createsuperuser
   ```
9. Запускаешь проект локально:

   ```python
   # для OS Lunix и MacOS
   python3 manage.py runserver

   # для OS Windows
   python manage.py runserver
   ```

### Вход в админку
Заходишь по адресу http://127.0.0.1:8000/admin со своим почтой и паролем


### Работа с документацией и Postman после запуска проекта

1. Открываешь документацию по ссылке:

   - [Swagger](http://127.0.0.1:8000/swagger/)_