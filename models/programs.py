from enum import Enum, auto as enum_auto
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, ConfigDict
from typing import Optional, Union 


class Trigger(Enum):
    daily = "Daily"
    even_days = "Even Days"
    odd_days = "Odd Days"
    week_days = "Week Day"
    week_ends = "Weekend"
    day_of_week = "Day of Week"


class DayOfWeek(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    def to_long(self):
        return {
            self.monday: "Monday",
            self.tuesday: "Tuesday",
            self.wednesday: "Wednesday",
            self.thursday: "Thursday",
            self.friday: "Friday",
            self.saturday: "Saturday",
            self.sunday: "Sunday"
        }[self]

    @staticmethod
    def from_short(short: str):
        short = short.lower()[:3]
        return DayOfWeek({
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6
        }[short])

    @staticmethod
    def from_long(long_d: str):
        long_d = long_d.lower()
        return DayOfWeek[long_d]

class States(Enum):
    initial = "initial"
    activated = "activated"
    finished = "finished"
    disabled = "disabled"

class Transitions(Enum):
    day_reset = "day_reset"     # the test_date is different to the last triggered date
    trigger = "trigger"       # state is "before_trigger" && the trigger rules are activated
    finished = "finished"      # state is activated && and the trigger duration has been exceeded
    disable = "disable"       # sets us to the disabled state
    enable = "enable"        # sets us to initial state (before_trigger)

class ProgramModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    _input_dt : datetime 
    _state : States
    trigger: Trigger
    start_time : datetime
    week_day : Optional[DayOfWeek]
    enabled : Optional[bool]
    enabled_after : Optional[datetime]
    enabled_before : Optional[datetime]
    duration : timedelta

    last_triggered : Optional[datetime]

class Program :
    def __init__(
        self, 
        trigger: Trigger, 
        start_time: datetime,
        duration: timedelta,
        week_day: DayOfWeek | None,
        enabled: bool | None,
        enabled_after: datetime | None = None,
        enabled_before: datetime | None = None
    ):
        self.trigger = trigger
        self.start_time = start_time
        self.week_day = week_day
        self.enabled = enabled
        self.enabled_after = enabled_after
        self.enabled_before = enabled_before
        self.duration = duration

        self.last_triggered = None # we need to keep this
        self._set_state_initial()
        self._input_dt : datetime | None = None 
        # don't like defining here, but feel it'll be neater than passing variables

    @property 
    def input_dt(self) -> datetime | None :
        return self._input_dt

    def get_state(self) -> States:
        return self._state

    def get_state_h(self) -> str:
        return self.get_state().name.capitalize()

    def _set_state_disabled(self):
        self._state = States.disabled
    
    def _set_state_initial(self):
        self._state = States.initial

    def _set_state_activated(self):
        self._state = States.activated
    
    def _set_state_finished(self):
        self._state = States.finished

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
            self._set_state_disabled()
            return

    def _transitions_disabled(self):
        if not self._disabled_condition():
            self._set_state_initial()
            return 

    def _transitions_reset(self): 
        
        start_dt = self.start_time
        start_time = start_dt.time()

        input_dt = self.input_dt
        input_time = input_dt.time() 

        if input_time < start_time:
            # no transition change so return
            return 

        day_of_week = DayOfWeek(input_dt.weekday())
        match self.trigger:
            case Trigger.even_days:
                if dt_input.date().day % 2 == 1:
                    return
            case Trigger.odd_days:
                if dt_input.date().day % 2 == 0:
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
        self._set_state_activated()
         

    def _transitions_active(self):
        if self.input_dt >= self.last_triggered + self.duration:
            self._set_state_finished()

    def _transitions_finished(self):
        # The job has finished 
        # and it's a new day
        # last_triggered will be set by this time
        if self.last_triggered.date() != self.input_dt.date(): 
            self._set_state_initial()

    def _state_machine(self):
        self._transitions_all()

        match self.get_state():
            case States.activated:
                self._transitions_active()
            case States.finished:
                self._transitions_finished()
            case States.initial:
                self._transitions_reset()
            case States.disabled:
                self._transitions_disabled()

    def run(self, dt_input : datetime=None) -> States :
        
        if dt_input is None:
            dt_input = datetime.now().time()

        self._input_dt = dt_input
        self._state_machine()
        return self.get_state()

    def is_active(self, dt_input: datetime=None) -> States:
        return self.run(dt_input=dt_input) == States.activated
    
    @classmethod
    def default(cls):
        return cls(
            trigger = Trigger.day_of_week,
            start_time = datetime.fromisoformat("1970-01-01T08:00:00"),
            duration = timedelta(minutes=30),
            week_day= DayOfWeek.tuesday,
            enabled= False
        )
