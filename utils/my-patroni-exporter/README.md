FORK OF https://github.com/Showmax/patroni-exporter

# local run at 9101 (-p 9101:9101 port forwarding), (--port 9101 where server starts)
docker run -ti -p 9101:9101 patroni_exporter --port 9101 --patroni-url http://77.105.185.143:8008/patroni --timeout 5 --debug

# metrics 
http://localhost:9101/metrics


# at vm with patroni needed to do
docker build -t alexblacknn/patroni_exporter:0.0.1 .
docker push alexblacknn/patroni_exporter:0.0.1
ssh alexblacknn@77.105.185.143
sudo docker run -d -ti -p 9101:9101 alexblacknn/patroni_exporter:0.0.1 --port 9101 --patroni-url http://10.0.10.6:8008/patroni --timeout 5 --debug




# patroni-exporter

Provides Patroni related metrics for Prometheus.

This exporter scrapes Patroni API (https://github.com/zalando/patroni) and transforms the obtained information into Prometheus-scrapable (https://prometheus.io/) format.

Configuration can by environment variables or commandline arguments. If both is available the value of the commandline argument is taken.
The following configuration parameters are available:
- port: `PATRONI_EXPORTER_PORT`, `-p`, `--port` specifies the port it should listen at
- bind: `PATRONI_EXPORTER_BIND`, `-b`, `--bind` specifies the address to bind to
- patroni url: `PATRONI_EXPORTER_URL`, `-u`, `--patroni-url` specifies the full to path the patroni API endpoint
- debug: `PATRONI_EXPORTER_DEBUG`, `-d`, `--debug` enables debug output
- timeout: `PATRONI_EXPORTER_TIMEOUT`, `-t`, `--timeout` configures the timeout for patroni API
- address family: `PATRONI_EXPORTER_ADDRESS_FAMILY`, `-a`, `--address-family` chooses which adress family to use. Either `ipv4` (`AF_INET`) or `ipv6` (`AF_INET6`). If listening on both `ipv6` and `ipv4` is required, `AF_INET6` and a bind to '' or '::' must be used (the unfortunate side-effect is that it listens on all interfaces)
- requests verify: `PATRONI_EXPORTER_REQUEST_VERIFY`, `--requests-verify` Accepts `true|false`, in which case it controls whether Python's requests library verifies the server's TLS certificate. It also accepts a path to a CA bundle to use. Defaults to ``true``

This service also responds on the `/health` endpoint and can be monitored this way.

The `/metrics` endpoint is designated for the prometheus scraping.

The default `9547` port has been reserved on https://github.com/prometheus/prometheus/wiki/Default-port-allocations

Requires python >= 3.6 because of the usage of `f-strings` and type hints.

## Docker

There is a simple `Dockerfile` which allows you to run `patroni-exporter` in the Docker container.
Usage example:

1. Build `patroni-exporter` docker image.

```
docker build -t patroni_exporter .
```

2. Run Docker container. Don't forget to pass required commandline arguments at the end of the `run` command.

```
docker run -d -ti patroni_exporter --port some_port --patroni-url http://some_host_fqdn:some_port/patroni --timeout 5 --debug
```

## Known issues/limitations/workarounds

- due to how Patroni replicas respond with their information, but, when compared to primary, use HTTP code 503 (Service Unavailable) to avoid being registered as write-capable endpoints on load balancers, the exporter will attempt proper parsing when the response is a JSON with key-value `{"role": "replica"}`
