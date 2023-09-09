import time

import requests
from kubernetes import client, config

from rushguard.settings import settings

PROMETHEUS_URL = settings.prometheus_url
INGRESS_NAME = settings.ingress_name
INTERVAL = settings.interval_unit
THRESHOLD = settings.response_time_threshold
SLEEP_TIME = 60  # 60초마다 체크
NAMESPACE = settings.kube_namespace
DEPLOYMENT_NAME = settings.kube_deployment
MAX_REPLICAS = settings.max_replicas

config.load_kube_config(context=settings.kube_context)
v1 = client.AppsV1Api()  # Create an API client object for the AppsV1 API group


def get_avg_response_time(prom_url, ingress_name, interval="5m"):
    query = (
        f'rate(nginx_ingress_controller_request_duration_seconds_sum{{ingress="{ingress_name}"}}[{interval}]) / '
        f'rate(nginx_ingress_controller_request_duration_seconds_count{{ingress="{ingress_name}"}}[{interval}])'
    )

    response = requests.get(f"{prom_url}/api/v1/query", params={"query": query})

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


def scale_up_pods():
    try:
        # 현재의 replica 수를 가져옵니다.
        current_deployment = v1.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)
        current_replicas = current_deployment.spec.replicas

        if current_replicas < MAX_REPLICAS:
            current_deployment.spec.replicas = current_replicas + 1
            v1.patch_namespaced_deployment(
                DEPLOYMENT_NAME, NAMESPACE, current_deployment
            )
            print(
                f"Scaled up {DEPLOYMENT_NAME} to {current_deployment.spec.replicas} replicas."
            )
        else:
            print(
                f"{DEPLOYMENT_NAME} has already reached max replicas ({MAX_REPLICAS})."
            )

    except Exception as e:
        print(f"Error scaling up: {e}")


def scale_down_pods():
    try:
        current_deployment = v1.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)
        current_replicas = current_deployment.spec.replicas

        if current_replicas > 1:
            current_deployment.spec.replicas = current_replicas - 1
            v1.patch_namespaced_deployment(
                DEPLOYMENT_NAME, NAMESPACE, current_deployment
            )
            print(
                f"Scaled down {DEPLOYMENT_NAME} to {current_deployment.spec.replicas} replicas."
            )
        else:
            print(f"{DEPLOYMENT_NAME} is already at minimum replicas.")

    except Exception as e:
        print(f"Error scaling down: {e}")


if __name__ == "__main__":
    while True:
        avg_time = get_avg_response_time(
            PROMETHEUS_URL, INGRESS_NAME, interval=INTERVAL
        )
        print(
            f"Average response time for {INGRESS_NAME} over the last {INTERVAL}: {avg_time} seconds"
        )

        if avg_time > THRESHOLD:
            print("Average response time exceeded threshold. Scaling up...")
            scale_up_pods()
        else:
            scale_difference = (THRESHOLD - avg_time) / THRESHOLD

            if scale_difference >= 0.10:
                print("Significant difference from threshold detected. Scaling down...")
                scale_down_pods()

        time.sleep(SLEEP_TIME)
