from enum import Enum, auto as enum_auto, StrEnum

from datetime import datetime, timedelta, timezone, time 

from pydantic import BaseModel, ConfigDict
from typing import Optional, Union 

from lib.dt_helpers import DayOfWeek
from lib.pydantic_helper import FromPydantic


class Trigger(FromPydantic, StrEnum):
    daily = enum_auto()
    even_days = enum_auto()
    odd_days = enum_auto()
    week_days = enum_auto()
    week_ends = enum_auto()
    day_of_week = enum_auto()

class State(FromPydantic, StrEnum):
    initial = enum_auto()
    activated = enum_auto()
    finished = enum_auto()
    disabled = enum_auto()

class Transition(FromPydantic, StrEnum):
    day_reset = enum_auto()     # the test_date is different to the last triggered date
    trigger = enum_auto()       # state is "before_trigger" && the trigger rules are activated
    finished = enum_auto()      # state is activated && and the trigger duration has been exceeded
    disable = enum_auto()       # sets us to the disabled state
    enable = enum_auto()        # sets us to initial state (before_trigger)

class Program(FromPydantic) :
    def __init__(
        self, 
        trigger: Trigger | str , 
        start_time: datetime,
        duration: timedelta,
        program_id: int,
        name: str | None,
        description: str | None, 
        week_day: DayOfWeek | None | str ,
        enabled: bool = False  ,
        enabled_after: datetime | None = None,
        enabled_before: datetime | None = None,
        last_triggered: datetime | None = None 
    ):
        self.start_time = start_time
        self.set_trigger(trigger)
        self.set_week_day(week_day)
        self.set_description(description)
        self.set_name(name)

        self.enabled = enabled
        self.enabled_after = enabled_after
        self.enabled_before = enabled_before
        
        self.set_duration(duration)

        self.program_id = program_id

        self.last_triggered = last_triggered # we need to keep this
        self._state = State.initial
        self._input_dt : datetime | None = None 
        # don't like defining here, but feel it'll be neater than passing variables

    def set_trigger(self, trigger: Trigger|str):
        self.trigger = Trigger.from_pydantic(trigger)

    def set_start_time(self, t: time ):
        d = datetime(1970, 1, 1)
        d.hour = t.hour
        d.minute = t.minute 
        self.start_time = d

    def set_duration(self, dur: int | timedelta):
        match dur:
            case x if type(x) is int:
                self.duration = timedelta(minutes=minutes)
            case x if type(x) is timedelta:
                self.duration = dur 
            case _:
                raise Exception("unexpected type")        

    def set_name(self, name: str):
        self.name = name 

    def set_description(self, desc: str):
        self.description = desc

    def set_enabled(self):
        self.enabled = True 

    def set_disabled(self):
        self.enabled = False

    def set_enabled_after(self, d:datetime):
        self.enabled_after = d
    
    def set_enabled_before(self, d:datetime):
        self.enabled_before = d
    
    def set_week_day(self, week_day: DayOfWeek | str):
        if week_day is not None:
            self.week_day = week_day if type(week_day) is DayOfWeek else DayOfWeek(week_day)
        else: 
            week_day is None

    @property 
    def input_dt(self) -> datetime | None :
        return self._input_dt

    def get_state(self) -> State:
        return self._state

    def get_state_h(self) -> str:
        return self.get_state().name.capitalize()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, s: State ):
        if not isinstance(s, State):
            self._state = s 
            return 

        raise Exception(f"{type(s)} is not State")

    def _disabled_condition(self):
        if (
            self.enabled == False
            or (self.enabled_after is not None and (self.enabled_after < self.input_dt ))
            or (self.enabled_before is not None and (self.enabled_before > self.input_dt ))
            or (self.duration).seconds < 30  
        ):
            return True

    def _transitions_all(self):
        if self._disabled_condition():
            self._state = State.disabled
            return

    def _transitions_disabled(self):
        if not self._disabled_condition():
            self._state = State.initial
            return 

    def _transitions_reset(self): 
        
        start_dt = self.start_time
        start_time = start_dt.time()

        input_dt = self.input_dt
        input_time = input_dt.time() 

        if input_time < start_time:
            # no transition change so return
            return 

        day_of_week = DayOfWeek.from_dt(input_dt.weekday())
        match self.trigger:
            case Trigger.even_days:
                if input_dt.date().day % 2 == 1:
                    return
            case Trigger.odd_days:
                if input_dt.date().day % 2 == 0:
                    return
            case Trigger.week_days:
                if day_of_week in (DayOfWeek.saturday, DayOfWeek.sunday):
                    return
            case Trigger.week_ends:
                if day_of_week not in (DayOfWeek.saturday, DayOfWeek.sunday):
                    return
            case Trigger.day_of_week:
                if self.week_day != day_of_week:
                    return
            case _: # daily
                pass 

        self.last_triggered = self.input_dt
        self._state = State.activated
         

    def _transitions_active(self):
        if self.input_dt >= self.last_triggered + self.duration:
            self._state = State.finished

    def _transitions_finished(self):
        # The job has finished 
        # and it's a new day
        # last_triggered will be set by this time
        if self.last_triggered.date() != self.input_dt.date(): 
            self._state = State.initial

    def _state_machine(self):
        self._transitions_all()

        match self.get_state():
            case State.activated:
                self._transitions_active()
            case State.finished:
                self._transitions_finished()
            case State.initial:
                self._transitions_reset()
            case State.disabled:
                self._transitions_disabled()

    def run(self, dt_input : datetime=None) -> State :
        
        if dt_input is None:
            dt_input = datetime.now().time()

        self._input_dt = dt_input
        self._state_machine()
        return self.get_state()

    def is_active(self, dt_input: datetime=None) -> State:
        return self.run(dt_input=dt_input) == State.activated
    
    @classmethod
    def default(cls):
        return cls(
            trigger = Trigger.day_of_week,
            start_time = datetime.fromisoformat("1970-01-01T08:00:00"),
            duration = timedelta(minutes=30),
            week_day= DayOfWeek.tuesday,
            enabled= False,
            program_id=1,
            name="",
            description=""
        )

class ProgramModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    #_input_dt : datetime 
    #_state : State
    trigger: Trigger
    start_time : datetime
    week_day : Optional[DayOfWeek]
    enabled : bool
    enabled_after : Optional[datetime]
    enabled_before : Optional[datetime]
    duration : timedelta
    program_id: int 
    description: str 
    name: str 

    last_triggered : Optional[datetime]