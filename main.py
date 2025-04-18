from typing import Union
from contextlib import asynccontextmanager
from models import Config, ConfigModel, StationModel, Station, StationSummaryModel 
from copy import deepcopy

from datetime import datetime 

import os, sys 

from fastapi import FastAPI, HTTPException
config = Config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass 
    yield
    pass 

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
dict[int, dict[str, any]]
@app.get("/config", response_model = ConfigModel  )
def get_full_config() -> Config :
    return config

@app.get("/config/station/{station_no}", response_model=StationModel )
def get_station(station_no:int ) -> Station:
    s = config.stations.get(station_no, None)
    if s is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return s 

@app.get("/status/station", response_model=list[StationSummaryModel])
def get_station_statuses():
    return [x.status(datetime.now()) for x in config.stations.values()]

@app.get("/status/station/{station_id}", response_model=StationSummaryModel)
def get_status_status(station_id: int):
    r = [x.status(datetime.now()) for x in config.stations.values() if x.station_id == station_id]
    if r == []:
        raise HTTPException(status_code=404)
    return r[0]