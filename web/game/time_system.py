class GameTime:
    FACTOR = 10

    def __init__(self):
        self.game_minutes = 0.0

    def update(self, real_dt_seconds: float):
        self.game_minutes += real_dt_seconds * self.FACTOR / 60.0

    def get_minutes(self) -> float:
        return self.game_minutes

    def get_hours(self) -> float:
        return self.game_minutes / 60.0

    def get_days(self) -> float:
        return self.game_minutes / (24.0 * 60.0)

    def reset(self):
        self.game_minutes = 0.0
