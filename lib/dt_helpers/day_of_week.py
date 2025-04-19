from enum import StrEnum, auto 

class DayOfWeek(StrEnum):
    monday = auto()
    tuesday = auto()
    wednesday = auto()
    thursday = auto()
    friday = auto()
    saturday = auto()
    sunday = auto()

    @classmethod
    def from_dt(cls, day:int):
        match day:
            case 0:
                return cls.monday
            case 1:
                return cls.tuesday
            case 2:
                return cls.wednesday
            case 3: 
                return cls.thursday
            case 4:
                return cls.friday
            case 5:
                return cls.saturday
            case 6:
                return cls.sunday
        
        raise Exception("invalid day code")

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