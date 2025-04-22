
from .programs import Program, ProgramModel, State 
from .overrides import Override, OverrideModel, OverrideType

from pydantic import BaseModel, ConfigDict
from typing import Optional, Union 

from datetime import datetime , timedelta

from lib.pydantic_helper import FromPydantic

class Station(FromPydantic):

    _not_updatable = [
        "station_id"
    ]

    def __init__(
        self, 
        station_id: int, 
        programs: dict[int, Program] | dict[int, BaseModel] | dict[int, dict],
        override: Override | None | dict | list[BaseModel],
        name: str = "",
        description: str = "",
        enabled: bool = False 
    ):
        self.station_id = station_id 
        self.programs = {x[0] : Program.from_pydantic(x[1]) for x in programs.items()}
        self.override = Override.from_pydantic(override) if override else None 
        self.description = description
        self.name = name 
        self.enabled = enabled

    @classmethod
    def default(cls):
        p = Program.default()
        return cls(
            1,
            programs = {p.program_id: p},
            override = None ,
            enabled = False
        )
    
    def update_description(self, desc: str):
        self.description = desc 

    def set_enabled(self):
        self.enabled = True

    def set_disabled(self):
        self.enabled = False 

    def set_override(
        self, 
        start_time: datetime, 
        duration: timedelta, 
        override_type: OverrideType | str,
        enabled: bool

    ):
        self.override = Override(
            start_time=start_time, 
            duration=duration, 
            override_enabled=enabled, 
            override_type= OverrideType.from_pydantic(override_type)
        )

    def get_program(self, program_id: int) -> Program | None :
        return self.programs.get(program_id, None )

    def add_program(self) -> Program:
        ids = [x for x in self.programs.keys()]
        ids.sort()
        new_id = 1
        for i in ids:
            if new_id < i:
                break
            new_id += 1
        
        p = Program.default()
        p.program_id = new_id
        self.programs[new_id] = p
        return p

    def delete_program(self, program_id):
        if program_id in self.programs.keys():
            del self.programs[program_id]

    def status(self, dt : Optional[datetime] = None):
        if dt is None:
            dt = datetime.now()

        (override_active, override_type) = (False, None) if self.override is None else self.override.applies(dt)

        summary = StationSummaryModel(
            station_id = self.station_id,
            description = self.description if self.description else "",
            override_active = override_active,
            override_type = override_type,
            program_states = {
                x[0]: x[1].run(dt) for x in self.programs.items()
            },
            enabled = self.enabled
        )
        return summary 
    
    def is_active(self) -> bool:
        s = self.status()

        if s.enabled is not True:
            return False

        if (
            s.override_active
        ):
            return True if s.override_type is OverrideType.On else False 

        if any(x.is_active() for x in self.programs.values()):
            return True 

class StationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station_id: int 
    programs: dict[int, ProgramModel]
    override: Optional[OverrideModel]
    enabled: bool 

    description: str 
    name: str 
    
    def to_orm(self) -> Station:
        return Station(**self.model_dump())

class StationSummaryModel(BaseModel):
    station_id: int 
    description: str 
    name: str 
    override_active: bool
    override_type: Optional[OverrideType]
    program_states: dict[int, State ]
    enabled: bool 