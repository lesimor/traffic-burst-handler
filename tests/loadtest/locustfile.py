import math
import os

import pandas as pd
from locust import HttpUser, LoadTestShape, constant_throughput, task

pattern_file = os.getenv("PATTERN_FILE_PATH")
pattern_name = os.getenv("PATTERN_NAME")
patterns = pd.read_csv(pattern_file, usecols=[pattern_name])


class StepLoadShape(LoadTestShape):
    """
    A step load shape


    Keyword arguments:

        step_time -- Time between steps
        step_load -- User increase amount at each step

    """

    step_time = 20
    step_load = 1

    qps = patterns[pattern_name].tolist()

    def tick(self):
        run_time = self.get_run_time()
        total_time = self.step_time * len(self.qps)

        if run_time > total_time:
            return None

        current_qps = self.qps[math.floor(run_time / self.step_time)]

        return (current_qps, current_qps)


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")

    wait_time = constant_throughput(1)
