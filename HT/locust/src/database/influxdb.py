from influxdb_client import InfluxDBClient

from HT.locust.src.core.config_new import cfg

influx_client = InfluxDBClient(
    url=cfg.influxdb_host,
    token=cfg.influxdb_token,
    org=cfg.influxdb_org,
)
