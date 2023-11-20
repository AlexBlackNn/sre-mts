import http
import random

import requests
from faker import Faker

from HT.locust.src.core import config
from HT.locust.src.core.config_new import cfg
from HT.locust.src.repository.influxdb import InfluxDbRepo
from HT.locust.src.repository.postgres import PostgresRepo
from HT.locust.src.service.influxdb import TSDBDService
from HT.locust.src.service.postgres import DatabaseService
from locust import HttpUser, constant_pacing, task

from HT.locust.src.utils.checker import (
    CheckerPipline,
    CheckResponseStatus,
    CheckResponseValue,
    CheckResponseElapsedTotalSeconds
)

requests.packages.urllib3.disable_warnings()

influxdb = InfluxDbRepo()
tsdb_client = TSDBDService(influxdb)


def create_checker_forecast():
    checker_pipline = CheckerPipline()
    checker_pipline.add(CheckResponseStatus(http.HTTPStatus.OK))
    checker_pipline.add(CheckResponseElapsedTotalSeconds(0.5))
    return checker_pipline


class ForecastUser(HttpUser):

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


    @task(1)
    @tsdb_client.proceed_request
    def add_forecast(self) -> None:
        headers = {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        city_id = random.choice(self.database_service.city_ids)
        body = {
            "cityId": city_id,
            "dateTime": 0,
            "temperature": 0,
            "summary": "string"
        }

        with self.client.post(
                "/Forecast/" + city_id,
                headers=headers,
                json=body,
                catch_response=True,
                name=self.add_forecast.__name__
        ) as request:

            self.database_service.add_forecast_id(request.json()['id'])
            checker_pipline = create_checker_forecast()
            checker_pipline.execute(request)

    @task(1)
    @tsdb_client.proceed_request
    def put_forecast(self) -> None:
        headers = {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        forecast_id = random.choice(self.database_service.forecast_ids)
        city_id = random.choice(self.database_service.city_ids)
        body = {
          "id": forecast_id,
          "cityId": city_id,
          "dateTime": 0,
          "temperature": 0,
          "summary": "NewSummaryString"
        }


        with self.client.put(
                f"/Forecast/{forecast_id}",
                headers=headers,
                json=body,
                catch_response=True,
                name=self.put_forecast.__name__
        ) as request:
            checker_pipline = create_checker_forecast()
            checker_pipline.execute(request)

    @task(1)
    @tsdb_client.proceed_request
    def get_one_forecast(self) -> None:
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        _id = random.choice(self.database_service.forecast_ids)
        with self.client.get(
                f"/Forecast/{_id}",
                headers=headers,
                catch_response=True,
                name=self.get_one_forecast.__name__
        ) as request:
            checker_pipline = create_checker_forecast()
            checker_pipline.execute(request)

    @task(1)
    @tsdb_client.proceed_request
    def get_forecast(self) -> None:
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        _id = random.choice(self.database_service.city_ids)
        with self.client.get(
                f"/Forecast",
                headers=headers,
                catch_response=True,
                name=self.get_forecast.__name__
        ) as request:
            checker_pipline = create_checker_forecast()
            checker_pipline.execute(request)