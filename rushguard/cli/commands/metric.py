import click

from rushguard.settings import Settings

from ...metric.qps import get_qps


@click.command()
@click.pass_context
def metric(ctx):
    settings: Settings = ctx.obj["settings"]

    prometheus_url = settings.prometheus_url
    ingress = settings.ingress_name
    interval = settings.interval_unit

    qps_series = get_qps(prometheus_url, ingress, interval=interval)
    print(qps_series)
