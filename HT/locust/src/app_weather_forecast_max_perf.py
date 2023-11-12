import http

from locust import events, HttpUser, constant_pacing, task, LoadTestShape
import time
from config import cfg, logger
from functools import wraps
import assertion
import os
import requests
requests.packages.urllib3.disable_warnings()

def proceed_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_start_time = time.time()
        transaction = func(*args, **kwargs)
        processing_time = int((time.time() - request_start_time) * 1000)

        cfg.influxdb.write(
            cfg.influx_bucket,
            cfg.influx_org,
            [{
                "measurement": f"{cfg.conf_name}_db",
                "tags": {"transaction_name": func.__name__},
                "time": time.time_ns(),
                "fields": {"response_time": processing_time},
            }],
        )

        logger.debug(
            f"""{func.__name__} status: {transaction.status_code 
            if func.__name__ != 'send_payment'
            else 'message delivered'}"""
        )

    return wrapper


class GlobalUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    def on_start(self):
        # disable ssl check
        self.client.verify = False

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        os.remove("test_logs.log")
        logger.info("TEST STARTED")

    @task
    @proceed_request
    def get_weather_forecast(self) -> None:
        transaction = self.get_weather_forecast.__name__
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        with self.client.get(
                "/WeatherForecast",
                headers=headers,
                catch_response=True,
                name=transaction
        ) as request:
            assertion.check_http_response(transaction, request)
        return request


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 20, "users": 1, "spawn_rate": 1},
        {"duration": 40, "users": 2, "spawn_rate": 1},
        {"duration": 60, "users": 3, "spawn_rate": 1},
        {"duration": 80, "users": 4, "spawn_rate": 1},
        {"duration": 100, "users": 5, "spawn_rate": 1},
        {"duration": 120, "users": 6, "spawn_rate": 1},
        {"duration": 140, "users": 7, "spawn_rate": 1},
        {"duration": 160, "users": 8, "spawn_rate": 1},
        {"duration": 180, "users": 9, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None
