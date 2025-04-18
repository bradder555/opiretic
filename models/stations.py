from .programs import Program
from .overrides import Override

class Station:
    def __init__(
        self, 
        station_id: int, 
        programs: list[Program],
        override: Override | None,
        weather_override: Override | None 
    ):
        self.station_id = station_id 
        self.programs = programs
        self.override = override
        self.weather_override = weather_override

    @classmethod
    def default(cls):
        return cls(
            1,
            programs = [Program.default()],
            override = None,
            weather_override = None
        )