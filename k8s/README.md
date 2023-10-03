# Сервис прогноза погоды 

## Важно! Кластер Postgres должен быть запущен в облаке. Для его запуска смотри Readme в my_postgres_cluster.

Переменная DOTNET_ENVIRONMENT = Development - режим разрботки. Swagger в таком
режиме будет доступен по
https://weather-forecast.ddns.net/swagger/index.html


## telegram:
https://t.me/Alexblacknn

## Структура 
```
k8s
├── ingress
│   ├── Chart.yaml
│   ├── templates
│   │   └── ingress.yaml
│   └── values.yaml
├── local_run.sh
├── mts-ingress
│   ├── Chart.yaml
│   ├── templates
│   │   └── ingress.yaml
│   └── values.yaml
├── mts_run.sh
├── README.md
└── weather
    ├── Chart.yaml
    ├── templates
    │   ├── deployment.yaml
    │   ├── hpa.yaml
    │   ├── secrets.yaml
    │   └── service.yaml
    └── values.yaml
```
## Локальный запуск приложения в minikube (для тестового запуска)
1. Убеждаемся, что контекст - minikube
```bash
kubectl config current-context
```
Вывод в терминал: minikube

2. В /etc/hosts прописать
```
192.168.49.2 weather.local
```
где 192.168.49.2 - IP minikube, который можно получить, командой 
```bash
 minikube ip
```

3. Запускаем приложение
```bash
./local_run.sh
```

# Инициализация БД 
в init.sql лежит файл начальной миграции
```bash
psql "host=localhost port=5432 dbname=postgres user=postgres password=postgres" -f init.sql
```
