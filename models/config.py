from .stations import Station, StationModel
from copy import deepcopy
import yaml

from pydantic import BaseModel, ConfigDict
from typing import Optional, Union 

yaml.Dumper.ignore_aliases = lambda x,y: True 

class ConfigModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    stations: dict[int, StationModel]

class Config():
    def __init__(self, stations = None ):
        if stations:
            self.stations = stations
            return 
        
        try:
            with open("config.yaml", "r") as conf:
                c = yaml.unsafe_load(conf)
                self.stations = deepcopy(c.stations)
                if self is None:
                    raise Exception("config is none")
        except:
            self.set_default()
        self._write_config()

    def set_default(self):
        self.stations = {}
        for i in range(6):
            s = Station.default()
            s.station_id = i
            self.stations[i] = s

    def _write_config(self):
        with open("config.yaml", "w") as conf:
            yaml.dump(self, conf, sort_keys=False, indent=2, Dumper=yaml.Dumper)
