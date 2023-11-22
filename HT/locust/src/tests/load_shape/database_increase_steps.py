from locust import LoadTestShape


class DataBaseStagesShape(LoadTestShape):
    stages = [
        {"duration": 40, "users": 10, "spawn_rate": 5},
        {"duration": 80, "users": 50, "spawn_rate": 5},
        {"duration": 120, "users": 100, "spawn_rate": 5},

    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
