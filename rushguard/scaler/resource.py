from kubernetes import client


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
