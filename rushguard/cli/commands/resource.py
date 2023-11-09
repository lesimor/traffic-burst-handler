import math
import time
import traceback
from datetime import datetime, timedelta

import click

from rushguard.metric.ingress import get_avg_response_time, get_recent_qps_time_series
from rushguard.settings import Settings
from rushguard.utils.graph import generate_graph
from rushguard.utils.resource import get_current_pod_count, scale_pods

from ...metric.resource import get_resource_utility_metrics
from ...utils.buffer import buffer_pod_number


@click.group()
@click.pass_context
def resource(ctx):
    pass


@click.command()
@click.option("--test-duration-second")
@click.option("--scaling-interval-second")
@click.option("--output-file")
@click.option("--graph", is_flag=True, default=True)
@click.pass_context
def scale(ctx, test_duration_second, scaling_interval_second, output_file, graph):
    settings: Settings = ctx.obj["settings"]

    k8s_client = ctx.obj["k8s_client"]
    prometheus_url = settings.ingress_metric_url
    ingress = settings.ingress_name
    interval = settings.avg_rt_duration
    namespace = settings.kube_namespace
    deployment = settings.kube_deployment

    start_time = datetime.now()

    graph_data = []

    adaptive_pod_history = []
    while datetime.now() < start_time + timedelta(seconds=int(test_duration_second)):
        try:
            avg_response_time = get_avg_response_time(
                prometheus_url, ingress, interval=interval
            )
            if math.isnan(avg_response_time):
                avg_response_time = 0
            print(
                f"Average response time for {ingress} over the last {interval}: {avg_response_time} seconds"  # noqa
            )

            current_pod_count = current_adaptive_pods_volume = get_current_pod_count(
                k8s_client, namespace, deployment
            )

            if adaptive_pod_history:
                current_adaptive_pods_volume = adaptive_pod_history[-1]

            qps_time_series = get_recent_qps_time_series(
                prometheus_url,
                ingress,
                duration=settings.qps_time_series_duration,
                step=settings.qps_time_series_step,
            )

            current_qps = qps_time_series[-settings.qps_mean_window_size :][
                "qps"
            ].mean()

            qps_capacity_per_pod = settings.qps_capacity_per_pod

            pod_number_by_latency = current_qps // qps_capacity_per_pod

            (
                current_avg_cpu_usage_nano_second,
                current_avg_memory_usage_kilobyte,
            ) = get_resource_utility_metrics(settings=settings)
            cpu_usage_limit_nano_second = settings.cpu_utilization_threshold_second * (
                2**30
            )
            mem_usage_limit_kilobyte = (
                settings.memory_utilization_threshold_megabyte * (2**10)
            )

            required_pod_by_cpu = math.ceil(
                current_adaptive_pods_volume
                * (current_avg_cpu_usage_nano_second / cpu_usage_limit_nano_second)
            )
            required_pod_by_memory = math.ceil(
                current_adaptive_pods_volume
                * (current_avg_memory_usage_kilobyte / mem_usage_limit_kilobyte)
            )

            required_pod_by_latency = math.ceil(
                (current_qps / settings.qps_capacity_per_pod)
                * (avg_response_time / settings.response_time_threshold)
            )

            pod_number_by_utilization = max(
                required_pod_by_cpu,
                required_pod_by_memory,
            )

            pod_elapsed, pod_volatility = buffer_pod_number(
                qps_time_series["qps"],
                settings,
                timedelta(seconds=int(test_duration_second)),
            )
            buffer_pod = pod_elapsed + pod_volatility

            adaptive_pod_volume = max(
                pod_number_by_latency,
                pod_number_by_utilization,
                required_pod_by_latency,
                settings.min_replicas,
            )

            adaptive_pod_history.append(adaptive_pod_volume)

            pod_to_scale = int(
                min(adaptive_pod_volume + buffer_pod, settings.max_replicas)
            )

            print("----min----")
            print("----max----")
            print(f"pod_number_by_latency: {pod_number_by_latency}")
            print(f"pod_number_by_utilization: {pod_number_by_utilization}")
            print(f"required_pod_by_latency: {required_pod_by_latency}")
            print(f"settings.min_replicas: {settings.min_replicas}")
            print(f"==> adaptive_pod_volume: {adaptive_pod_volume}")
            print("-----------")
            print(f"max_replicas: {settings.max_replicas}")
            print("-----------")
            print("+")
            print(f"buffer_pod: {buffer_pod} (elapsed + volatility)")
            print(f"ㄴpod_elapsed: {pod_elapsed}")
            print(f"ㄴpod_volatility: {pod_volatility}")
            print("=========================")
            print(f"==> pod_to_scale: {pod_to_scale}")

            if current_pod_count != pod_to_scale:
                print(
                    f"Scaling from {current_pod_count} to {pod_to_scale}... ({datetime.now().strftime('%H:%M:%S')})"
                )
                scale_pods(k8s_client, namespace, deployment, pod_to_scale)
                graph_data.append((datetime.now(), pod_to_scale))
            else:
                print(f"Pods are already scaled to {current_pod_count}.")
        except Exception as e:
            print(f"Error scaling pods: {e}")
            print(traceback.format_exc())
            print("unexpected error, but continue...")
        finally:
            time.sleep(int(scaling_interval_second))

    if graph:
        times = [time[0] for time in graph_data]
        values = [time[1] for time in graph_data]
        generate_graph(times, values, output_file=output_file)

        print("scaling down to min replicas...")
        scale_pods(k8s_client, namespace, deployment, settings.min_replicas)


resource.add_command(scale, "scale")
