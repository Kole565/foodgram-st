[![Main Foodgram Workflow](https://github.com/Kole565/foodgram-st/actions/workflows/main.yml/badge.svg?branch=main&event=push)](https://github.com/Kole565/foodgram-st/actions/workflows/main.yml)
# Продуктовый помощник Foodgram 

## Описание проекта Foodgram

Из задания: Вам предстоит поработать с проектом «Фудграм» — сайтом, на котором
пользователи будут публиковать свои рецепты, добавлять чужие рецепты в избранное
и подписываться на публикации других авторов. Зарегистрированным пользователям
также будет доступен сервис «Список покупок». Он позволит создавать список
продуктов, которые нужно купить для приготовления выбранных блюд.

## Запуск проекта в dev-режиме (только backend)

- Клонируйте репозиторий с проектом на свой компьютер. В терминале из рабочей директории выполните команду:

```bash
git clone https://github.com/Kole565/foodgram-st.git
cd foodgram-st/backend
```

- Установить и активировать виртуальное окружение (для linux, для windows используйте ```./env/Scripts/activate```)

```bash
python -m venv env
source ./env/bin/activate
```

- Установить зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Выполните миграции:

```bash
# foodgram-st/backend
python manage.py migrate
```

- Создание нового суперпользователя 

```bash
python manage.py createsuperuser
```

### Загрузите статику:

```bash
python manage.py collectstatic --no-input
```
### Заполните базу тестовыми данными: 

```bash
python manage.py loaddata initial_data.json
```

- Запуск сервера (если хотите оставить терминал можете добавить ```&``` в конец для фонового процесса):

```bash
python manage.py runserver
```

Таким образом вы можете активировать backend часть foodgram. Этого достаточно для запуска тестов postman api. Используется конфигурация по умолчанию - debug: True, db: sqlite3.

## Полный запуск проекта

Для полноценного рабочего сайта необходимы еще прокси, фронтенд и база данных.

Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

Клонируйте репозиторий с проектом на свой компьютер (если вы этого не сделали в прошлом разделе).
В терминале из рабочей директории выполните команду:

```bash
git clone https://github.com/Kole565/foodgram-st.git
```

- Создайте файл .env в папке проекта (или ```mv example.env .env```):
```.env
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
DEBUG=0
```

Выполните команду сборки контейнеров:
```bash
# foodgram-st
docker compose up -d --build # d - отсоединить от консоли, оставив её доступной, build - пересобирать контейнер при каждом запуске
```
При последующий обновлениях обновите образ перед сборкой, иначе изменения в конфигурации django не сохранятся:
```bash
# foodgram-st
docker image pull kole565/foodgram_backend
```

- В результате должны быть собрано четыре контейнера и три останется активными (контейнер frontend является статическим - служит хранилищем, поэтому не отображается как активный, используйте ```docker container ls -a``` для просмотра всех), при введении следующей команды получаем список запущенных контейнеров:  
```bash
docker container ls
```
Назначение контейнеров:

|    NAMES            |        DESCRIPTIONS                      |
|:--------------------|:----------------------------------------:|
| infra-nginx-1       | обратный прокси                          |
| infra-db-1          | база данных                              |
| infra-backend-1     | приложение Django (то, над чем работаем) |
| infra-frontend-1    | приложение React (не активен)            |

### Выполните миграции:
```bash
docker compose exec backend python manage.py migrate
```
### Создайте суперпользователя:
```bash
docker compose exec backend python manage.py createsuperuser
```
### Заполните базу тестовыми данными:
```bash
docker compose exec backend python manage.py loaddata initial_data.json
```
### Загрузите статику:
```bash
docker compose exec backend python manage.py collectstatic --no-input
```
Если какой то пункт не работает (требует winpty), попробуйте сначала зайти в контейнер (на примере загрузки данных):
```bash
docker compose exec backend /bin/bash
python manage.py loaddata initial_data.json
exit
```

### Основные адреса: 

| Адрес                 | Описание |
|:----------------------|:---------|
| 127.0.0.1            | Главная страница |
| 127.0.0.1/admin/     | Панель администратора |
| 127.0.0.1/api/docs/  | Описание требований к API |

## Пользовательские роли
| Функционал                                                                                                                | Неавторизованные пользователи |  Авторизованные пользователи | Администратор  |
|:--------------------------------------------------------------------------------------------------------------------------|:---------:|:---------:|:---------:|
| Доступна главная страница.                                                                                                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма авторизации                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница отдельного рецепта.                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма регистрации.                                                                                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Мои подписки»                                                                                          | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице рецепта                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице автора                                                                         | :x: | :heavy_check_mark: | :heavy_check_mark: |
| При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Избранное»                                                                                             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда                             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда           | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Список покупок»                                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда                                | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда              | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок» | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Создать рецепт»                                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность опубликовать свой рецепт                                                                                 | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность отредактировать и сохранить изменения в своём рецепте                                                    | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность удалить свой рецепт                                                                                      | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма изменения пароля                                                                                | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна возможность выйти из системы (разлогиниться)                                                                     | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает система восстановления пароля.                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Изменять пароль любого пользователя.                                                                                      | :x: | :x: | :heavy_check_mark: |
| Создавать/блокировать/удалять аккаунты пользователей.                                                                     | :x: | :x: | :heavy_check_mark: |
| Редактировать/удалять любые рецепты.                                                                                      | :x: | :x: | :heavy_check_mark: |
| Добавлять/удалять/редактировать ингредиенты.                                                                              | :x: | :x: | :heavy_check_mark: |
| Добавлять/удалять/редактировать теги.                                                                                     | :x: | :x: | :heavy_check_mark: |


### Автор оригинального README и проекта для вдохновения:
Не защищен лицензией и использован в качестве основы.<br>
_Кузьмич Александр_<br>
**email**: _sashakuzmich69@yandex.ru_<br>
**telegram** _@xofmdo_<br>
**Ссылка на репозиторий**: https://github.com/xofmdo/foodgram-project/tree/master

### Автор проекта
Проект выполнен в рамках курса "Ассоциированные программы: бэкенд-разработчик".<br>
Статус проекта: на доработке.
_Степанов Николай Викторович_<br>
**VK**: @kole565<br>
**Telegram**: @Kole565<br>
**Email (основной)**: rjkz565rjkz565@gmail.com<br>
**Email (учебный)**: stepanov.n.v@edu.narfu.ru
