from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteOptions

from HT.locust.src.core.config import cfg

influx_client = InfluxDBClient(
    url="http://localhost:8086",
    token='demo_token',
    org=cfg.influx_org,
)

influxdb = influx_client.write_api(
    write_options=WriteOptions(
        batch_size=10,
        flush_interval=10_000,
        jitter_interval=2_000,
        retry_interval=5_000,
    )
)