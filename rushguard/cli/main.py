import click
from kubernetes import client, config

from rushguard.cli.commands.metric import metric
from rushguard.cli.commands.resource import resource

from ..settings import Settings


@click.group()
@click.option("--env-file")
@click.option("--incluster", is_flag=True, default=False)
@click.pass_context
def cli(ctx, env_file, incluster):
    ctx.ensure_object(dict)

    settings = Settings(_env_file=env_file)
    ctx.obj["settings"] = settings

    if incluster:
        config.load_incluster_config()
    else:
        config.load_kube_config(context=settings.kube_context)

    ctx.obj["k8s_client"] = client.AppsV1Api()


cli.add_command(resource, "resource")
cli.add_command(metric, "metric")
