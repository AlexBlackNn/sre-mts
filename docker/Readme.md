# Сервис прогноза погоды 

Только для тестового запуска. Внимание: порт в БД открыт.

Переменная DOTNET_ENVIRONMENT = Development - режим разрботки. Swagger в таком
режиме будет доступен по

http://127.0.0.1:8001/swagger/index.html


## telegram:
https://t.me/Alexblacknn

## Локальный запуск приложения (для тестового запуска)
```bash
mv .env.example .env
docker-compose up
```

# Инициализация БД 
в init.sql лежит файл начальной миграции
```bash
psql "host=localhost port=5432 dbname=postgres user=postgres password=postgres" -f init.sql
```
