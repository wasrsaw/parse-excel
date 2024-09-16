# Сервис парсинга расписания. 
_https://github.com/wasrsaw/parse-excel_

## Основные настройки сервиса
Все необходимые настройки сервиса производятся в файле .env.

## Запуск сервиса
Сервис поддерживает работу как с использованием контейнеризации (Docker) так и без. В случае запуска вне контейнера сервис будет работать ограниченном режиме, без базы данных и OpenAPI документации. 

### Первоначальная установка:
```
someuser@domain:~# git clone https://github.com/wasrsaw/parse-excel.git
```
### Запуск в контейнере
В случае запуска приложения через контейнер все зависисмые сервисы (база данных, документация OpenAPI) будут также работать. 
Перед запуском необходимо установить Docker Engine и Docker-Compose Plugin.

*Ubuntu:* https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
*Debian:* https://docs.docker.com/engine/install/debian/#install-using-the-repository

Далее собираем и запускаем контейнер всего-лишь одной командой:
```
someuser@domain:~# docker-compose up
```

Документация OpenAPI находится по адресу: http://0.0.0.0:8099

### Запуск вне контейнера:
В случае запуска вне контейнера необходмо запустить виртуальную среду и установить все пакеты, используемые сервисом.

Настраиваем виртуальную среду:
```
someuser@domain:~# python -m venv venv
someuser@domain:~# source venv/bin/activate
```

Скачиваем все необходимые пакеты:
```
someuser@domain:~# pip install -r app/requirements.txt
```

Запускаем приложение вне докера:
```
someuser@domain:~# python app/main.py
```

##Как пользоваться сервисом
> Самое главное, чтобы в файле info.json пристуствовали названия всех групп, иначе  сервис не будет работать корректно. Остальные данные можно не заполнять, но тогда в  БД могут быть дублирующие записи, если какая-то запись в расписании записана с ошибкой или в другом формате: например Иванов И.И. и ИвановИ.И. будут иметь отдельные > записи в БД!!!

1.	Проверяем как парсится расписание. 
  Путь *post*: http://0.0.0.0:port/view/schedule-excel
2.	Для того чтобы загрузить данные в БД необходимо в первую очередь вручную создать и загрузить файл info.json с данными по группам, преподавателям, предметам.
  Путь *post*: http://0.0.0.0:port/upload/info-json
4.	После этого необходимо загрузить расписание, чтобы программа распарсила его превратила в json. 
  Путь *post*: http://0.0.0.0:port/upload/schedule-excel
5.	Программа обновляет БД из json файлов. 
  Путь *post*: http://0.0.0.0:port/database/update-from-json

