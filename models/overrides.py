from datetime import datetime, timedelta
from enum import StrEnum, auto

from pydantic import BaseModel, ConfigDict
from typing import Optional, Union 

from lib.pydantic_helper import FromPydantic

class OverrideType(FromPydantic, StrEnum):
    On = auto()
    Off = auto()


class Override(FromPydantic):
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
        self.override_type = OverrideType.from_pydantic(override_type) 
    
    def applies(self, ref_time: datetime):
        if self.override_enabled == False:
            return False, None 
        
        if self.start_time <= ref_time < (self.start_time + self.duration):
            return True, self.override_type
        
        return False 

class OverrideModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    start_time : datetime
    duration: timedelta
    override_enabled : bool 
    override_type: OverrideType 