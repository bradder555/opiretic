from .stations import Station, StationModel
from copy import deepcopy
import yaml

from pydantic import BaseModel, ConfigDict
from typing import Optional, Union 

from contextlib import contextmanager

from logging import getLogger
logger = getLogger()

yaml.Dumper.ignore_aliases = lambda x,y: True 

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
        for i in range(1,7):
            s = Station.default()
            s.station_id = i
            self.stations[i] = s

    def _write_config(self):
        with open("config.yaml", "w") as conf:
            yaml.dump(self, conf, sort_keys=False, indent=2, Dumper=yaml.Dumper)
            logger.info("updated config")

    def get_station(self, station_id: int) -> Station | None :
        return self.stations.get(station_id, None )

    def add_station(self) -> Station:
        with self.update_config():
            ids = [x for x in self.stations.keys()]
            ids.sort()
            new_id = 1
            for i in ids:
                if new_id < i:
                    break
                new_id += 1
            
            s = Station.default()
            s.station_id = new_id 
            self.stations[new_id] = s
            return s

    def delete_station(self, station_no):
        with self.update_config():
            if station_no in self.stations.keys():
                del self.stations[station_no]

    @contextmanager
    def update_config(self):
        yield 
        self._write_config()            
    

class ConfigModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    stations: dict[int, StationModel]
        