
from .programs import Program, ProgramModel, States 
from .overrides import Override, OverrideModel, OverrideType

from pydantic import BaseModel, ConfigDict
from typing import Optional, Union 

from datetime import datetime 

class StationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station_id: int 
    programs: list[ProgramModel]
    override: Optional[OverrideModel]

class StationSummaryModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station_id: int 
    description: str 
    override_active: Optional[OverrideModel]
    override_type: Optional[OverrideType]
    weather_override: Optional[OverrideModel]
    weather_override_type: Optional[OverrideType]
    program_states: list[States ]

class Station:

    def __init__(
        self, 
        station_id: int, 
        programs: list[Program],
        override: Override | None,
        weather_override: Override | None ,
        description: str = ""
    ):
        self.station_id = station_id 
        self.programs = programs
        self.override = override
        self.weather_override = weather_override
        self.description = description

    @classmethod
    def default(cls):
        return cls(
            1,
            programs = [Program.default()],
            override = None,
            weather_override = None
        )

    def status(self, datetime : Optional[datetime] = None):
        if datetime is None:
            datetime = datetime.now()

        override_active, override_type = None, None if self.override is None else self.override.applies(datetime)
        weather_active, weather_type = None, None if self.weather_override is None else self.weather_override.applies(datetime)

        summary = StationSummaryModel(
            station_id = self.station_id,
            description = self.description if self.description else "",
            override_active = override_active,
            override_type = override_type,
            weather_override = weather_active,
            weather_override_type = weather_type,
            program_states = [
                x.run(datetime) for x in self.programs
            ]
        )
        return summary 
        
