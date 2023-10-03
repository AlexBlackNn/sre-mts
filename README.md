# Сервис прогноза погоды 

https://weather-forecast.ddns.net/swagger/index.html


![img.png](docs/img.png)

Задачи

- [X] Написать ansible playbook для развертывания postgresql в patroni сетапе.
    Разворачиваем etcd, patroni, postgres и Haproxy.
- [X] Написать helm chart для разворачивания api в выделенном неймспейсе. Docker image лежит в публичном registry, разворачивать стоит актуальную версию ghcr.io/ldest/sre-course/api

- [X] Из образа вытащить скрипт миграции для создания БД, настроить на работу с кластером api, проверить работоспособность



# Порядок развертывания. 
1. FAQ лежит в папке docs
2. Настраиваем Postgres кластер. Переходим в my_postgresql_cluster. Читаем README.md
3. Запускам приложение в k8s. Переходим в k8s. Читаем README.md

В postgresql_cluster.txt полезные команды для работы с postgresql в patroni сетапе