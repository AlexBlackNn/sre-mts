import os

import requests
from faker import Faker

from HT.locust.src.core import config
from HT.locust.src.core.config import cfg, logger
from HT.locust.src.repository.postgres import PostgresRepo
from HT.locust.src.service.postgres import DatabaseService
from HT.locust.src.utils import assertion
from HT.locust.src.utils.proceed_request import proceed_request
from locust import HttpUser, constant_pacing, events, task

requests.packages.urllib3.disable_warnings()


class GlobalUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host
    postgres_repo = PostgresRepo(config.DSN)
    database_service = DatabaseService(postgres_repo)

    def on_start(self):
        # create fake data in database
        self.database_service.init_from_file()
        # disable ssl check
        self.client.verify = False

    def on_stop(self):
        # delete fake data in database
        self.database_service.delete_test_data()

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        os.remove("test_logs.log")
        logger.info("TEST STARTED")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
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

    # @task(1)
    # def add_city(self) -> None:
    #     transaction = self.add_city.__name__
    #     headers = {
    #         "accept": "text/html",
    #         "accept-encoding": "gzip, deflate, br",
    #         "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    #     }
    #     faker = Faker()
    #     body = {
    #         "name": faker.city()
    #     }
    #     with self.client.post(
    #             "/Cities",
    #             headers=headers,
    #             json=body,
    #             catch_response=True,
    #             name=transaction
    #     ) as request:
    #         assertion.check_http_response_post(transaction, request)

