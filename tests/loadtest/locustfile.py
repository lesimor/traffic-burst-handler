import math

from locust import HttpUser, LoadTestShape, constant_throughput, task


class StepLoadShape(LoadTestShape):
    """
    A step load shape


    Keyword arguments:

        step_time -- Time between steps
        step_load -- User increase amount at each step
        spawn_rate -- Users to stop/start per second at every step
        time_limit -- Time limit in seconds

    """

    step_time = 30
    step_load = 10
    spawn_rate = 10
    time_limit = 600

    qps = [
        10,
        10,
        100,
        90,
        80,
        70,
        60,
        50,
        40,
        30,
        20,
        10,
    ]

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
