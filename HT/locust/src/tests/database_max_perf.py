import time

import requests
from locust import HttpUser, constant_pacing, events, task

from HT.locust.src.core import config
from HT.locust.src.core.config_new import cfg
from HT.locust.src.models.models import City
from HT.locust.src.repository.influxdb import InfluxDbRepo
from HT.locust.src.repository.postgres import PostgresRepo
from HT.locust.src.service.influxdb import TSDBDService
from HT.locust.src.service.postgres import DatabaseService
from HT.locust.src.utils.checker import (CheckerPipline,
                                         CheckResponseElapsedTotalSeconds)

requests.packages.urllib3.disable_warnings()

influxdb = InfluxDbRepo()
tsdb_client = TSDBDService(influxdb)


def create_checker_database():
    checker_pipline = CheckerPipline()
    checker_pipline.add(CheckResponseElapsedTotalSeconds(0.5))
    return checker_pipline


class DataBaseUser(HttpUser):
    wait_time = constant_pacing(0.001)
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
    def add_test_data_database(self) -> None:
        city_data = [
            City(name='TestCity1'),
        ]
        request_start_time = time.time()
        self.database_service.write_test_data(city_data)
        processing_time = int((time.time() - request_start_time) * 1000)
        events.request.fire(
            request_type="postgresql",
            name='writing data into tables',
            response_time=processing_time,
            response_length=0,
            context=None,
            exception=None,
        )
