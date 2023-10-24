# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring, line-too-long, broad-exception-raised
from datetime import datetime, timedelta

import pandas as pd
from prometheus_api_client import PrometheusConnect
from pytimeparse.timeparse import timeparse


def get_qps_time_series(
    prom_url, ingress_name, duration, end_time=None, step="1m"
) -> pd.DataFrame:
    # This is a simple example using http_requests_total metric.
    # You might need to adjust this to your specific metric name or labels.

    query = f'sum(irate(nginx_ingress_controller_requests{{ingress="{ingress_name}"}}[{duration}]))'

    prom = PrometheusConnect(url=prom_url, disable_ssl=True)

    if not end_time:
        end_time = datetime.now()

    start_time = end_time - timedelta(seconds=timeparse(duration))

    data = prom.custom_query_range(
        query, start_time=start_time, end_time=end_time, step=step
    )

    values = data[0]["values"]
    datetimes = [datetime.fromtimestamp(_timestamp) for _timestamp, _ in values]
    qps_list = [float(qps) for _, qps in values]

    df = pd.DataFrame({"datetime": datetimes, "qps": qps_list})

    return df
