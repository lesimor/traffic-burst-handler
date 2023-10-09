import requests
from kubernetes import client


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


def scale_up_pods(
    api: client.AppsV1Api,
    namespace: str,
    deployment: str,
    max_replicas: int,
):
    try:
        # 현재의 replica 수를 가져옵니다.
        current_deployment = api.read_namespaced_deployment(deployment, namespace)
        current_replicas = current_deployment.spec.replicas

        if current_replicas < max_replicas:
            current_deployment.spec.replicas = current_replicas + 1
            api.patch_namespaced_deployment(deployment, namespace, current_deployment)
            print(
                f"Scaled up {deployment} to {current_deployment.spec.replicas} replicas."
            )
        else:
            print(f"{deployment} has already reached max replicas ({max_replicas}).")

    except Exception as e:
        print(f"Error scaling up: {e}")


def scale_down_pods(
    api,
    namespace: str,
    deployment: str,
    min_replicas: int = 1,
):
    try:
        current_deployment = api.read_namespaced_deployment(deployment, namespace)
        current_replicas = get_current_pod_count(api, namespace, deployment)

        if current_replicas > min_replicas:
            current_deployment.spec.replicas = current_replicas - 1
            api.patch_namespaced_deployment(deployment, namespace, current_deployment)
            print(
                f"Scaled down {deployment} to {current_deployment.spec.replicas} replicas."
            )
        else:
            print(f"{deployment} is already at minimum replicas.")

    except Exception as e:
        print(f"Error scaling down: {e}")


def scale_pods(
    api,
    namespace: str,
    deployment: str,
    replicas: int,
):
    try:
        current_deployment = api.read_namespaced_deployment(deployment, namespace)
        current_replicas = get_current_pod_count(api, namespace, deployment)

        if current_replicas != replicas:
            current_deployment.spec.replicas = replicas
            api.patch_namespaced_deployment(deployment, namespace, current_deployment)
            print(
                f"Scaled {deployment} to {current_deployment.spec.replicas} replicas."
            )
        else:
            print(f"{deployment} is already at {replicas} replicas.")

    except Exception as e:
        print(f"Error scaling: {e}")


def get_current_pod_count(api, namespace: str, deployment: str):
    try:
        current_deployment = api.read_namespaced_deployment(deployment, namespace)
        current_replicas = current_deployment.spec.replicas
        return current_replicas
    except Exception as e:
        print(f"Error getting current pod count: {e}")
        return 0
