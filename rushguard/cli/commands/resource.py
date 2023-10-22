from datetime import datetime, timedelta

import click

from rushguard.metric.rt import get_avg_response_time
from rushguard.scaler.buffer import buffer_pod_number
from rushguard.scaler.resource import get_current_pod_count, scale_pods
from rushguard.settings import Settings


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
    interval = settings.interval_unit
    rt_threshold = settings.response_time_threshold
    namespace = settings.kube_namespace
    deployment = settings.kube_deployment
    max_replicas = settings.max_replicas
    rt_bandwidth_below = settings.response_time_threshold_bandwidth_below

    avg_time = get_avg_response_time(prometheus_url, ingress, interval=interval)
    print(
        f"Average response time for {ingress} over the last {interval}: {avg_time} seconds"  # noqa
    )

    pods_to_scale = current_pods = get_current_pod_count(
        k8s_client, namespace, deployment
    )

    if avg_time > rt_threshold:
        print("Average response time exceeded threshold. Scaling up...")
        # scale_up_pods(k8s_client, namespace, deployment, max_replicas)
        pods_to_scale += 1
    else:
        scale_difference = (rt_threshold - avg_time) / rt_threshold

        if scale_difference >= rt_bandwidth_below:
            print("Significant difference from threshold detected. Scaling down...")
            # scale_down_pods(k8s_client, namespace, deployment)
            pods_to_scale -= 1

    buffer_pods = buffer_pod_number(
        settings,
        t_start=datetime.now() - timedelta(minutes=5),
    )

    total_pods = pods_to_scale + buffer_pods

    if total_pods > max_replicas:
        print(f"Max replicas ({max_replicas}) exceeded. Scaling down...")
        total_pods = max_replicas

    if total_pods == current_pods:
        print("No scaling required.")
    else:
        print(f"Scaling from {current_pods} to {total_pods}...")
        scale_pods(k8s_client, namespace, deployment, total_pods)


resource.add_command(scale, "scale")
