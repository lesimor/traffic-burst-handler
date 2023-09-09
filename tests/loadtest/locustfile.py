from locust import HttpUser, constant_throughput, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")

    wait_time = constant_throughput(1)
