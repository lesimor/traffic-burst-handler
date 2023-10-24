import click

from rushguard.settings import Settings

from ...metric.qps import get_qps_time_series
from ...metric.rt import get_avg_response_time


@click.command()
@click.pass_context
def metric(ctx):
    settings: Settings = ctx.obj["settings"]

    prometheus_url = settings.prometheus_url
    ingress = settings.ingress_name
    qps_time_series_duration = settings.qps_time_series_duration

    qps_series = get_qps_time_series(
        prometheus_url, ingress, duration=qps_time_series_duration, step="1s"
    )
    print(qps_series)

    avg_response_time = get_avg_response_time(prometheus_url, ingress, interval="5m")
    print(avg_response_time)
