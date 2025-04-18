from typing import Union
from contextlib import asynccontextmanager
from models import Station
import yaml

import os, sys 

from fastapi import FastAPI

def get_config_context():
    config = {}
    try:
        with open("config.yaml", "w") as conf:
            config = yaml.parse(conf)
    except:
        config["stations"] = []
        for i in range(6):
            s = Station.default()
            s.station_id = i
            config["stations"].append(s)
        with open("config.yaml", "w") as conf:
            yaml.dump(config, conf)

    def read_config():
        return config

    def write_config():
        pass
    
    return {
        "read": read_config,
        "write": write_config
    }

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}