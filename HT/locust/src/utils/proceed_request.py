import time
from functools import wraps

from HT.locust.src.core.config import cfg, logger


def proceed_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_start_time = time.time()
        transaction = func(*args, **kwargs)
        processing_time = int((time.time() - request_start_time) * 1000)

        cfg.influxdb.write(
            cfg.influx_bucket,
            cfg.influx_org,
            [{
                "measurement": f"{cfg.conf_name}_db",
                "tags": {"transaction_name": func.__name__},
                "time": time.time_ns(),
                "fields": {"response_time": processing_time},
            }],
        )

        logger.debug(
            f"""{func.__name__} status: {transaction.status_code
            if func.__name__ != 'send_payment'
            else 'message delivered'}"""
        )

    return wrapper
