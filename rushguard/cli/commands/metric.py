import click

from rushguard.settings import Settings

from ...metric.ingress import get_avg_response_time, get_recent_qps_time_series
from ...metric.resource import get_resource_utility_metrics


@click.command()
@click.pass_context
def metric(ctx):
    settings: Settings = ctx.obj["settings"]

    prometheus_url = settings.ingress_metric_url
    ingress = settings.ingress_name
    qps_time_series_duration = settings.qps_time_series_duration

    qps_series = get_recent_qps_time_series(
        prometheus_url, ingress, duration=qps_time_series_duration, step="1s"
    )
    print(qps_series)

    avg_response_time = get_avg_response_time(prometheus_url, ingress, interval="5m")
    print(avg_response_time)

    avg_cpu_usage, avg_memory_usage = get_resource_utility_metrics(settings=settings)
    print(avg_cpu_usage, avg_memory_usage)
