# Проект FOODGRAM - продуктовый помощник

![Alt](https://github.com/Aleksandr-Fedotov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg 'Actions Status')

Учебный проект доступен по адресу: 
* http://158.160.3.124/signup - страница аутентификации
* http://158.160.3.124/admin - админка

Админ:
* логин: super
* пароль: F20zd921

Пользователь 1:
* почта: qwfwr2@yandex.ru
* пароль: Parol123

Пользователь 2:
* почта: qwfwr3@yandex.ru
* пароль: Parol123

Пользователь 3:
* почта: qwfwr4@yandex.ru
* пароль: Parol123

## Tехнологии:
- Python
- Django REST Framework
- PostgreSQL
- Nginx
- Docker
- GitHub Actions

Для проекта настроено `Continuous Integration и Continuous Deployment`  
При пуше в ветку `master` отрабатывают сценарии:
1. Проверка кода на соответствие стандарту PEP8
2. Сборка и доставка докер-образа для контейнеров `foodgram_backend` и `foodgram_frontend` на Docker Hub
3. Автоматический деплой на боевой сервер
4. Отправка сообщения в телеграмм-бот в случае успеха.

## Начало работы

1. Клонируйте репозиторий на локальную машину.
```
git clone <адрес репозитория>
```
2. Для работы с проектом локально - установите вирутальное окружение и установите зависимости.
```
python -m venv venv
pip install -r requirements.txt
```

### Подготовка удаленного сервера для развертывания приложения

Для работы с проектом на удаленном сервере должен быть установлен Docker и docker-compose.
Установить Docker:
```
sudo apt install docker.io
```
Установить docker-compose:
```
sudo apt install docker-compose
```
Скопируйте файлы `docker-compose.yaml` и `nginx.conf` из локального проекта из директории `infra`  
на сервер в `/home/<ваш_username>/docker-compose.yaml` и `/home/<ваш_username>/nginx.conf` соответственно
```
scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/
```


### Подготовка репозитория на GitHub

Для использования `Continuous Integration` и `Continuous Deployment` необходимо в репозитории на GitHub во вкладке `Settings` прописать `Secrets` - переменные доступа к вашим сервисам.
Переменые используются в `/workflows/foodgram_workflow.yaml`

* `DOCKER_PASSWORD, DOCKER_USERNAME` - для загрузки и скачивания образа с DockerHub 
* `USER, HOST, PASSPHRASE, SSH_KEY` - для подключения к удаленному серверу 
* `DB_ENGINE, DB_NAME, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT` - для выполнения на удалённом сервере ssh-команд для деплоя
* `TELEGRAM_TO, TELEGRAM_TOKEN` - для отправки сообщений в Telegram
* `SECRET_KEY` - серкретный ключ проекта Django

### Развертывание приложения

При пуше в ветку `master` приложение пройдет тесты, обновит образ на DockerHub и сделает деплой на сервер. Дальше необходимо подключиться к серверу.
```
ssh <USER>@<HOST>
```
* После успешной сборки на сервере выполните команды (только после первого деплоя):
    - Соберите статические файлы:
    ```
    sudo docker exec <container_ID> python manage.py collectstatic --no-input
    ```
    - Примените миграции:
    ```
    sudo docker exec <container_ID> python manage.py makemigrations  
    sudo docker exec <container_ID> python manage.py migrate
    ```
    - Создайте суперпользователя Django:
    ```
    sudo docker container exec -it <container_ID> bash
    python manage.py createsuperuser
    ```
    - Загрузите предустановленные ингредиенты и теги в базу данных:
    ```
    sudo docker exec <container_ID> python manage.py loaddata fixtures/tags.json
    sudo docker exec <container_ID> python manage.py loaddata fixtures/ingredients.json
    ```

## Работу выполнил:
- Федотов Александр
