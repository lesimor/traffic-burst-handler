import time

from click.testing import CliRunner

from rushguard.cli.main import cli

if __name__ == "__main__":
    while True:
        result = CliRunner().invoke(
            cli,
            [
                "--env-file",
                "/Users/user/Projects/traffic-burst-handler/.env",
                "resource",
                "scale",
            ],
        )
        print(result.output)
        time.sleep(30)
