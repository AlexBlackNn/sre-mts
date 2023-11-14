import os

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions
import logging
from dotenv import load_dotenv


class Config:
    conf_name = 'Heisenbug'
    pacing_sec = 1
    api_host = 'https://weather-forecast.ddns.net'

    influx_bucket = 'demo_bucket'
    influx_org = 'demo_org'
    influx_client = InfluxDBClient(url="http://localhost:8086",
                                   token='demo_token',
                                   org=influx_org, )
    influxdb = influx_client.write_api(
        write_options=WriteOptions(
            batch_size=10,
            flush_interval=10_000,
            jitter_interval=2_000,
            retry_interval=5_000
        )
    )


class LogConfig():
    logger = logging.getLogger('demo_logger')
    logger.setLevel('DEBUG')
    file = logging.FileHandler(filename='test_logs.log')
    file.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(file)
    logger.propagate = False


load_dotenv()
DSN = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

logger = LogConfig().logger
cfg = Config()