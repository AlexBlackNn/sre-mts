from locust import LoadTestShape


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 40, "users": 50, "spawn_rate": 1},
        {"duration": 80, "users": 100, "spawn_rate": 1},
        {"duration": 120, "users": 150, "spawn_rate": 1},
        {"duration": 180, "users": 200, "spawn_rate": 1},
        {"duration": 240, "users": 250, "spawn_rate": 1},
        {"duration": 300, "users": 300, "spawn_rate": 1},
        {"duration": 350, "users": 400, "spawn_rate": 1},
        {"duration": 400, "users": 500, "spawn_rate": 1},
        {"duration": 450, "users": 600, "spawn_rate": 1},
        {"duration": 500, "users": 700, "spawn_rate": 1},
        {"duration": 550, "users": 800, "spawn_rate": 1},
        {"duration": 600, "users": 900, "spawn_rate": 1},
        {"duration": 650, "users": 1000, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
