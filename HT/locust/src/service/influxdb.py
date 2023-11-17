import time
from functools import wraps

from HT.locust.src.core.config_new import cfg


class TSDBDService:
    def __init__(self, tsdb_client):
        self.tsdb_client = tsdb_client

    def proceed_request(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_start_time = time.time()
            func(*args, **kwargs)
            processing_time = int((time.time() - request_start_time) * 1000)
            self.tsdb_client.write(
                [{
                    "measurement": f"{cfg.influxdb_conf_name}_db",
                    "tags": {"transaction_name": func.__name__},
                    "time": time.time_ns(),
                    "fields": {"response_time": processing_time},
                }],
            )
        return wrapper
