from influxdb_client.client.write_api import WriteOptions

from HT.locust.src.core.config_new import cfg
from HT.locust.src.database.influxdb import influx_client


class InfluxDbRepo():
    def __init__(self):
        self.options = WriteOptions(
            batch_size=cfg.influxdb_batch_size,
            flush_interval=cfg.influxdb_flush_interval,
            jitter_interval=cfg.influxdb_jitter_interval,
            retry_interval=cfg.influxdb_retry_interval,
        )

    def write(self, data):
        with influx_client.write_api(write_options=self.options) as client:
            client.write(cfg.influxdb_bucket, cfg.influxdb_org, data)
