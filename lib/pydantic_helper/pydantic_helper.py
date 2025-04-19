from pydantic import BaseModel, ConfigDict
import pydantic 
from enum import Enum 

class FromPydantic:

    @classmethod
    def from_pydantic(cls, pyd: any):
        if pyd is None:
            return None 
            
        if type(pyd) is cls:
            return pyd

        if isinstance(pyd, Enum):
            return cls(pyd)
        
        if isinstance(pyd, BaseModel):
            return cls(**pyd.model_dump())
        
        if type(pyd) is dict:
            return cls(**pyd)
        
        raise Exception("Unable to deserialize")