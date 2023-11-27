from locust import LoadTestShape


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 7200, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
