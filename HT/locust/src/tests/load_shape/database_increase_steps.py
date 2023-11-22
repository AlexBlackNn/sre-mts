from locust import LoadTestShape


class DataBaseStagesShape(LoadTestShape):
    stages = [
        {"duration": 40, "users": 100, "spawn_rate": 100},
        {"duration": 80, "users": 500, "spawn_rate": 100},
        {"duration": 120, "users": 1000, "spawn_rate": 100},

    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
