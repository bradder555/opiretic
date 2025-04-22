from typing import Union
from contextlib import asynccontextmanager
from models import (
    Config, 
    ConfigModel, 
    StationModel, 
    Station, 
    StationSummaryModel, 
    ProgramModel, 
    OverrideType,
    Trigger,
    DayOfWeek
)
from copy import deepcopy

from datetime import datetime, timedelta, time

import os, sys 

from fastapi import FastAPI, HTTPException, status, Request, Response 
from fastapi.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import logging 
logging.basicConfig()
logger = logging.getLogger()

config = Config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass 
    yield
    pass 

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/config", response_model = ConfigModel  )
def get_full_config() -> Config :
    return ConfigModel.from_orm(config)

@app.get("/config/station/{station_no}", response_model=StationModel )
def get_station(station_no:int ) -> Station:
    s = config.get_station(station_id=station_no)
    if s is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return StationModel.from_orm(s)

@app.get("/status/station", response_model=list[StationSummaryModel])
def get_station_statuses():
    return [x.status(datetime.now()) for x in config.stations.values()]

@app.get("/status/active_stations", response_model=dict[int, bool])
def get_active_stations():
    return {x.station_id : x.is_active() for x in config.stations.values()}

@app.get("/status/station/{station_id}", response_model=StationSummaryModel)
def get_station_status(station_id: int):
    r = [x.status(datetime.now()) for x in config.stations.values() if x.station_id == station_id]
    if r == []:
        raise HTTPException(status_code=404)
    return r[0]

@app.get("/status/station/{station_id}/is_active", response_model=bool)
def get_station_is_active(station_id: int):
    s = config.get_station(station_id)
    if s is None:
        raise HTTPException(status_code=404, detail=f"station {station_id} does not exist")
    return s.is_active()



@app.post("/config/station")
def get_new_station():
    s = config.add_station()
    return RedirectResponse(f"/status/station/{s.station_id}", 201)

@app.delete("/config/station/{station_id}")
def delete_station(station_id: int):
    with config.update_config():
        config.delete_station(station_no=station_id)

@app.get("/config/station/{station_id}/program", response_model=list[ProgramModel])
def get_station_programs(station_id:int):
    return [
        ProgramModel.from_orm(x) 
        for x 
        in config.get_station(station_id=station_id).programs.values()
    ]

@app.put("/config/station/{station_id}/description")
def set_station_description(station_id:int, desc:str):
    with config.update_config():
        config.get_station(station_id).update_description(desc)

@app.put("/config/station/{station_id}/enable")
def set_station_enabled(station_id:int):
    with config.update_config():
        config.get_station(station_id).set_enabled()

@app.put("/config/station/{station_id}/disable")
def set_station_disabled(station_id:int):
    with config.update_config():
        config.get_station(station_id).set_disabled()

@app.put("/config/station/{station_id}/override")
def set_station_override(
    station_id: int, 
    start_time: datetime, 
    duration: timedelta, 
    override_type: OverrideType,
    enabled: bool
):
    with config.update_config():
        config.get_station(station_id).set_override(
            start_time,
            duration,
            override_type,
            enabled
        )

@app.post("/config/station/{station_id}/program")
def get_new_program(station_id: int):
    with config.update_config():
        p = config.get_station(station_id).add_program()
        
        return RedirectResponse(f"/config/station/{station_id}/program/{p.program_id}", 201)

@app.get("/config/station/{station_id}/program/{program_id}", response_model=ProgramModel)
def get_station_program(station_id:int, program_id:int, response: Response):
    s = config.get_station(station_id)
    if s is None:
        raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
        
    p = s.get_program(program_id) 
    if p is None:
        raise HTTPException(
            status_code=404, 
            detail=f"station {station_id}, program {program_id} doesn't exist"
        )

    #response.headers.append("test", "hello")
    return ProgramModel.from_orm(p)


@app.delete("/config/station/{station_id}/program/{program_id}")
def delete_station_program(station_id: int, program_id: int):
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        s.delete_program(p.program_id)

@app.put("/config/station/{station_id}/program/{program_id}/name")
def set_program_name(station_id: int, program_id: int, name:str) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_name(name)
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/description")
def set_program_description(station_id: int, program_id: int, descr:str) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_description(desc=descr)
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/trigger")
def set_program_trigger(station_id: int, program_id: int, trigger:Trigger) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_trigger(trigger)
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/day")
def set_program_day(station_id: int, program_id: int, day:DayOfWeek) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_week_day(day)
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/duration")
def set_program_duration(station_id: int, program_id: int, duration:timedelta) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_duration(duration)
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/enabled")
def set_program_enabled(station_id: int, program_id: int) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_enabled()
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/disabled")
def set_program_disabled(station_id: int, program_id: int) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_disabled()
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/start_time")
def set_program_start_time(station_id: int, program_id: int, start_time:time) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_start_time(start_time)
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/enabled_after")
def set_program_enabled_after(station_id: int, program_id: int, enabled_after:datetime|None ) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_enabled_after(enabled_after)
        return ProgramModel.from_orm(p)

@app.put("/config/station/{station_id}/program/{program_id}/enabled_before")
def set_program_enabled_before(station_id: int, program_id: int, enabled_before:datetime|None) -> ProgramModel:
    with config.update_config():
        s = config.get_station(station_id)

        if s is None:
            raise HTTPException(status_code=404, detail=f"station {station_id} doesn't exist")
            
        p = s.get_program(program_id) 
        if p is None:
            raise HTTPException(
                status_code=404, 
                detail=f"station {station_id}, program {program_id} doesn't exist"
            )
        
        p.set_enabled_before(enabled_before)
        return ProgramModel.from_orm(p)

app.mount("/", StaticFiles(directory="./front_end/dist", html=True))

