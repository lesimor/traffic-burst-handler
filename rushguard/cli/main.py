import click


@click.command()
@click.option("--name", default="World", help="Who to greet.")
def hello(name):
    click.echo(f"Hello, {name}!")
