## План работы
[X] 1. Разработать профиль нагрузки для системы

[X] 2. Реализовать профиль на любом инструменте НТ (разработать скрипт)

[X] 3. Задать нефункциональные требования по производительности к системе (SLO/SLA)

[X] 4. Найти максимальную производительность системы

[X] 5. Написать краткий вывод: где достигнута максимальная производительность, где узкое место в системе, для подтверждения привести графики.

## TODO: 
[ ] 1. Сделать запись в influxdb метрик рассчитываемых (сделал, но время записи большое, стоит разобраться с чем связано.) 

## Установка 
1. Установить Python 
2. Установить зависимости из src/requirements.txt 

## Примеры 
**Для запуска нужно находиться в корневой папке проекта -> mts-sre.** 

Пример запуска на 1 пк в 1 процесс
```bash
locust -f HT/locust/src/tests/forecast_max_perf.py,HT/locust/src/tests/weather_forecast_max_perf.py,HT/locust/src/tests/city_max_perf.py,HT/locust/src/tests/load_shape/increase_steps.py 
```
Пример запуска на 1 пк в несколько процессов
В первом терминале 
```bash
locust -f HT/locust/src/tests/forecast_max_perf.py,HT/locust/src/tests/city_max_perf.py,HT/locust/src/tests/load_shape/increase_steps_no_data_in_db.py --master
```
Во втором терминале 
```bash
locust -f HT/locust/src/tests/forecast_max_perf.py,HT/locust/src/tests/city_max_perf.py,HT/locust/src/tests/load_shape/increase_steps_no_data_in_db.py --worker --master-host=localhost
```



## Другие инструменты НТ 
Просто полезные команды, для быстрых тестов, используя [vegeta](https://github.com/tsenart/vegeta)
```bash
echo "GET http://weather-forecast.ddns.net/Cities" | vegeta attack -duration=10m -rate=10/s 
```
```bash
echo "GET https://weather-forecast.ddns.net/Cities/1" | vegeta attack -duration=10m -rate=2/s 
```
```bash
echo "GET https://weather-forecast.ddns.net/Cities/122" | vegeta attack -duration=10m -rate=2/s 
```

