Данный playbook является копией https://github.com/vitabaks/postgresql_cluster с настроенными vars/main.yml и inventory 



# 1. Перед началом работы,
Устанавливаем ansible локально (на управляющий ПК). При старых версиях, будут ошибки! 
ansible==8.4.0
ansible-core==2.15.4
```
pip install -r requirements.txt
```

Необходимо создать 5 ВМ в облаке c ОS Ubuntu 20.04
![vm.png](..%2Fdocs%2Fvm.png)
принимая в расчет требования к железу:
    1. https://etcd.io/docs/v3.3/op-guide/hardware/ 
    2. https://www.haproxy.com/documentation/hapee/latest/getting-started/hardware/

В vars/main.yml изменено: 
```
with_haproxy_load_balancing: true
```

В inventory пример прописывания хостов: 
```
10.0.10.2 ansible_host=91.185.84.150
10.0.10.3 ansible_host=91.185.84.151
10.0.10.4 ansible_host=91.185.84.15
```
где 10.0.10.Х - private IP виртуальной машины, 91.185.84.Х - публичный IP виртуальной машины

# 2. Запуск 
```bash
ansible-playbook deploy_pgcluster.yml
```

# 3. Применяем миграцию
```bash
psql "host=91.185.85.228 port=5000 dbname=postgres user=postgres password=postgres-pass" -f init.sql
```

Проверка, что таблицы, были созданы
```bash
psql "host=91.185.85.228 port=5000 dbname=postgres user=postgres password=postgres-pass" -c "SELECT * FROM cities"
psql "host=91.185.85.228 port=5000 dbname=postgres user=postgres password=postgres-pass" -c "SELECT * FROM forecast"
```