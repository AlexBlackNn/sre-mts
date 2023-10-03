#!/bin/bash

#Важно! Кластер Postgres должен быть запущен в облаке. Для его запуска смотри Readme в my_postgres_cluster.
helm install weather weather
helm install ingress mts-ingress