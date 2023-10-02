kubectl get all
helm install weather weather
helm delete weather 
helm install ingress mts-ingress
kubectl get ing

CREATE TABLES
psql "host=91.185.84.153 port=5000 dbname=postgres user=postgres password=postgres-pass" -f init.sql

CHECK TABLES
psql "host=91.185.84.153 port=5000 dbname=postgres user=postgres password=postgres-pass" -c "SELECT * FROM cities"
psql "host=91.185.84.153 port=5000 dbname=postgres user=postgres password=postgres-pass" -c "SELECT * FROM forecast"

echo 'Server=91.185.84.153;Port=5000;Database=postgres;User Id=postgres;Password=postgres-pass;' | base64
U2VydmVyPTkxLjE4NS44NC4xNTM7UG9ydD01MDAwO0RhdGFiYXNlPXBvc3RncmVzO1VzZXIgSWQ9

