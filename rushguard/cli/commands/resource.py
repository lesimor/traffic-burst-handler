import click

from rushguard.metric.qps import get_qps_time_series
from rushguard.metric.rt import get_avg_response_time
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
    interval = settings.avg_rt_duration
    namespace = settings.kube_namespace
    deployment = settings.kube_deployment

    avg_time = get_avg_response_time(prometheus_url, ingress, interval=interval)
    print(
        f"Average response time for {ingress} over the last {interval}: {avg_time} seconds"  # noqa
    )

    pods_to_scale = current_pods = get_current_pod_count(
        k8s_client, namespace, deployment
    )

    qps_time_series = get_qps_time_series(
        prometheus_url, ingress, duration="2m", step="1s"
    )

    current_qps = qps_time_series[-30:]["qps"].mean()

    qps_capacity_per_pod = settings.qps_capacity_per_pod

    pod_number_by_latency = current_qps // qps_capacity_per_pod

    pods_to_scale = min(
        max(
            pod_number_by_latency,
            settings.min_replicas,
        ),
        settings.max_replicas,
    )

    if current_pods != pods_to_scale:
        print(f"Scaling from {current_pods} to {pods_to_scale}...")
        scale_pods(k8s_client, namespace, deployment, pods_to_scale)

    # if avg_time > rt_threshold:
    #     print("Average response time exceeded threshold. Scaling up...")
    #     # scale_up_pods(k8s_client, namespace, deployment, max_replicas)
    #     pods_to_scale += 1
    # else:
    #     scale_difference = (rt_threshold - avg_time) / rt_threshold

    #     if scale_difference >= rt_bandwidth_below:
    #         print("Significant difference from threshold detected. Scaling down...")
    #         # scale_down_pods(k8s_client, namespace, deployment)
    #         pods_to_scale -= 1

    # buffer_pods = buffer_pod_number(
    #     settings,
    #     t_start=datetime.now() - timedelta(minutes=5),
    # )

    # total_pods = pods_to_scale + buffer_pods

    # if total_pods > max_replicas:
    #     print(f"Max replicas ({max_replicas}) exceeded. Scaling down...")
    #     total_pods = max_replicas

    # if total_pods == current_pods:
    #     print("No scaling required.")
    # else:
    #     print(f"Scaling from {current_pods} to {total_pods}...")
    #     scale_pods(k8s_client, namespace, deployment, total_pods)


resource.add_command(scale, "scale")
