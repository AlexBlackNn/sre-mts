import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, PostgresDsn

# from pydantic import BaseSettings, PostgresDsn

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = os.getenv('PROJECT_PORT', '8005')

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_name = os.path.abspath(__file__)
length_file_name = len(file_name.split('/')[-1])
directory = file_name[:-length_file_name]
path_env = os.path.join(directory, '.env')


class AppSettings(BaseSettings):
    app_title: str = 'Notifications'
    database_dsn: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    rabbit_mq: str = 'amqp://localhost?connection_attempts=10&retry_delay=10'
    class Config:
        # почему - то работает только с полным путем
        env_file = path_env


app_settings = AppSettings()
