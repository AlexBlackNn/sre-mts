import time
from functools import wraps
from multiprocessing import Process

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
            # p = Process(
            #     target=self.write_to_tsdb,
            #     args=(func.__name__, processing_time)
            # )
            # p.start()
        return wrapper

    def write_to_tsdb(self, name, processing_time):
        self.tsdb_client.write(
            [{
                "measurement": f"{cfg.influxdb_conf_name}_db",
                "tags": {"transaction_name": name},
                "time": time.time_ns(),
                "fields": {"response_time": processing_time},
            }]
        )


if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
