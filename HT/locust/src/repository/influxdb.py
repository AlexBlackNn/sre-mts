from influxdb_client.client.write_api import WriteOptions

from HT.locust.src.database.influxdb import influx_client
from HT.locust.src.core.config_new import cfg


class InfluxDbRepo():
    def __init__(self):
        self.influxdb = influx_client.write_api(
            write_options=WriteOptions(
                batch_size=cfg.influxdb_batch_size,
                flush_interval=cfg.influxdb_flush_interval,
                jitter_interval=cfg.influxdb_jitter_interval,
                retry_interval=cfg.influxdb_retry_interval,
            )
        )

    def write(self, data):
        self.influxdb.write(cfg.influxdb_bucket, cfg.influxdb_org, data)
