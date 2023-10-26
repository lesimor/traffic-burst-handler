from kubernetes import client


def get_resource_metrics(namespace="default"):
    # 파드의 CPU 및 메모리 사용량을 조회하기 위해 메트릭 API를 사용합니다.
    # 메트릭 서버가 필요합니다.
    api_instance = client.CustomObjectsApi()
    api_response = api_instance.list_namespaced_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        namespace=namespace,
        plural="pods",
    )

    # 파드별 메트릭 정보 출력
    cpu_usages = []
    memory_usages = []
    for pod in api_response["items"]:
        # pod_name = pod["metadata"]["name"]

        # 컨테이너 메트릭 정보
        for container in pod["containers"]:
            usage = container["usage"]
            cpu_usage = usage["cpu"]
            memory_usage = usage["memory"]
            cpu_usages.append(int(cpu_usage.replace("n", "")))
            memory_usages.append(int(memory_usage.replace("Ki", "")))

    # 파드별 평균 CPU, 메모리 사용량 출력
    avg_cpu_usage = sum(cpu_usages) / len(cpu_usages)
    avg_memory_usage = sum(memory_usages) / len(memory_usages)

    return avg_cpu_usage, avg_memory_usage
