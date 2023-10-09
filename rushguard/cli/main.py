import click
from kubernetes import client, config

from ..metric.rt import get_avg_response_time
from ..scaler.resource import get_current_pod_count, scale_pods
from ..settings import Settings


@click.group()
@click.option("--env-file")
@click.pass_context
def cli(ctx, env_file):
    ctx.ensure_object(dict)

    ctx.obj["settings"] = Settings(_env_file=env_file)


@cli.command()
@click.option("--incluster", is_flag=True, default=False)
@click.pass_context
def scaler(ctx, incluster):
    settings: Settings = ctx.obj["settings"]
    if incluster:
        config.load_incluster_config()
    else:
        config.load_kube_config(context=settings.kube_context)
    k8s_client = client.AppsV1Api()
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
        f"Average response time for {ingress} over the last {interval}: {avg_time} seconds"
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
    if pods_to_scale > max_replicas:
        print(f"Max replicas ({max_replicas}) exceeded. Scaling down...")
        pods_to_scale = max_replicas

    if pods_to_scale == current_pods:
        print("No scaling required.")
    else:
        scale_pods(k8s_client, namespace, deployment, pods_to_scale)
