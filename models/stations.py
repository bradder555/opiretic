
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