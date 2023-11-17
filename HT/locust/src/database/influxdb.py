from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions

from HT.locust.src.core.config_new import cfg

influx_client = InfluxDBClient(
    url=cfg.influxdb_host,
    token=cfg.influxdb_token,
    org=cfg.influxdb_org,
)

influxdb = influx_client.write_api(
    write_options=WriteOptions(
        batch_size=cfg.influxdb_batch_size,
        flush_interval=cfg.influxdb_flush_interval,
        jitter_interval=cfg.influxdb_jitter_interval,
        retry_interval=cfg.influxdb_retry_interval,
    )
)