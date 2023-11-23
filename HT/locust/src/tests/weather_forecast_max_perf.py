import http

import requests
from locust import HttpUser, constant_pacing, task

from HT.locust.src.core import config
from HT.locust.src.core.config_new import cfg
from HT.locust.src.repository.influxdb import InfluxDbRepo
from HT.locust.src.repository.postgres import PostgresRepo
from HT.locust.src.service.influxdb import TSDBDService
from HT.locust.src.service.postgres import DatabaseService
from HT.locust.src.utils.checker import (CheckerPipline,
                                         CheckResponseElapsedTotalSeconds,
                                         CheckResponseStatus,
                                         )

requests.packages.urllib3.disable_warnings()

influxdb = InfluxDbRepo()
tsdb_client = TSDBDService(influxdb)


def create_checker():
    checker_pipline = CheckerPipline()
    checker_pipline.add(CheckResponseStatus(http.HTTPStatus.OK))
    # checker_pipline.add(CheckResponseValue('TestCity1'))
    checker_pipline.add(CheckResponseElapsedTotalSeconds(0.5))
    return checker_pipline


class WeatherForecastUser(HttpUser):

    weight = 1
    wait_time = constant_pacing(cfg.test_pacing_sec)
    host = cfg.test_api_host
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

    @task
    @tsdb_client.proceed_request
    def get_weather_forecast(self) -> None:
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        with self.client.get(
                "/WeatherForecast",
                headers=headers,
                catch_response=True,
                name=self.get_weather_forecast.__name__
        ) as request:
            checker_pipline = create_checker()
            checker_pipline.execute(request)
