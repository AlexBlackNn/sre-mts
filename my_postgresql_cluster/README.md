
CREATE TABLES
psql "host=91.185.84.153 port=5000 dbname=postgres user=postgres password=postgres-pass" -f init.sql

CHECK TABLES
psql "host=91.185.84.153 port=5000 dbname=postgres user=postgres password=postgres-pass" -c "SELECT * FROM cities"
psql "host=91.185.84.153 port=5000 dbname=postgres user=postgres password=postgres-pass" -c "SELECT * FROM forecast"
