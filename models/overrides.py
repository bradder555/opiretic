from datetime import datetime, timedelta
from enum import Enum, auto

class OverrideType(Enum):
    On = auto()
    Off = auto()


class Override:
    def __init__(
        self, 
        start_time: datetime,
        duration: timedelta,
        override_enabled: bool,
        override_type: OverrideType
    ):
        self.start_time = start_time
        self.duration = duration
        self.override_enabled = override_enabled
        self.override_type = override_type