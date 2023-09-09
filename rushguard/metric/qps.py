# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring, line-too-long, broad-exception-raised
import requests

PROMETHEUS_URL = "http://kaist-ingress-prometheus.dchain-connect.com"
INGRESS_NAME = "php-apache-ingress"


def get_qps(prom_url, ingress_name, interval="5m"):
    # This is a simple example using http_requests_total metric.
    # You might need to adjust this to your specific metric name or labels.
    query = f'rate(nginx_ingress_controller_requests{{ingress="{ingress_name}"}}[{interval}])'

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

    qps = data["data"]["result"][0]["value"][1]
    return float(qps)


if __name__ == "__main__":
    INTERVAL_UNIT = "2m"
    qps_value = get_qps(PROMETHEUS_URL, INGRESS_NAME, interval=INTERVAL_UNIT)
    print(f"QPS (over the last 5 minutes): {qps_value}")
