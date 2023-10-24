import math

import click

from rushguard.metric.ingress import get_avg_response_time, get_qps_time_series
from rushguard.scaler.resource import get_current_pod_count, scale_pods
from rushguard.settings import Settings

from ...metric.resource import get_resource_metrics


@click.group()
@click.pass_context
def resource(ctx):
    pass


@click.command()
@click.pass_context
def scale(ctx):
    settings: Settings = ctx.obj["settings"]

    k8s_client = ctx.obj["k8s_client"]
    prometheus_url = settings.prometheus_url
    ingress = settings.ingress_name
    interval = settings.avg_rt_duration
    namespace = settings.kube_namespace
    deployment = settings.kube_deployment

    avg_response_time = get_avg_response_time(
        prometheus_url, ingress, interval=interval
    )
    print(
        f"Average response time for {ingress} over the last {interval}: {avg_response_time} seconds"  # noqa
    )

    pods_to_scale = current_pods = get_current_pod_count(
        k8s_client, namespace, deployment
    )

    qps_time_series = get_qps_time_series(
        prometheus_url,
        ingress,
        duration=settings.qps_time_series_duration,
        step=settings.qps_time_series_step,
    )

    current_qps = qps_time_series[-3:]["qps"].mean()

    qps_capacity_per_pod = settings.qps_capacity_per_pod

    pod_number_by_latency = current_qps // qps_capacity_per_pod

    (
        current_avg_cpu_usage_nano_second,
        current_avg_memory_usage_kilobyte,
    ) = get_resource_metrics(namespace)
    cpu_usage_limit_nano_second = settings.cpu_utilization_threshold_second * (2**30)
    mem_usage_limit_kilobyte = settings.memory_utilization_threshold_megabyte * (
        2**10
    )

    required_pod_by_cpu = math.ceil(
        current_pods * (current_avg_cpu_usage_nano_second / cpu_usage_limit_nano_second)
    )
    required_pod_by_memory = math.ceil(
        current_pods * (current_avg_memory_usage_kilobyte / mem_usage_limit_kilobyte)
    )

    required_pod_by_latency = math.ceil(
        current_pods * (avg_response_time / settings.response_time_threshold)
    )

    pod_number_by_utilization = max(
        required_pod_by_cpu,
        required_pod_by_memory,
    )

    pods_to_scale = min(
        max(
            pod_number_by_latency,
            pod_number_by_utilization,
            required_pod_by_latency,
            settings.min_replicas,
        ),
        settings.max_replicas,
    )

    if current_pods != pods_to_scale:
        print(f"Scaling from {current_pods} to {pods_to_scale}...")
        scale_pods(k8s_client, namespace, deployment, pods_to_scale)


resource.add_command(scale, "scale")
