from .programs import Program
from .overrides import Override

class Station:
    def __init__(
        self, 
        station_id: int, 
        programs: list[Program],
        override: Override
    ):
        self.station_id = station_id 
        self.conditions = conditions
        self.override = override