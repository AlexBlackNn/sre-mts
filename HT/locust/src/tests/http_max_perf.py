from locust import task, constant_pacing, HttpUser, LoadTestShape
import random


from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions
import logging


class Config:
    conf_name = 'Heisenbug'
    pacing_sec = 0.1
    api_host = 'http://localhost:9090'
    kafka_hosts = ['localhost:29092']
    influx_bucket = 'demo_bucket'
    influx_org = 'demo_org'
    influx_client = InfluxDBClient(url="http://localhost:8086",
                                   token='demo_token',
                                   org=influx_org, )
    influxdb = influx_client.write_api(write_options=WriteOptions(batch_size=10,
                                                                  flush_interval=10_000,
                                                                  jitter_interval=2_000,
                                                                  retry_interval=5_000, ))
    products = [
        {"Code": 111, "Name": "Молоко 1 л.", "Price": 150},
        {"Code": 123, "Name": "Кефир 1 л.", "Price": 100},
        {"Code": 124, "Name": "Сметана 100 г.", "Price": 80},
        {"Code": 125, "Name": "Творог 100 г.", "Price": 120},
        {"Code": 126, "Name": "Сгущёнка", "Price": 170},
    ]


class LogConfig():
    logger = logging.getLogger('demo_logger')
    logger.setLevel('DEBUG')
    file = logging.FileHandler(filename='test_logs.log')
    file.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(file)
    logger.propagate = False


logger = LogConfig().logger
cfg = Config()


class CartUser(HttpUser):
    wait_time = constant_pacing(0.1)
    host = 'http://localhost:9090'
    token_id = ''

    @task
    def add_to_cart(self) -> None:
        transaction = self.add_to_cart.__name__
        headers = {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "token": self.token_id,
        }
        product = random.choice(cfg.products)
        body = {
            "Product": product["Name"],
            "Prod_code": product["Code"],
        }
        with self.client.post("/cart/add", headers=headers, json=body, catch_response=True, name=transaction) as request:
            pass

    def login(self) -> None:
        with self.client.get(f"/login/demo-user", catch_response=True, name='login') as request:
            pass
        self.token_id = request.text

    def on_stop(self):
        logger.debug(f"user stopped")


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 20, "users": 1, "spawn_rate": 1},
        {"duration": 40, "users": 2, "spawn_rate": 1},
        {"duration": 60, "users": 4, "spawn_rate": 1},
        {"duration": 80, "users": 8, "spawn_rate": 1},
        {"duration": 100, "users": 10, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None