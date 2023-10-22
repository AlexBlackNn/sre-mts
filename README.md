# Сервис прогноза погоды 

![img.png](docs/img.png)

**Задачи**

**Инфраструктура** 
- [X] Написать ansible playbook для развертывания postgresql в patroni сетапе.
    Разворачиваем etcd, patroni, postgres и Haproxy.
- [X] Написать helm chart для разворачивания api в выделенном неймспейсе. Docker image лежит в публичном registry, разворачивать стоит актуальную версию ghcr.io/ldest/sre-course/api

- [X] Из образа вытащить скрипт миграции для создания БД, настроить на работу с кластером api, проверить работоспособность

**Мониторинг** 
- [X] Развернуть Prometheus на виртуальной машине
- [X] Установить Docker-compose для запуска экспортеров PostgreSQL и Patroni
- [X] Настроить сбор метрик с PostgreSQL
- [X] Настроить сбор метрик с Patroni
- [X] Настроить сбор метрик с etcd
- [X] Настроить сбор black box мониторинг API демоприложения
- [X] Настроить сбор метрик ОС с виртуальных машин
- [X] Создать в Grafana в организации Main Org:
- [X] Каталог для дашбордов со своим ФИ латиницей
- [X] Источник данных для своего Prometheus(в названии ФИ латиницей)
- [Х] Создать в своем каталоге типовой дашборд для PostgreSQL (Требует дороботки!!!!!!!!!!!!!!!!!!!)
- [X] Создать в своем каталоге типовой дашборд для Patroni
- [X] Создать в своем каталоге типовой дашборд для etcd
- [X] Создать в своем каталоге типовой дашборд для blackbox 
- [X] Создать в своем каталоге типовой дашборд для node exporter (Требует дороботки!!!!!!!!!!!!!!!!!!!!!)
- [X] Создать в своем каталоге дашборд с 4 золотыми сигналами для API демоприложения по данным метрик ingressk8s
- [Х] Настроить алерты на несколько метрик каждого компонента системы (Node exporter, Patroni, etcd, Postgres)
- [ ] Рефакторинг
- [ ] Документация
- [ ] Сбор логов (??? Postgresql log CSV -> Python Beaver -> Logstash -> Elastic -> Kibana ???)

- **Бэкапы** 
- [ ] ??? BarMan ???
 

# Порядок развертывания. 
1. FAQ лежит в папке docs
2. Настраиваем Postgres кластер. Переходим в my_postgresql_cluster. Читаем README.md
3. Запускам приложение в k8s. Переходим в k8s. Читаем README.md

В postgresql_cluster.txt полезные команды для работы с postgresql в patroni сетапе


# Полезные ссылки
[Готовим PostgreSQL в эпоху DevOps. Опыт 2ГИС. Павел Молявин](https://habr.com/ru/articles/509926/) 

https://lindevs.com/install-vegeta-on-ubuntu for load tesing 


echo "GET http://weather-forecast.ddns.net/Cities" | vegeta attack -duration=10m -rate=10/s 
echo "GET https://weather-forecast.ddns.net/Cities/1" | vegeta attack -duration=10m -rate=2/s 
echo "GET https://weather-forecast.ddns.net/Cities/122" | vegeta attack -duration=10m -rate=2/s 


Checking Kubernetes pod CPU and memory utilization
https://stackoverflow.com/a/71874558/22644912


https://samber.github.io/awesome-prometheus-alerts/
https://gist.github.com/krisek/62a98e2645af5dce169a7b506e999cd8