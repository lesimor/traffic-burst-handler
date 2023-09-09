# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring, line-too-long, broad-exception-raised
import requests

from rushguard.settings import settings

PROMETHEUS_URL = settings.prometheus_url
INGRESS_NAME = settings.ingress_name


def get_avg_response_time(prom_url, ingress_name, interval="5m"):
    query = (
        f'rate(nginx_ingress_controller_request_duration_seconds_sum{{ingress="{ingress_name}"}}[{interval}]) / '
        f'rate(nginx_ingress_controller_request_duration_seconds_count{{ingress="{ingress_name}"}}[{interval}])'
    )

    response = requests.get(
        f"{prom_url}/api/v1/query", params={"query": query}, timeout=5
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


if __name__ == "__main__":
    INTERVAL_UNIT = "2m"
    avg_time = get_avg_response_time(
        PROMETHEUS_URL, INGRESS_NAME, interval=INTERVAL_UNIT
    )
    print(
        f"Average response time for {INGRESS_NAME} over the last {INTERVAL_UNIT}: {avg_time} seconds"
    )
