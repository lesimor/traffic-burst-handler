# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring, line-too-long, broad-exception-raised
from datetime import datetime, timedelta

import pandas as pd
import requests
from prometheus_api_client import PrometheusConnect
from pytimeparse.timeparse import timeparse


def get_recent_qps_time_series(
    prom_url, ingress_name, duration, step="1m"
) -> pd.DataFrame:
    end_time = datetime.now()

    start_time = end_time - timedelta(seconds=timeparse(duration))

    return get_qps_time_series(
        prom_url, ingress_name, start_time, end_time, step=step, query_duration=duration
    )


def get_qps_time_series(
    prom_url, ingress_name, start_time, end_time, step="2m", query_duration="2m"
) -> pd.DataFrame:
    # This is a simple example using http_requests_total metric.
    # You might need to adjust this to your specific metric name or labels.

    query = f'sum(irate(nginx_ingress_controller_requests{{ingress="{ingress_name}"}}[{query_duration}]))'

    prom = PrometheusConnect(url=prom_url, disable_ssl=True)

    data = prom.custom_query_range(
        query, start_time=start_time, end_time=end_time, step=step
    )

    values = data[0]["values"]
    datetimes = [datetime.fromtimestamp(_timestamp) for _timestamp, _ in values]
    qps_list = [float(qps) for _, qps in values]

    df = pd.DataFrame({"datetime": datetimes, "qps": qps_list})

    return df


def get_avg_response_time(prom_url, ingress_name, interval="5m"):
    query = (
        f'rate(nginx_ingress_controller_request_duration_seconds_sum{{ingress="{ingress_name}"}}[{interval}]) / '
        f'rate(nginx_ingress_controller_request_duration_seconds_count{{ingress="{ingress_name}"}}[{interval}])'
    )

    response = requests.get(
        f"{prom_url}/api/v1/query", params={"query": query}, timeout=10
    )

    if response.status_code != 200:
        raise Exception(f"Error querying Prometheus: {response.content}")

    data = response.json()
    if (
        "data" not in data
        or "result" not in data["data"]
        or len(data["data"]["result"]) == 0
    ):
        raise Exception(f"Unexpected Prometheus response format: {response.content}")

    avg_response_time = data["data"]["result"][0]["value"][1]
    return float(avg_response_time)


def get_average_response_time_series(
    prom_url, ingress_name, start_time, end_time, step="1m", query_duration="2m"
) -> pd.DataFrame:
    query = f"histogram_quantile(0.80, sum(rate(nginx_ingress_controller_request_duration_seconds_bucket{{ingress='{ingress_name}'}}[{query_duration}])) by (le))"

    prom = PrometheusConnect(url=prom_url, disable_ssl=True)

    data = prom.custom_query_range(
        query, start_time=start_time, end_time=end_time, step=step
    )

    values = data[0]["values"]
    datetimes = [datetime.fromtimestamp(_timestamp) for _timestamp, _ in values]
    rt_list = [float(qps) for _, qps in values]
    df = pd.DataFrame({"datetime": datetimes, "rt": rt_list})
    return df
