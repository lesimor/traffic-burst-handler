def scale_pods(
    api,
    namespace: str,
    deployment: str,
    replicas: int,
):
    current_deployment = api.read_namespaced_deployment(deployment, namespace)
    current_deployment.spec.replicas = replicas
    api.patch_namespaced_deployment(deployment, namespace, current_deployment)


def get_current_pod_count(api, namespace: str, deployment: str):
    try:
        current_deployment = api.read_namespaced_deployment(deployment, namespace)
        current_replicas = current_deployment.spec.replicas
        return current_replicas
    except Exception as e:
        print(f"Error getting current pod count: {e}")
        return 0
