from locust import LoadTestShape


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1},
        {"duration": 120, "users": 20, "spawn_rate": 1},
        {"duration": 180, "users": 40, "spawn_rate": 1},
        {"duration": 240, "users": 60, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
