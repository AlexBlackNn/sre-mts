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


def create_checker_cities():
    checker_pipline = CheckerPipline()
    checker_pipline.add(CheckResponseStatus(http.HTTPStatus.OK))
    checker_pipline.add(CheckResponseElapsedTotalSeconds(0.5))
    return checker_pipline


class CityUser(HttpUser):

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
    def add_city(self) -> None:
        headers = {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        faker = Faker()
        body = {
            "name": faker.city()
        }
        with self.client.post(
                "/Cities",
                headers=headers,
                json=body,
                catch_response=True,
                name=self.add_city.__name__
        ) as request:
            try:
                self.database_service.add_city_id(str(request.json()['id']))
            except:
                pass
            checker_pipline = create_checker_cities()
            checker_pipline.execute(request)

    @task(1)
    @tsdb_client.proceed_request
    def put_city(self) -> None:
        headers = {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        faker = Faker()
        body = {
            "name": "NewCityName"
        }

        _id = random.choice(self.database_service.city_ids)
        with self.client.put(
                f"/Cities/{_id}",
                headers=headers,
                json=body,
                catch_response=True,
                name=self.put_city.__name__
        ) as request:
            checker_pipline = create_checker_cities()
            checker_pipline.execute(request)

    @task(1)
    @tsdb_client.proceed_request
    def get_one_city(self) -> None:
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        _id = random.choice(self.database_service.city_ids)
        with self.client.get(
                f"/Cities/{_id}",
                headers=headers,
                catch_response=True,
                name=self.get_one_city.__name__
        ) as request:
            checker_pipline = create_checker_cities()
            checker_pipline.execute(request)

    @task(1)
    @tsdb_client.proceed_request
    def get_cities(self) -> None:
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        _id = random.choice(self.database_service.city_ids)
        with self.client.get(
                f"/Cities",
                headers=headers,
                catch_response=True,
                name=self.get_cities.__name__
        ) as request:
            checker_pipline = create_checker_cities()
            checker_pipline.execute(request)