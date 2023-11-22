[ ] 1. Разработать профиль нагрузки для системы
[ ] 2. Реализовать профиль на любом инструменте НТ (разработать скрипт)
[X] 3. Задать нефункциональные требования по производительности к системе (SLO/SLA)
[ ] 4. Найти максимальную производительность системы
[ ] 5. Написать краткий вывод: где достигнута максимальная производительность, где узкое место в системе, для подтверждения привести графики.

1.Установить Docker
2. Установить Python 
3. Через командную строку открыть папку "./docker" из данного репозитория и выполнить команды:

     - docker-compose up -d

Запуск
 locust -f HT/locust/src/tests/forecast_max_perf.py,HT/locust/src/tests/weather_forecast_max_perf.py,HT/locust/src/tests/city_max_perf.py,HT/locust/src/tests/load_shape/increase_steps.py 

locust -f HT/locust/src/tests/forecast_max_perf.py,HT/locust/src/tests/weather_forecast_max_perf.py,HT/locust/src/tests/city_max_perf.py,HT/locust/src/tests/load_shape/stape_load_shape.py 

 locust -f HT/locust/src/tests/database_max_perf.py,HT/locust/src/tests/load_shape/increase_steps.py 
