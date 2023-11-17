import os
from pydantic import BaseSettings, PostgresDsn

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.abspath(__file__)
length_file_name = len(file_name.split('/')[-1])
directory = file_name[:-length_file_name]
path_env = os.path.join(directory, '.env')


class AppSettings(BaseSettings):
    influxdb_host: str = "http://localhost:8086",
    influxdb_token: str = 'demo_token',
    influxdb_org: str = 'demo_org',
    influxdb_batch_size: int = 10
    influxdb_flush_interval: int = 10_000
    influxdb_jitter_interval: int = 2000
    influxdb_retry_interval: int = 5000

    class Config:
        env_file = '.env'


cfg = AppSettings()
