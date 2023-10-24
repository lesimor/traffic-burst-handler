import click

from rushguard.settings import Settings

from ...metric.qps import get_qps_time_series


@click.command()
@click.pass_context
def metric(ctx):
    settings: Settings = ctx.obj["settings"]

    prometheus_url = settings.prometheus_url
    ingress = settings.ingress_name
    interval = settings.interval_unit

    qps_series = get_qps_time_series(
        prometheus_url, ingress, duration="2m", step=interval
    )
    print(qps_series)
