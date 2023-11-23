import os

from pydantic import BaseSettings

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.abspath(__file__)
length_file_name = len(file_name.split('/')[-1])
directory = file_name[:-length_file_name]
path_env = os.path.join(directory, '.env')


class AppSettings(BaseSettings):
    influxdb_host: str = "http://localhost:8086"
    influxdb_token: str = 'demo_token'
    influxdb_org: str = 'demo_org'
    influxdb_bucket: str = 'demo_bucket'
    influxdb_conf_name: str = 'Heisenbug'
    influxdb_batch_size: int = 10
    influxdb_flush_interval: int = 10_000
    influxdb_jitter_interval: int = 2000
    influxdb_retry_interval: int = 5000
    db_name: str = 'postgres'
    db_user: str = 'postgres'
    db_password: str = 'postgres-pass'
    db_host: str = '77.105.185.143'
    port: int = 5000
    test_pacing_sec: float = 0.01
    test_api_host: str = 'https://weather-forecast.ddns.net'

    class Config:
        env_file = '.env'


cfg = AppSettings()
DSN = {
    'dbname': cfg.db_name,
    'user': cfg.db_user,
    'password': cfg.db_password,
    'host': cfg.db_host,
    'port': cfg.port
}
