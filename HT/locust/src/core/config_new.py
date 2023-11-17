import os
from pydantic import BaseSettings, PostgresDsn

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.abspath(__file__)
length_file_name = len(file_name.split('/')[-1])
directory = file_name[:-length_file_name]
path_env = os.path.join(directory, '.env')


class AppSettings(BaseSettings):
    influxdb_host = "http://localhost:8086",
    influxdb_token = 'demo_token',
    influxdb_org = 'demo_org',

    class Config:
        env_file = '.env'


app_settings = AppSettings()
