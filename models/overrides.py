from datetime import datetime, timedelta


class Override:
    def __init__(
        self, 
        start_time: datetime,
        duration: timedelta,
        override_enabled: bool
    ):
        self.start_time = start_time
        self.duration = duration
        self.override_enabled = override_enabled