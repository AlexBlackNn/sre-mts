from locust import LoadTestShape


class DataBaseStagesShape(LoadTestShape):
    stages = [
        {"duration": 40, "users": 5, "spawn_rate": 1},
        {"duration": 80, "users": 10, "spawn_rate": 1},
        {"duration": 120, "users": 15, "spawn_rate": 1},

    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]