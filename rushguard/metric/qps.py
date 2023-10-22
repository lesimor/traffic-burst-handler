# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring, line-too-long, broad-exception-raised
from datetime import datetime, timedelta

import pandas as pd
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime


def get_qps(prom_url, ingress_name, interval="1m"):
    # This is a simple example using http_requests_total metric.
    # You might need to adjust this to your specific metric name or labels.
    query = f'sum(rate(nginx_ingress_controller_requests{{ingress="{ingress_name}"}}[{interval}]))'

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=60)

    prom = PrometheusConnect(url=prom_url, disable_ssl=True)

    data = prom.custom_query_range(
        query, start_time=start_time, end_time=end_time, step="1m"
    )

    # NOTE: 일단 특정 시간 간격으로 평균 QPS를 얻는 것은 성공...!

    # 결과를 데이터프레임으로 변환
    df = pd.DataFrame(data)
    df.columns = ["timestamp", "qps"]

    # Unix 타임스탬프를 datetime 형식으로 변환
    df["timestamp"] = df["timestamp"].apply(parse_datetime)

    # 데이터를 1분 간격으로 다시 샘플링
    df.set_index("timestamp", inplace=True)
    print(df)
    # df_resampled = df.resample("1T").sum()

    # response = requests.get(f"{prom_url}/api/v1/query", params=params, timeout=5)

    # if response.status_code != 200:
    #     raise Exception(f"Error querying Prometheus: {response.content}")

    # data = response.json()
    # if (
    #     "data" not in data
    #     or "result" not in data["data"]
    #     or len(data["data"]["result"]) == 0
    # ):
    #     raise Exception(f"Unexpected Prometheus response format: {response.content}")

    # qps = data["data"]["result"][0]["value"][1]
    # return float(qps)
