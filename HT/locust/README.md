1. Установить Docker
2. Установить Python 
3. Через командную строку открыть папку "./docker" из данного репозитория и выполнить команды:

     - docker-compose up -d

Запуск
 locust -f HT/locust/src/tests/weather_forecast_max_perf.py,HT/locust/src/tests/city_max_perf.py,HT/locust/src/tests/load_shape/increase_steps.py 

