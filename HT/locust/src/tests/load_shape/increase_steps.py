from locust import LoadTestShape


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 40, "users": 5, "spawn_rate": 1},
        {"duration": 80, "users": 10, "spawn_rate": 1},
        {"duration": 120, "users": 15, "spawn_rate": 1},
        {"duration": 180, "users": 20, "spawn_rate": 1},
        {"duration": 240, "users": 25, "spawn_rate": 1},
        {"duration": 300, "users": 30, "spawn_rate": 1},
        {"duration": 350, "users": 40, "spawn_rate": 1},
        {"duration": 400, "users": 50, "spawn_rate": 1},
        {"duration": 450, "users": 60, "spawn_rate": 1},
        {"duration": 500, "users": 70, "spawn_rate": 1},
        {"duration": 550, "users": 80, "spawn_rate": 1},
        {"duration": 600, "users": 90, "spawn_rate": 1},
        {"duration": 650, "users": 100, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
